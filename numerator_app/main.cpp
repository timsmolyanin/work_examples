#include <QGuiApplication>
#include <QDebug>
#include <QThread>

#include "App.h"
#include "SerialPort.h"
#include "TableModel.h"


int main(int argc, char *argv[])
{
//    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    App app(argc, argv, "KRYPTEN", "Numerator_GUI");
    qInfo("App created");
    app.init();
    qInfo("App inited");

    return app.exec();
}
