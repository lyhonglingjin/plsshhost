#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from os import mkdir,getcwd
import paramiko
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from time import sleep, strftime, localtime, time
import sys
from logging import warning, error
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# messagebox attached the main,withdraw() can hide the main window
tkinter.Tk().withdraw()
# Defiswn a var to associate the value of the radiobutton with the value of the Label.
# ser=serial.Serial("/dev/ttyUSB0",9600,timeout=0.5)
#use USB connect serial port
# ser.open() #open port
# s = ser.read(10)#from port read 10 bytes
# ser.write(“hello”)#Write data to port
# ser.close()#close port
# data = ser.readliswns() and ser.xreadliswns Both require a timeout
    # def sstrip(ssship):
    #     xsship = ssship.strip()
    #     return xsship

class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

class Login(object):

    def __init__(self):
        #The main window,no shut down,Will always be there
        self.tk = tkinter.Tk()
        self.tk.title("Network config")
        #Sets the window initialization size and location, plus is location
        self.tk.geometry('390x330+530+300')
        self.tk.iconbitmap('D:/PYjiaoben/lyex.ico')
        # self.can = tkinter.Canvas(self.tk, height=150, width=350)
        # self.select_path = tkinter.StringVar()
        tkinter.Label(self.tk, bg='yellow', height=2,font=('KaiTi', 12),width=30, \
                      text='输入对应的SSH设备信息').pack()
        self.swname = tkinter.Label(self.tk, text='SSH设备用户名:', font=('KaiTi', 12))
        self.iswn = tkinter.Entry(self.tk, width=25)
        self.swps = tkinter.Label(self.tk, text='SSH设备密码:', font=('KaiTi', 12))
        self.iswi = tkinter.Entry(self.tk, width=25,show='*')
        self.swpsb = tkinter.Label(self.tk, text='SSH设备备用密码:', font=('KaiTi', 12))
        self.iswp = tkinter.Entry(self.tk, width=25,show='*')
        self.swname.place(x=25, y=65)
        self.iswn.place(x=160, y=65)
        self.swps.place(x=38, y=125)
        self.iswi.place(x=160, y=125)
        self.swpsb.place(x=15, y=185)
        self.iswp.place(x=160, y=185)
        # resetsw = tkinter.Button(self.tk, command=self.cp_resetsw, text="直接重置交换机", width=13)
        # resetsw.place(x=15, y=239)
        selectF = tkinter.Button(self.tk, text="选择主机文件:", command=self.select_file, width=12, font=('KaiTi',11))
        selectF.place(x=10, y=233)
        self.tken = tkinter.Entry(self.tk, width=35)
        self.tken.place(x=120, y=235)
        confirm = tkinter.Button(self.tk, command=self.cp_confirm, text="确定", width=8, font=('KaiTi'))
        confirm.place(x=260, y=275)
        # def print_selection():
        #     l.config(text='you have selected ' + var.get())
        #     var.set(A)
        # # 第5步，创建三个radiobutton选项，其中variable=var, value='A'的意思就是，当我们鼠标选中了其中一个选项，把value的值A放到变量var中，然后赋值给variable
        # r1 = tkinter.Radiobutton(self.tk, text='Console连接', variable=var, value='serial', command=self.comconf, \
        #                          indicatoron=0, width=15, height=2, font=('KaiTi', 15))

        self.tk.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
        # pack(side='bottom') font can choice Arial below down

    # def cp_resetsw(self):
    #     i = 0
    #     while True:
    #         serialFd.write('\r\n'.encode('utf-8'))
    #         sleep(0.5)
    #         serialFd.write('\n'.encode('utf-8'))
    #         sleep(0.5)
    #         i += 1
    #         sRda = serialFd.read_all()
    def select_file(self):
        # 单个文件选择
        self.selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
        self.tken.delete(0, 200)
        self.tken.insert(0, self.selected_file_path)

    def login_ssh_host(self):
        '''自动添加策略,保存服务器的主机名和公钥信息'''
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host_ip, 22, self.username, self.password, timeout=8)
            sleep(1)
            stdin, stdout, sdterr = self.ssh.exec_command('N')
            out = stdout.read()
            print(out)
            print("\nssh(%s)连接成功." % self.host_ip)
            # self.output.insert(tkinter.END, "\nssh(%s)连接成功." % self.host_ip)
            # self.output.update()
            sleep(0.5)
            return True
        except Exception:
            # warning("\n网络(%s)连接失败!" % self.host_ip)
            print("请检查网络(%s)是否畅通[ssh]" % self.host_ip)
            # self.output.insert(tkinter.END, "\n请检查网络(%s)是否畅通[ssh]" % self.host_ip)
            # self.output.update()
            sleep(0.5)
            return False

    def exec_ssh_command(self):
        # stdin, stdout, stderr = self.ssh.exec_command('%s\n\n' % command)
        chan = self.ssh.invoke_shell()
        chan.sendall(self.result + '\n')
        sleep(1)
        # 等待1秒给设备一个缓冲时间

    def cp_confirm(self):
        self.str_time = strftime("%Y%m%d", localtime())
        path = r'%s' % getcwd()
        try:
            mkdir(path + './%s' % self.str_time)
        except:
            warning("当前目录下文件夹%s存在" % self.str_time)
            sleep(3)
            pass
        try:
            print(self.selected_file_path)
        except:
            self.selfile = False
        else:
            self.selfile = True
        self.wintext = tkinter.Tk()
        self.wintext.title('需要远程配置的命令文本')
        self.wintext.geometry('+300+50')
        self.wintext.iconbitmap('D:/PYjiaoben/lyex.ico')
        self.tkt = tkinter.Text(self.wintext, width=80, height=25, font=('KaiTi', 13))
        self.tkt.grid(row=0, column=0, columnspan=3)
        # b1 = Button(root,text='插入')
        # b1.grid(row=1,column=0)
        # grid Space partition, bigspace use row=1,column=0,rowspan=2,columnspan=2)
        # b2 = Button(root,text='清空')
        # b2.grid(row=1,column=1)
        b3 = tkinter.Button(self.wintext, text='刷入配置', font=('KaiTi', 18), command=self.getTextInput)
        b3.grid(row=1, column=1)
        self.output = tkinter.Text(self.wintext, width=60, height=15,font=('KaiTi', 12))
        self.output.grid(row=1, column=0)
        self.wintext.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    def psship(self, sshipex):
        # swnstr = self.iswn.get().ljust(1)
        # swistr = self.iswi.get().ljust(1)
        # swpsbum = self.iswp.get().ljust(1)
        # print(swnstr,swistr,swpsbum)
        # if self.selfile == True:
        #     with open( self.selected_file_path, 'r', encoding='utf-8') as ssh_obj:
        #         sys.stdout = Logger(F'{getcwd()}/{self.str_time}/log.txt')
        #         print('----------------------------------------------')
        #         print('文件路径：' + self.selected_file_path)
        #         print('执行命令：' + self.result)
        #         for ssh_ip in ssh_obj:
        #             # 根据类实例化一个ssh对象
        try:
            self.ssh = paramiko.SSHClient()
            self.host_ip = sshipex.strip()
            self.username = self.swnstr
            self.password = self.swistr
            if  self.login_ssh_host():
                self.exec_ssh_command()
                self.ssh.close()
            else:
                self.password = self.swpsbum
                sleep(0.2)
                self.login_ssh_host()
                self.exec_ssh_command()
                self.ssh.close()
        except Exception:
            pass
    # messagebox.showinfo(title='刷入提示', message='配置已刷入，请检查是否成功')
    sleep(1)
        # else:
        #     try:
        #         open('%s\ssh_connect.txt' % getcwd(), 'r')
        #     except Exception:
        #         messagebox.showinfo(title='错误提示', message='无默认主机文件，需要当前路径新建ssh_connect.txt')
        #         sys.exit(0)
        #     with open('%s\ssh_connect.txt' % getcwd(), 'r', encoding='utf-8') as ssh_obj:
        #         sys.stdout = Logger(F'{getcwd()}/{self.str_time}/log.txt')
        #         print('----------------------------------------------')
        #         print('执行命令：' + self.result)
        #         for ssh_ip in ssh_obj:
        #             # 根据类实例化一个ssh对象
        #             try:
        #                 self.ssh = paramiko.SSHClient()
        #                 self.host_ip = ssh_ip.strip()
        #                 self.username = swnstr
        #                 self.password = swistr
        #                 if self.login_ssh_host():
        #                     self.exec_ssh_command()
        #                     self.ssh.close()
        #                 else:
        #                     self.password = swpsbum
        #                     sleep(0.2)
        #                     self.login_ssh_host()
        #                     self.exec_ssh_command()
        #                     self.ssh.close()
        #             except Exception:
        #                 pass
        #         # messagebox.showinfo(title='刷入提示', message='配置已刷入，请检查是否成功')
        #         sleep(1)

    def getTextInput(self):
        self.result = self.tkt.get("1.0", "end")
        if self.selfile == True:
            with open( self.selected_file_path, 'r', encoding='utf-8') as ssh_obj:
                sys.stdout = Logger(F'{getcwd()}/{self.str_time}/log.txt')
                print('----------------------------------------------')
                print('文件路径：' + self.selected_file_path)
                print('执行命令：' + self.result)
                t1 = time()
                self.swnstr = self.iswn.get().ljust(1)
                self.swistr = self.iswi.get().ljust(1)
                self.swpsbum = self.iswp.get().ljust(1)
                for ssh_ip in ssh_obj:
                    # try:
                    #     loop = asyncio.get_event_loop()
                    #     loop.run_until_complete(self.psship(ssh_ip))
                    self.psship(ssh_ip)
                    self.output.insert(tkinter.END, "\nssh(%s)尝试连接." % ssh_ip.strip())
                    self.output.update()
                    # except Exception as exc:
                    #     error("exception {}".format(exc))
                    #     sys.exit('Exception: ' + str(exc))

                    # self.psship(task1.result())
                # for t in t_list:
                #     t.join()
                t2 = time()
                print('耗时：', t2 - t1)
        else:
            try:
                open('%s\ssh_connect.txt' % getcwd(), 'r')
            except Exception:
                messagebox.showinfo(title='错误提示', message='无默认主机文件，需要当前路径新建ssh_connect.txt')
                sys.exit(0)
            with open('%s\ssh_connect.txt' % getcwd(), 'r', encoding='utf-8') as ssh_obj:
                sys.stdout = Logger(F'{getcwd()}/{self.str_time}/log.txt')
                print('----------------------------------------------')
                print('执行命令：' + self.result)
                # with ThreadPoolExecutor(3) as t:
                # for ssh_ip in ssh_obj:
                #     try:
                #         loop = asyncio.get_event_loop()
                #         loop.run_until_complete(self.psship(ssh_ip))
                #         self.output.insert(tkinter.END, "\nssh(%s)尝试连接." % ssh_ip.strip())
                #         self.output.update()
                #     except Exception as exc:
                #         error("exception {}".format(exc))
                #         sys.exit('Exception: ' + str(exc))
                    # self.psship(task1.result())
        messagebox.showinfo(title='刷入提示', message='配置已刷入，请检查是否成功')

def main():
    Login()
    # L = Login()
    # 进行布局
    # L.gui()
    # 主程序执行
    tkinter.mainloop()
    #在哪个线程里调用了tk.mainloop()，就只能在哪个线程里更新UI

if __name__ == '__main__':
    main()