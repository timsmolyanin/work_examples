#include "App.h"


App::App(int& argc, char** argv, const QString& strOrg, const QString strAppName)
    : QGuiApplication(argc, argv)
    , settings(nullptr)
{
    qInfo("start App");
    setOrganizationName(strOrg);
    setApplicationName(strAppName);
    qInfo("load App settings");
    settings = std::make_shared<QSettings>("./settings.ini", QSettings::IniFormat, this);

    runsNumber++;
    settings->setValue("/General/runsNumber", runsNumber);
    qInfo("RunsNumber: %d", settings->value("/General/runsNumber").toInt());
}

void App::setupContext()
{
    QSerialPortInfo serialPortInfo;
    QList<QSerialPortInfo> ports = serialPortInfo.availablePorts();
    QList<qint32> bauds = serialPortInfo.standardBaudRates();
    QStringList portsName;
    QStringList baudsStr;
    foreach(QSerialPortInfo port, ports){
        portsName.append(port.portName());
    }
    foreach(qint32 baud, bauds){
        baudsStr.append(QString::number(baud));
    }
    context->setContextProperty("portsNameModel", QVariant::fromValue(portsName));
    context->setContextProperty("baudsModel", QVariant::fromValue(baudsStr));


    // Это, в совокупности с использованием класса в QML было ошибочно, поскольку
    // вместо созданных объектов serialTerminal и tableModel в QML создавались новые объекты
    //qmlRegisterType<TableModel>("TableModel", 0, 1, "TableModel");
    //qmlRegisterType<SerialTerminal>("SerialPort", 1, 0, "SerialPort");

    if (serialPort) {
        context->setContextProperty("serialPort", serialPort.get());
    } else {
        qFatal("serialTerminal is nullptr");
    }
    if (tableModel) {
        context->setContextProperty("tableModel", tableModel.get());
    } else {
        qFatal("tableModel is nullptr");
    }
}

void App::init()
{
    createObjects();

    setupContext();

    setConnections();
}

void App::createObjects()
{
    serialPort = std::make_shared<SerialPort>();
    serialPort->moveToThread(&serialTerminalThread);
    serialTerminalThread.start();

    tableModel = std::make_shared<TableModel>();
    tableModel->moveToThread(&tableModelThread);
    tableModelThread.start();

    context = engine.rootContext();

    qInfo("Objects created");
}

void App::setConnections()
{
    qDebug() << Q_FUNC_INFO;

    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
        this, [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        }, Qt::QueuedConnection);
    engine.load(url);

    if (serialPort && tableModel){
        const bool connected = connect(serialPort.get(),SIGNAL(changeTable()),
                                       tableModel.get(), SLOT(onSerialChangeTable()),
                                       Qt::QueuedConnection);
        serialPort->dumpObjectInfo();
        tableModel->dumpObjectInfo();

        Q_ASSERT(connected);
        Q_UNUSED(connected);
    } else {
        qFatal("serialTerminal or tableModel is nullptr");
    }

    qInfo("Connections setted");
}

App::~App()
{
    serialTerminalThread.quit();
    if (!serialTerminalThread.wait(2000)) //Wait until it actually has terminated (max. 2 sec)
    {
        qWarning("Thread serialTerminalThread deadlock detected, bad things may happen !!!");
        serialTerminalThread.terminate();
        serialTerminalThread.wait();
    }

    tableModelThread.quit();
    if (!tableModelThread.wait(2000)) //Wait until it actually has terminated (max. 2 sec)
    {
        qWarning("Thread tableModelThread deadlock detected, bad things may happen !!!");
        tableModelThread.terminate();
        tableModelThread.wait();
    }

    qDebug() << "Program Finished";
}
