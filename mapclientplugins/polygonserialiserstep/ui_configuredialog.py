# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/configuredialog.ui'
#
# Created: Wed Jun  3 21:04:02 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 228)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.configGroupBox = QtGui.QGroupBox(Dialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.idLabel = QtGui.QLabel(self.configGroupBox)
        self.idLabel.setObjectName("idLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.idLabel)
        self.idLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.idLineEdit.setObjectName("idLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.idLineEdit)
        self.fileFormatLabel = QtGui.QLabel(self.configGroupBox)
        self.fileFormatLabel.setObjectName("fileFormatLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fileFormatLabel)
        self.fileFormatCombo = QtGui.QComboBox(self.configGroupBox)
        self.fileFormatCombo.setObjectName("fileFormatCombo")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fileFormatCombo)
        self.fileLocLabel = QtGui.QLabel(self.configGroupBox)
        self.fileLocLabel.setObjectName("fileLocLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.fileLocLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileLocLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.fileLocLineEdit.setObjectName("fileLocLineEdit")
        self.horizontalLayout.addWidget(self.fileLocLineEdit)
        self.fileLocButton = QtGui.QPushButton(self.configGroupBox)
        self.fileLocButton.setObjectName("fileLocButton")
        self.horizontalLayout.addWidget(self.fileLocButton)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.idLineEdit, self.fileFormatCombo)
        Dialog.setTabOrder(self.fileFormatCombo, self.fileLocLineEdit)
        Dialog.setTabOrder(self.fileLocLineEdit, self.fileLocButton)
        Dialog.setTabOrder(self.fileLocButton, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Configure Polygon Export Step", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setText(QtGui.QApplication.translate("Dialog", "Identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.fileFormatLabel.setText(QtGui.QApplication.translate("Dialog", "File Format:", None, QtGui.QApplication.UnicodeUTF8))
        self.fileLocLabel.setText(QtGui.QApplication.translate("Dialog", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.fileLocButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))

