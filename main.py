import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType
import os
import sqlite3

FORM_CLASS,_=loadUiType(os.path.join(os.path.dirname(__file__), "uis\main.ui"))

class Main(QMainWindow, FORM_CLASS):
    '''
    QMainWindowClass 
    '''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handelButtons()
        self.navigate()

    def handelButtons(self):
        ''' Function to Conntain all Buttons Events'''
        self.refreshBtn.clicked.connect(self.getDATA)
        self.searchBtn.clicked.connect(self.search)
        self.checkBtn.clicked.connect(self.levelTop)
        self.updateBtn.clicked.connect(self.updateDb)
        self.deleteBtn.clicked.connect(self.deleteData)
        self.addBtn.clicked.connect(self.addData)

    
    def updateDb(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        id = int(self.idLabel.text())
        reference = self.referenceText.text()
        partName = self.partNameText.text()
        minArea = self.minAreaText.text()
        maxArea = self.maxAreaText.text()
        minDiameter = self.minDiameterText.text()
        maxDiameter = self.maxDiameterText.text()
        nbrOfHoles = self.nbrOfHolesText.text()
        count = str(self.editInvCountSpinBox.value())

        row = (reference, partName, minArea, maxArea, minDiameter, maxDiameter, nbrOfHoles, count, id)

        sqlUpdateCommand = '''update parts_table SET partReference=?,partName=?,minArea=?,maxArea=?,minDiameter=?,maxDiameter=?,NumberOfHoles=?,Count=? where Id=?'''

        cursor.execute(sqlUpdateCommand,row)

        db.commit()
        self.prozessLabel.setText(str("Item was update"))

    def addData(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        reference = self.referenceText.text()
        partName = self.partNameText.text()
        minArea = self.minAreaText.text()
        maxArea = self.maxAreaText.text()
        minDiameter = self.minDiameterText.text()
        maxDiameter = self.maxDiameterText.text()
        nbrOfHoles = self.nbrOfHolesText.text()
        count = str(self.editInvCountSpinBox.value())

        row = (reference, partName, minArea,maxArea, minDiameter, maxDiameter,nbrOfHoles,count)

        sqlAddCommand = '''INSERT INTO parts_table (partReference,partName,minArea,maxArea,minDiameter,maxDiameter, NumberOfHoles, Count) VALUES (?,?,?,?,?,?,?,?)'''

        cursor.execute(sqlAddCommand,row)

        db.commit()
        self.prozessLabel.setText(str("Item was added"))

    def deleteData(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
       
        id = self.idLabel.text()

        sqlDeleteCommand = '''delete from parts_table where Id=?'''

        cursor.execute(sqlDeleteCommand,id)

        db.commit()
        self.prozessLabel.setText(str("Item was deleted")) 

    def levelTop(self):
        '''insert the top datas '''
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        sqlCommand = '''select partReference, partName, Count from parts_table order by Count asc limit 3'''

        result = cursor.execute(sqlCommand)

        self.topTable.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.topTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.topTable.setItem(row_number,column_number, QTableWidgetItem(str(data)))
    
    def search(self):
        ''' search the database for refence by using the count level lower or equal to the count we give in the SpinBox '''
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        nbrCount = int(self.detailInvCountSpinBox.text())

        sqlCommand = '''select * from parts_table where count<=? '''

        result = cursor.execute(sqlCommand, [nbrCount])
        self.listTable.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.listTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.listTable.setItem(row_number,column_number, QTableWidgetItem(str(data)))

    
    def getDATA(self):
        ''' Connect to Sqlite 3 Database by using sql'''
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        sqlCommand = '''select * from parts_table'''

        result = cursor.execute(sqlCommand)

        self.listTable.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.listTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.listTable.setItem(row_number,column_number, QTableWidgetItem(str(data)))


        # fill the InventoryStatic Tab 
        invStaticCursor = db.cursor()
        
        sqlComCountPartNames = '''select count (distinct partName) from parts_table'''
        sqlComCountReference = '''select count (distinct partReference) from parts_table'''

        resultCountParts = invStaticCursor.execute(sqlComCountPartNames)
        self.partsCounterLbl.setText(str(resultCountParts.fetchone()[0]))

        resultCountReference = invStaticCursor.execute(sqlComCountReference)
        self.referenceCounterLbl.setText(str(resultCountReference.fetchone()[0]))

        # fill the last 4 

        sqlComMinReference = '''select min (NumberOfHoles), partReference from parts_table'''
        sqlComMaxReference = '''select max (NumberOfHoles), partReference from parts_table'''

        resMinReference = invStaticCursor.execute(sqlComMinReference)
        r1 = resMinReference.fetchone()
        self.minHolesLbl.setText(str(r1[0]))
        self.minHolesReferenceLbl.setText(str(r1[1]))

        resMaxReference = invStaticCursor.execute(sqlComMaxReference)
        r2 = resMaxReference.fetchone()
        self.maxHolesLbl.setText(str(r2[0]))
        self.maxHolesReferenceLbl.setText(str(r2[1]))

    def navigate(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        sqlCommand = '''select * from parts_table'''

        result = cursor.execute(sqlCommand)
        val = result.fetchone()

        self.idLabel.setText(str(val[0]))
        self.referenceText.setText(str(val[1]))
        self.partNameText.setText(str(val[2]))
        self.maxAreaText.setText(str(val[3]))
        self.minAreaText.setText(str(val[4]))
        self.nbrOfHolesText.setText(str(val[5]))
        self.minDiameterText.setText(str(val[6]))
        self.maxDiameterText.setText(str(val[7]))
        self.editInvCountSpinBox.setValue(val[8])

def main():
    app = QApplication(sys.argv)
    window= Main()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
