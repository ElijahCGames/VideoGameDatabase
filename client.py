"""
CLINET CODE FOR CS3200 Final Project

Video Game Database

Tasks for Application:
 
====
Input a users name 
(If not, they can sign up with one (adds name to database))
====

====
Adding games from a users collection
Removing games from a users collection


Recommending a game from collection or database based on parameters

Adding a review
(Game reviews are based on the average of all the reviews associated with a specfic game)

Adding a game to a database 
(Will be done on a different screen)


All these functions are task bar level events
====

====
Primary views

User entry
Collection
Game View
Add Game to Database
Recommend Screen
====

"""
from tkinter import *

class App(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        self.title("Video Game Database")
        self.option_add('*tearOff', FALSE)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (UserEntry,GameCollection):
            page_name = F.__name__
            frame = F(parent=container,controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame("UserEntry")

        menu = AppMenu(self)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class AppMenu(Menu):
    def __init__(self,parent):
        Menu.__init__(self, parent)

        appmenu = Menu(self, name='apple')
        self.add_cascade(menu=appmenu)

        appmenu.add_command(label='About My Application')
        appmenu.add_separator()
        parent['menu'] = self

        menu_user = Menu(self)
        menu_collection = Menu(self)
        menu_data = Menu(self)
        menu_window = Menu(self,name = "window")

        self.add_cascade(menu=menu_user, label='User')
        self.add_cascade(menu=menu_collection, label='Collection')
        self.add_cascade(menu=menu_data, label='Data')
        self.add_cascade(menu=menu_window, label='Window')

        self.user_options(menu_user)
        self.collection_options(menu_collection)
        self.data_options(menu_data)

    def user_options(self, subMenu):
        subMenu.add_command(label="Change Username")
        subMenu.add_command(label="Goto User Page")

    def collection_options(self,subMenu):
        subMenu.add_command(label="Add Game")
        subMenu.add_command(label="Remove Game")
        subMenu.add_command(label="Reccomend Game")

    def data_options(self,subMenu):
        subMenu.add_command(label="Add Game")
        subMenu.add_command(label="Add Review")


class UserEntry(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller

        self.startTitle = Label(self,text="VGDB")
        self.startTitle.pack(side="top",fill="x",pady=10)
        self.usernameEntry = Entry(self)
        self.submit = Button(self,text="Submit",command=self.submitUsername)

        self.usernameEntry.pack()
        self.submit.pack()

    def submitUsername(self):
        print(self.usernameEntry.get())
        self.controller.show_frame("GameCollection")

class GameCollection(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

        label = Label(self,text="Collection")
        label.grid(row=0,column=0)
        r = 1
        for name,dev in [("Mario","Nintendo"),("Celeste","Matt Makes Games"),("Last of Us","Naughty Dog")]:
            item = GameListing(self,name,dev)
            item.grid(row=r,column=0)
            r+=1

class GameListing(Frame):
    def __init__(self,parent,name,dev):
        Frame.__init__(self,parent,highlightbackground="black",highlightthickness=1,width=300)

        self.nameLab = Label(self,text=name)
        self.devLab = Label(self,text="Developer: " + dev)
        self.nameLab.grid(row=0,column=0)
        self.devLab.grid(row=0,column=1)

if __name__ == "__main__":
    root = App()
    root.mainloop()

"""
Menu System 

from tkinter import *

def donothing():
    print("hello")

root = Tk()
root.title("VideoGameDatabase")
root.option_add('*tearOff', FALSE)

menubar = Menu(root)
appmenu = Menu(menubar, name='apple')
menubar.add_cascade(menu=appmenu)
appmenu.add_command(label='About My Application')
appmenu.add_separator()
root['menu'] = menubar

menu_file = Menu(menubar)
menu_edit = Menu(menubar)
windowmenu = Menu(menubar, name='window')

menubar.add_cascade(menu=menu_file, label='Hello')
menubar.add_cascade(menu=menu_edit, label='Test')
menubar.add_cascade(menu=windowmenu, label='Window')

menu_file.add_command(label='New', command=donothing)
menu_file.add_command(label='Open...', command=donothing)
menu_file.add_command(label='Close', command=donothing)

menu = Menu(root)
for i in ('One', 'Two', 'Three'):
    menu.add_command(label=i)
if (root.tk.call('tk', 'windowingsystem')=='aqua'):
    root.bind('<2>', lambda e: menu.post(e.x_root, e.y_root))
    root.bind('<Control-1>', lambda e: menu.post(e.x_root, e.y_root))
else:
    root.bind('<3>', lambda e: menu.post(e.x_root, e.y_root))


root.mainloop()
"""

"""
Example code to deal with tk.

import random
from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E

class GuessingGame:
    def __init__(self, master):
        self.master = master
        master.title("Guessing Game")

        self.secret_number = random.randint(1, 100)
        self.guess = None
        self.num_guesses = 0

        self.message = "Guess a number from 1 to 100"
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.guess_button = Button(master, text="Guess", command=self.guess_number)
        self.reset_button = Button(master, text="Play again", command=self.reset, state=DISABLED)

        self.label.grid(row=0, column=0, columnspan=2, sticky=W+E)
        self.entry.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.guess_button.grid(row=2, column=0)
        self.reset_button.grid(row=2, column=1)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.guess = None
            return True

        try:
            guess = int(new_text)
            if 1 <= guess <= 100:
                self.guess = guess
                return True
            else:
                return False
        except ValueError:
            return False

    def guess_number(self):
        self.num_guesses += 1

        if self.guess is None:
            self.message = "Guess a number from 1 to 100"

        elif self.guess == self.secret_number:
            suffix = '' if self.num_guesses == 1 else 'es'
            self.message = "Congratulations! You guessed the number after %d guess%s." % (self.num_guesses, suffix)
            self.guess_button.configure(state=DISABLED)
            self.reset_button.configure(state=NORMAL)

        elif self.guess < self.secret_number:
            self.message = "Too low! Guess again!"
        else:
            self.message = "Too high! Guess again!"

        self.label_text.set(self.message)

    def reset(self):
        self.entry.delete(0, END)
        self.secret_number = random.randint(1, 100)
        self.guess = 0
        self.num_guesses = 0

        self.message = "Guess a number from 1 to 100"
        self.label_text.set(self.message)

        self.guess_button.configure(state=NORMAL)
        self.reset_button.configure(state=DISABLED)

root = Tk()
my_gui = GuessingGame(root)
root.mainloop()
"""
