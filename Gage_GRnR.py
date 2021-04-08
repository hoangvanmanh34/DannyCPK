from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
import subprocess
import time
import socket
from ast import literal_eval
from threading import Thread
import Login_SNMP
import Login_Telnet
import Login_SSH
import shutil
import serial
from tkinter import simpledialog
from tkinter import messagebox
import hashlib
import json
import DannyCPK
#import DannyGRnR

#temp_dir_df = 'D:/Temp'
#if not os.path.isdir(temp_dir_df):
#    os.mkdir(temp_dir_df)
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        #self.Load_CFG()
        self.master.title("Danny-GR&R. 2018")
        self.Frame1 = Frame(master, bg="lightskyblue")
        self.Frame1.grid(row=0, column=0, sticky=W + E + N + S, pady=10, padx=10)

        if os.path.isfile('usr.id'):
            USER_INP = simpledialog.askstring(title="Danny-GR&R User", prompt="Enter Password", show='#')
            usercode = hashlib.md5(USER_INP.encode()).hexdigest()
            ufile = open('usr.id','r')
            ufinfo = ufile.read()
            if usercode.upper() == str(ufinfo).upper():
                self.btnStart = Button(self.Frame1, text="Analysis", font='serif 25', fg='white', width=10, bg='blue', command=self.Test_Main)
                self.btnStart.grid(row=0, column=0, sticky=W)
                self.btnStart.focus_set()
                self.lbStatus = tk.Label(self.Frame1, text='GR&R Data Analysis', borderwidth=4, font='serif 33',
                                         bg='lightskyblue', fg='white', height=2)
                self.lbStatus.grid(row=0, column = 1, columnspan=4, sticky=W)
                self.lbspace = tk.Label(self.Frame1, text='', borderwidth=0, font='serif 10',
                                        bg='lightskyblue', fg='white', height=1)
                self.lbspace.grid(row=1, columnspan=4, sticky=W)
                #self.sfclog = Text(self.Frame1, height=1, width=18, font='serif 15', fg='red', bg='yellow')
                #self.sfclog.grid(row=2, column=0, sticky=W)

                self.tFileConfig = Text(self.Frame1, height=1, width=20, font='serif 15', fg='black', bg='white')
                self.tFileConfig.grid(row=2, column=0, sticky=W)
                self.tFileConfig.insert(END, '-> Choose data..')
                self.tFileConfig.bind("<Button>", self.ChooseFileCFG)

                LoginTypeList = ['ANOVA','CPK']
                self.vLoginType = StringVar(root)
                self.vLoginType.set('ANOVA')
                #self.Login_Type = 'Camera'
                lLoginType = OptionMenu(self.Frame1, self.vLoginType, *LoginTypeList)
                lLoginType.grid(row=2, column=1, sticky=W)


                self.tfigname = Text(self.Frame1, height=1, width=20, font='serif 15', fg='black', bg='white')
                self.tfigname.grid(row=2, column=2, sticky=W)
                self.tfigname.insert(END, 'Type CPK Name')
                
                self.tUSL = Text(self.Frame1, height=1, width=8, font='serif 12', fg='black', bg='white')
                self.tUSL.grid(row=2, column=3, sticky=W)
                self.tUSL.insert(END, 'Set USL')
                
                self.tLSL = Text(self.Frame1, height=1, width=8, font='serif 12', fg='black', bg='white')
                self.tLSL.grid(row=2, column=4, sticky=W)
                self.tLSL.insert(END, 'Set LSL')               
                

                self.log = Text(self.Frame1, height=18, width=86, font='serif 12')
                self.log.grid(row=3, columnspan=5, sticky=W)
                scrollb = Scrollbar(self.Frame1, command=self.log.yview)
                scrollb.grid(row=4, column=5, sticky='nsew')
                self.log['yscrollcommand'] = scrollb.set

                self.send_sfc_flag = False
                self.SFC_Result = False
                self.data_to_SFC = ''
                self.cfg_filename = ''
            else:
                tk.messagebox.askquestion('User warning', 'User info incorrect, pls contact your leader!',
                                          icon='warning')
                root.destroy()

        else:
            tk.messagebox.askquestion('User warning', 'No user info, pls contact your leader!',
                                               icon='warning')
            root.destroy()

        #Thread(target=self.Start_SFC).start()
        #Thread(target=self.Del_Temp_File).start()
    def ChooseFileCFG(self,event):
        if self.vLoginType.get() != 'Test_Type':
            self.cfg_filename = filedialog.askopenfilename(initialdir=os.curdir, title="Select file",
                                                           filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            print(self.cfg_filename)
            self.tFileConfig.delete(1.0, END)
            self.tFileConfig.insert(END, os.path.basename(self.cfg_filename))
            #-----------------
            file = open(self.cfg_filename, 'r')
            cfile = file.read()
            self.log.delete(1.0, END)
            self.log.insert(END, str(cfile))

    def Test_Main(self):
        #Thread(target=self.Check_info).start()
        filepath = self.tFileConfig.get(1.0,END).strip()
        iUSL = self.tUSL.get(1.0,END).strip()
        iLSL = self.tLSL.get(1.0,END).strip()
        if iUSL == '': iUSL = None
        if iLSL == '': iLSL = None
        ifigname = self.tfigname.get(1.0,END).strip()
        #-------CPK---------
        dannycpk = DannyCPK.DannyCPK(filepath, None, iUSL, iLSL, ifigname)
        #-------GR&R---------
        #dannygrnr = DannyGRnR.DannyGRnR(filepath, None, iUSL, iLSL, ifigname)
        analysistype = self.vLoginType.get()
        print(analysistype)
        if analysistype == "CPK":
            dannycpk.AnalysisCPK()
        #if analysistype == "ANOVA":
        #    dannygrnr.AnalysisGRnR()
        print('Danny TE')

    def Reset_Status(self):
        self.data_to_SFC = ''
        self.log.delete(1.0, END)
        self.sfclog.delete(1.0, END)
        self.send_sfc_flag = False
        self.SFC_Result = False
        self.FResult = False
        self.Login_Type = self.vLoginType.get()

    

    def Return_Result(self,fresult):
        if fresult:
            self.btnStart.configure(state='normal')
            self.lbStatus.configure(text='PASS', fg='green')
        else :
            self.btnStart.configure(state='normal')
            self.lbStatus.configure(text='FAIL', fg='red')
        self.data_to_SFC = ''
        self.send_sfc_flag = False

    def Check_Ping(self,DUT_IP, Stime, Ssize):
        print('Ping DUT')
        # self.log.insert(END, 'Check DUT Alive\r\n')
        cmd = 'ping ' + DUT_IP + ' -n ' + str(Stime) + ' -l ' + str(Ssize)
        buffer = ''
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, 'utf-8'):
            res = str(line, 'utf-8')
            buffer += res
            # print(res)
            self.log.insert(END, res)
            if not line: break
        p.stdout.close()
        p.wait()
        # print('##############################################')

        if buffer.find('Lost = 1 (100% loss)') > 0:
            print('Check Ping fail')
            return False
        if buffer.find('Lost = 0 (0% loss)') > 0:
            try:
                sMIN = int(self.GetContent(buffer, 'Maximum = ', 'ms'))
                # sMAX = int(self.GetContent(buffer, 'Minimum = ', 'ms'))
                sAVG = int(self.GetContent(buffer, 'Average = ', 'ms'))
                if sMIN < 5 and sAVG < 7:
                    print('Check Ping pass')
                    return True
                else:
                    print('Check Ping fail')
                    return False
            except:
                print('Check Ping fail')
                return False   


    def Load_CFG(self):
        if not os.path.isfile(self.cfg_filename):
            self.log.insert(END, 'No config file\n')
            return False
        try:
            CFG_file = open(self.cfg_filename, 'r')
            CFG_data = CFG_file.read().strip()
            CFG_file.close()
            self.cfg_value_list = literal_eval(str(json.loads(CFG_data)))
            # print(self.cfg_value_list)
            # print(type(self.cfg_value_list))
            self.PC_IP = self.vPCIP.get()  # self.cfg_value_list['SFC_IP']
            self.Socket_Port = 5555  # self.cfg_value_list['Socket_Port']
            self.Login_Type = self.vLoginType.get()  # self.cfg_value_list['Login_Type']
            self.DUT_IP = self.cfg_value_list['DUT_IP']
            return True
        except Exception as e:
            self.log.insert(END, e+'\n')
            return False

    def GetContent(self, buf, strstart, strend):
        # strresult="none"
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult

    

    '''def Del_Temp_File(self):
        for rootdir, dirs, files in os.walk(temp_dir_df):
            print('del')
            for f in files:
                try:
                    os.unlink(os.path.join(rootdir, f))
                except:
                    continue
            for d in dirs:
                try:
                    shutil.rmtree(os.path.join(rootdir, d))
                except:
                    continue'''
    def Open_Proc(self):
        os.system('D:\\RE_Rework\\RE_Rework.exe')
        #self.quit()

    def Open_COM(self):
        try:
            self.ser = serial.Serial(self.Fixture_COM,115200)
            print(self.ser.name)
            time.sleep(0.2)
            self.ser.flush()
            #self.ser.open()
            #self.ser.set_input_flow_control(enable=False)
            #self.ser.set_output_flow_control(enable=False)
            print('COM opened')
        except Exception as e:
            print(e)
            print('COM already open')

    def Close_COM(self):
        try:
            self.ser.flush()
            time.sleep(0.2)
            self.ser.close()
        except:
            print('close com fail')
        return True

    def Get_in(self):
        data_de = ''
        if not self.ser.is_open:
            print('re-open com')
            self.Open_COM()
        #time.sleep(0.1)
        #self.ser.flush()
        time.sleep(0.1)
        data_de = self.ser.read_all().strip()
        #time.sleep(0.1)
        self.ser.flush()
        if data_de != b'':
            print(self.ser.name)
            print('Fixture:' + str(data_de))
        return data_de

    def Send_COM(self,scmd):
        try:
            self.ser.write(scmd.encode()+b'\n')
        except Exception as e:
            print('send to com fail')
            print(e)
def on_Closing():
    if messagebox.askokcancel('Exit Test Message', 'Bạn có chắc muốn thoát ?\n Are you sure you want to exit ?',
                              icon='warning'):
        root.destroy()

root = Tk()
root.protocol('WM_DELETE_WINDOW', on_Closing)
root.geometry("820x500+300+100")
root.configure(bg='lightskyblue')
app = Application(master=root)
app.mainloop()

#------Check MBSN:Do_Memory_Read -i /dev/hwcfg/indivdatas.binary -a 0x000000 -s 18 -f ASCII
#------Check MAC ETH:Do_Memory_Read -i /dev/hwcfg/indivdatas.binary -a 0x000090 -s 6
    

