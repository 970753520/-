import sys,os
import time
import threading
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer,QThread, pyqtSignal,QObject
from PyQt5.QtWidgets import QMainWindow,QApplication,QTabWidget,QWidget,QTextEdit,\
                            QLabel,QLineEdit,QListView,\
                            QAction,qApp,QPushButton,QGroupBox,QComboBox,QHBoxLayout,\
                            QSpacerItem,QSizePolicy,QSplitter,QVBoxLayout,QMessageBox
                            
from PyQt5.QtGui import QIcon
import qtawesome
#pip install qtawesome

class Ui_MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.resize(1200,650)
        self.setWindowTitle("测试工具")
        self.setWindowIcon(QIcon("./images/ico1.png"))

        self.setupMenubar()
        self.setupToolbar()
        self.setupUi()
        self.setupStatusbar()

        
    #菜单栏    
    def setupMenubar(self):
        self.menubar = self.menuBar()
        
        self.menu1 = self.menubar.addMenu("文件(F)")
        self.pub = QAction("pub",self)
        self.menu1.addAction(self.pub)
        self.dpan = QAction("D盘",self)
        self.menu1.addAction(self.dpan)
        self.menu1.addAction(QAction("退出(Q)",self))
        
        self.menu2 = self.menubar.addMenu("编辑(E)")
        self.menu2.addAction(QAction("复制(C)",self))
        
        self.menu3 = self.menubar.addMenu("工具(L)")
        self.ftp_sever = QAction("启动 Ftp-Server",self)
        self.menu3.addAction(self.ftp_sever)
        self.http_server = QAction("启动 Http-Server",self)
        self.menu3.addAction(self.http_server)
        self.mohe = QAction("魔盒刷机工具",self)
        self.menu3.addAction(self.mohe)
        self.timer = QAction("时间差计算器",self)
        self.menu3.addAction(self.timer)
        
        self.menu4 = self.menubar.addMenu("帮助(H)")
        self.usinghelp = QAction("使用文档(H)",self)
        self.menu4.addAction(self.usinghelp)
        self.menu4.addAction(QAction("关于工具(A)",self,triggered=lambda :QMessageBox.about(self,'关于','@Version: 1.0.0\n@WJN\n@2019')))
        self.menu4.addSeparator()
        self.command = QAction("命令大全",self)
        self.menu4.addAction(self.command)
        self.crt_script = QAction("Crt_脚本",self)
        self.menu4.addAction(self.crt_script)
        self.sh_script = QAction("Shell_脚本",self)
        self.menu4.addAction(self.sh_script)


         
    #工具栏
    def setupToolbar(self):
        self.toolbar1 = self.addToolBar('')
        self.toolbar1.setIconSize(QtCore.QSize(30, 18))
        
        self.new = QAction(QIcon("./images/shell.png"), "Adb常用命令", self)
        self.toolbar1.addAction(self.new)
        
        self.open = QAction(QIcon("./images/open.png"), "打开Cache目录", self)
        self.toolbar1.addAction(self.open)
        
        self.edit = QAction(QIcon("./images/edit.png"), "备忘录", self)
        self.toolbar1.addAction(self.edit)

        self.toolbar2 = self.addToolBar('')
        self.toolbar2.setIconSize(QtCore.QSize(30, 18))

        self.toolbar2.addAction(QAction(QIcon("./images/android.png"), "系统监控", self))
        self.toolbar2.addAction(QAction(QIcon("./images/cpu.png"), "监控CPU信息", self))
        self.toolbar2.addAction(QAction(QIcon("./images/meminfo.png"), "监控内存PSS", self))
        self.toolbar2.addAction(QAction(QIcon("./images/temperature.png"), "监控温度", self))

        self.toolbar3 = self.addToolBar('')
        self.toolbar3.setIconSize(QtCore.QSize(30, 18))
        self.toolbar3.addAction(QAction(QIcon("./images/newTask.png"), "NEW", self))
        self.cmd = QAction(QIcon("./images/CMD.png"), "CMD", self)
        self.toolbar3.addAction(self.cmd)
        
    def setupUi(self):
        #中心widget
        self.centralwidget = QWidget(self)
        #self.centralwidget.setStyleSheet("background:red")
        self.setCentralWidget(self.centralwidget)

        #创建水平布局_2
        self.hboxLayout_2 = QHBoxLayout(self.centralwidget)
        self.hboxLayout_2.setContentsMargins(1, 1, 1, 1)

        #创建分裂器
        self.splitter = QSplitter(self.centralwidget)
        #self.splitter.setSizes([700,500])
        self.splitter.setLineWidth(1)#外边距1
        self.splitter.setOrientation(QtCore.Qt.Horizontal)#分裂器水平布局
        self.splitter.setHandleWidth(0)#中间竖杠边距

        #水平布局：分裂器
        self.hboxLayout_2.addWidget(self.splitter)

        
        #分割器布局:Tabs
        self.tabs = QTabWidget(self.splitter)
        self.tab1Ui()
        #self.tab4Ui()
        self.tab2Ui()
        self.tab3Ui()
        #self.tab4Ui()
        #self.tab5Ui()
        #self.tab6Ui()

        #分割器布局:QWidget                                          s
        self.widget = QWidget(self.splitter)
        #self.widget.setStyleSheet("background:blue")
        #创建竖直布局_1
        self.vboxLayout = QVBoxLayout(self.widget)
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.vboxLayout.setSpacing(1)

        #水平布局_1：按钮+弹簧
        self.save_bt =  QPushButton(self.centralwidget)
        self.save_bt.setText("保存")
        self.save_bt.setIcon(QIcon("./images/save.png"))
        self.clear_bt =  QPushButton(self.centralwidget)
        self.clear_bt.setText("清空控制台")
        self.clear_bt.setIcon(QIcon("./images/clear.jpg"))
        self.hboxLayout_1 = QHBoxLayout()#水平布局
        self.hboxLayout_1.setSpacing(1)#外边距1
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)#弹簧
        self.hboxLayout_1.addItem(spacerItem)
        self.hboxLayout_1.addWidget(self.clear_bt)
        self.hboxLayout_1.addWidget(self.save_bt)
        
        #将水平布局_1和文本框 添加到竖直布局_1
        self.vboxLayout.addLayout(self.hboxLayout_1)
        self.textedit = QTextEdit(self.widget)
        self.textedit.setStyleSheet("background-color:#3c3f41;color:#ffffff")
        self.vboxLayout.addWidget(self.textedit)

        #向Splitter内添加控件后。设置的初始大小
        self.splitter.setSizes([540,660])
        
        #self.setCentralWidget(self.centralwidget)
    def tab1Ui(self):
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1,"设备信息")

        groupbox_1 = QGroupBox(self.tab1)
        groupbox_1.setGeometry(QtCore.QRect(25,20, 480,190))
        connect_lb = QLabel(self.tab1)
        connect_lb.setText('设备ip地址：')
        connect_lb.setGeometry(QtCore.QRect(50,32,150,25))
        self.connect_le = QLineEdit(self.tab1)
        self.connect_le.setText('192.168.1.100')
        self.connect_le.setStyleSheet("background-color:#ffffff;color:red")
        self.connect_le.setGeometry(QtCore.QRect(130,32,200,25))
        self.connect_bt = QPushButton(self.tab1)
        self.connect_bt.setText("连接..")
        self.connect_bt.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.connect_bt.setGeometry(QtCore.QRect(370,32,100,25))
        #self.connect_bt.clicked.connect(self.connect_th)

        #groupbox_2 = QGroupBox(self.tab1)
        #groupbox_2.setTitle("")
        #groupbox_2.setGeometry(QtCore.QRect(25,70, 480,130))
        self.info_bt = QPushButton(self.tab1)
        self.info_bt.setText("获取设备信息")
        self.info_bt.setGeometry(QtCore.QRect(50,80,100,25))
        self.md5_bt = QPushButton(self.tab1)
        self.md5_bt.setText("MD5查询工具")
        self.md5_bt.setGeometry(QtCore.QRect(50,120,100,25))
        self.asr_bt = QPushButton(self.tab1)
        self.asr_bt.setText("语音压测")
        self.asr_bt.setGeometry(QtCore.QRect(50,160,62,25))
        self.asr_txt_bt = QPushButton(self.tab1)
        self.asr_txt_bt.setText("语料")
        self.asr_txt_bt.setGeometry(QtCore.QRect(110,160,40,25))
        
        self.apk_bt = QPushButton(self.tab1)
        #self.logcat_bt.setIcon(QIcon("./images/open.png"))
        self.apk_bt.setText("APK信息")
        self.apk_bt.setGeometry(QtCore.QRect(215,80,100,25))
        self.clock_bt = QPushButton(self.tab1)
        self.clock_bt.setText("秒表")
        self.clock_bt.setGeometry(QtCore.QRect(215,120,100,25))
        self.log_viewpro_bt = QPushButton(self.tab1)
        self.log_viewpro_bt.setText("LogViewPro")
        self.log_viewpro_bt.setGeometry(QtCore.QRect(215,160,100,25))
        
        self.screenshot_bt = QPushButton(self.tab1)
        self.screenshot_bt.setText("截图")
        self.screenshot_bt.setGeometry(QtCore.QRect(370,80,100,25))
        self.ota_bt = QPushButton(self.tab1)
        self.ota_bt.setText("OTA上传工具")
        self.ota_bt.setGeometry(QtCore.QRect(370,120,100,25))
        self.test2_bt = QPushButton(self.tab1)
        self.test2_bt.setText("...")
        self.test2_bt.setGeometry(QtCore.QRect(370,160,100,25))

        #groupbox_3 = QGroupBox(self.tab1)
        #groupbox_3.setTitle("监控本机attached设备和串口")
        #groupbox_3.setGeometry(QtCore.QRect(25,250, 480,250))
        com_lb = QLabel(self.tab1)
        com_lb.setText('监控本机attached设备和串口：')
        com_lb.setGeometry(QtCore.QRect(30,250,200,25))
        self.listview=QListView(self.tab1)
        self.listview.setGeometry(QtCore.QRect(25,280,480,220))
        self.stringlist = QtCore.QStringListModel()
        self.listview.setModel(self.stringlist)
    def tab2Ui(self):
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2,"冒烟测试")

        groupbox_1 = QGroupBox(self.tab2)
        groupbox_1.setTitle("SmokeTest")
        groupbox_1.setGeometry(QtCore.QRect(25,50, 480,300))

        script_lb = QLabel(self.tab2)
        script_lb.setText('脚本路径：')
        script_lb.setGeometry(QtCore.QRect(50,80,150,25))
        self.script_bt = QPushButton(self.tab2)
        self.script_bt.setText("冒烟脚本路径..")
        self.script_bt.setGeometry(QtCore.QRect(150,80,100,25))
        self.script_bt.setStyleSheet("QPushButton{color:black}"
                                       "QPushButton:hover{color:red}"
                                       "QPushButton{background-color:lightgreen}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}")
        
        
        smoketest_lb = QLabel(self.tab2)
        smoketest_lb.setText('项目选择：')
        smoketest_lb.setGeometry(QtCore.QRect(50,130,150,25))
        infomation1 = ["请选择","魔盒系列", "魔屏系列", "天猫精灵系列", "图兰朵系列"]
        self.infomation2 = ["请选择"]

        self.project_combox = QComboBox(self.tab2)
        self.project_combox.addItems(infomation1)
        self.project_combox.setGeometry(QtCore.QRect(150,130,200,25))

        smoketest_lb = QLabel(self.tab2)
        smoketest_lb.setText('型号选择：')
        smoketest_lb.setGeometry(QtCore.QRect(50,180,150,25))
        self.model_combox = QComboBox(self.tab2)
        self.model_combox.addItems(self.infomation2)
        self.model_combox.setGeometry(QtCore.QRect(150,180,200,25))

        self.smokestart_bt = QPushButton(self.tab2)
        self.smokestart_bt.setText("开始测试")
        self.smokestart_bt.setGeometry(QtCore.QRect(150,250,100,25))
        self.smokestop_bt = QPushButton(self.tab2)
        self.smokestop_bt.setText("取消测试")
        self.smokestop_bt.setGeometry(QtCore.QRect(250,250,100,25))

        

    def tab3Ui(self):
        self.aaaa=1
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3,"语音测试")

        groupbox_1 = QGroupBox(self.tab3)
        groupbox_1.setTitle("VoiceTest")
        groupbox_1.setGeometry(QtCore.QRect(25,50, 480,300))

        self.textedit3=QTextEdit(self.tab3)
        self.textedit3.setPlainText('杭州的天气\n声音大一点')
        self.textedit3.setStyleSheet("background-color:#ffcc00;color:#000000")
        self.textedit3.setGeometry(QtCore.QRect(63,80,400,230))

        self.open3_bt = QPushButton(self.tab3)
        self.open3_bt.setText("打开自定义语料")
        self.open3_bt.setGeometry(QtCore.QRect(63,310,100,25))
        
        self.save3_bt = QPushButton(self.tab3)
        self.save3_bt.setText("保存后生效")
        self.save3_bt.setGeometry(QtCore.QRect(363,310,100,25))

        self.asrtest_bt = QPushButton(self.tab3)
        self.asrtest_bt.setText("开始测试")
        self.asrtest_bt.setGeometry(QtCore.QRect(150,400,100,25))
        self.asrtest_bt.setEnabled(False)

        self.cancel3_bt = QPushButton(self.tab3)
        self.cancel3_bt.setText("取消测试")
        self.cancel3_bt.setGeometry(QtCore.QRect(250,400,100,25))
        
        self.asrreport_bt = QPushButton(self.tab3)
        self.asrreport_bt.setText("生成测试报告")
        self.asrreport_bt.setGeometry(QtCore.QRect(350,400,100,25))

        #groupbox_3 = QGroupBox(self.tab3)
        #groupbox_3.setTitle("测试说明")
        #groupbox_3.setGeometry(QtCore.QRect(50,350, 400,150))

    def tab4Ui(self):
        self.tab4 = QWidget()
        self.tabs.addTab(self.tab4,"Linux系统")
        
        groupbox_1 = QGroupBox(self.tab4)
        groupbox_1.setGeometry(QtCore.QRect(25,20, 480,190))

        self.info_bt = QPushButton(self.tab4)
        self.info_bt.setText("获取设备信息")
        self.info_bt.setGeometry(QtCore.QRect(50,40,100,25))
        self.info_bt = QPushButton(self.tab4)
        self.info_bt.setText("获取设备信息")
        self.info_bt.setGeometry(QtCore.QRect(50,80,100,25))
        self.md5_bt = QPushButton(self.tab4)
        self.md5_bt.setText("MD5查询工具")
        self.md5_bt.setGeometry(QtCore.QRect(50,120,100,25))
        self.asr_bt = QPushButton(self.tab4)
        self.asr_bt.setText("语音压测")
        self.asr_bt.setGeometry(QtCore.QRect(50,160,100,25))


        self.logcat_bt = QPushButton(self.tab4)
        self.logcat_bt.setText("抓取logcat")
        self.logcat_bt.setGeometry(QtCore.QRect(215,40,100,25))
        self.logcat_bt = QPushButton(self.tab4)
        self.logcat_bt.setText("抓取logcat")
        self.logcat_bt.setGeometry(QtCore.QRect(215,80,100,25))
        self.clock_bt = QPushButton(self.tab4)
        self.clock_bt.setText("秒表")
        self.clock_bt.setGeometry(QtCore.QRect(215,120,100,25))
        self.test_bt = QPushButton(self.tab4)
        self.test_bt.setText("...")
        self.test_bt.setGeometry(QtCore.QRect(215,160,100,25))

        self.screenshot_bt = QPushButton(self.tab4)
        self.screenshot_bt.setText("截图")
        self.screenshot_bt.setGeometry(QtCore.QRect(370,40,100,25))
        self.screenshot_bt = QPushButton(self.tab4)
        self.screenshot_bt.setText("截图")
        self.screenshot_bt.setGeometry(QtCore.QRect(370,80,100,25))
        self.ota_bt = QPushButton(self.tab4)
        self.ota_bt.setText("OTA上传工具")
        self.ota_bt.setGeometry(QtCore.QRect(370,120,100,25))
        self.test2_bt = QPushButton(self.tab4)
        self.test2_bt.setText("...")
        self.test2_bt.setGeometry(QtCore.QRect(370,160,100,25))

        
    def tab5Ui(self):
        self.tab_5 = QWidget()
        self.tabs.addTab(self.tab_5,"冒烟测试")
        
    def tab6Ui(self):
        self.tab_6 = QWidget()
        self.tabs.addTab(self.tab_6,"Test..")
        
        
#状态栏
    def setupStatusbar(self):
        self.statusBar().showMessage('Reday')
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
