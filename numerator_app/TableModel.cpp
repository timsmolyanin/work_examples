#include <QDebug>

#include "TableModel.h"
#include <QPoint>
#include <vector>

TableModel::TableModel(QObject *parent) : QAbstractTableModel(parent)
{
    row_count = 1;
    column_count = 1;

    table_size = row_count*column_count;
}

int TableModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return 0;

    return row_count;
}

void TableModel::setRowCount(const int rowCount)
{
    qInfo() << row_count << " x " << column_count;

    row_count = rowCount;

    table_size = row_count*column_count;

    //    qInfo() << "row_count = " << row_count;

    beginResetModel();
    endResetModel();
}

int TableModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return 0;

    return column_count;
}

void TableModel::setColumnCount(const int columnCount)
{
    qInfo() << row_count << " x " << column_count;

    column_count = columnCount;

    table_size = row_count*column_count;

    //    qInfo() << "column_count = " << column_count;

    beginResetModel();
    endResetModel();
}

QVariant TableModel::data(const QModelIndex &index, int role) const
{
    QVariant data;
    int N = dataNum;
    int size_digits = numDigitsBegin.length();

    int digits = numDigitsBegin.toInt();

    switch (role) {
    case Qt::DisplayRole:

        return data = QString("%1 %2").arg(numLetters).arg((digits + ((N/column_count)*(index.column()) + index.row())), size_digits, 10, QLatin1Char('0'));

    default:
        break;
    }
    return data;
}

void TableModel::addDataBegin(QString dataReceiveBegin)
{
    int letters_count = 0;
    int digits_count = 0;
    dataNumBegin = dataReceiveBegin;

    foreach(QChar str, dataReceiveBegin){
        if(str.isLetter()){
            numLetters += str;
            letters_count++;
        }
        else if(str.isDigit()){
            numDigitsBegin += str;
            digits_count++;
        }
    }
    qInfo() << "dataBeginNum letters is " << numLetters;
    qInfo() << "dataBeginNum digits is " << numDigitsBegin;

    beginResetModel();
    endResetModel();
}

void TableModel::addNumsNum(QString dataReceiveNum)
{
    dataNum = dataReceiveNum.toInt();

    qInfo() << "dataNum: " << dataNum;

    beginResetModel();
    endResetModel();
}

void TableModel::addStartWithNum(QString dataStartWithNum)
{
    receiveDataStartWithNum = dataStartWithNum;

    qInfo() << "dataStartWithNum: " << receiveDataStartWithNum;

    beginResetModel();
    endResetModel();
}

void TableModel::onSerialChangeTable()
{
    qInfo() << Q_FUNC_INFO;

    setRowCount(3);
    setColumnCount(5);

    qInfo() << row_count << " x " << column_count;
}

void TableModel::onSetNumNumerations()
{

}
