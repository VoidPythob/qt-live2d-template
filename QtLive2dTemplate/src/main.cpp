#include <QApplication>
#include <QMainWindow>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLive2DWidget.h>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QMainWindow m;
    QWidget center;
    QPushButton btn;
    QHBoxLayout layout;

    QLive2DWidget live2D;

    btn.setText("btn");

    center.setLayout(&layout);
    layout.addWidget(&btn);
    layout.addWidget(&live2D);

    m.setCentralWidget(&center);
    m.setAttribute(Qt::WA_TranslucentBackground);

    m.show();

    return a.exec();
}