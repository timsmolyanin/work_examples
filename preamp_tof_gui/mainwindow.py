

from PySide2 import QtWidgets, QtCore, QtGui
import styles


class UiMainWindow(object):
    def setup_ui(self, MainWindow, ids):
        self.ids = ids
        horizontal_header_text = ['ID', 'V+,\nmV', 'V-,\nmV', 'Vdelta,\nmV', 'Vpower,\nmV',
                                  'DAC,\nmV', 'Tboard,\n°C', 'Tgas,\n°C']

        number_of_columns = len(horizontal_header_text)

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName('central')

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.inner_settings_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.inner_settings_layout)

        self.table_widget = QtWidgets.QTableWidget()
        self.main_layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(number_of_columns)
        self.table_widget.setHorizontalHeaderLabels(horizontal_header_text)
        self.table_widget.setColumnWidth(0, 30)

        for i in range(1, number_of_columns):
            self.table_widget.setColumnWidth(i, 85)

        self.table_widget.setFont(styles.def_font)
        self.table_widget.setStyleSheet(styles.some_style_sheet)

        self.table_widget.horizontalHeader().setFont(styles.larger_font)
        self.table_widget.horizontalHeader().setStyleSheet(styles.header_style_sheet)
        self.table_widget.horizontalHeader().setHighlightSections(False)
        self.table_widget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.table_widget.verticalHeader().hide()

        self.table_widget.setFixedHeight(self.table_widget.horizontalHeader().height() + 30)

        self.create_table_amps()

        self.table_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.table_widget.setFixedWidth(
            self.table_widget.horizontalHeader().length() + self.table_widget.verticalScrollBar().sizeHint().width())

        self.table_widget.setFixedHeight(
            self.table_widget.verticalHeader().length() + self.table_widget.verticalScrollBar().sizeHint().width() + 50)

        vert_head_height = 0
        count = self.table_widget.verticalHeader().count()
        for i in range(count):
            vert_head_height += self.table_widget.verticalHeader().sectionSize(i)

        #
        # table_max_h = self.table_widget.horizontalHeader().height() + vert_head_height + 3
        # self.table_widget.setMaximumHeight(table_max_h)

        self.status_group_box = QtWidgets.QGroupBox('')
        self.status_hbox = QtWidgets.QHBoxLayout()

        self.status_label_text = QtWidgets.QLabel('Some of preamps is no response')
        self.status_label_text.setFont(styles.status_font)

        self.status_label = QtWidgets.QLabel()
        self.status_label.setStyleSheet("background-color: #deca99")
        self.status_label.setFixedWidth(20)

        self.status_hbox.addWidget(self.status_label_text)
        self.status_hbox.addWidget(self.status_label)

        self.status_group_box.setLayout(self.status_hbox)
        self.status_group_box.setFixedSize(300, 40)

        MainWindow.setCentralWidget(self.central_widget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_table_amps(self):
        number_of_rows = len(self.ids)
        current_row = 0

        self.table_widget.setRowCount(number_of_rows)
        for i in self.ids:
            setattr(self, f'amp_{i}', Amp(i))
            amp = getattr(self, f'amp_{i}')
            id_cell = getattr(amp, 'id_cell')
            self.table_widget.setItem(current_row, 0, id_cell)
            id_cell.setText(str(i))
            id_cell.setFont(styles.id_font)

            self.table_widget.setItem(current_row, 1, getattr(amp, 'vplus_cell'))
            self.table_widget.setItem(current_row, 2, getattr(amp, 'vminus_cell'))
            self.table_widget.setItem(current_row, 3, getattr(amp, 'vdelta_cell'))
            self.table_widget.setItem(current_row, 4, getattr(amp, 'vpower_cell'))
            self.table_widget.setItem(current_row, 5, getattr(amp, 'dac_cell'))
            self.table_widget.setItem(current_row, 6, getattr(amp, 'tboard_cell'))
            self.table_widget.setItem(current_row, 7, getattr(amp, 'tgas_cell'))

            color = [235, 235, 235]

            if current_row % 2 == 0:
                self.paint_the_rows(amp, color)

            current_row += 1

    def paint_the_rows(self, amp, color):
        red, green, blue = color
        getattr(amp, 'vplus_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'vminus_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'vdelta_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'vpower_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'dac_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'tboard_cell').setBackground(QtGui.QColor(red, green, blue))
        getattr(amp, 'tgas_cell').setBackground(QtGui.QColor(red, green, blue))


class ValuesTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, parent=None):
        QtWidgets.QTableWidgetItem.__init__(self, parent)
        self.setTextAlignment(QtCore.Qt.AlignCenter)


class Amp():
    def __init__(self, idx):

        self.idx = idx

        self.set_widgets()

        self.vplus = 0
        self.vminus = 0
        self.vpower = 0
        self.dac = 0
        self.tboard = 0
        self.tgas = 0
        self.vdelta = 0

    def set_widgets(self):
        self.id_cell = ValuesTableWidgetItem()
        self.vplus_cell = ValuesTableWidgetItem()
        self.vminus_cell = ValuesTableWidgetItem()
        self.vpower_cell = ValuesTableWidgetItem()
        self.dac_cell = ValuesTableWidgetItem()
        self.tboard_cell = ValuesTableWidgetItem()
        self.tgas_cell = ValuesTableWidgetItem()
        self.vdelta_cell = ValuesTableWidgetItem()