import pymongo as pym
from tkinter import *

conn = pym.MongoClient('localhost',27017)
db = conn['MyDatabase']

colln = db['users']



root = Tk()
# ---------------- Main Window---------------------------#
root.title("Python: Simple Login Application")

root.resizable(0, 0)
# -------------------------------------------------------#

USERNAME = StringVar()
PASSWORD = StringVar()

class Member():
    
    def __init__(self, un="" ,pw="",fn="",ln="",ph="",em=""):
        self.uname = un;
        self.pwd = pw;
        self.fname = fn;
        self.lname = ln;
        self.phone = ph;
        self.email = em;
    
    def find(self, un,pw):
        #----- Database Connection ----------#
        result = colln.find_one({"username":un,"passwd":pw})
        if result == None:  
            return False
        else:
            self.uname = result['username']
            self.pwd = result['passwd']
            self.fname = result['first_nm']
            self.lname = result['last_nm']
            self.phone = result['phone']
            self.email = result['email']
            
            return True

    def get(self):
        return self.fname + " " + self.lname + " " + self.phone + " " + self.email

user = Member()

def Login():
    exist = user.find(USERNAME.get(),PASSWORD.get())
    if (exist == False):    
        lbl_text.config(text="Invalid username or password", fg="red")
        USERNAME.set("")
        PASSWORD.set("")
    else:
        USERNAME.set("")
        PASSWORD.set("")
        lbl_text.config(text="")
        Details(user.get())
    

def Details(msg):
    root.withdraw()
    popup = Toplevel()
    popup.wm_title("!")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = lambda:Back(popup))
    B1.pack()
    B2 = Button(popup, text="Update", command = lambda:Register(True,popup))
    B2.pack()
    


def Back(child):
    child.destroy()
    root.deiconify()


def Register(exist,window):
    if (exist == True):
        window.destroy()
    else:
        window.withdraw()
    global Home, unm, psw, fnm, lnm, phn, eml
    Home = Toplevel()
    Home.title("Python: Simple Login Application")
    #Labels
    lbl_un = Label(Home, text = "Username:", font=('arial', 14), bd=15)
    lbl_un.grid(row=0, sticky="e")
    lbl_pw = Label(Home, text = "Password:", font=('arial', 14), bd=15)
    lbl_pw.grid(row=1, sticky="e")
    lbl_fn = Label(Home, text = "First Name:", font=('arial', 14), bd=15)
    lbl_fn.grid(row=2, sticky="e")
    lbl_ln = Label(Home, text = "Last Name:", font=('arial', 14), bd=15)
    lbl_ln.grid(row=3, sticky="e")
    lbl_ph = Label(Home, text = "Phone No.:", font=('arial', 14), bd=15)
    lbl_ph.grid(row=4, sticky="e")
    lbl_em = Label(Home, text = "Email:", font=('arial', 14), bd=15)
    lbl_em.grid(row=5, sticky="e")
    #Entries
    unm = StringVar()
    psw = StringVar()
    fnm = StringVar()
    lnm = StringVar()
    phn = StringVar()
    eml = StringVar()
    en_unm = Entry(Home, textvariable=unm, font=(14))
    en_unm.grid(row=0, column=1)
    en_psw = Entry(Home, textvariable=psw, show="*", font=(14))
    en_psw.grid(row=1, column=1)
    en_fnm = Entry(Home, textvariable=fnm, font=(14))
    en_fnm.grid(row=2, column=1)
    en_lnm = Entry(Home, textvariable=lnm, font=(14))
    en_lnm.grid(row=3, column=1)
    en_phn = Entry(Home, textvariable=phn, font=(14))
    en_phn.grid(row=4, column=1)
    en_eml = Entry(Home, textvariable=eml, font=(14))
    en_eml.grid(row=5, column=1)
    #Buttons
    btn_back = Button(Home, text='Back', command = lambda:Back(Home))
    btn_back.grid(row = 6,column = 0)
    btn_save = Button(Home, text = 'Save', command = lambda:Save(exist))
    btn_save.grid(row = 6, column = 1)

def Save(exist):
    #----- Database Connection ----------#
    data = {"username":unm.get(),"passwd":psw.get(),"first_nm":fnm.get(),"last_nm":lnm.get(),"phone":phn.get(),"email":eml.get()}
    if (exist == True):
        colln.update_one({"username":unm.get()},{"$set":data}, upsert = True)
    else:
        colln.insert_one(data);
    
    Back(Home)        



#----------------- Main Window Features ------------------#
# Frames
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

#Labels
lbl_title = Label(Top, text = "Python: Simple Login Application", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)

#Entry
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)

#Buttons
btn_login = Button(Form, text='Login', width=45, command=Login)
btn_login.grid(row = 3, column = 0)
#btn_login.bind('<Return>', Login)
btn_register = Button(Form, text='Register', width=45, command= lambda:Register(False,root))
btn_register.grid(row = 3, column = 1)


def main():
    root.mainloop()

if __name__ == '__main__':
    main() 