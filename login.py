from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
class Login:
    def __init__(self,root):
        self.root = root
        self.root.title("Advanced Student Managment System [Login Panel]")
        self.root.geometry("1500x780+0+0")
        self.root.resizable(False,False)
        self.bg = ImageTk.PhotoImage(file="lbg.jpg")
        bgl = Label(self.root,text="Login",image=self.bg).place(relwidth=1,relheight=1,x=0,y=0)

        # Login Frame      
        head = Label(self.root,text="Advanced Student Managment System",font=("Cambria",45),fg="#abc6ff",bg="black").place(x=320,y=0)

        title = Label(self.root,text="Login Here",font=("Arial",35,"bold"),fg="#346eeb",bg="black").place(x=150,y=200)
        Label(self.root,text="").place(x=0,y=260,width=490,height=1)

        uname = Label(self.root,text="Username :",font=("Arial",15),fg="white",bg="black").place(x=150,y=290)
        self.uname = ttk.Entry(self.root,font=("Arial",13),justify='center')
        self.uname.place(x=270,y=290)

        pwd = Label(self.root,text="Password :",font=("Arial",15),fg="white",bg="black").place(x=150,y=340)
        self.pwd = ttk.Entry(self.root,font=("Arial",13),justify='center')
        self.pwd.place(x=270,y=340)

        self.loginbtn = Button(self.root,text="Login",font=("Arial,15"),command=self.login)
        self.loginbtn.place(x=300,y=390,width=120,height=40)

    def login(self):
        if self.pwd.get()=="" or self.uname.get()=="":
            messagebox.showerror("Error","All Fields are Required",parent=self.root)
        elif self.pwd.get()=="root" or self.uname.get()=="admin":
            self.root.destroy() 
            import main
            
        else:
            messagebox.showinfo("Username and Password is incorrect ")

        Label(self.root,text="Note : if you have not username or password,  \n please contact @himanshuraj1209@gmail.com",bg="black",fg="white").place(x=150,y=500)
root = Tk()
obj = Login(root)
root.mainloop()