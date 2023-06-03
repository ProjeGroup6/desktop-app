#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QThread>
#include <QTimer>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    QString IP;
    int sockfd;
    struct sockaddr_in serverAddress;
    int movemenet_delay;

    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void socket_connection();

private slots:
    void on_pushButton_5_clicked();  // Connect

    void on_pushButton_9_clicked();  // single click

    void on_pushButton_10_clicked(); // single click

    void on_pushButton_7_clicked();

    void on_pushButton_8_clicked();

    void on_pushButton_4_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_clicked();

    void on_pushButton_6_clicked();

    void on_pushButton_3_clicked();

    void on_horizontalSlider_sliderMoved(int position);

    void on_pushButton_2_pressed();

    void on_pushButton_2_released();

    void on_pushButton_9_pressed();

    void on_pushButton_9_released();

    void on_pushButton_10_pressed();

    void on_pushButton_10_released();

    void on_pushButton_7_pressed();

    void on_pushButton_7_released();

    void on_pushButton_8_pressed();

    void on_pushButton_8_released();

    void on_pushButton_4_pressed();

    void on_pushButton_4_released();

     void checkClick2Type(); // declare the new slot
     void checkClick4Type(); // declare the new slot
     void checkClick7Type(); // declare the new slot
     void checkClick8Type(); // declare the new slot
     void checkClick9Type(); // declare the new slot
     void checkClick10Type(); // declare the new slot

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
