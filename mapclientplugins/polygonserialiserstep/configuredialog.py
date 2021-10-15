"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""

import os
from PySide2 import QtWidgets
from mapclientplugins.polygonserialiserstep.ui_configuredialog import Ui_Dialog
from mapclientplugins.polygonserialiserstep import exporter

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        self._workflow_location = None

        self._setupDialog()
        self._makeConnections()

    def _setupDialog(self):
        for s in exporter.supported_suffixes:
            self._ui.fileFormatCombo.addItem(s)

    def _makeConnections(self):
        self._ui.fileLocButton.clicked.connect(self._fileLocClicked)
        self._ui.fileLocLineEdit.textChanged.connect(self._fileLocEdited)

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        output_path = self._ui.fileLocLineEdit.text()
        output_directory = os.path.dirname(output_path)
        non_empty = len(output_path)

        if not os.path.isabs(output_path):
            output_directory = os.path.join(self._workflow_location, output_directory)

        output_directory_valid = os.path.exists(output_directory) and non_empty

        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(output_directory_valid)
        self._ui.fileLocLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET if output_directory_valid else INVALID_STYLE_SHEET)

        return output_directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.
        """
        self._previousFileLoc = self._ui.fileLocLineEdit.text()
        config = {}
        config['fileFormat'] = self._ui.fileFormatCombo.currentText()
        config['fileLoc'] = self._ui.fileLocLineEdit.text()
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.
        """
        self._previousFileLoc = config['fileLoc']
        self._ui.fileFormatCombo.setCurrentIndex(
            exporter.supported_suffixes.index(
                config['fileFormat']
            )
        )
        self._ui.fileLocLineEdit.setText(config['fileLoc'])

    def _fileLocClicked(self):
        location = QtWidgets.QFileDialog.getSaveFileName(self, 'Select File Location', self._previousFileLoc)
        if location[0]:
            self._previousFileLoc = location[0]
            self._ui.fileLocLineEdit.setText(location[0])

    def _fileLocEdited(self):
        self.validate()
