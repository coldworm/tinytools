from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import os

CountMax = 7
Version = '2.0'


class MyWindow:

    def __init__(self):
        self.count = 3
        self.ent_s = []
        self.ent_m = []
        self.ent_e = []

        self.window = Tk()
        self.window.title('Data Pick ' + Version)
        self.window.geometry('600x400')
        # self.window.resizable(width=False, height=False)

        Label(self.window, text='开始').grid(row=0, column=0, stick="we", padx=5, pady=5)
        Label(self.window, text='键值').grid(row=0, column=1, stick="we", padx=5, pady=5)
        Label(self.window, text='结束').grid(row=0, column=2, stick="we", padx=5, pady=5)

        for i in range(self.count):
            self.ent_s.append(Entry(self.window, width=25))
            self.ent_m.append(Entry(self.window, width=25))
            self.ent_e.append(Entry(self.window, width=25))

        self.refresh_entry()

        self.bt_add = Button(self.window, text="增加", bg='#008B8B', command=self.add_button, width=4).place(relx=.84, rely=.7, anchor="c")
        self.bt_del = Button(self.window, text="删除", bg='#008B8B', command=self.remove_button, width=4).place(relx=.94, rely=.7, anchor="c")
        self.skip_flag = BooleanVar()
        self.skip_flag.set(True)
        Checkbutton(self.window, text="不显示空数据", variable=self.skip_flag, onvalue=True, offvalue=False).place(relx=.60, rely=.7, anchor="w")

        Label(self.window, text='路径').place(relx=.02, rely=.82, anchor="w")
        self.ent_path = Entry(self.window, width=60, state=DISABLED)
        self.ent_path.place(relx=.08, rely=.82, anchor="w")
        Button(self.window, text='选择', bg='#008B8B', command=self.select_path, width=4).place(relx=.84, rely=.82, anchor="c")
        self.ent_path_tail = Entry(self.window, width=5)
        self.ent_path_tail.place(relx=.91, rely=.82, anchor="w")
        self.ent_path_tail.insert(0, ".txt")

        self.bt_valid = Button(self.window, text="确定", bg='#00B080', command=self.pick_data, width=10).place(relx=.5, rely=.94, anchor="c")

        self.window.mainloop()

    # create new entry
    def add_button(self):
        if self.count < CountMax:
            self.count = self.count + 1
            self.ent_s.append(Entry(self.window, width=25))
            self.ent_m.append(Entry(self.window, width=25))
            self.ent_e.append(Entry(self.window, width=25))
        self.refresh_entry()

    # delete entry
    def remove_button(self):
        if self.count > 1:
            self.ent_s[self.count - 1].destroy()
            self.ent_m[self.count - 1].destroy()
            self.ent_e[self.count - 1].destroy()
            self.count = self.count-1
            self.ent_s.pop(-1)
            self.ent_m.pop(-1)
            self.ent_e.pop(-1)
        self.refresh_entry()

    def refresh_entry(self):
        for i in range(self.count):
            self.ent_s[i].grid(row=i + 1, column=0, padx=10, pady=5)
            self.ent_m[i].grid(row=i + 1, column=1, padx=10, pady=5)
            self.ent_e[i].grid(row=i + 1, column=2, padx=10, pady=5)

    def select_path(self):
        self.ent_path.config(state=NORMAL)
        self.ent_path.delete(0, END)
        self.ent_path.insert(0, filedialog.askdirectory(title='选择文件夹'))
        self.ent_path.config(state=DISABLED)

    def pick_data(self):
        path = self.ent_path.get()
        key_flag = 0
        key_str = ''
        if len(path) == 0:
            tkinter.messagebox.showwarning('提示', '路径为空')
            return

        for i in range(self.count):
            if len(self.ent_m[i].get()) != 0:
                key_flag = 1
        if key_flag == 0:
            tkinter.messagebox.showwarning('提示', '键值为空')
            return

        try:
            rootdir = os.path.join(path)
            t_obj = open('res.csv', 'wt')

            # write csv head line
            t_obj.write('File,')
            for i in range(self.count):
                key_str = self.ent_m[i].get()
                if len(key_str) != 0:
                    t_obj.write(key_str.replace(' ', '').replace('=', '').replace(',', '')+',')
            t_obj.write('\n')

            # Loop files in the path
            file_num = 0
            for (dirpath, dirnames, filenames) in os.walk(rootdir):
                for filename in filenames:
                    tail = self.ent_path_tail.get()
                    if len(tail) == 0:
                        tail = '.txt'
                    if os.path.splitext(filename)[1] == tail:
                        file_num += 1
                        f_obj = open(dirpath + '\\' + filename, 'rt')
                        s_read = f_obj.read()
                        f_obj.close()
                        wt_pos = t_obj.tell()           # save current position

                        full_path = dirpath + '\\' + filename
                        ind = full_path.index('\\')
                        t_obj.write(full_path[ind+1:] + ',')     # write file name
                        found_flag = False
                        for i in range(self.count):
                            pre_str = self.ent_s[i].get()
                            key_str = self.ent_m[i].get()
                            end_str = self.ent_e[i].get()
                            if len(key_str) != 0:
                                pos = 0
                                if len(pre_str) != 0:
                                    pos = s_read.find(pre_str)
                                if pos != -1:
                                    pos_s = s_read.find(key_str, pos)
                                    pos_e = 0
                                    if pos_s != -1:
                                        pos_s = pos_s + len(key_str)
                                        if len(end_str) != 0:
                                            pos_e = s_read.find(end_str, pos_s)
                                        else:
                                            pos_e = s_read.find('\n', pos_s)
                                    if pos_s != -1 and pos_e != -1:
                                        t_obj.write(s_read[pos_s:pos_e] + ',')
                                        found_flag = True
                                    else:
                                        t_obj.write(',')
                                else:
                                    t_obj.write(',')
                        t_obj.write('\n')
                        # haven't found any key value, go back
                        if not found_flag and self.skip_flag.get():
                            t_obj.seek(wt_pos, 0)
            t_obj.truncate()
            t_obj.close()
            tkinter.messagebox.showinfo('结果', '完成遍历' + str(file_num) + '个文件')
        except Exception as err:
            print(err)


if __name__ == '__main__':
    w = MyWindow()
