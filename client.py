import socket
from threading import Thread
from tkinter import *

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ipAddress="127.0.0.1"
port=8000
client.connect((ipAddress,port))
print("Connected with the server successfully!")

class gui:
    def __init__(self):
        self.window=Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)

        self.title=Label(self.login,text="Please log in to continue!",justify="center",font="Arial 14 bold")
        self.title.place(relheight=0.15,relx=0.2,rely=0.07)

        self.labelName=Label(self.login,text="Name: ",font="arial 10")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)

        self.entry=Entry(self.login,font="Arial 14")
        self.entry.place(relheight=0.12,relx=0.25,rely=0.2,relwidth=0.4)
        self.entry.focus()

        self.button=Button(self.login,text="Continue:",font="Arial 14 bold",command=lambda:self.goAhead(self.entry.get()))
        self.button.place(relx=0.4,rely=0.5)

        self.window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width = False,
							height = False)
        self.window.configure(width = 470,
							height = 550,
							bg = "#17202A")
        self.labelHead = Label(self.window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.window,
						width = 450,
						bg = "#ABB2B9")
		
        self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
        self.textCons = Text(self.window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
        self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
        self.labelBottom=Label(self.window,bg="blue",height="80")
        self.labelBottom.place(relwidth=1,rely=0.825)

		# Msg means message

        self.entryMsg=Entry(self.labelBottom,bg="yellow",fg="lime",font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg=Button(
			self.labelBottom,
			text="Send",
			font="Helvetica 10 bold",
			width=20,
			bg="green",
			command=lambda:self.sendButton(self.entryMsg.get())
		)
        self.buttonMsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)

        self.textCons.config(cursor="arrow")

        scrollbar=Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self,msg):
        self.textCons.config(state=DISABLED)
        self.msg=msg
        self.entryMsg.delete(0,END)
		# snd means 'send'
        snd=Thread(target=self.write)
        snd.start()

    def show_message(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message=(f"{self.name} says: {self.msg}")
            client.send(message.encode("utf-8"))
            self.show_message(message)
            break

    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message=="NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except:
                print("⚠️ An error occured! ⚠️")
                client.close()
                break

g=gui()