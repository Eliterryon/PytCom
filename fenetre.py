from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox

class Interface(Frame):

    def affiche(self, Message):
        temp = ""
        for mess in Message:
            temp += mess + "\n"
        self.txt.insert(END, temp)

    def addaffiche(self, Message):
        self.txt.insert(END, Message + "\n")

    def clean(self):
        self.txt.delete('1.0', END)

    def openFile(self):
            filepath = filedialog.askopenfilename(filetypes=[('txt files','.txt')])
    
            with open(filepath, 'r') as FILE:
                content = FILE.read()
    
            self.txt.insert("end", content)

    def add(self, _name):
        self.liste.insert(END, _name)
    
    def sub (self, _name):
        pass

    def onselect(self):
        pass

    def val(self):
        pass

    def alert(self, txt = ""):
        messagebox.showinfo("alerte", "Bravo! tu a clicker sur : ")
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        frame=Frame(fenetre,borderwidth=2,bg="red")
        frame.grid(row=0,column=0)

        frameR=Frame(frame,bg="yellow")
        frameL=Frame(frame,bg="blue")
        frameR.pack(side=RIGHT ,padx=10, pady=10)
        frameL.pack(side=LEFT ,padx=10, pady=10)


        self.liste = Listbox(frameL,selectbackground = "grey", height=30)
        self.liste.pack()

        frameH=Frame(frameR,bg="orange")
        frameLO=Frame(frameR,bg="blue")
        frameH.pack(side=TOP ,padx=10, pady=10)
        frameLO.pack(side=BOTTOM ,padx=10, pady=10)

        self.txt=Text(frameH,bg='#FFFFFF',)
        c=["hello","plouf"]
        self.affiche(c)

        vbar=Scrollbar(frameH,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.txt.yview)

        self.txt.config( yscrollcommand=vbar.set)
        self.txt.pack(side=LEFT,expand=True,fill=BOTH,padx=10, pady=10)

        self.saisi = Entry(frameLO, width=100)
        self.saisi.pack(side=LEFT,padx=10, pady=10)
        self.valider = Button(frameLO, text="envoyer", command=self.val)
        self.valider.pack(side=RIGHT,padx=10, pady=10)


        menubar = Menu(fenetre)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Clean", command=self.clean)
        menu1.add_command(label="Editer", command=self.alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=fenetre.quit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Couper", command=self.alert)
        menu2.add_command(label="Copier", command=self.alert)
        menu2.add_command(label="Coller", command=self.alert)
        menubar.add_cascade(label="Editer", menu=menu2)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="A propos", command=self.alert)
        menubar.add_cascade(label="Aide", menu=menu3)

        fenetre.config(menu=menubar)
