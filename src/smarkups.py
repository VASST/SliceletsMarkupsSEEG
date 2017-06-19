#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Markups Slicelets.

This Slicelets can add data, show 'Markups' module, 2d and 3d viewers.

Usage: slicer --no-main-window --python-script path/to/smarkups.py
    
Author: YingLi Lu, yinglilu@gmail.com

Date: 2017-06-16

Note: tested with slicer 4.6.2

"""

import qt
import __main__

#True: show 'Save Data' button
saveData=True

#True: show 'Modules Search'. Selected module will be added to modules tab dynamically.
addModule=True

defaultModules=["markups"]

def onModuleSelected(modulename):
  global tabWidget
  tabWidget.addTab(getattr(slicer.modules, modulename.lower()).widgetRepresentation(), modulename)

#splitter
splitter = qt.QSplitter()

leftWidget = qt.QWidget()
rightWidget = qt.QWidget()

splitter.addWidget(leftWidget)
splitter.addWidget(rightWidget)

#left layout for [add data,save data,search modules] and modules(tab)
leftLayout = qt.QVBoxLayout()
leftWidget.setLayout(leftLayout)

#right layout for 2d/3d viewer
rightLayout = qt.QVBoxLayout()
rightWidget.setLayout(rightLayout)

#top left layout: add data, save data,search modules
topleftLayout = qt.QHBoxLayout()
leftLayout.addLayout(topleftLayout)

#add data button
addDataButton = qt.QPushButton("Add Data")
topleftLayout.addWidget(addDataButton)
addDataButton.connect('clicked()', slicer.util.openAddDataDialog)

#save data button
if saveData:
  saveDataButton = qt.QPushButton("Save Data")
  topleftLayout.addWidget(saveDataButton)
  saveDataButton.connect('clicked()', slicer.util.openSaveDataDialog)

#dynamic add modules
if addModule:
  moduleSelector = slicer.qSlicerModuleSelectorToolBar()
  moduleSelector.setModuleManager(slicer.app.moduleManager())
  topleftLayout.addWidget(moduleSelector)
  moduleSelector.connect('moduleSelected(QString)', onModuleSelected)

tabWidget = qt.QTabWidget()
leftLayout.addWidget(tabWidget)

for module in defaultModules:
  onModuleSelected(module)

#add 2d/3d viewer to right layout
layoutManager = slicer.qMRMLLayoutWidget()
layoutManager.setMRMLScene(slicer.mrmlScene)
layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
rightLayout.addWidget(layoutManager)

splitter.show()

__main__.splitter = splitter # Keep track of the widget to avoid its premature destruction