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
from PySide6 import QtWidgets
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

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        self._previousFileLoc = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._setupDialog()
        self._makeConnections()

    def _setupDialog(self):
        for s in exporter.supported_suffixes:
            self._ui.fileFormatCombo.addItem(s)

    def _makeConnections(self):
        self._ui.idLineEdit.textChanged.connect(self.validate)
        self._ui.fileLocButton.clicked.connect(self._fileLocClicked)
        self._ui.fileLocLineEdit.textChanged.connect(self._fileLocEdited)

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.StandardButton.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration', 'This configuration is invalid.  Unpredictable behaviour '
                                                   'may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                                                   QtWidgets.QMessageBox.StandardButton(QtWidgets.QMessageBox.StandardButton.Yes |
                                                                                        QtWidgets.QMessageBox.StandardButton.No),
                                                   QtWidgets.QMessageBox.StandardButton.No)

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QDialog.accept(self)

    def set_workflow_location(self, location):
        self._workflow_location = location

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        id_value = self.identifierOccursCount(self._ui.idLineEdit.text())
        id_valid = (id_value == 0) or (id_value == 1 and self._previousIdentifier == self._ui.idLineEdit.text())
        self._ui.idLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET if id_valid else INVALID_STYLE_SHEET)

        output_location = self._output_location()
        if self._workflow_location:
            output_location = os.path.join(self._workflow_location, output_location)

        file_loc_valid = os.path.exists(os.path.dirname(output_location))
        self._ui.fileLocLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET if file_loc_valid else INVALID_STYLE_SHEET)

        valid = id_valid and file_loc_valid
        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(id_valid)

        return valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.idLineEdit.text()
        self._previousFileLoc = self._ui.fileLocLineEdit.text()
        config = {
            'identifier': self._ui.idLineEdit.text(),
            'fileFormat': self._ui.fileFormatCombo.currentText(),
            'fileLoc': self._ui.fileLocLineEdit.text()
        }
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._previousFileLoc = config['fileLoc']
        self._ui.idLineEdit.setText(config['identifier'])
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
            display_location = self._output_location(location[0])
            self._ui.fileLocLineEdit.setText(display_location)

    def _output_location(self, location=None):
        if location is None:
            display_path = self._ui.fileLocLineEdit.text()
        else:
            display_path = location
        if self._workflow_location and os.path.isabs(display_path):
            display_path = os.path.relpath(display_path, self._workflow_location)

        return display_path

    def _fileLocEdited(self):
        self.validate()
