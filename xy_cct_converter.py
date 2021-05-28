# xy to CCT:
# n = (x - 0.3320)/(y - 0.1858)
# CCT = -449*n^3 + 3525*n^2 - 6823.3*n + 5520.33
#
# CCT to xy:
# CCT 7000K ~ 25000K
# x = -2.0064*(10^9/CCT^3) + 1.9018*(10^6/CCT^2) + 0.2478*(10^3/CCT) + 0.237040
# y = -3*x^2 + 2.87*x-0.275
# CCT 4000K ~ 7000K
# x = -4.607*(10^9/CCT^3) + 2.9678*(10^6/CCT^2) + 0.09911*(10^3/CCT) + 0.244063
# y = -3*x^2 + 2.87*x-0.275
#
# X Y Z to x y
# x = X/(X+Y+Z)
# y = Y/(X+Y+Z)
# Y is lux value
from tkinter import *
import tkinter.messagebox


class MyWindow:

    def __init__(self):
        self.window = Tk()
        self.window.title('xy cct converter')
        self.window.geometry('350x150')
        # self.window.resizable(width=False, height=False)

        self.frame_left = Frame(self.window, bd=5, bg='#4682B4')  # create frame
        self.frame_left.grid(row=0, column=0, stick="we", padx=15, pady=30)

        self.frame_middle = Frame(self.window, bd=5)
        self.frame_middle.grid(row=0, column=1, stick="we", padx=0, pady=30)

        self.frame_right = Frame(self.window, bd=5, bg="#5F9EA0")
        self.frame_right.grid(row=0, column=2, stick="we", padx=15, pady=30)

        Label(self.frame_left, text='x').grid(row=0, column=0, stick="w", padx=5, pady=5)
        self.ent_x = Entry(self.frame_left, width=10)
        self.ent_x.grid(row=0, column=1, stick="we", padx=5, pady=5)
        self.ent_x.insert(0, "0.3128")

        Label(self.frame_left, text='y').grid(row=1, column=0, stick="w", padx=5, pady=5)
        self.ent_y = Entry(self.frame_left, width=10)
        self.ent_y.grid(row=1, column=1, stick="we", padx=5, pady=5)
        self.ent_y.insert(0, "0.3292")

        Button(self.frame_middle, text='>>', command=self.xy_to_cct).grid(row=0, column=0, stick="we", padx=5, pady=1)
        Button(self.frame_middle, text='<<', command=self.cct_to_xy).grid(row=1, column=0, stick="we", padx=5, pady=1)

        Label(self.frame_right, text='cct').grid(row=0, column=0, stick="w", padx=5, pady=5)
        self.ent_cct = Entry(self.frame_right, width=10)
        self.ent_cct.grid(row=0, column=1, stick="we", padx=5, pady=5)
        self.ent_cct.insert(0, "6500")

        self.window.mainloop()

    def xy_to_cct(self):
        x_str = self.ent_x.get()
        y_str = self.ent_y.get()
        if len(x_str) == 0:
            tkinter.messagebox.showwarning('Warning', 'Please input float value for x')
            return
        if len(y_str) == 0:
            tkinter.messagebox.showwarning('Warning', 'Please input float value for y')
            return

        for i in x_str:
            if i not in '0123456789.':
                tkinter.messagebox.showwarning('Warning', 'Please input float value for x')
                return
        for i in y_str:
            if i not in '0123456789.':
                tkinter.messagebox.showwarning('Warning', 'Please input float value for y')
                return
        x = float(x_str)
        y = float(y_str)
        if x <= 0 or y <= 0 or (x+y) >= 1:
            tkinter.messagebox.showwarning('Warning', 'x>0,y>0,x+y<1')
            return

        n = (x - 0.332) / (y - 0.1858)
        cct = -449*n**3 + 3525*n**2 - 6823.3*n + 5520.33
        self.ent_cct.delete(0, END)
        self.ent_cct.insert(0, int(cct))

    def cct_to_xy(self):
        cct_str = self.ent_cct.get()
        if len(cct_str) == 0:
            tkinter.messagebox.showwarning('Warning', 'Please input integer value for cct')
            return
        for i in cct_str:
            if i not in '0123456789':
                tkinter.messagebox.showwarning('Warning', 'Please input integer value for cct')
                return

        cct = int(cct_str)
        if cct < 4000:
            tkinter.messagebox.showwarning('Warning', 'cct > 4000')
            return

        # the result is not guaranteed if cct is smaller than 4000 or bigger than 25000
        if cct > 7000:  # 7000K ~ 25000K
            x = -2.0064 * (10**9 / cct**3) + 1.9018 * (10**6 / cct**2) + 0.2478*(10**3 / cct) + 0.237040
        else:           # 4000K ~ 7000K
            x = -4.607 * (10**9 / cct**3) + 2.9678 * (10**6 / cct**2) + 0.09911*(10**3 / cct) + 0.244063
        y = -3 * x**2 + 2.87 * x - 0.275
        self.ent_x.delete(0, END)
        self.ent_x.insert(0, '%.4f' % x)
        self.ent_y.delete(0, END)
        self.ent_y.insert(0, '%.4f' % y)


if __name__ == "__main__":
    w = MyWindow()
