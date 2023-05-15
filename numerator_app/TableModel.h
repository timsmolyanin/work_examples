#ifndef TABLEMODEL_H
#define TABLEMODEL_H

#include <QObject>
#include <QAbstractTableModel>
#include <array>
#include <QPoint>


class TableModel : public QAbstractTableModel
{
    Q_OBJECT

    Q_ENUMS(Roles)
public:

    enum Roles {
        CellRole,
        DisplayRole
    };

    QHash<int, QByteArray> roleNames() const override {
        return {
            { CellRole, "value" },
            {Qt::DisplayRole, "display"}
        };
    }

    explicit TableModel(QObject *parent = nullptr);

    int rowCount(const QModelIndex & = QModelIndex()) const override;
    Q_INVOKABLE void setRowCount(const int rowCount);

    int columnCount(const QModelIndex & = QModelIndex()) const override;
    Q_INVOKABLE void setColumnCount(const int columnCount);

    QVariant data(const QModelIndex &index, int role) const override;

    Q_INVOKABLE void addDataBegin(QString dataReceiveBegin);
    Q_INVOKABLE void addNumsNum(QString dataReceiveNum);
    Q_INVOKABLE void addStartWithNum(QString dataStartWithNum);

signals:
    void sendToQml(int count);

public slots:
    void onSerialChangeTable();
    void onSetNumNumerations();

private:
    int column_count;
    int row_count;
    int table_size = 0;

    QString dataNumBegin;
    int dataNum;
    QString receiveDataStartWithNum;

    QString numLetters;
    QString numDigitsBegin;

};

#endif // TABLEMODEL_H
