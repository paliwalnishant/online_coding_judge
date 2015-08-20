from Tkinter import *
import tkFileDialog
import tkMessageBox

class MyText(Frame):
    def __init__(self, parent=None, *args, **kwargs):
        Frame.__init__(self, parent)
        self.pack()
        self.text = Text(self, *args, **kwargs)
        self.text.config(background='white')
        self.text.pack(expand=YES, fill=BOTH)
    def get(self):
        return self.text.get(1.0,"%s-1c" % END)
    def set(self, astr):
        self.text.delete(1.0, END)
        self.text.insert(INSERT, astr)
    def set_from_file(self):
        afilename = tkFileDialog.askopenfilename()
        if afilename:
            try:
                afile = open(afilename)
                self.set(afile.read())
                afile.close()
            except Exception, e:
                tkMessageBox.showwarning("File Problem",
                "Couldn't read file '%s': %s" % (afilename, str(e)))
    #def abc(self):
     #   sys.exit(0)

def main():
    tk = Tk()
    tk.title('Text Reader App')
    atext = MyText(tk)
    atext.pack()
    open_button = Button(tk, text="Open File",activeforeground='blue',command=atext.set_from_file)
    #close_button = Button(tk, text="close",activeforeground='blue',command=atext.abc)
    #close_button.pack()
    open_button.pack()
    tk.mainloop()

if __name__ == "__main__":
    main()
