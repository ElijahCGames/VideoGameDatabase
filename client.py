"""
CLINET CODE FOR CS3200 Final Project

Video Game Database

Tasks for Application:
 
Input a users name 
(If not, they can sign up with one (adds name to database))

Adding games from a user's collection
Removing games from a user's collection


Recommending a game from collection or database based on parameters

Adding a review
(Game reviews are based on the average of all the reviews associated with a specfic game)

Adding a game to a database 
(Will be done on a different screen)


"""
from tkinter import *
import pymysql

# Main App Controller
class App(Tk):
    def __init__(self,*args, **kwargs):
        # Sets main options for app
        Tk.__init__(self,*args, **kwargs)
        self.title("Video Game Database")
        self.option_add('*tearOff', FALSE)
        self.geometry("800x400")

        # Sets options for the display
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Variables to be used througout
        self.username = StringVar()

        # Dictonary of frames
        self.frames = {}

        # Tuple of frames to be initilized once user inputs username
        self.mainPages = (
            GameCollection,UserPage,
            GamePage,Recomendation,
            AddGameToCollection,
            AddGameToDatabase)

        # Dummy Data for testing (will not be in final version)
        self.game_array = [("Mario","Nintendo"),("Celeste","Matt Makes Games"),("Last of Us","Naughty Dog"),("Pong","Atari")]

        # Setting up User Entry page
        f = UserEntry(parent=self.container,controller=self)
        self.frames["UserEntry"] = f 
        f.grid(row=0,column=0,sticky="nsew")

        # Setting up task bar
        menu = AppMenu(self)

        self.show_frame("UserEntry")

    def show_frame(self, page_name):
        """
        Displays frame

        Input:
        string page_name (Name of Class)
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def makeTheOtherFrames(self):
        """
        Adds the rest of the frames
        """
         for F in self.mainPages:
            page_name = F.__name__
            frame = F(parent=self.container,controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0,column=0,sticky="nsew")

    def repop(self,F):
        """
        Resets a frame to update display

        Input: 
        Class F
        """
        page_name = F.__name__
        frame = self.frames[page_name]
        for widget in frame.winfo_children():
            widget.destroy()
        frame.populateFrame()
        self.show_frame(page_name)

    def setUsername(self,username):
        """
        Set function for the username

        Input:
        string username
        """
        self.username.set(username)
        
# Top Menu
# This is where most of the functions are avaliable to be selected
# The long list of one line functions handeles all that

class AppMenu(Menu):
    def __init__(self,parent):
        Menu.__init__(self, parent)
        self.parent = parent

        # First Menu Item
        appmenu = Menu(self, name='apple')
        self.add_cascade(menu=appmenu)

        appmenu.add_command(label='About My Application',command= lambda: AboutMyApplication())
        appmenu.add_separator()
        parent['menu'] = self

        # Other Menu Items
        menu_user = Menu(self)
        menu_collection = Menu(self)
        menu_data = Menu(self)
        menu_window = Menu(self,name = "window")

        # Adds rest of menus
        self.add_cascade(menu=menu_user, label='User')
        self.add_cascade(menu=menu_collection, label='Collection')
        self.add_cascade(menu=menu_data, label='Data')
        self.add_cascade(menu=menu_window, label='Window')

        # Adds menu functions
        self.user_options(menu_user)
        self.collection_options(menu_collection)
        self.data_options(menu_data)

    def user_options(self, subMenu):
        subMenu.add_command(label="Change Username",command=self.change_username)
        subMenu.add_command(label="Goto User Page",command=self.goto_user_page)

    def collection_options(self,subMenu):
        subMenu.add_command(label="Add Game",command=self.add_game)
        subMenu.add_command(label="Remove Game",command=self.remove_game)
        subMenu.add_command(label="Reccomend Game",command=self.rec_game)

    def data_options(self,subMenu):
        subMenu.add_command(label="Add Game",command=self.add_data_game)
        subMenu.add_command(label="Add Review",command=self.add_review)

    # Functions that run when assocaited menu function is selected
    def change_username(self):
        page = ChangeUserName(self.parent)

    def goto_user_page(self):
        self.parent.show_frame("UserPage")

    def add_game(self):
        self.parent.show_frame("AddGameToCollection")

    def remove_game(self):
        page = RemoveGame(self.parent)

    def rec_game(self):
        self.parent.show_frame("Recomendation")

    def add_data_game(self):
        self.parent.show_frame("AddGameToDatabase")

    def add_review(self):
        page = AddReview()



# MAIN SCREENS

"""
User Entry
Interface Function: 
First screen of the program
Interaction: 
Allows entry of username (and password)

SQL Function:
Set's variable so all user actions occur within username's scope
Will get list of games owned by the user and use that to populate Game Collection

Note:
All Frames follow a similar format. 
Comments here apply to all frames
"""
class UserEntry(Frame):
    # Boilerplate initilization for our classes
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller

        # Setting all element of the UI
        self.startTitle = Label(self,text="VGDB")
        self.startTitle.pack(side="top",fill="x",pady=10)
        self.usernameEntry = Entry(self)
        self.passwordEntry = Entry(self,show="*")
        self.submit = Button(self,text="Submit",command=self.submitUsername)

        # Rendering elements (either with pack() or grid())
        self.usernameEntry.pack()
        self.passwordEntry.pack()
        self.submit.pack()

    # Function that runs the main logic of the interface
    def submitUsername(self):
        print(self.usernameEntry.get())
        self.controller.setUsername(self.usernameEntry.get())
        self.controller.makeTheOtherFrames()
        self.controller.show_frame("GameCollection")

"""
User Page
Interface Function:
Page to display information about the user
Interaction:
Can change some elements of the user's profile

SQL Function:
Get's the elements from the User record in the user tables and displays some.
"""
class UserPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.populateFrame()

    def populateFrame(self):
        self.userName = Label(self,textvariable=self.controller.username)
        self.backButton = Button(self,text="Back",command=lambda: self.controller.show_frame("GameCollection"))

        self.userName.pack()
        self.backButton.pack()

    def goToGameCollection(self):
        self.controller.show_frame("GameCollection")

"""
Game Page
Interface Function:
Shows infromation about a specfic game 
Interaction:
Can change some elements of the user's relationship to the game (playtime, has completed, add to collection, remove from collection)

SQL Function:
Get's the elements from the records in games and presents them.
Allows updates of the game records, and changes to the users game collection.
"""
class GamePage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

"""
Recomeendation
Interface Function:
Allows search of games database based on parameters

Interaction:
Can select from parameters and input different values, and will get a list of games 
back pertatining to the information

SQL Function:
Queries the games table using the information and returns a list of games

Note:
This could become rather complicated, focus should be on things like selecting platform and genre 
and not much else.

"""
class Recomendation(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

        nameEntry = Entry(self)
        backButton = Button(self,text="Back",command=lambda: controller.show_frame("GameCollection"))
        submitButton = Button(self,text="Submit",command=self.searchGame)
        backButton.pack()
        nameEntry.pack()
        submitButton.pack()

    def searchGame(self):
        self.controller.repop(GameCollection)

"""
Add Game to Collection:
Interface Function:
Allows for specfic game search and adding
Interaction:
User searches for a game, and will get the game back with the option of adding the game to their collection.

SQL Function:
Adds record to the user_game table with the new addition to the collection 

"""

class AddGameToCollection(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

        nameEntry = Entry(self)
        backButton = Button(self,text="Back",command=lambda: controller.show_frame("GameCollection"))
        submitButton = Button(self,text="Submit",command=self.searchGame)
        backButton.pack()
        nameEntry.pack()
        submitButton.pack()

    def searchGame(self):
        self.controller.repop(GameCollection)

"""
Add Game to Database
Interace Function:
Adds a compeltely new game to the database
Interaction:
Can enter, select, and set all the neccacary information for the game.

SQL Function:
Adds a new record in the games table, with all the applicable data
Additonally, if any information in releated tables (genre, developer, platform) is new, adds a record for that.
"""
class AddGameToDatabase(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

        self.gameNameEntry = Entry(self)
        self.devNameEntry = Entry(self)
        self.submitButton = Button(self,text="Submit",command=self.submit_to_database)

        self.gameNameEntry.pack()
        self.devNameEntry.pack()
        self.submitButton.pack()

    def submit_to_database(self):
        self.controller.game_array.append((self.gameNameEntry.get(),self.devNameEntry.get()))
        print("Adding")
        self.controller.repop(GameCollection)


"""
Game Collection
Interface Function:
Displays users personal collection of games
Interaction:
Can go to the pages for each game, or remove them from their collection

SQL Function:
Gets a list of the user's games and displays it.
Is able to remove a game from the list.
"""
class GameCollection(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller 

        self.populateFrame()

    def populateFrame(self):
        """
        Frames aren't rerendered automatically
        This function allows a frame to rerender with new data (in this case, a new user games list.)
        """
        topLabel = Frame(self)
        label = Label(topLabel,textvariable=self.controller.username)
        labelMore = Label(topLabel,text="'s Collection")
        label.grid(row=0,column=0)
        labelMore.grid(row=0,column=1)
        topLabel.grid(row=0,column=0,sticky="nsew",)
        r = 1
        for name,dev in self.controller.game_array:
            item = GameListing(self,name,dev)
            item.grid(row=r,column=0,sticky="nsew")
            r+=1

# POPUPS

"""
Add Review

Interface Function:
Adds a new review for a game
Interaction:
Fills in the game, reviewer, and review score for the game.

SQL Function:
Adds new record to the review table
"""
class AddReview(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.gameLabel = Label(self,text="Game")
        self.gameEntry = Entry(self)
        self.reviewLabel = Label(self,text="Reviewer")
        self.reviewEntry = Entry(self)
        self.scoreLabel = Label(self,text="Score")
        self.score = Spinbox(self,from_=0,to=100)
        self.submit = Button(self,text="Submit",command=self.addgame)

        self.gameLabel.grid(row=0,column=0)
        self.gameEntry.grid(row=0,column=1)
        self.reviewLabel.grid(row=1,column=0)
        self.reviewEntry.grid(row=1,column=1)
        self.scoreLabel.grid(row=2,column=0)
        self.score.grid(row=2,column=1)
        self.submit.grid(row=3,column=0)

    def addgame(self):
        self.destroy()
"""
Remove Game

Interface Function:
Menu level interface to remove a game from the user's collection

Interaction:
Can select from the user's list of games and will remove the ones (multiple?) that they choose.

SQL Function:
Deletes record from game_user table associated with the game.
"""
class RemoveGame(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller
        self.gamelist = Listbox(self,selectmode="BROWSE")
        counter = 1;
        for game,dev in self.controller.game_array:

            self.gamelist.insert(counter,game)
            counter+=1

        self.gamelist.pack()
        self.submitButton = Button(self,text="Submit",command=self.removegame)
        self.submitButton.pack()

    def removegame(self):
        gar = self.controller.game_array
        index = self.gamelist.curselection()[0]
        gar.pop(index)
        self.controller.repop(GameCollection)
        self.destroy()

"""
Change Username

Interface Function:
Allows User to change their username

Interaction:
Entry box for the new username (will show an error if username already exists)

SQL Function:
Updates username in the user table.
"""
class ChangeUserName(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller
        self.usernameEntry = Entry(self)
        self.submit = Button(self,text="Submit",command=self.changeUsername)

        self.usernameEntry.pack()
        self.submit.pack()

    def changeUsername(self):
        self.controller.setUsername(self.usernameEntry.get())
        self.destroy()

class AboutMyApplication(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.mainLabel = Label(self,text="Application for browing of the VGDB")
        self.subLabel = Label(self,text="Made for CS 3200: Database Design at Northeastern University")

        self.mainLabel.pack()
        self.subLabel.pack()

# SUBFRAMES 
# These are complex and abstract frames that are used in lists and other purposes 

"""
GameListing

A single listing on the Game Collection page.
"""
class GameListing(Frame):
    def __init__(self,parent,name,dev):
        Frame.__init__(self,parent,highlightbackground="black",highlightthickness=1,width=300)

        self.nameLab = Label(self,text=name)
        self.devLab = Label(self,text="Developer: " + dev)
        self.nameLab.grid(row=0,column=0)
        self.devLab.grid(row=0,column=1)

# Sets app, and runs the loop 
# DO NOT TOUCH
if __name__ == "__main__":
    root = App()
    root.mainloop()



# Reference programs
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
