import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import random
from MyCalculator import MyCalculator

import interface  # Это наш конвертированный файл дизайна

class MyTable(QtCore.QAbstractTableModel):
    def __init__(self, N):
        super().__init__()
        self.myData = []
        self.myUpdate(N)

    def myUpdate(self, N):
        self.N = N
        #self.myData = [[0]*3 for i in range(N)]
        self.makeData()
        print(self.myData)

    def makeData(self):
        index = QtCore.QModelIndex()
        index.siblingAtRow(0)
        index.siblingAtColumn(0)
        self.removeRows(0, len(self.myData), index)
        for i in range(self.N):
            index = QtCore.QModelIndex()
            index.siblingAtRow(i)
            index.siblingAtColumn(0)
            self.setData(index, self.flags(index), random.random() * 10)
            self.insertRows(i, 1, index)
            self.myData[i][0] = random.random() * 10
            self.myData[i][1] = random.random() * 10
            self.myData[i][2] = 1
            self.myData.sort()
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.myData[index.row()][index.column()] = int(value)
        print(self.myData, role)
        return True
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.myData[index.row()][index.column()]
    def flags(self, index):
        if(index.column() == 2):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable | QtCore.QAbstractTableModel.flags(self, index)
        else:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled  | QtCore.QAbstractTableModel.flags(self, index)
    def rowCount(self, buffer):
        return self.N
    def columnCount(self, buffer):
        return 3
    def insertRows(self, row, count, index):
        self.beginInsertRows(index, row, row + count - 1)
        for i in range(count):
            self.myData.insert(row, [0, 0, 0])
        self.endInsertRows()
        return True
    def removeRows(self, row, count, index):
        self.beginRemoveRows(index, row, row + count - 1)
        for i in range(count):
            self.myData.pop(row)
            print(row)
        self.endRemoveRows()
        return True

class MyMainWindow(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    table = None
    def makeTable(self):
        if self.table == None:
            self.table = MyTable(int(self.N_line.text()))
            self.tableView.setModel(self.table)        
        else:
            self.table.myUpdate(int((self.N_line.text())))
        index = QtCore.QModelIndex()
        index.siblingAtRow(1)
        index.siblingAtColumn(0)
        self.tableView.update(index)     
    def drawPlot(self):
        self.myCalculator.drawPlot(self.table.myData, int((self.lineEdit.text())))
    def setConnect(self):
        self.makeTableButton.clicked.connect(self.makeTable)
        self.drawButton.clicked.connect(self.drawPlot)
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.setConnect()
        #self.N_line.setValidator(QtGui.QIntValidator)
        #self.lineEdit.setValidator(QtGui.QIntValidator)
        self.myCalculator = MyCalculator()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyMainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
