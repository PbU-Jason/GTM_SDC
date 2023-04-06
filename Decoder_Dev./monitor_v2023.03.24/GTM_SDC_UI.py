# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GTM_SDC.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(553, 707)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(20, 10, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(30)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.Decode_Modes_CheckBox_Sci = QtWidgets.QCheckBox(self.centralwidget)
        self.Decode_Modes_CheckBox_Sci.setGeometry(QtCore.QRect(80, 260, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Decode_Modes_CheckBox_Sci.setFont(font)
        self.Decode_Modes_CheckBox_Sci.setObjectName("Decode_Modes_CheckBox_Sci")
        self.Decoder_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Decoder_Button.setGeometry(QtCore.QRect(20, 60, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(20)
        self.Decoder_Button.setFont(font)
        self.Decoder_Button.setObjectName("Decoder_Button")
        self.InputFile_Decoder_Text = QtWidgets.QTextEdit(self.centralwidget)
        self.InputFile_Decoder_Text.setGeometry(QtCore.QRect(180, 110, 351, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.InputFile_Decoder_Text.setFont(font)
        self.InputFile_Decoder_Text.setObjectName("InputFile_Decoder_Text")
        self.InputFile_Decoder_Button = QtWidgets.QPushButton(self.centralwidget)
        self.InputFile_Decoder_Button.setGeometry(QtCore.QRect(70, 110, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.InputFile_Decoder_Button.setFont(font)
        self.InputFile_Decoder_Button.setObjectName("InputFile_Decoder_Button")
        self.Decode_Modes_Text = QtWidgets.QLabel(self.centralwidget)
        self.Decode_Modes_Text.setGeometry(QtCore.QRect(80, 220, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Decode_Modes_Text.setFont(font)
        self.Decode_Modes_Text.setObjectName("Decode_Modes_Text")
        self.Decode_Modes_CheckBox_TMTC = QtWidgets.QCheckBox(self.centralwidget)
        self.Decode_Modes_CheckBox_TMTC.setGeometry(QtCore.QRect(80, 320, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Decode_Modes_CheckBox_TMTC.setFont(font)
        self.Decode_Modes_CheckBox_TMTC.setObjectName("Decode_Modes_CheckBox_TMTC")
        self.Export_Modes_CheckBox_Sci_Raw = QtWidgets.QCheckBox(self.centralwidget)
        self.Export_Modes_CheckBox_Sci_Raw.setGeometry(QtCore.QRect(360, 260, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Export_Modes_CheckBox_Sci_Raw.setFont(font)
        self.Export_Modes_CheckBox_Sci_Raw.setObjectName("Export_Modes_CheckBox_Sci_Raw")
        self.Export_Modes_CheckBox_Sci_Pipeline = QtWidgets.QCheckBox(self.centralwidget)
        self.Export_Modes_CheckBox_Sci_Pipeline.setGeometry(QtCore.QRect(360, 290, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Export_Modes_CheckBox_Sci_Pipeline.setFont(font)
        self.Export_Modes_CheckBox_Sci_Pipeline.setObjectName("Export_Modes_CheckBox_Sci_Pipeline")
        self.Export_Modes_CheckBox_Sci_Both = QtWidgets.QCheckBox(self.centralwidget)
        self.Export_Modes_CheckBox_Sci_Both.setGeometry(QtCore.QRect(360, 320, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Export_Modes_CheckBox_Sci_Both.setFont(font)
        self.Export_Modes_CheckBox_Sci_Both.setObjectName("Export_Modes_CheckBox_Sci_Both")
        self.Decoder_Button_Status = QtWidgets.QLabel(self.centralwidget)
        self.Decoder_Button_Status.setGeometry(QtCore.QRect(140, 60, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Decoder_Button_Status.setFont(font)
        self.Decoder_Button_Status.setText("")
        self.Decoder_Button_Status.setObjectName("Decoder_Button_Status")
        self.Extract_NSPO_CheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.Extract_NSPO_CheckBox.setGeometry(QtCore.QRect(100, 290, 201, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Extract_NSPO_CheckBox.setFont(font)
        self.Extract_NSPO_CheckBox.setObjectName("Extract_NSPO_CheckBox")
        self.GTM_ICON = QtWidgets.QLabel(self.centralwidget)
        self.GTM_ICON.setGeometry(QtCore.QRect(390, 10, 131, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(30)
        self.GTM_ICON.setFont(font)
        self.GTM_ICON.setText("")
        self.GTM_ICON.setObjectName("GTM_ICON")
        self.Module_Sensor_GroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Module_Sensor_GroupBox.setGeometry(QtCore.QRect(270, 360, 251, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Module_Sensor_GroupBox.setFont(font)
        self.Module_Sensor_GroupBox.setObjectName("Module_Sensor_GroupBox")
        self.Master_GroupBox = QtWidgets.QGroupBox(self.Module_Sensor_GroupBox)
        self.Master_GroupBox.setGeometry(QtCore.QRect(10, 30, 231, 91))
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Master_GroupBox.setFont(font)
        self.Master_GroupBox.setInputMethodHints(QtCore.Qt.ImhNone)
        self.Master_GroupBox.setFlat(False)
        self.Master_GroupBox.setCheckable(True)
        self.Master_GroupBox.setChecked(False)
        self.Master_GroupBox.setObjectName("Master_GroupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.Master_GroupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 205, 61))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.Master_GridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.Master_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.Master_GridLayout.setObjectName("Master_GridLayout")
        self.Master_CheckBox_Sensor3 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Master_CheckBox_Sensor3.setFont(font)
        self.Master_CheckBox_Sensor3.setObjectName("Master_CheckBox_Sensor3")
        self.Master_GridLayout.addWidget(self.Master_CheckBox_Sensor3, 1, 0, 1, 1)
        self.Master_CheckBox_Sensor2 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Master_CheckBox_Sensor2.setFont(font)
        self.Master_CheckBox_Sensor2.setObjectName("Master_CheckBox_Sensor2")
        self.Master_GridLayout.addWidget(self.Master_CheckBox_Sensor2, 0, 1, 1, 1)
        self.Master_CheckBox_Sensor4 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Master_CheckBox_Sensor4.setFont(font)
        self.Master_CheckBox_Sensor4.setObjectName("Master_CheckBox_Sensor4")
        self.Master_GridLayout.addWidget(self.Master_CheckBox_Sensor4, 1, 1, 1, 1)
        self.Master_CheckBox_Sensor1 = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Master_CheckBox_Sensor1.setFont(font)
        self.Master_CheckBox_Sensor1.setObjectName("Master_CheckBox_Sensor1")
        self.Master_GridLayout.addWidget(self.Master_CheckBox_Sensor1, 0, 0, 1, 1)
        self.Slave_GroupBox = QtWidgets.QGroupBox(self.Module_Sensor_GroupBox)
        self.Slave_GroupBox.setGeometry(QtCore.QRect(10, 130, 231, 91))
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Slave_GroupBox.setFont(font)
        self.Slave_GroupBox.setFlat(False)
        self.Slave_GroupBox.setCheckable(True)
        self.Slave_GroupBox.setChecked(False)
        self.Slave_GroupBox.setObjectName("Slave_GroupBox")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.Slave_GroupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 205, 61))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.Slave_GridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.Slave_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.Slave_GridLayout.setObjectName("Slave_GridLayout")
        self.Slave_CheckBox_Sensor3 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Slave_CheckBox_Sensor3.setFont(font)
        self.Slave_CheckBox_Sensor3.setObjectName("Slave_CheckBox_Sensor3")
        self.Slave_GridLayout.addWidget(self.Slave_CheckBox_Sensor3, 1, 0, 1, 1)
        self.Slave_CheckBox_Sensor2 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Slave_CheckBox_Sensor2.setFont(font)
        self.Slave_CheckBox_Sensor2.setObjectName("Slave_CheckBox_Sensor2")
        self.Slave_GridLayout.addWidget(self.Slave_CheckBox_Sensor2, 0, 1, 1, 1)
        self.Slave_CheckBox_Sensor4 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Slave_CheckBox_Sensor4.setFont(font)
        self.Slave_CheckBox_Sensor4.setObjectName("Slave_CheckBox_Sensor4")
        self.Slave_GridLayout.addWidget(self.Slave_CheckBox_Sensor4, 1, 1, 1, 1)
        self.Slave_CheckBox_Sensor1 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Slave_CheckBox_Sensor1.setFont(font)
        self.Slave_CheckBox_Sensor1.setObjectName("Slave_CheckBox_Sensor1")
        self.Slave_GridLayout.addWidget(self.Slave_CheckBox_Sensor1, 0, 0, 1, 1)
        self.Monitor_Modes_Group = QtWidgets.QGroupBox(self.centralwidget)
        self.Monitor_Modes_Group.setGeometry(QtCore.QRect(80, 360, 181, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Monitor_Modes_Group.setFont(font)
        self.Monitor_Modes_Group.setObjectName("Monitor_Modes_Group")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Monitor_Modes_Group)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 162, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Monitor_Modes_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Monitor_Modes_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Monitor_Modes_verticalLayout.setObjectName("Monitor_Modes_verticalLayout")
        self.Monitor_Modes_radioButton_Plotting = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Monitor_Modes_radioButton_Plotting.setFont(font)
        self.Monitor_Modes_radioButton_Plotting.setObjectName("Monitor_Modes_radioButton_Plotting")
        self.Monitor_Modes_verticalLayout.addWidget(self.Monitor_Modes_radioButton_Plotting)
        self.Monitor_Modes_radioButton_Silence = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.Monitor_Modes_radioButton_Silence.setFont(font)
        self.Monitor_Modes_radioButton_Silence.setObjectName("Monitor_Modes_radioButton_Silence")
        self.Monitor_Modes_verticalLayout.addWidget(self.Monitor_Modes_radioButton_Silence)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(80, 210, 451, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(80, 350, 451, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.Control_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Control_groupBox.setGeometry(QtCore.QRect(280, 620, 241, 41))
        self.Control_groupBox.setTitle("")
        self.Control_groupBox.setObjectName("Control_groupBox")
        self.Start_Button = QtWidgets.QPushButton(self.Control_groupBox)
        self.Start_Button.setGeometry(QtCore.QRect(10, 0, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(20)
        self.Start_Button.setFont(font)
        self.Start_Button.setObjectName("Start_Button")
        self.Terminate_Button = QtWidgets.QPushButton(self.Control_groupBox)
        self.Terminate_Button.setGeometry(QtCore.QRect(110, 0, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(20)
        self.Terminate_Button.setFont(font)
        self.Terminate_Button.setObjectName("Terminate_Button")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(70, 600, 451, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.Update_Rate_Group = QtWidgets.QGroupBox(self.centralwidget)
        self.Update_Rate_Group.setGeometry(QtCore.QRect(80, 480, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)
        self.Update_Rate_Group.setFont(font)
        self.Update_Rate_Group.setObjectName("Update_Rate_Group")
        self.Update_Rate_comboBox = QtWidgets.QComboBox(self.Update_Rate_Group)
        self.Update_Rate_comboBox.setGeometry(QtCore.QRect(10, 30, 161, 26))
        self.Update_Rate_comboBox.setObjectName("Update_Rate_comboBox")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        self.Update_Rate_comboBox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 553, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "GTM - SDC"))
        self.Decode_Modes_CheckBox_Sci.setText(_translate("MainWindow", "Science Data → Export Modes:"))
        self.Decoder_Button.setText(_translate("MainWindow", "Decoder"))
        self.InputFile_Decoder_Text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p></body></html>"))
        self.InputFile_Decoder_Button.setText(_translate("MainWindow", "Input File"))
        self.Decode_Modes_Text.setText(_translate("MainWindow", "Decode Modes:"))
        self.Decode_Modes_CheckBox_TMTC.setText(_translate("MainWindow", "Telemetry Data"))
        self.Export_Modes_CheckBox_Sci_Raw.setText(_translate("MainWindow", "Raw Format"))
        self.Export_Modes_CheckBox_Sci_Pipeline.setText(_translate("MainWindow", "Pipeline Format"))
        self.Export_Modes_CheckBox_Sci_Both.setText(_translate("MainWindow", "Both"))
        self.Extract_NSPO_CheckBox.setText(_translate("MainWindow", "Extract NSPO Header"))
        self.Module_Sensor_GroupBox.setTitle(_translate("MainWindow", "Module and Sensor:"))
        self.Master_GroupBox.setTitle(_translate("MainWindow", "Master"))
        self.Master_CheckBox_Sensor3.setText(_translate("MainWindow", "Sensor 3"))
        self.Master_CheckBox_Sensor2.setText(_translate("MainWindow", "Sensor 2"))
        self.Master_CheckBox_Sensor4.setText(_translate("MainWindow", "Sensor 4"))
        self.Master_CheckBox_Sensor1.setText(_translate("MainWindow", "Sensor 1"))
        self.Slave_GroupBox.setTitle(_translate("MainWindow", "Slave"))
        self.Slave_CheckBox_Sensor3.setText(_translate("MainWindow", "Sensor 3"))
        self.Slave_CheckBox_Sensor2.setText(_translate("MainWindow", "Sensor 2"))
        self.Slave_CheckBox_Sensor4.setText(_translate("MainWindow", "Sensor 4"))
        self.Slave_CheckBox_Sensor1.setText(_translate("MainWindow", "Sensor 1"))
        self.Monitor_Modes_Group.setTitle(_translate("MainWindow", "Monitor Modes:"))
        self.Monitor_Modes_radioButton_Plotting.setText(_translate("MainWindow", "Realtime Plotting"))
        self.Monitor_Modes_radioButton_Silence.setText(_translate("MainWindow", "Keep Silence"))
        self.Start_Button.setText(_translate("MainWindow", "Start"))
        self.Terminate_Button.setText(_translate("MainWindow", "Terminate"))
        self.Update_Rate_Group.setTitle(_translate("MainWindow", "Update Rate (s):"))
        self.Update_Rate_comboBox.setItemText(0, _translate("MainWindow", "1"))
        self.Update_Rate_comboBox.setItemText(1, _translate("MainWindow", "5"))
        self.Update_Rate_comboBox.setItemText(2, _translate("MainWindow", "10"))
        self.Update_Rate_comboBox.setItemText(3, _translate("MainWindow", "30"))
        self.Update_Rate_comboBox.setItemText(4, _translate("MainWindow", "60"))
        self.Update_Rate_comboBox.setItemText(5, _translate("MainWindow", "300"))
        self.Update_Rate_comboBox.setItemText(6, _translate("MainWindow", "600"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
