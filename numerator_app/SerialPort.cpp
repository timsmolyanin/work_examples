#include "SerialPort.h"


#include <QtSerialPort/QSerialPort>
#include <QDebug>

#include "App.h"

SerialPort::SerialPort(QObject *parent ):QObject(parent)
{
    _qSerialPort = new QSerialPort(this);
    connect(_qSerialPort, &QSerialPort::readyRead, this, &SerialPort::onReadData);

    openDefault();
}

SerialPort::~SerialPort()
{
    delete _qSerialPort;
}

void SerialPort::openSerialPort(QString comName, int baud){
    _qSerialPort->setPortName(comName);
    _qSerialPort->setBaudRate(baud);
    _qSerialPort->setParity(QSerialPort::NoParity);
    _qSerialPort->setFlowControl(QSerialPort::NoFlowControl);
    _qSerialPort->setDataBits(QSerialPort::Data8);
    _qSerialPort->setStopBits(QSerialPort::OneStop);
    _qSerialPort->open(QSerialPort::ReadWrite);
    connect(_qSerialPort, &QSerialPort::readyRead, this, &SerialPort::onReadData);
    //    connect(serialPort,SIGNAL(readyRead()),this,SLOT(readFromSerialPort()));
    if(_qSerialPort->isOpen() != true){
        qDebug("Port not open");
    }
}

void SerialPort::closeSerialPort(){
    _qSerialPort->close();
}

bool SerialPort::getConnectionStatus(){
    return _qSerialPort->isOpen();
}

void SerialPort::writeToSerialPort(QString message){
    const QByteArray &messageArray = message.toLocal8Bit();
    _qSerialPort->write(messageArray);
    //    serialPort->waitForBytesWritten(500);
}

void SerialPort::openSerialPortSlot(QString comName, int baud){

    this->openSerialPort(comName, baud);
}

void SerialPort::writeToSerialPortSlot(QString message){
    if (_qSerialPort->isOpen()) {
        this->writeToSerialPort(message);
        //                qDebug()<<"mserial_data = " << mserial_data;
        emit changeTable();
    } else {
        emit changeTable();
        qWarning() << "Serial port not opened.";
        //                qDebug()<<"mserial_data = " << mserial_data;
    }
}

void SerialPort::closeSerialPortSlot(){

    this->closeSerialPort();
}

bool SerialPort::getConnectionStatusSlot(){

    return this->getConnectionStatus();
}

void SerialPort::set_serial_data(QString newValue)
{
    if (mserial_data == newValue){
        qDebug()<<"mserial_data = " << mserial_data;
        return;
    }
    mserial_data = newValue;

    if (mserial_data == "31"){
        emit changeTable();
    }
    emit serial_data_Changed(mserial_data);
}

void SerialPort::onReadData()
{
    if(_qSerialPort->bytesAvailable()>0){
        QByteArray data = _qSerialPort->readAll();
        QString value = QString(data).trimmed();
        set_serial_data(value);
    }
}

void SerialPort::openDefault()
{
    _qSerialPort->setPortName("COM6");
    _qSerialPort->setBaudRate(QSerialPort::Baud9600);
    _qSerialPort->setDataBits(QSerialPort::Data8);
    _qSerialPort->setParity(QSerialPort::NoParity);
    _qSerialPort->setStopBits(QSerialPort::OneStop);
    _qSerialPort->setFlowControl(QSerialPort::NoFlowControl);

    if(_qSerialPort->open(QSerialPort::ReadWrite))
        qDebug()<<"Connected to "<< "COM6";
    else {
        qCritical()<<"Serial Port error: " << _qSerialPort->errorString();
    }

}
QString SerialPort::get_serial_data() const
{
    return mserial_data;
}

