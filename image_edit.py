from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import matplotlib.pyplot as plt


class MyWindow:

    def __init__(self):
        self.window = Tk()
        self.window.title('Image Edit')
        self.window.geometry('350x250')

        Button(self.window, text='Open', bg='#008B8B', command=self.select_picture, width=7)\
            .place(relx=.05, rely=.15, anchor="w")
        self.ent_path = Entry(self.window, width=32, state=DISABLED)
        self.ent_path.place(relx=.25, rely=.15, anchor="w")

        Button(self.window, text='Rotate', bg='#008B8B', command=self.rotate, width=7)\
            .place(relx=.05, rely=.5, anchor="w")

        Button(self.window, text='X mirror', bg='#008B8B', command=self.x_mirror, width=7)\
            .place(relx=.25, rely=.5, anchor="w")

        Button(self.window, text='Y mirror', bg='#008B8B', command=self.y_mirror, width=7)\
            .place(relx=.45, rely=.5, anchor="w")

        Button(self.window, text='Reset', bg='#008B8B', command=self.reset, width=7)\
            .place(relx=.65, rely=.5, anchor="w")

        Button(self.window, text='Save', bg='#008B8B', command=self.save, width=7)\
            .place(relx=.5, rely=.85, anchor="c")

        self.img = Image.new('RGB', (256, 256), (255, 255, 255))
        self.window.mainloop()

    def select_picture(self):
        self.ent_path.config(state=NORMAL)
        self.ent_path.delete(0, END)
        img_name = filedialog.askopenfilename(title='Select picture',
                                              filetypes=[("PNG", ".png"), ("JPG", ".jpg"), ('All Files', '*')])
        self.ent_path.insert(0, img_name)
        self.ent_path.config(state=DISABLED)

        if len(img_name) == 0:
            return
        self.img = Image.open(img_name)
        plt.figure(img_name.split('/', -1)[-1])
        plt.imshow(self.img)
        plt.axis('off')
        plt.show()

    def rotate(self):
        img_name = self.ent_path.get()
        if len(img_name) == 0:
            return
        self.img = self.img.transpose(Image.ROTATE_90)
        plt.imshow(self.img)
        plt.show()

    def x_mirror(self):
        img_name = self.ent_path.get()
        if len(img_name) == 0:
            return
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        plt.imshow(self.img)
        plt.show()

    def y_mirror(self):
        img_name = self.ent_path.get()
        if len(img_name) == 0:
            return
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        plt.imshow(self.img)
        plt.show()

    def reset(self):
        img_name = self.ent_path.get()
        if len(img_name) == 0:
            return
        self.img = Image.open(img_name)
        plt.imshow(self.img)
        plt.show()

    def save(self):
        img_name = self.ent_path.get()
        if len(img_name) == 0:
            return
        new_name = 'new' + '.' + img_name.split('/', -1)[-1].split('.', -1)[-1]
        self.img.save(new_name)
        messagebox.showinfo(title='Finish', message='Save ' + new_name + ' success!')


if __name__ == "__main__":
    MyWindow()
