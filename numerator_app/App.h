#ifndef APP_H
#define APP_H

#include <memory>

#include <QGuiApplication>
#include <QObject>
#include <QSettings>
#include <QDebug>
#include <QThread>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QtSerialPort/QSerialPortInfo>

#include "SerialPort.h"
#include "TableModel.h"




class App : public QGuiApplication
{
    Q_OBJECT
private:
    std::shared_ptr<QSettings> settings;
    int runsNumber;

    std::shared_ptr<SerialPort> serialPort;
    QThread serialTerminalThread;

    std::shared_ptr<TableModel> tableModel;
    QThread tableModelThread;

    QQmlApplicationEngine engine;
    QQmlContext *context;


    void createObjects();
    void setupContext();
    void setConnections();

public:
    App(int&, char**, const QString&, const QString);
    ~App();

    static App* theApp()
    {
        return static_cast<App*>(qApp);
    }

    std::shared_ptr<QSettings> getSettings()
    {
        return settings;
    }


    void init();


signals:

public slots:

};

#endif // APP_H
