/****************************************************************************
** Meta object code from reading C++ file 'TableModel.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../TableModel.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'TableModel.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_TableModel_t {
    QByteArrayData data[19];
    char stringdata0[232];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_TableModel_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_TableModel_t qt_meta_stringdata_TableModel = {
    {
QT_MOC_LITERAL(0, 0, 10), // "TableModel"
QT_MOC_LITERAL(1, 11, 9), // "sendToQml"
QT_MOC_LITERAL(2, 21, 0), // ""
QT_MOC_LITERAL(3, 22, 5), // "count"
QT_MOC_LITERAL(4, 28, 19), // "onSerialChangeTable"
QT_MOC_LITERAL(5, 48, 19), // "onSetNumNumerations"
QT_MOC_LITERAL(6, 68, 11), // "setRowCount"
QT_MOC_LITERAL(7, 80, 8), // "rowCount"
QT_MOC_LITERAL(8, 89, 14), // "setColumnCount"
QT_MOC_LITERAL(9, 104, 11), // "columnCount"
QT_MOC_LITERAL(10, 116, 12), // "addDataBegin"
QT_MOC_LITERAL(11, 129, 16), // "dataReceiveBegin"
QT_MOC_LITERAL(12, 146, 10), // "addNumsNum"
QT_MOC_LITERAL(13, 157, 14), // "dataReceiveNum"
QT_MOC_LITERAL(14, 172, 15), // "addStartWithNum"
QT_MOC_LITERAL(15, 188, 16), // "dataStartWithNum"
QT_MOC_LITERAL(16, 205, 5), // "Roles"
QT_MOC_LITERAL(17, 211, 8), // "CellRole"
QT_MOC_LITERAL(18, 220, 11) // "DisplayRole"

    },
    "TableModel\0sendToQml\0\0count\0"
    "onSerialChangeTable\0onSetNumNumerations\0"
    "setRowCount\0rowCount\0setColumnCount\0"
    "columnCount\0addDataBegin\0dataReceiveBegin\0"
    "addNumsNum\0dataReceiveNum\0addStartWithNum\0"
    "dataStartWithNum\0Roles\0CellRole\0"
    "DisplayRole"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_TableModel[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       1,   74, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   54,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       4,    0,   57,    2, 0x0a /* Public */,
       5,    0,   58,    2, 0x0a /* Public */,

 // methods: name, argc, parameters, tag, flags
       6,    1,   59,    2, 0x02 /* Public */,
       8,    1,   62,    2, 0x02 /* Public */,
      10,    1,   65,    2, 0x02 /* Public */,
      12,    1,   68,    2, 0x02 /* Public */,
      14,    1,   71,    2, 0x02 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::Int,    3,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,

 // methods: parameters
    QMetaType::Void, QMetaType::Int,    7,
    QMetaType::Void, QMetaType::Int,    9,
    QMetaType::Void, QMetaType::QString,   11,
    QMetaType::Void, QMetaType::QString,   13,
    QMetaType::Void, QMetaType::QString,   15,

 // enums: name, alias, flags, count, data
      16,   16, 0x0,    2,   79,

 // enum data: key, value
      17, uint(TableModel::CellRole),
      18, uint(TableModel::DisplayRole),

       0        // eod
};

void TableModel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<TableModel *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->sendToQml((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: _t->onSerialChangeTable(); break;
        case 2: _t->onSetNumNumerations(); break;
        case 3: _t->setRowCount((*reinterpret_cast< const int(*)>(_a[1]))); break;
        case 4: _t->setColumnCount((*reinterpret_cast< const int(*)>(_a[1]))); break;
        case 5: _t->addDataBegin((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 6: _t->addNumsNum((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 7: _t->addStartWithNum((*reinterpret_cast< QString(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (TableModel::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TableModel::sendToQml)) {
                *result = 0;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject TableModel::staticMetaObject = { {
    QMetaObject::SuperData::link<QAbstractTableModel::staticMetaObject>(),
    qt_meta_stringdata_TableModel.data,
    qt_meta_data_TableModel,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *TableModel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *TableModel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_TableModel.stringdata0))
        return static_cast<void*>(this);
    return QAbstractTableModel::qt_metacast(_clname);
}

int TableModel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QAbstractTableModel::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 8;
    }
    return _id;
}

// SIGNAL 0
void TableModel::sendToQml(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
