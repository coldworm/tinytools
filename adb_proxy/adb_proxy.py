from tkinter import *
from tkinter import filedialog
import os
import subprocess
import json
import time
import threading

Version = '1.1'

class MyWindow:

    def __init__(self):
        self.window = Tk()
        self.window.title('ADB proxy ' + Version)
        self.window.geometry('810x700')
        # self.window.bind('<Configure>', self.window_configure)

        self.Msg = Text(self.window, width=100, height=50)
        self.Msg.place(x=90, y=8, anchor="nw")

        Button(self.window, text='Clear Log', command=self.clear_log).grid(row=0, column=0, stick="w", padx=5, pady=5)

        self.button = []
        self.run = []
        self.load_command()
        self.run_flag = False

        self.window.mainloop()

    def load_command(self):
        path = os.getcwd() + '/command'
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                with open(dirpath + '/' + filename, 'rb') as load_f:
                    load_dict = json.load(load_f)
                    # check key
                    if 'key' in load_dict.keys() and load_dict['key'] == 'command':
                        # generate buttons
                        index = len(self.button)
                        self.button.append(Button(self.window, text=load_dict['name'],
                                                  command=lambda index_f=index: self.click_call(index_f)))
                        self.button[index].grid(row=index+1, column=0, stick="w", padx=5, pady=5)
                        if 'cmdlist' in load_dict.keys():
                            self.run.append(load_dict['cmdlist'])
                        else:
                            self.run.append([])
        # print(self.run)

    def click_call(self, index):
        if not self.run_flag:
            self.run_flag = True
            thread_cmd = threading.Thread(target=self.run_thread_cmd, args=(index,))
            thread_cmd.start()
        else:
            self.Msg.insert(END, '--------------------------Thread running!--------------------------\n')

    def run_thread_cmd(self, index=0):
        for i in range(len(self.run[index])):
            if 'id' in self.run[index][i].keys():
                step = self.run[index][i]['id']
                self.Msg.insert(END, '----step ' + str(step) + '\n')

            if 'run' in self.run[index][i].keys():
                order = self.run[index][i]['run']
                self.Msg.insert(END, order+'\n')
                res = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
                self.Msg.insert(END, str(res.stdout.read(), encoding="utf-8"))

            if 'delay' in self.run[index][i].keys():
                delay_time = self.run[index][i]['delay']
                if delay_time > 0:
                    self.Msg.insert(END, '--------------------------Delay %f seconds--------------------------\n' % delay_time)
                    time.sleep(delay_time)

            if 'remark' in self.run[index][i].keys():
                self.Msg.insert(END, self.run[index][i]['remark'] + '\n')
        self.Msg.insert(END, '--------------------------Command finished!--------------------------\n')
        self.run_flag = False

    def clear_log(self):
        self.Msg.delete(1.0, END)

    # def window_configure(self, event):
    #     width_w = self.window.winfo_width()
    #     height_w = self.window.winfo_height()
    #     self.Msg.config(width=width_w-100)


if __name__ == '__main__':
    MyWindow()
