from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon

from icecream import ic

from methods.json_methods import ConfigMethods

import sqlite3

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUIConfig()
        self.conn = sqlite3.connect('browser.db')
        self.curs = self.conn.cursor()


    def initUIConfig(self):
       self.closeBtn = QPushButton(self)
       self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
       self.closeBtn.clicked.connect(self.closeConfig)
       self.closeBtn.setGeometry(5, 10, 390, 30)


       #URL do Botao Inicial
       self.homeLabel = QLabel(self)
       self.homeLabel.setText('URL do Botao Inicial')
       self.homeLabel.setGeometry(20, 80, 130, 30)

       self.homeEdit = QLineEdit(self)
       self.homeEdit.setText(f"{ConfigMethods().loadJson()['homeURL']}")
       self.homeEdit.setGeometry(180, 80, 200, 30)


       #URL da Pagina Inicial
       self.newPageLabel = QLabel(self)
       self.newPageLabel.setText('URL da Pagina Inicial')
       self.newPageLabel.setGeometry(20, 150, 130, 30)
       
       self.newPageEdit = QLineEdit(self)
       self.newPageEdit.setText(f"{ConfigMethods().loadJson()['newTabURL']}")
       self.newPageEdit.setGeometry(180, 150, 200, 30)


       #Engine de Busca
       self.searchEngineLabel = QLabel(self)
       self.searchEngineLabel.setText('Engine de Busca')
       self.searchEngineLabel.setGeometry(20, 220, 200, 30)

       self.searchEngineCombo = QComboBox(self)
       self.searchEngineCombo.addItem('Google')
       self.searchEngineCombo.addItem('Yahoo')
       self.searchEngineCombo.addItem('Bing')
       self.searchEngineCombo.addItem('DuckDuckGo')
       self.searchEngineCombo.setGeometry(180, 220, 200, 30)

       if ConfigMethods().loadJson()['searchEngine'] == "Google":
            self.searchEngineCombo.setCurrentIndex(0)

       elif ConfigMethods().loadJson()['searchEngine'] == "Yahoo":
            self.searchEngineCombo.setCurrentIndex(1)

       elif ConfigMethods().loadJson()['searchEngine'] == "Bing":
            self.searchEngineCombo.setCurrentIndex(2)

       elif ConfigMethods().loadJson()['searchEngine'] == "DuckDuckGo":
            self.searchEngineCombo.setCurrentIndex(3)


       #Salvar Dados
       self.saveBtn = QPushButton(self)
       self.saveBtn.setText('Salvar Dados')
       self.saveBtn.clicked.connect(self.saveAllData)
       self.saveBtn.setGeometry(5, 380, 390, 30)


       with open('assets/css/config.css') as file:
           self.setStyleSheet(file.read())

       QMetaObject.connectSlotsByName(self)

       self.setGeometry(70, 340, 400, 420)
       self.setWindowFlags(Qt.WindowType.Popup)


    def saveAllData(self) -> None:
        homeText = self.homeEdit.text()
        newPageText = self.newPageEdit.text()
        engineText = self.searchEngineCombo.currentText()


        fncReplace = self.replaceUrl({'homeURL': homeText, 'newPageUrl': newPageText})

        ConfigMethods().writeJson('homeURL', fncReplace['homeURL'])
        ConfigMethods().writeJson('newTabURL', fncReplace['newPageURL'])
        ConfigMethods().writeJson('searchEngine', engineText)


    def replaceUrl(self, url: dict) -> dict:
        newDict = {}
        if not str(url['homeURL']).startswith('https://'): 
            newDict = {'homeURL': f'https://{url['homeURL']}', 'newPageURL': f'{ConfigMethods().loadJson()['newTabURL']}'}

        elif not str(url['newPageUrl']).startswith('https://'):
            newDict = {'homeURL': f'{ConfigMethods().loadJson()['homeURL']}', 'newPageURL': f'https://{url['newPageURL']}'}
            
        return newDict


    def closeConfig(self):
        self.close()