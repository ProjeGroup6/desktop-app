#include "mainwindow.h"
#include "./ui_mainwindow.h"

 bool click=false;
 bool isSingleClick = false;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    movemenet_delay = 200;

    char buffer[PATH_MAX];
    if (getcwd(buffer, sizeof(buffer)) != nullptr) {
        std::string path(buffer);

        // Find the last occurrence of the directory separator
        size_t lastSeparator = path.find_last_of("/\\");

        // Remove the last file
        path = path.substr(0, lastSeparator);

        // Find the second last occurrence of the directory separator
        size_t secondLastSeparator = path.find_last_of("/\\");

        // Remove the second last file
        path = path.substr(0, secondLastSeparator);

        path += "/robot/Resources/";

        QPixmap pix(QString::fromStdString(path + "startcamera.png"));
        QIcon icon(pix);
        ui->pushButton->setIcon(icon);
        ui->pushButton->setIconSize(ui->pushButton->size());

        QPixmap pix2(QString::fromStdString(path + "forward.png"));
        QIcon icon2(pix2);
        ui->pushButton_2->setIcon(icon2);
        ui->pushButton_2->setIconSize(ui->pushButton->size());

        QPixmap pix4(QString::fromStdString(path + "back.png"));
        QIcon icon4(pix4);
        ui->pushButton_4->setIcon(icon4);
        ui->pushButton_4->setIconSize(ui->pushButton->size());


        QPixmap pix7(QString::fromStdString(path + "right.png"));
        QIcon icon7(pix7);
        ui->pushButton_7->setIcon(icon7);
        ui->pushButton_7->setIconSize(ui->pushButton->size());

        QPixmap pix8(QString::fromStdString(path + "right.png"));
        QIcon icon8(pix8);
        ui->pushButton_8->setIcon(icon8);
        ui->pushButton_8->setIconSize(ui->pushButton->size());

        QPixmap pix9(QString::fromStdString(path + "left.png"));
        QIcon icon9(pix9);
        ui->pushButton_9->setIcon(icon9);
        ui->pushButton_9->setIconSize(ui->pushButton->size());

        QPixmap pix10(QString::fromStdString(path + "left.png"));
        QIcon icon10(pix10);
        ui->pushButton_10->setIcon(icon10);
        ui->pushButton_10->setIconSize(ui->pushButton->size());

        /*QPixmap pix11("joker.png");
        ui->label_3->setPixmap(pix11);
        ui->label_3->setMask(pix11.mask());
        ui->label_3->show();*/
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

//******************************************************
//****************************************************

void MainWindow::on_pushButton_5_clicked()
{
    // girilen ip
    IP = ui->lineEdit->text();
    qInfo() << IP.toStdU32String();
    socket_connection();

}
//***********************************************

void MainWindow::checkClick9Type()
{
    const char *message = "Step Left";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "1 Step Left";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "1 Step Left";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::checkClick10Type()
{
    const char *message = "Turn Left";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "2 Turn Left";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "2 Turn Left";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::checkClick2Type()
{
    const char *message = "Forward";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "2 Forward";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "2 Forward";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::checkClick8Type()
{
    const char *message = "Turn Right";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "4 Turn Right";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "4 Turn Right";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::checkClick7Type()
{
    const char *message = "Step Right";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "3 Step Right";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "3 Step Right";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::checkClick4Type()
{
    const char *message = "Backward";
    if(click) {
        isSingleClick = false;
        while(click) {
            qInfo() << "5 Backward";
            QCoreApplication::processEvents();
            write(sockfd, message, strlen(message));
            QThread::msleep(movemenet_delay);
        }
    } else if(isSingleClick) {
        qInfo() << "5 Backward";
        write(sockfd, message, strlen(message));
    }
}

void MainWindow::on_pushButton_clicked()
{
    const char *message = "Open Camera";
    qInfo() << "7 Open Camera ";
    write(sockfd, message, strlen(message));
//    sleep(500);
//    std::string command = "python";
//    std::string argument = "reciever.py";

//    try
//    {
//        std::string fullCommand = command + " " + argument;

//        FILE* pipe = popen(fullCommand.c_str(), "r");

//        if (!pipe) {
//            throw std::runtime_error("Failed to open pipe");
//        }

//        pclose(pipe);
//    } catch (const std::exception& e) {
//        qInfo() << "Error: " << e.what();
//        exit(1);
//    }
}







//**************************************************

void MainWindow::on_pushButton_6_clicked()
{
    const char *message = "Autonom";
    qInfo() << "8 Autonom";
    write(sockfd, message, strlen(message));
}

//********************************************************************

void MainWindow::on_pushButton_3_clicked()
{
    const char *message = "Buzzer";
    qInfo() << "9 Buzzer";
    write(sockfd, message, strlen(message));
}


void MainWindow::on_pushButton_2_released()
{
    click = false;
}

//******************************************************

void MainWindow::on_pushButton_7_clicked()
{
    isSingleClick = true;
}

void MainWindow::on_pushButton_7_pressed()
{
    click = true;
    QTimer::singleShot(200, this, SLOT(checkClick7Type()));
}

void MainWindow::on_pushButton_7_released()
{
    click = false;
}



//***********************************************************


void MainWindow::on_pushButton_8_clicked()
{
    isSingleClick = true;
}

void MainWindow::on_pushButton_8_pressed()
{
    click = true;
    QTimer::singleShot(200, this, SLOT(checkClick8Type()));
}

void MainWindow::on_pushButton_8_released()
{
    click = false;
}



//**************************************************

void MainWindow::on_pushButton_9_clicked()
{
    isSingleClick = true;
}

void MainWindow::on_pushButton_9_pressed()
{
    click = true;
    QTimer::singleShot(200, this, SLOT(checkClick9Type()));
}

void MainWindow::on_pushButton_9_released()
{
    click = false;
}



//****************************************************************

void MainWindow::on_pushButton_10_clicked()
{
    isSingleClick = true;
}

void MainWindow::on_pushButton_10_pressed()
{
    click = true;
    QTimer::singleShot(200, this, SLOT(checkClick10Type()));
}

void MainWindow::on_pushButton_10_released()
{
    click = false;
}


//****************************************************

void MainWindow::on_horizontalSlider_valueChanged(int value)
{
    qInfo() << value;
    ui->label->setText(QString::number(value));
}

//*******************************************************

void MainWindow::on_pushButton_2_clicked()
{
     isSingleClick = true;
}

void MainWindow::on_pushButton_2_pressed()
{
     click = true;
     QTimer::singleShot(200, this, SLOT(checkClick2Type()));
}

//*********************************************************************

void MainWindow::on_pushButton_4_clicked()
{
     isSingleClick = true;
}

void MainWindow::on_pushButton_4_pressed()
{
     click = true;
     QTimer::singleShot(200, this, SLOT(checkClick4Type()));
}

void MainWindow::on_pushButton_4_released()
{
     click = false;
}
void MainWindow::socket_connection() {

     QByteArray ba = IP.toLocal8Bit();
     const char *ipAddress = ba.data();
     memset(&serverAddress, 0, sizeof(serverAddress));
     serverAddress.sin_family = AF_INET;
     serverAddress.sin_port = htons(8081);
     qDebug() << ipAddress;
     if (inet_pton(AF_INET, ipAddress, &(serverAddress.sin_addr)) <= 0) {
        qDebug() << "Invalid IP address";
        return;
     }

     if (::connect(sockfd, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        qDebug() << "Failed to connect";
        return;
     }

     qDebug() << "Connected to: " << ipAddress;
}

