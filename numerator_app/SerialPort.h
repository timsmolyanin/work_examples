#ifndef SERIALPORT_H
#define SERIALPORT_H

#include <QObject>
#include <QtSerialPort/QSerialPort>
#include <QtSerialPort/QSerialPortInfo>


class SerialPort : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString serial_data READ get_serial_data WRITE set_serial_data NOTIFY serial_data_Changed)
public:
    SerialPort(QObject *parent = 0);
    ~SerialPort();

    QString get_serial_data() const;
    void set_serial_data(QString newValue);

    void openSerialPort(QString comName, int baud);
    void writeToSerialPort(QString message);
    bool getConnectionStatus();
    void closeSerialPort();    

public slots:
    void onReadData();

    void openSerialPortSlot(QString comName, int baud);
    void writeToSerialPortSlot(QString message);
    bool getConnectionStatusSlot();
    void closeSerialPortSlot();

signals:
    void serial_data_Changed(QString newValue);
    void changeTable();
    void testSignal1(int a);
    void testSignal2(QString s);

private:
    QSerialPort *_qSerialPort;

    QString mserial_data;

    QSerialPortInfo portInfo;

    void openDefault();


};
#endif // SERIALPORT_H
