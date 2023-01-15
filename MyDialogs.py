# -----------------------------------------------------------
# Copyright (C) 2022 Ludwig Kniprath
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QDockWidget, QWidget, QDoubleSpinBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTranslator, QCoreApplication, QLocale

import os

class LRefDockWidget(QDockWidget):
    '''Ergebnis-Dialog für die Lineare Referenzierung

    QDockWidget → andockbares Fenster,
    ähnlich wie QDialog,
    muss via self.iface.addDockWidget(...) hinzugefügt werden, um innerhalb der QGis-App canvas andockbar zu sein
    sonst frei auf dem Desktop
    '''

    def __init__(self, iface, parent=None):
        '''Konstruktor, Hardcore-Qt/Python, ohne ui
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        :param parent: Qt-Elternelement, in welchem das Widget angedockt werden kann
        '''
        QDockWidget.__init__(self, parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )



        self.iface = iface

        self.setWindowTitle(self.tr("Linear Referencing"))

        self.canvas_unit_widgets = []
        self.canvas_measure_widgets = []

        self.layer_unit_widgets = []
        self.layer_measure_widgets = []

        self.wdg_central = QWidget(self)

        self.setWidget(self.wdg_central)

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel(self.tr('Reference Layer:'), self), 0, 0)

        self.le_pt1_layer_name = QLineEdit(self)
        self.layout.addWidget(self.le_pt1_layer_name, 0, 1, 1, 4)

        self.layout.addWidget(QLabel('Feature-ID:', self), 1, 0)
        self.le_snapped_fid = QLineEdit(self)
        self.le_snapped_fid.setValidator(QIntValidator(0,1000000000))
        self.layout.addWidget(self.le_snapped_fid, 1, 1, 1, 2)
        self.layout.addWidget(QLabel('Offset:', self), 1, 3)

        self.dspbx_offset = QDoubleSpinBox(self)
        self.dspbx_offset.setValue(0)
        self.dspbx_offset.setMinimum(-1000)
        self.dspbx_offset.setMaximum(1000)
        self.layer_measure_widgets.append(self.dspbx_offset)
        self.layout.addWidget(self.dspbx_offset, 1, 4)

        unit_widget_1 = QLabel('[]', self)
        self.layout.addWidget(unit_widget_1, 1, 5)
        self.layer_unit_widgets.append(unit_widget_1)



        self.layout.addWidget(QLabel(self.tr('Point...'), self), 2, 0)

        self.pb_pt1_redigitize = QPushButton('...1',self)
        self.pb_pt1_redigitize.setFixedSize(50, 20)
        self.pb_pt1_redigitize.setStyleSheet("QPushButton { border: 3px solid lime; }")
        self.pb_pt1_redigitize.setIconSize(QtCore.QSize(12, 12))
        self.pb_pt1_redigitize.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icons/crosshairs-gps.svg')))
        self.pb_pt1_redigitize.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_pt1_redigitize.setToolTip(self.tr("Re-Digitize Point 1"))
        self.layout.addWidget(self.pb_pt1_redigitize, 2,1 , 1,2, Qt.AlignCenter)

        self.pb_pt2_redigitize = QPushButton('...2',self)
        self.pb_pt2_redigitize.setFixedSize(50, 20)
        self.pb_pt2_redigitize.setStyleSheet("QPushButton { border: 3px solid red; }")
        self.pb_pt2_redigitize.setIconSize(QtCore.QSize(12, 12))
        self.pb_pt2_redigitize.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icons/crosshairs-gps.svg')))
        self.pb_pt2_redigitize.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_pt2_redigitize.setToolTip(self.tr("Re-Digitize Point 2"))
        self.layout.addWidget(self.pb_pt2_redigitize, 2,3,1,2, Qt.AlignCenter)


        self.layout.addWidget(QLabel('Map x/y:', self), 3, 0)
        self.le_map_pt1_x = QLineEdit(self)
        self.le_map_pt1_y = QLineEdit(self)
        self.layout.addWidget(self.le_map_pt1_x, 3, 1)
        self.layout.addWidget(self.le_map_pt1_y, 3, 2)
        self.le_map_pt2_x = QLineEdit(self)
        self.le_map_pt2_y = QLineEdit(self)
        self.layout.addWidget(self.le_map_pt2_x, 3, 3)
        self.layout.addWidget(self.le_map_pt2_y, 3, 4)
        unit_widget_2 = QLabel('[]', self)
        self.layout.addWidget(unit_widget_2, 3, 5)
        self.canvas_unit_widgets.append(unit_widget_2)

        self.layout.addWidget(QLabel('Snap x/y:', self), 4, 0)
        self.le_snap_pt1_x = QLineEdit(self)
        self.le_snap_pt1_y = QLineEdit(self)
        self.layout.addWidget(self.le_snap_pt1_x, 4, 1)
        self.layout.addWidget(self.le_snap_pt1_y, 4, 2)
        self.le_snap_pt2_x = QLineEdit(self)
        self.le_snap_pt2_y = QLineEdit(self)
        self.layout.addWidget(self.le_snap_pt2_x, 4, 3)
        self.layout.addWidget(self.le_snap_pt2_y, 4, 4)
        unit_widget_3 = QLabel('[]', self)
        self.layout.addWidget(unit_widget_3, 4, 5)
        self.canvas_unit_widgets.append(unit_widget_3)

        self.layout.addWidget(QLabel(self.tr('Measure:'), self), 5, 0)
        self.dspbx_pt1_m = QDoubleSpinBox(self)
        #erst bei Enter das valueChanged-Signal auslösen, nicht bei jeder einzelnen Änderung
        self.dspbx_pt1_m.setKeyboardTracking(False)
        #beachten: beim programmgesteuerten Setzen des Wertes (setValue() vs. Benutzereingabe) via blockSignals das valueChanged-Signal unterbinden

        self.layer_measure_widgets.append(self.dspbx_pt1_m)
        self.dspbx_pt1_m.setRange(0, 999999999)
        self.dspbx_pt2_m = QDoubleSpinBox(self)
        self.dspbx_pt2_m.setKeyboardTracking(False)
        self.layer_measure_widgets.append(self.dspbx_pt2_m)
        self.dspbx_pt2_m.setRange(0, 999999999)
        self.layout.addWidget(self.dspbx_pt1_m, 5, 1, 1, 2)
        self.layout.addWidget(self.dspbx_pt2_m, 5, 3, 1, 2)
        unit_widget_4 = QLabel('[]', self)
        self.layout.addWidget(unit_widget_4, 5, 5)
        self.layer_unit_widgets.append(unit_widget_4)

        self.layout.addWidget(QLabel(self.tr('Distance:'), self), 6, 0)
        self.dspbx_pt_dist = QDoubleSpinBox(self)
        self.dspbx_pt_dist.setRange(-999999999, 999999999)
        self.dspbx_pt_dist.setKeyboardTracking(False)
        self.layout.addWidget(self.dspbx_pt_dist, 6, 2, 1, 2)
        self.layer_measure_widgets.append(self.dspbx_pt_dist)

        self.pb_lock_dist = QPushButton(self)
        self.pb_lock_dist.setFixedSize(20, 20)
        self.pb_lock_dist.setStyleSheet("QPushButton { border: none; }")
        self.pb_lock_dist.setIconSize(QtCore.QSize(20, 20))
        self.pb_lock_dist.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icons/lock-open-variant-outline.svg')))
        self.pb_lock_dist.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_lock_dist.setToolTip(self.tr("Fix Distance"))
        self.layout.addWidget(self.pb_lock_dist, 6, 4)

        unit_widget_5 = QLabel('[]', self)
        self.layout.addWidget(unit_widget_5, 6, 5)
        self.layer_unit_widgets.append(unit_widget_5)

        self.pbtn_reset = QPushButton(self)
        self.pbtn_reset.setText("Reset")
        # clicked.connect siehe LinearReferencing, von dort aus wird auch das u. a. "reset()" angestoßen
        self.layout.addWidget(self.pbtn_reset, 7, 0, 1, 5)

        self.pbtn_create_vl = QPushButton(self)
        self.pbtn_create_vl.setText(self.tr("Create virtual Layer"))
        self.layout.addWidget(self.pbtn_create_vl, 8, 0, 1, 5)

        self.pbtn_save_to_vl = QPushButton(self)
        self.pbtn_save_to_vl.setText(self.tr("Save to virtual Layer"))
        self.layout.addWidget(self.pbtn_save_to_vl, 9, 0, 1, 5)

        self.wdg_central.setLayout(self.layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def sizeHint(self):
        #bewirkt mit self.setSizePolicy bei adjustSize() ein Skalieren auf die Minimalgröße gem. des Inhalts
        return QtCore.QSize(1, 1)

    def reset(self):
        '''Formularelemente zurücksetzen'''
        self.le_snapped_fid.clear()
        self.le_map_pt1_x.clear()
        self.le_map_pt1_y.clear()
        self.le_snap_pt1_x.clear()
        self.le_snap_pt1_y.clear()
        self.le_map_pt2_x.clear()
        self.le_map_pt2_y.clear()
        self.le_snap_pt2_x.clear()
        self.le_snap_pt2_y.clear()
        self.dspbx_pt1_m.clear()
        self.dspbx_pt2_m.clear()
        self.dspbx_pt_dist.clear()

    def closeEvent(self, e):
        '''auszuführender Code beim Schließen des Dialogs
         den Toolmodus auf Pan switchen und alle Grafiken entfernen'''
        self.reset()
        self.iface.actionPan().trigger()
