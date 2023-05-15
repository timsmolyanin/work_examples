import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3

Window {
    visibility: Window.FullScreen
    screen: Qt.application.screens[0]

    MouseArea {
        anchors.fill: parent
        onClicked: {
            Qt.quit()

        }
    }

    Component.onCompleted : {
        var screens = Qt.application.screens;
        for (var i = 0; i < screens.length; ++i)
            console.log("screen " + screens[i].name + " has geometry " +
                        screens[i].virtualX + ", " + screens[i].virtualY + " " +
                        screens[i].width + "x" + screens[i].height)
    }

    id: root
    maximumWidth: 1920
    minimumHeight: 1080
    visible: true
    title: qsTr("Hello World")

    property alias sendBtn: sendBtn
    property alias dataToSend: dataToSend

    property string dataTransmithToCtrl
    property string commandState: "1" // pause

    property string textBegin

    TableView{
        id: tableView
        anchors{
            fill: parent
            left: parent.left
            right: parent.right
            bottom: parent.bottom

            leftMargin: spinbox5.value
            rightMargin: 30
            topMargin: spinbox6.value
            bottomMargin: 450


        }
        columnSpacing: spinbox3.value - spinbox7.value // Расстояние между столбцами это шаг сетки за вычетом ширины голограммы
        rowSpacing: spinbox4.value - spinbox8.value // Расстояние между строками это шаг сетки за вычетом высоты голограммы

        interactive: false

        clip: true

        model: tableModel

        delegate: Rectangle{
            implicitWidth: spinbox7.value
            implicitHeight: spinbox8.value
            color: "lightgreen"
            border.color: "black"
            border.width: 1

           // clip: true

            layer.enabled: true

            Text {
                text: display
                font.pointSize: 12
                x: spinbox9.value
                y: spinbox10.value
            }
        }
    }


    Button{
        id: button_start
        text: "ПУСК"
        width: parent.width/16
        height: parent.height/9
        font.pointSize: 16
        anchors.top: parent.top
        anchors.topMargin: 850
        anchors.left: parent.left
        anchors.leftMargin: 1212

        onClicked: {
            commandState = "2"
            var txtToSend = commandState + " " + dataToSend.text + " " + dataToSend1.text
            console.log("data to send is " + txtToSend)
            serialPort.writeToSerialPortSlot(txtToSend)

            spinbox1.enabled = false
            spinbox2.enabled = false
            spinbox3.enabled = false
            spinbox4.enabled = false
            spinbox5.enabled = false
            spinbox6.enabled = false
            spinbox7.enabled = false
            spinbox8.enabled = false
            spinbox9.enabled = false
            spinbox10.enabled = false
            spinbox11.enabled = false
            spinbox12.enabled = false
            spinbox13.enabled = false
            spinbox14.enabled = false
            spinbox15.enabled = false

            sendBtn.enabled = false

            dataToSend.enabled = false
            dataToSend1.enabled = false
            textfield1.enabled = false
        }

    }
    Button{
        id: button_pause
        text: "ПАУЗА"
        width: parent.width/16
        height: parent.height/9
        font.pointSize: 16
        anchors.top: parent.top
        anchors.topMargin: 850
        anchors.left: parent.left
        anchors.leftMargin: 1437

        onClicked: {
            commandState = "1"
            var txtToSend = commandState + " " + dataToSend.text + " " + dataToSend1.text
            console.log("data to send is " + txtToSend)
            serialPort.writeToSerialPortSlot(txtToSend)

            spinbox1.enabled = true
            spinbox2.enabled = true
            spinbox3.enabled = true
            spinbox4.enabled = true
            spinbox5.enabled = true
            spinbox6.enabled = true
            spinbox7.enabled = true
            spinbox8.enabled = true
            spinbox9.enabled = true
            spinbox10.enabled = true
            spinbox11.enabled = true
            spinbox12.enabled = true
            spinbox13.enabled = true
            spinbox14.enabled = true
            spinbox15.enabled = true

            sendBtn.enabled = true

            dataToSend.enabled = true
            dataToSend1.enabled = true
            textfield1.enabled = true
        }

    }
    Button{
        id: button_stop
        text: "СТОП"
        width: parent.width/16
        height: parent.height/9
        font.pointSize: 16
        anchors.top: parent.top
        anchors.topMargin: 850
        anchors.left: parent.left
        anchors.leftMargin: 1649

        onClicked: {
            commandState = "0"
            var txtToSend = commandState + " " + "0" + " " + "0"
            console.log("data to send is " + txtToSend)
            serialPort.writeToSerialPortSlot(txtToSend)

            spinbox1.enabled = true
            spinbox2.enabled = true
            spinbox3.enabled = true
            spinbox4.enabled = true
            spinbox5.enabled = true
            spinbox6.enabled = true
            spinbox7.enabled = true
            spinbox8.enabled = true
            spinbox9.enabled = true
            spinbox10.enabled = true
            spinbox11.enabled = true
            spinbox12.enabled = true
            spinbox13.enabled = true
            spinbox14.enabled = true
            spinbox15.enabled = true

            sendBtn.enabled = true

            dataToSend.enabled = true
            dataToSend1.enabled = true
            textfield1.enabled = true

        }
    }

    Button{
        id: sendBtn
        text: qsTr("Отправить")
        width: parent.width/12
        height: parent.height/13
        font.pointSize: 16
        anchors.top: dataToSend.top
        anchors.topMargin: 130
        anchors.left: dataToSend.left

        onClicked:{
            var txtToSend = commandState + " " + dataToSend.text + " " + dataToSend1.text
            console.log("data to send is " + txtToSend)
            serialPort.writeToSerialPortSlot(txtToSend)
        }
    }

    SpinBox{
        id: spinbox1
        anchors.top: parent.top
        anchors.topMargin: 26
        anchors.left: parent.left
        anchors.leftMargin: 517

        from: 1
        to: 100
        value: 1
        editable: true

        onValueChanged: {
            console.log("spinbox1.value = " + spinbox1.value)
            tableView.model.setRowCount(spinbox1.value)
        }

    }

    SpinBox{
        id: spinbox2
        anchors.top: parent.top
        anchors.topMargin: 79
        anchors.left: parent.left
        anchors.leftMargin: 517

        from: 1
        to: 100
        value: 1
        editable: true

        onValueChanged: {
            console.log("spinbox2.value = " + spinbox2.value)
            tableView.model.setColumnCount(spinbox2.value)
        }

    }

    SpinBox{
        id: spinbox3
        anchors.top: parent.top
        anchors.topMargin: 151
        anchors.left: parent.left
        anchors.leftMargin: 517

        editable: true

        from: 1
        value: 60
        to: 100*100
        stepSize: 1*5.6 // 5.6 - коэфф. для пересчета из пикселей в мм

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox7.from, spinbox7.to)
            top: Math.max(spinbox7.from, spinbox7.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox7.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }
    }

    SpinBox{
        id: spinbox4
        anchors.top: parent.top
        anchors.topMargin: 209
        anchors.left: parent.left
        anchors.leftMargin: 517

        editable: true

        from: 1
        value: 60
        to: 100*100
        stepSize: 1*5.6 // 5.6 - коэфф. для пересчета из пикселей в мм

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox7.from, spinbox7.to)
            top: Math.max(spinbox7.from, spinbox7.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox7.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }

    }

    SpinBox{
        id: spinbox5
        anchors.top: parent.top
        anchors.topMargin: 285
        anchors.left: parent.left
        anchors.leftMargin: 517

        editable: true

        from: 1
        value: 677
        to: 100*100
        stepSize: 1*5.6 // 5.6 - коэфф. для пересчета из пикселей в мм

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox5.from, spinbox5.to)
            top: Math.max(spinbox5.from, spinbox5.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox5.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }

    }

    SpinBox{
        id: spinbox6
        anchors.top: parent.top
        anchors.topMargin: 345
        anchors.left: parent.left
        anchors.leftMargin: 517

        editable: true

        from: 1
        value: 72
        to: 100*100
        stepSize: 1*5.6 // 5.6 - коэфф. для пересчета из пикселей в мм

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox6.from, spinbox6.to)
            top: Math.max(spinbox6.from, spinbox6.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox6.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }

    }

    SpinBox{
        id: spinbox7
        anchors.top: parent.top
        anchors.topMargin: 425
        anchors.left: parent.left
        anchors.leftMargin: 517
        editable: true

        from: 1
        value: 50
        to: 100*100
        stepSize: 1*5.6 // 5.6 - коэфф. для пересчета из пикселей в мм

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox7.from, spinbox7.to)
            top: Math.max(spinbox7.from, spinbox7.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox7.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }

    }

    SpinBox{
        id: spinbox8
        anchors.top: parent.top
        anchors.topMargin: 482
        anchors.left: parent.left
        anchors.leftMargin: 517
        editable: true

        from: 1
        value: 50
        to: 100*100
        stepSize: 1*5.6

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox8.from, spinbox8.to)
            top: Math.max(spinbox8.from, spinbox8.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox8.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }

    }

    SpinBox{
        id: spinbox9
        anchors.top: parent.top
        anchors.topMargin: 559
        anchors.left: parent.left
        anchors.leftMargin: 517

        editable: true

        from: 0
        value: 0
        to: 100*100
        stepSize: 1*5.6

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox9.from, spinbox9.to)
            top: Math.max(spinbox9.from, spinbox9.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox9.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }
    }

    SpinBox{
        id: spinbox10
        anchors.top: parent.top
        anchors.topMargin: 619
        anchors.left: parent.left
        anchors.leftMargin: 518

        editable: true

        from: 0
        value: 0
        to: 100*100
        stepSize: 1*5.6

        property int decimals: 0

        validator: IntValidator{
            bottom: Math.min(spinbox10.from, spinbox10.to)
            top: Math.max(spinbox10.from, spinbox10.to)
        }

        textFromValue: function(value, locale) {
            return Number(value/5.6).toLocaleString(locale, 'f', spinbox10.decimals)
        }

        valueFromText: function(text, locale) {
            return Number.fromLocaleString(locale, text) * 5.6
        }
    }

    SpinBox{
        id: spinbox11
        anchors.top: parent.top
        anchors.topMargin: 680
        anchors.left: parent.left
        anchors.leftMargin: 517

    }
    SpinBox{
        id: spinbox12
        anchors.top: parent.top
        anchors.topMargin: 753
        anchors.left: parent.left
        anchors.leftMargin: 517

    }

    SpinBox{
        id: spinbox13
        anchors.top: parent.top
        anchors.topMargin: 803
        anchors.left: parent.left
        anchors.leftMargin: 517
    }



    Label{
        id: label1
        text: "Размер сетки X"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 33
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label2
        text: "Размер сетки Y"
        font.family: "Helvetica"
        font.pointSize: 14

        anchors.top: parent.top
        anchors.topMargin: 79
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label3
        text: "Шаг сетки Х"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 158
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label4
        text: "Шаг сетки Y"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 216
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label5
        text: "Положение сетки Х"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 292
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label6
        text: "Положение сетки Y"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 352
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label7
        text: "Размер зоны персонализации Х"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 429
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label8
        text: "Размер зоны персонализации Y"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 489
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label9
        text: "Положение области персонализации X"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 566
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label10
        text: "Положение области персонализации Y"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 626
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label11
        text: "Угол поворота области персонализации"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 687
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label12
        text: "Количество букв в нумерации"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 760
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label13
        text: "Количество цифр в нумерации"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 810
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label14
        text: "Начало нумерации"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 872
        anchors.left: parent.left
        anchors.leftMargin: 50

    }
    Label{
        id: label15
        text: "Кол-во номеров"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 929
        anchors.left: parent.left
        anchors.leftMargin: 50
    }

    Label{
        id: label19
        text: "Начать с фрейма"
        font.family: "Helvetica"
        font.pointSize: 14
        anchors.top: parent.top
        anchors.topMargin: 986
        anchors.left: parent.left
        anchors.leftMargin: 50
    }

    Label{
        id: label16
        x: 1333
        y: 40
        text: "Начало копирования"
        font.family: "Helvetica"
        font.pointSize: 14
    }

    Label{
        id: label17
        x: 1336
        y: 626
        text: "Конец копированния"
        font.family: "Helvetica"
        font.pointSize: 14
    }

    Label{
        id: label18
        x: 700
        y: 40
        text: "Фрейм"
        font.family: "Helvetica"
        font.pointSize: 14
    }

    TextField{
        id:textfield1
        color: "Black"
        font.pointSize: 14
        width: 150
        height: 40
        anchors.top: parent.top
        anchors.topMargin: 865
        anchors.left: parent.left
        anchors.leftMargin: 517

        onEditingFinished: {
            var txt1 = textfield1.text
            textBegin = txt1

            console.log("textfield1: " + textBegin)
            tableView.model.addDataBegin(textBegin)
        }

    }

    SpinBox{
        id: spinbox14
        anchors.top: parent.top
        anchors.topMargin: 922
        anchors.left: parent.left
        anchors.leftMargin: 517

        from: 0
        to: 9999999

        editable: true

        onValueChanged: {
            var numValue = spinbox14.value

            console.log("numValue: " + numValue)
            tableView.model.addNumsNum(numValue)

        }
    }

    SpinBox{
        id: spinbox15
        anchors.top: parent.top
        anchors.topMargin: 979
        anchors.left: parent.left
        anchors.leftMargin: 517

        from: 0
        to: 9999999

        editable: true

        onValueChanged: {
            var startValue = spinbox15.value

            console.log("startValue: " + startValue)
            tableView.model.addStartWithNum(startValue)

        }
    }


    TextField{
        id: dataToSend
        wrapMode: TextArea.Wrap
        placeholderText: "Задержка для всспышки"
        color: "Black"
        font.pointSize: 14
        width: 350
        height: 50
        anchors{
            bottom: parent.bottom
            bottomMargin: 300
            left: parent.left
            leftMargin: 680
        }
    }
    TextField{
        id: dataToSend1
        y: 750
        wrapMode: TextArea.Wrap
        placeholderText: "Задержка для обновления персонализации"
        color: "Black"
        font.pointSize: 14
        width: 480
        height: 50
        anchors{
            bottom: parent.bottom
            bottomMargin: 240
            left: parent.left
            leftMargin: 680
        }

    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:1080;width:1920}
}
##^##*/
