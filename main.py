import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db
from cryptography.fernet import Fernet
db.createDB()
class MainApplication:

    def __init__(self, master):

        self.large_font = ('Verdana', 25)
        self.small_font = ('Verdana', 10)
        self.small_font2 = ('Arial', 13)
        self.key = "Be1PA8snHgb1DS6oaWek62WLE9nxipFw3o3vB4uJ8ZI="
        self.cipher_suite = Fernet(self.key)
        self.user = tk.StringVar()
        self.password = tk.StringVar()

        self.master = master
        self.master.title("Password Storage")
        self.master.resizable(False, False)


        self.frameLogin = tk.Frame(self.master)
        self.frameLogin.pack()

        self.loginLabel = tk.Label(self.frameLogin, text="**Login**", width=3, height=2, font=self.large_font)
        self.loginLabel.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S , padx=10, pady=5)

        self.userLabel = tk.Label(self.frameLogin, text="User:", width=3, height=3, font=self.large_font)
        self.userLabel.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=5)

        self.userEntry = tk.Entry(self.frameLogin, textvariable=self.user, font=self.large_font)
        self.userEntry.grid(row=2, column=0, padx=10, pady=5, columnspan=3)
        self.userEntry.config(fg="black", justify="left")

        self.passwordLabel = tk.Label(self.frameLogin, text="Password:", width=3, height=3, font=self.large_font)
        self.passwordLabel.grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=5)

        self.passwordEntry = tk.Entry(self.frameLogin, textvariable=self.password, font=self.large_font)
        self.passwordEntry.grid(row=4, column=0, padx=10, pady=5, columnspan=3)
        self.passwordEntry.config(show="*", justify="left")

        self.bottonLog = tk.Button(self.frameLogin, text="Entrar", width=40, height=3, cursor="hand2", font=self.small_font, command=lambda:self.log_in())
        self.bottonLog.grid(row=5, column=1, padx=10, pady=11)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_rowconfigure(5, weight=1)


        self.user.trace("w", lambda *args: self.character_limit(self.user))
        self.password.trace("w", lambda *args: self.character_limit(self.password))

    def enter(self):
        print(self.master.winfo_screenheight())
        self.passwordStorageWindow()

    def character_limit(self,entry_text):
        value = entry_text.get()
        if len(value) > 16:
            entry_text.set(value[:16])

    def passwordStorageWindow(self):
        self.newNameList = tk.StringVar()
        self.newPasswordList = tk.StringVar()

        w = 10
        h = 2
        self.master.withdraw()
        self.passwordsScreen = tk.Toplevel(self.master)
        self.passwordsScreen.resizable(False, False)
        self.frame1 = tk.Frame(self.passwordsScreen)
        self.frame1.pack()

        self.frame2 = tk.Frame(self.passwordsScreen)
        self.frame2.pack()

        self.addPasswordLabel = tk.Label(self.frame1, text="Add New Password", width=3, height=2, font=self.large_font)
        self.addPasswordLabel.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S )

        self.nameLabel = tk.Label(self.frame1, text="Name:", font=self.large_font)
        self.nameLabel.grid(row=1, column=0, sticky=tk.E, pady=5)

        self.nameEntry = tk.Entry(self.frame1, font=self.large_font,textvariable=self.newNameList)
        self.nameEntry.grid(row=1, column=1)
        self.nameEntry.config(fg="black", justify="left")

        self.passwordLabel = tk.Label(self.frame1, text="Password:", font=self.large_font)
        self.passwordLabel.grid(row=2, column=0, sticky=tk.E ,pady=5)

        self.passwordEntry = tk.Entry(self.frame1, font=self.large_font,textvariable=self.newPasswordList)
        self.passwordEntry.grid(row=2, column=1)
        self.passwordEntry.config(fg="black", justify="left")

        self.noteLabel = tk.Label(self.frame1, text="Notes:", font=self.large_font)
        self.noteLabel.grid(row=3, column=0, sticky=tk.N+tk.E)

        self.noteText = tk.Text(self.frame1,width=20,height=3, font=self.large_font)
        self.noteText.grid(row=3, column=1)
        self.scrollVertNoteText = tk.Scrollbar(self.frame1, command=self.noteText.yview)
        self.scrollVertNoteText.grid(row=3, column=2, sticky="nsew")
        self.noteText.config(yscrollcommand=self.scrollVertNoteText.set)

        self.savePasswordButton = tk.Button(self.frame1, text="Save New Password", width=20, height=3, cursor="hand2", font=self.small_font2, command=lambda:self.insertNewPassword())
        self.savePasswordButton.grid(row=4, column=1)

        self.label = tk.Label(self.frame2, text="Passwords List", font=("Arial", 30)).grid(row=0, columnspan=3)

        self.cols = ('Password', 'Notes')

        style = ttk.Style()
        #style.configure('mystyle.Treeview', rowheight=10)
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings


        self.passwordsList = ttk.Treeview(self.frame2, columns=self.cols,style="mystyle.Treeview")
        self.passwordsList.grid(row=1,column=0,columnspan=2)
        self.scrollVertPasswordsList = tk.Scrollbar(self.frame2, command=self.passwordsList.yview)
        self.scrollVertPasswordsList.grid(row=1,column=3, sticky="nsew")
        self.passwordsList.config(yscrollcommand=self.scrollVertPasswordsList.set)

        self.passwordsList.heading("#0", text="Name")
        self.passwordsList.column("#0", width=150)
        self.passwordsList.heading("Password", text="Password")
        self.passwordsList.column("Password", width=150)
        self.passwordsList.heading("Notes", text="Notes")
        self.passwordsList.column("Notes", width=300)
        self.passwordsList.grid(row=1, column=0, columnspan=2, pady=5, padx=5)

        self.passwordsList.bind("<Double-1>", self.readNotes)
        self.passwordsList.bind("<BackSpace>", self.deleterow)
        self.passwordsList.bind("<Delete>", self.deleterow)

        self.newNameList.trace("w", lambda *args: self.character_limit(self.newNameList))
        self.newPasswordList.trace("w", lambda *args: self.character_limit(self.newPasswordList))

        self.passwordTabler()

    def readNotes(self, event):

        name = self.passwordsList.item(self.passwordsList.selection(), "text")
        notes = db.readNotes(self.user.get(), name)

        if notes==[]:
            pass
        else:
            self.notesScreen = tk.Toplevel(self.passwordsScreen)
            self.notesScreen.title("Notes")
            self.notesScreen.resizable(False, False)
            self.label = tk.Label(self.notesScreen, text=notes[0][0], font=("Arial", 30)).grid(row=0, columnspan=3)

    def deleterow(self, event):
        name = self.passwordsList.item(self.passwordsList.selection(), "text")
        row_selected = self.passwordsList.selection()

        answer = messagebox.askquestion("Delete Password", "Are you sure you want to delete "+name+" password?")
        if answer == "yes":
            db.erasePassword(self.user.get(), name)
            self.passwordsList.delete(row_selected)

    def passwordTabler(self):
        self.tempList = db.readPasswords(self.user.get())

        for i, (name, password, notes) in enumerate(self.tempList, start=1):
            decoded_text = self.cipher_suite.decrypt(password)
            decoded_text = decoded_text.decode("utf-8")
            self.passwordsList.insert("", "end", text=name,values=( decoded_text, notes.partition('\n')[0]))

    def insertNewPassword(self):


        if self.newPasswordList.get().isspace() or self.newPasswordList.get()=="" or self.newNameList.get().isspace() or self.newNameList.get()=="":
            messagebox.showwarning("Warning!", "Name and Password cannot be empty")
        else:
            encoded_text = self.cipher_suite.encrypt(bytes(self.newPasswordList.get(), encoding='utf-8'))
            db.insertPasswordData(self.user.get(), self.newNameList.get(), encoded_text, self.noteText.get("1.0", tk.END))
            self.newNameList.set("")
            self.newPasswordList.set("")
            self.noteText.delete(1.0, tk.END)
            messagebox.showinfo("Congratulations!", "New password added successfully!")
            self.passwordsList.delete(*self.passwordsList.get_children())
            self.passwordTabler()

    def log_in(self):

        value = db.loginUser(self.user.get(),self.password.get())
        if value=="yes":
            self.password = ""
            self.passwordStorageWindow()
        elif value=="no":
            messagebox.showwarning("Incorrect Password", "You typed a wrong password")
        elif value=="error":
            answer = messagebox.askquestion("Unregistered User", "Do you want to create a new one?")
            if answer=="yes":
                db.createUser(self.user.get(),self.password.get())
                self.password = ""
                self.passwordStorageWindow()

if __name__ == "__main__":

    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()