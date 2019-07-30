import sys,os
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QTimer,QThread,QObject
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
from PyQt5 import QtGui
#from ui.mainUi import MyWindow
from Ui_Main import Ui_MainWindow
import threading
from  serial.tools import list_ports
from subprocess import Popen,PIPE,call
import time
from bin import all_info,screencap,asrTest,MagicBox_M18S,MagicProjector_A2



ii=2
class XinHao(QObject):
    #声明带str类型参数的信号
    signal = pyqtSignal(str)  
    def write(self,text):
        self.signal.emit(str(text))  # 发射信号

            
class Logic(Ui_MainWindow):
    def __init__(self):
        super(Logic, self).__init__()
        self.button_connect()
        #重定向输出
        sys.stdout = XinHao(signal=self.Output)  
        sys.stderr = XinHao(signal=self.Output)
        #返回当前正在执行的线程和线程句柄
        #print('pid', os.getpid())
        #print('main id', int(QThread.currentThreadId()))
        #self.thread_stop = False
        self.devices_serial_th()
        
    def button_connect(self):
        #membar
        self.pub.triggered.connect(self.open_pub)
        self.dpan.triggered.connect(self.open_dpan)
        self.ftp_sever.triggered.connect(self.open_ftpserver)
        self.http_server.triggered.connect(self.open_httpserver)
        self.timer.triggered.connect(self.open_timer)

        self.command.triggered.connect(self.open_command)
        self.crt_script.triggered.connect(self.open_crt_script)
        self.sh_script.triggered.connect(self.open_sh_script)
        #toolbar
        self.new.triggered.connect(self.open_txt)
        self.open.triggered.connect(self.open_cache)
        self.edit.triggered.connect(self.open_edit)

        self.cmd.triggered.connect(self.open_cmd_th)
        
        #body
        self.clear_bt.clicked.connect(self.clear_textedit)
        self.save_bt.clicked.connect(self.save_textedit)
        #tab1
        self.connect_bt.clicked.connect(self.ip_th)
        self.info_bt.clicked.connect(self.info_th)
        self.apk_bt.clicked.connect(self.apk_start)
        self.screenshot_bt.clicked.connect(self.screencap_th)
        self.md5_bt.clicked.connect(self.md5_start)
        self.clock_bt.clicked.connect(self.clock_start)
        self.ota_bt.clicked.connect(self.ota_start)
        self.asr_bt.clicked.connect(self.asr_start)
        self.asr_txt_bt.clicked.connect(self.asr_txt_start)
        self.log_viewpro_bt.clicked.connect(self.log_viewpro_start)
        #tab2
        self.script_bt.clicked.connect(self.open_smoke)
        self.project_combox.activated[str].connect(self.project_choice)
        self.smokestart_bt.clicked.connect(self.smoketest_th)
        self.smokestop_bt.clicked.connect(self.smoketest_stop)
        #tab3
        self.open3_bt.clicked.connect(self.open3_textedit)
        self.save3_bt.clicked.connect(self.save3_textedit)
        self.asrtest_bt.clicked.connect(self.asrtest_th)

    ##membar
    def open_pub(self):
        try:
            os.startfile('\\\\10.101.169.117\\pub\pub\\')
        except Exception as e:
            print ('获取地址异常:',e)
    def open_dpan(self):
        os.startfile('D:\\')
        
    def open_ftpserver(self):
        os.startfile('bin\\FtpServer.exe')
    def open_httpserver(self):
        os.startfile('http_flask\\disk.exe')
    def open_timer(self):
        os.startfile('bin\\timer.exe')
        
    def open_command(self):
        os.startfile('android\\命令大全.txt')
    def open_crt_script(self):
        os.startfile('android\\crt')
    def open_sh_script(self):
        os.startfile('FtpServer')
        
    ##toolbar
    def open_txt(self):
        os.startfile('config\\Adb常用命令.txt')
    def open_edit(self):
        os.startfile('config\\备忘录.txt')
    def open_cache(self):
        os.startfile('cache')
    def open_cmd_th(self):
        cmd_th = threading.Thread(target=self.open_cmd_start)
        cmd_th.start()
    def open_cmd_start(self):
        os.startfile('C:\\windows\\system32\\cmd.exe')
    
    ##body
    def clear_textedit(self):
        self.textedit.setText("")

    def save_textedit(self):
        filename = QFileDialog.getSaveFileName(self,'save file','./cache/',"Text Files (*.txt);;All Files (*)")
        #print (filename[0])
        if filename[0] == "":
            print("\n取消保存")
            return
        with open(filename[0],'w') as f:
            my_text=self.textedit.toPlainText()
            f.write(my_text)

    #tab1
    def ip_th(self):
        t = threading.Thread(target=self.ip_start)
        t.start()
    def ip_start(self): 
        # 获取输入内容
        self.connect_bt.setEnabled(False)
        ip = self.connect_le.text()
        print ('连接%s中,请稍后..'%ip)
        Popen('adb connect %s'%ip, shell=True, stdout=PIPE).wait()
        Popen('adb devices|findstr "\<device\>"', shell=True, stdout=PIPE).wait()
        device = Popen('adb devices|findstr "\<device\>"', shell=True, stdout=PIPE).stdout.read().strip()
        ips = '%s:5555'%ip
        if ips in device.decode('utf-8'):
            print ('连接成功..')
        else:
            print ('连接失败..')
            print ('可能原因:确保在同一局域网下和调试模式打开')
        self.connect_bt.setEnabled(True)
    def info_th(self):
        t = threading.Thread(target=self.info_start)
        t.start()
    def info_start(self):
        self.info_bt.setEnabled(False)
        all_info.system_info()
        self.info_bt.setEnabled(True)
    def apk_start(self):
        os.startfile('bin\\apk_info.exe')
    def md5_start(self):
        os.startfile('bin\\Hash.exe')
    def clock_start(self):
        os.startfile('bin\\mb0.exe')
    def ota_start(self):
        os.startfile('bin\\Ota_Upload_Tool.jar')
    def asr_start(self):
        os.startfile('config\\asrTest-only.exe')
    def asr_txt_start(self):
        os.startfile('config\\asrWord100.txt')
        
    def screencap_th(self):
        t = threading.Thread(target=self.screencap_start)
        t.start()
    def screencap_start(self):
        screencap.screenshot()
   
    def devices_serial_start(self):
        self.devices_serial_list=[]
        #线程里必须先启动adb进程,才不会阻塞
        #Python3 中，bytes 和 str 的互相转换方式是
        #str.encode('utf-8')
        #bytes.decode('utf-8')
        adb_device_list =  Popen('adb devices|findstr "\<device\>"', shell=True, stdout=PIPE).stdout.readlines()
        for devices in adb_device_list:
            self.devices_serial_list.append(devices.split()[0].decode('utf-8'))
        for com in list_ports.comports():
            self.devices_serial_list.append(com[1])
        #print (self.devices_serial_list)
        self.stringlist.setStringList(self.devices_serial_list)
        self.thread_all = threading.Timer(1,self.devices_serial_start)
        self.thread_all.setDaemon(True)#True设置线程为后台线程
        self.thread_all.start()

        
    def devices_serial_th(self):
        t2 = threading.Timer(1,self.devices_serial_start)
        #os.popen('adb devices')
        t2.setDaemon(True)
        Popen('adb devices' ,stdout = PIPE,shell=True)
        t2.start()
    def log_viewpro_start(self):
        os.startfile('bin\\LogViewPro\\LogViewPro.exe')
        
    #tab2
    def open_smoke(self):
        #Popen('start cache', shell=True, stdout=PIPE)
        os.system('start smoke')
    def project_choice(self):
        project_choice = (self.project_combox.currentText())
        if project_choice == "魔盒系列":
            self.model_combox.clear()
            self.infomation2 = ["魔盒_MagicBox_M18S", "魔盒_MagicBox_A1C", "魔盒_MagicBox_4A", "魔盒_MagicBox_3C"]
            self.model_combox.addItems(self.infomation2)
        elif project_choice == "魔屏系列":
            self.model_combox.clear()
            self.infomation2 = ["魔屏_MagicProjector_S1", "魔屏_MagicProjector_A2", "魔屏_MagicProjector_S2", "魔屏_MagicProjector_A1C"]
            self.model_combox.addItems(self.infomation2)
        elif project_choice == "天猫精灵系列":
            self.model_combox.clear()
            self.infomation2 = ["天猫精灵_X1", "天猫精灵_X2"]
            self.model_combox.addItems(self.infomation2)
        elif project_choice == "图兰朵系列":
            self.model_combox.clear()
            self.infomation2 = ["图兰朵_S1"]
            self.model_combox.addItems(self.infomation2)
        elif project_choice == "请选择":
            self.model_combox.clear()
            print ("请选择..")
        else:
            self.model_combox.clear()
            print ("暂不支持该机型..")
    
    def smoketest_th(self):
        self.skt_th = threading.Thread(target=self.smoketest_start)
        self.skt_th.setDaemon(True)
        self.skt_th.start()
    def smoketest_start(self):
        self.smokestart_bt.setEnabled(False)
        model_choice = (self.model_combox.currentText())
        print (model_choice)
        if model_choice == "魔盒_MagicBox_M18S":
            MagicBox_M18S.SmokeTest()
        elif model_choice == "魔屏_MagicProjector_A2":
            MagicProjector_A2.SmokeTest()
        elif model_choice == "天猫精灵_X1":
            MagicProjector_A2.SmokeTest()
        else:
            print ("暂不支持该机型..")
        self.smokestart_bt.setEnabled(True)
        #QMessageBox.information(self,'提示', "请选择后测试")
    def smoketest_stop(self):
        #time.sleep(1)
        print ('I will stop it...')
        self.thread_stop = False
        return
        print ('done...')

    #tab3
    def open3_textedit(self):
        try:
            filename=QFileDialog.getOpenFileName(self,'open file','./config/',"Text Files (*.txt);;All Files (*)")
            if filename[0] == "":
                print("取消打开")
                return
            with open(filename[0],'rb') as f:
                my_txt=f.read()
                #print (my_txt.decode('utf-8'))
                self.textedit3.setPlainText(my_txt.decode('utf-8'))
        except Exception as e:
            print ('文本编码格式异常:',e)
    def save3_textedit(self):
        try:
            f =  open('config/asrWord.txt','wb+')
            my_text=self.textedit3.toPlainText()
            f.write(my_text.encode("utf-8"))
            #print (my_text)
            f.close()
            print ("保存成功..")
            self.asrtest_bt.setEnabled(True)
        except Exception as e:
            print ('文本编码格式异常:',e)
        #f.write(my_text)
    def asrtest_start(self):
        self.asrtest_bt.setEnabled(False)
        print('asr thread id', int(QThread.currentThreadId()))
        import pythoncom
        pythoncom.CoInitialize()
        asrTest.asr_test()
        self.asrtest_bt.setEnabled(True)
    def asrtest_th(self):
        t_asr = threading.Thread(target=self.asrtest_start)
        t_asr.setDaemon(True)
        t_asr.start()    
    #tab4
    #none

    #end
    def Output(self, text):
        cursor = self.textedit.textCursor()  # 光标
        cursor.movePosition(QtGui.QTextCursor.End) # 光标移至最后
        cursor.insertText(text)  # 插入文本
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyle('Windows')
    logic = Logic()
    logic.show()
    sys.exit(app.exec_())

