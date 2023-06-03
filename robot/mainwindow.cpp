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

void MainWindow::on_horizontalSlider_sliderMoved(int position)
{
     qInfo() <<ui->horizontalSlider->value();
     ui->label->setText( QString::number( ui->horizontalSlider->value() ) );
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

