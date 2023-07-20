from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets
import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
import numpy as np


class RunThread(QtCore.QThread):
    CUSTOM_MODEL_NAME = "my_ssd_mobnet"
    LABEL_MAP_NAME = "label_map.pbtxt"

    paths = {
        "ANNOTATION_PATH": os.path.join("Tensorflow", "workspace", "annotations"),
        "CHECKPOINT_PATH": os.path.join(
            "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME
        ),
    }

    files = {
        "PIPELINE_CONFIG": os.path.join(
            "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "pipeline.config"
        ),
        "LABELMAP": os.path.join(paths["ANNOTATION_PATH"], LABEL_MAP_NAME),
    }

    changePixmap = QtCore.pyqtSignal(QImage)
    configs = config_util.get_configs_from_pipeline_file(files["PIPELINE_CONFIG"])
    detection_model = model_builder.build(
        model_config=configs["model"], is_training=False
    )

    def __init__(self, sock, parent=None):
        super(RunThread, self).__init__(parent)
        self.sock = sock

    @tf.function
    def detect_fn(self, image):
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

    def run(self):
        ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        ckpt.restore(
            os.path.join(self.paths["CHECKPOINT_PATH"], "ckpt-3")
        ).expect_partial()

        print(self.sock)
        while True:
            # Receive the frame size
            data_size = int.from_bytes(self.sock.recv(4), byteorder="big")

            # Receive the frame data
            data = b""
            while len(data) < data_size:
                packet = self.sock.recv(data_size - len(data))
                if not packet:
                    break
                data += packet

            # Decode and display the frame in the PyQt5 window
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            height, width, _ = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            category_index = label_map_util.create_category_index_from_labelmap(
                self.files["LABELMAP"]
            )

            input_tensor = tf.convert_to_tensor(
                np.expand_dims(frame, 0), dtype=tf.float32
            )
            detections = self.detect_fn(input_tensor)

            num_detections = int(detections.pop("num_detections"))
            detections = {
                key: value[0, :num_detections].numpy()
                for key, value in detections.items()
            }
            detections["num_detections"] = num_detections

            # detection_classes should be ints.
            detections["detection_classes"] = detections["detection_classes"].astype(
                np.int64
            )

            label_id_offset = 1
            frame_with_detections = frame.copy()

            viz_utils.visualize_boxes_and_labels_on_image_array(
                frame_with_detections,
                detections["detection_boxes"],
                detections["detection_classes"] + label_id_offset,
                detections["detection_scores"],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=0.8,
                agnostic_mode=False,
            )

            image = QImage(
                frame_with_detections.data, width, height, QImage.Format_RGB888
            )
            self.changePixmap.emit(image)
