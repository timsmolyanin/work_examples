
from PySide2 import QtGui

def_font = QtGui.QFont()
def_font.setFamily("Tahoma")
def_font.setPointSize(12)
def_font.setWeight(50)

larger_font = QtGui.QFont()
larger_font.setFamily("Tahoma")
larger_font.setPointSize(14)
larger_font.setWeight(63)

id_font = QtGui.QFont()
id_font.setFamily("Tahoma")
id_font.setPointSize(14)
id_font.setWeight(50)

status_font = QtGui.QFont()
status_font.setFamily("Tahoma")
status_font.setPointSize(10)
status_font.setWeight(30)

state_font = QtGui.QFont()
state_font.setFamily("Tahoma")
state_font.setPointSize(13)
state_font.setWeight(40)

header_style_sheet = 'QHeaderView::section {border-bottom: 1 solid black; background-color: rgb(230, 230, 230);}'
some_style_sheet = 'QTableWidget:item:selectable{color: black;} QTableWidget::item:selected{ background-color: #0078D7}'