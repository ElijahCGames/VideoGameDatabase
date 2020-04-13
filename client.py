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
        self.geometry("800x600")

        # Sets options for the display
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Variables to be used througout
        self.username = StringVar()
        self.gid = 1

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
        valCur = self.cnx.cursor()
        userQ = "SELECT id FROM player WHERE name = %s"
        valCur.execute(userQ,username)
        self.usernameId = [item["id"] for item in valCur.fetchall()]
        valCur.close()

        valCur = self.cnx.cursor()
        userQ = f"SET @uname = '{username}'"
        valCur.execute(userQ)
        print("Inserted valuess")
        self.cnx.commit()
        valCur.close()

        self.username.set(username)

    def login(self,username,password):
        self.cnx = pymysql.connect(host='127.0.0.1', user=username, password=password,
                      db='gamePlay', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def add_to_database(self,querey):
        cur = self.cnx.cursor()
        cur.execute(querey)
        self.cnx.commit()
        cur.close()

    def get_from_database(self,querey):
        cur = self.cnx.cursor()
        cur.execute(querey)
        temp = cur.fetchall()
        cur.close()
        return temp

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
        subMenu.add_command(label="Add Location",command=self.add_location)
        subMenu.add_command(label="Add Platform",command=self.add_platform)

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
        page = AddReview(self.parent)

    def add_location(self):
        page = AddLoc(self.parent)

    def add_platform(self):
        page = AddPlatform(self.parent)



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
        self.startTitle = Label(self,text="VGDB",font=("Courier", 44))
        self.startTitle.pack(side="top",fill="x",pady=10)

        inputFrame = Frame(self)

        self.usernameLabel = Label(inputFrame,text="Player Name")
        self.sqlUsernameLabel = Label(inputFrame,text="Database Username")
        self.passwordLabel = Label(inputFrame,text="Database Password")

        self.usernameEntry = Entry(inputFrame)
        self.sqlUsernameEntry = Entry(inputFrame)

        self.passwordEntry = Entry(inputFrame,show="*")
        self.submit = Button(self,text="Submit",command=self.submitUsername)

        self.usernameEntry.insert(END,"Elijah")
        self.sqlUsernameEntry.insert(END,"root")
        # Rendering elements (either with pack() or grid())
        inputFrame.pack()

        self.usernameLabel.grid(row=0,column=0)
        self.usernameEntry.grid(row=0,column=1)
        self.sqlUsernameLabel.grid(row=1,column=0)
        self.sqlUsernameEntry.grid(row=1,column=1)
        self.passwordLabel.grid(row=2,column=0)
        self.passwordEntry.grid(row=2,column=1)

        self.submit.pack()

    # Function that runs the main logic of the interface
    def submitUsername(self):
        print(self.usernameEntry.get())
        self.controller.login(self.sqlUsernameEntry.get(),self.passwordEntry.get())
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
        self.populateFrame()

    def populateFrame(self):
        gameCur = self.controller.cnx.cursor()
        gameQ = "SELECT * FROM game WHERE gameID = %s"
        gameCur.execute(gameQ, self.controller.gid)
        game = gameCur.fetchone()
        gameLabel = Label(self,text="Title")
        gameName = Label(self, text=game["title"])
        descriptionLabel = Label(self,text="Description")
        description = Label(self,text=game["description"])


        devID = game["developerID"]
        pubID = game["publisherID"]
        gameplayID = game["gameplayGenre"]
        aestheticID = game["aestheticGenre"]
        


        ageRatingLabel = Label(self,text="Age Rating")
        ageRating = Label(self,text=game["ageRating"])
        localPlayerLabel = Label(self,text="Max Local Players")
        localPlayer = Label(self,text=game["localPlayer"])
        onlinePlayerLabel = Label(self,text="Max online players")
        onlinePlayer = Label(self,text=game["onlinePlayer"])
        hasMultiplayerLabel = Label(self,text="Has Multiplayer")
        hasMultiplayer = Label(self,text=game["has_multiplayer"])
        hasCampaignLabel = Label(self,text="Has Campaign")
        hasCampaign = Label(self,text=game["has_campaign"])
        completionTimeLabel = Label(self,text="Completion Time")
        completionTime = Label(self,text=game["completionTime"])
        gameCur.close()

        devCur = self.controller.cnx.cursor()
        devQ = "SELECT name FROM developer WHERE developerID = %s"
        devCur.execute(devQ, devID)
        dev = devCur.fetchone()
        developerLabel = Label(self,text="Developer")
        developer = Label(self,text=dev["name"])
        devCur.close()

        pubCur = self.controller.cnx.cursor()
        pubQ = "SELECT name FROM publisher WHERE publisherID = %s"
        pubCur.execute(pubQ, pubID)
        pub = pubCur.fetchone()
        publisherLabel = Label(self,text="Publisher")
        publisher = Label(self,text=pub["name"])
        pubCur.close


        gameplayCur = self.controller.cnx.cursor()
        gameplayQ = "SELECT gGenreTitle FROM gameplayGenre WHERE gGenreID = %s"
        gameplayCur.execute(gameplayQ, gameplayID)
        gameplay = gameplayCur.fetchone()
        gameplayLabel = Label(self,text="Gameplay Genre")
        gameplayText = Label(self,text=gameplay["gGenreTitle"])
        gameplayCur.close()

        aestheticCur = self.controller.cnx.cursor()
        aestheticQ = "SELECT aGenreTitle FROM aestheticGenre WHERE aGenreID = %s"
        aestheticCur.execute(aestheticQ, aestheticID)
        aesthetic = aestheticCur.fetchone()
        aestheticLabel = Label(self,text="Aesthetic Genre")
        aestheticText = Label(self,text=aesthetic["aGenreTitle"])
        aestheticCur.close()

        backButton = Button(self,text="Back",command=lambda: self.controller.show_frame("GameCollection"))

        gameLabel.grid(row=0,column=0)
        gameName.grid(row=0,column=1)
        ageRatingLabel.grid(row=1,column=0)
        ageRating.grid(row=1,column=1)
        descriptionLabel.grid(row=2,column=0)
        description.grid(row=2,column=1)
        developerLabel.grid(row=3,column=0)
        developer.grid(row=3,column=1)
        publisherLabel.grid(row=4,column=0)
        publisher.grid(row=4,column=1)
        gameplayLabel.grid(row=5,column=0)
        gameplayText.grid(row=5,column=1)
        aestheticLabel.grid(row=6,column=0)
        aestheticText.grid(row=6,column=1)
        localPlayerLabel.grid(row=7,column=0)
        localPlayer.grid(row=7,column=1)
        onlinePlayerLabel.grid(row=8,column=0)
        onlinePlayer.grid(row=8,column=1)
        hasMultiplayerLabel.grid(row=9,column=0)
        hasMultiplayer.grid(row=9,column=1)
        hasCampaignLabel.grid(row=10,column=0)
        hasCampaign.grid(row=10,column=1)
        backButton.grid(row=11,column=0)
        
        
        
        
        

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
        self.populateFrame()

    def populateFrame(self):
        self.add = Label(self,text="Add Game to Database",font=("Courier", 20))

        self.rightSide = Frame(self)
        self.title_desc = Frame(self.rightSide)
        self.littleThings = Frame(self.rightSide)
        self.overList = Frame(self)
        self.lists = Frame(self.overList)

        self.gameName = Entry(self.title_desc)

        self.gameDesc = Text(self.title_desc,height=5,width=20)

        self.age = Entry(self.littleThings)
        self.multi = Entry(self.littleThings)
        self.camp = Entry(self.littleThings)
        self.local = Entry(self.littleThings)
        self.online = Entry(self.littleThings)

        self.checkVar = BooleanVar()
        self.add_to = Checkbutton(self.littleThings,text="Add to my\nCollection",variable=self.checkVar)

        self.listOfBoxes = [Frame(self.lists) for i in range(0,4)]

        self.devL = Label(self.listOfBoxes[0],text="Developer")
        self.devs = Listbox(self.listOfBoxes[0],exportselection=0)
        self.addDev = Button(self.listOfBoxes[0],text="Add Developer",command=self.openDevBox)

        self.pubL = Label(self.listOfBoxes[2],text="Publisher")
        self.pubs = Listbox(self.listOfBoxes[2],exportselection=0)
        self.addPub = Button(self.listOfBoxes[2],text="Add Publisher",command=self.openPubBox)

        self.aGenL = Label(self.listOfBoxes[1],text="Aesthetic Genre")
        self.aGen = Listbox(self.listOfBoxes[1],exportselection=0)

        self.gGenL = Label(self.listOfBoxes[3],text="Gameplay Genre")
        self.gGen = Listbox(self.listOfBoxes[3],exportselection=0)

        self.submitButton = Button(self.overList,text="Submit",command = self.submit_to_database)

        #INSERTING
        self.gameName.insert(END,"Game Title")

        devCur = self.controller.cnx.cursor()
        devQ = "SELECT name FROM developer"
        devCur.execute(devQ)
        for name in [item["name"] for item in devCur.fetchall()]:
            self.devs.insert(END,name)
        devCur.close()

        pubCur = self.controller.cnx.cursor()
        pubQ = "SELECT name FROM publisher"
        pubCur.execute(pubQ)
        for name in [item["name"] for item in pubCur.fetchall()]:
            self.pubs.insert(END,name)
        pubCur.close()

        gCur = self.controller.cnx.cursor()
        gQ = "SELECT gGenreTitle FROM gameplayGenre"
        gCur.execute(gQ)
        for name in [item["gGenreTitle"] for item in gCur.fetchall()]:
            self.gGen.insert(END,name)
        gCur.close()

        aCur = self.controller.cnx.cursor()
        aQ = "SELECT aGenreTitle FROM aestheticGenre"
        aCur.execute(aQ)
        for name in [item["aGenreTitle"] for item in aCur.fetchall()]:
            self.aGen.insert(END,name)
        aCur.close()

        self.age.insert(END,"Age Rating")
        self.camp.insert(END,"Has Campaign")
        self.multi.insert(END,"Has Multiplayer")
        self.local.insert(END,"#Local Players")
        self.online.insert(END,"#Online Players")

        #PACKING AND GRIDING 
        self.gameName.pack()
        self.gameDesc.pack()

        self.age.grid(row=0,column=0)
        self.multi.grid(row=1,column=0)
        self.camp.grid(row=1,column=1)
        self.local.grid(row=2,column=0)
        self.online.grid(row=2,column=1)
        self.add_to.grid(row=0,column=1)

        self.devL.pack()
        self.devs.pack()
        self.addDev.pack()
        self.pubL.pack()
        self.pubs.pack()
        self.addPub.pack()
        self.aGenL.pack()
        self.aGen.pack()
        self.gGenL.pack()
        self.gGen.pack()
        for i in range(len(self.listOfBoxes)):
            self.listOfBoxes[i].grid(row=i%2,column=i//2)

        self.lists.pack()
        self.submitButton.pack()

        self.add.pack(side = TOP)
        self.rightSide.pack(side=LEFT)
        self.title_desc.pack()
        self.littleThings.pack()
        self.overList.pack(side = RIGHT)


    def submit_to_database(self):
        # Formatting apostrophes with double apostrophes to appease MySQL
        gameText = self.gameName.get()
        adjustedGameText = gameText.replace("'", "''")
        descText = self.gameDesc.get('1.0',END)
        adjustedDescText = descText.replace("'", "''")
        
        bigQ = f"CALL add_game_to_database('{adjustedGameText}','{adjustedDescText}',{self.devs.curselection()[0] + 1},{self.pubs.curselection()[0] + 1},'{self.age.get()}',{self.gGen.curselection()[0] + 1},{self.aGen.curselection()[0] + 1},{self.local.get()},{self.online.get()},'{self.multi.get()}','{self.camp.get()}',{self.checkVar.get()})"
        self.controller.add_to_database(bigQ)

        print("Adding")
        self.controller.repop(GameCollection)

        page = ChoosePlatforms(self.controller,self.controller.get_from_database("SELECT MAX(gameID) as gi FROM game")[0]["gi"])


    def openDevBox(self):
        page = AddDev(self.controller)

    def openPubBox(self):
        page = AddPub(self.controller)


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
        gameListCur = self.controller.cnx.cursor()
        gameListQ = "CALL get_users_games(%s)"
        print(self.controller.username.get())
        gameListCur.execute(gameListQ,self.controller.username.get())
        self.controller.game_array = [(item['gameID'],item['title'],item['name'],item['pub.name']) for item in gameListCur.fetchall()]

        for gId,name,dev,pub in self.controller.game_array:
            item = GameListing(self,gId,name,dev,pub)
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
    def __init__(self,controller):
        Toplevel.__init__(self)
        self.controller = controller;

        self.gameLabel = Label(self,text="Game")
        self.gameEntry = Entry(self)
        self.reviewLabel = Label(self,text="Reviewer")
        self.reviewEntry = Entry(self)
        self.scoreLabel = Label(self,text="Score")
        self.score = Spinbox(self,from_=0,to=100)
        self.urlLabel = Label(self,text="URL")
        self.urlEntry = Entry(self)
        self.submit = Button(self,text="Submit",command=self.addgame)

        self.gameLabel.grid(row=0,column=0)
        self.gameEntry.grid(row=0,column=1)
        self.reviewLabel.grid(row=1,column=0)
        self.reviewEntry.grid(row=1,column=1)
        self.scoreLabel.grid(row=2,column=0)
        self.score.grid(row=2,column=1)
        self.urlLabel.grid(row=3,column=0)
        self.urlEntry.grid(row=3,column=1)
        self.submit.grid(row=4,column=0)

    def addgame(self):
        revCursor = self.controller.cnx.cursor()
        revQ = f"CALL add_review('{self.gameEntry.get()}','{self.reviewEntry.get()}',{self.score.get()},'{self.urlEntry.get()}')"
        revCursor.execute(revQ)
        self.controller.cnx.commit()
        revCursor.close()
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
        self.controller.username.set(self.usernameEntry.get())
        userUpdateCur = self.controller.cnx.cursor()
        updateQ = f"UPDATE player SET name='{self.usernameEntry.get()}' WHERE id ={self.controller.usernameId}"
        userUpdateCur.execute(updateQ)
        self.controller.cnx.commit()
        userUpdateCur.close()

        self.destroy()

class ChoosePlatforms(Toplevel):
    def __init__(self,controller,gameID):
        Toplevel.__init__(self)

        self.controller = controller;
        self.gId = gameID

        self.gameTitle = self.controller.get_from_database(f"SELECT title FROM game WHERE gameID = {self.gId}")[0]["title"]

        self.topLabel = Label(self,text="Choose what platforms " + self.gameTitle + " is on.")

        self.platList = Listbox(self,exportselection=0,selectmode = MULTIPLE)
        self.save = Button(self,text="Submit",command=self.set_platforms)

        for name in [item['name'] for item in self.controller.get_from_database(f"SELECT name FROM platform")]:
            self.platList.insert(END,name)

        self.topLabel.pack()
        self.platList.pack()
        self.save.pack()

    def set_platforms(self):
        itemTup = self.platList.curselection()
        for item in itemTup:
            self.controller.add_to_database(f"INSERT INTO platform_game VALUES ({item + 1},{self.gId})")
        self.destroy()

class AddDev(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller

        self.devEntry = Entry(self)
        self.devEntry.insert(END,"Developer Name")
        self.locationBox = Listbox(self,exportselection=0)

        locCur = self.controller.cnx.cursor()
        locQ = "SELECT city,`state/province` FROM location"
        locCur.execute(locQ)
        for city,state in [(item["city"],item["state/province"]) for item in locCur.fetchall()]:
            self.locationBox.insert(END,city + ", " + state)
        locCur.close()

        self.save = Button(self,text="Save",command=self.add_dev)

        self.devEntry.pack()
        self.locationBox.pack()
        self.save.pack()


    def add_dev(self):
        devQ = f"INSERT INTO developer (name,locationIndex) VALUES ('{self.devEntry.get()}',{self.locationBox.curselection()[0] + 1})"
        self.controller.add_to_database(devQ)
        self.controller.repop(AddGameToDatabase)
        self.destroy()

class AddPub(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller

        self.pubEntry = Entry(self)
        self.pubEntry.insert(END,"Publisher Name")
        self.locationBox = Listbox(self,exportselection=0)

        locCur = self.controller.cnx.cursor()
        locQ = "SELECT city, `state/province` FROM location"
        locCur.execute(locQ)
        for city,state in [(item["city"],item["state/province"]) for item in locCur.fetchall()]:
            self.locationBox.insert(END,city + ", " + state)
        locCur.close()

        self.save = Button(self,text="Save",command=self.add_pub)

        self.pubEntry.pack()
        self.locationBox.pack()
        self.save.pack()

    def add_pub(self):
        pubQ = f"INSERT INTO publisher (name,locationIndex) VALUES ('{self.pubEntry.get()}',{self.locationBox.curselection()[0] + 1})"
        self.controller.add_to_database(pubQ)
        self.controller.repop(AddGameToDatabase)
        self.destroy()

class AddLoc(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller

        self.city = Entry(self)
        self.state = Entry(self)
        self.country = Entry(self)
        self.city.insert(END,"City")
        self.state.insert(END,"State/Province")
        self.country.insert(END,"Country")
        self.save = Button(self,text="Submit",command=self.add_loc)

        self.city.pack()
        self.state.pack()
        self.country.pack()
        self.save.pack()

    def add_loc(self):
        locQ = f"INSERT INTO location (city,`state/province`,country) VALUES ('{self.city.get()}','{self.state.get()}','{self.country.get()}')"
        self.controller.add_to_database(locQ)
        self.destroy()

class AddPlatform(Toplevel):
    def __init__(self,controller):
        Toplevel.__init__(self)

        self.controller = controller

        self.platform = Entry(self)
        self.platform.insert(END,"Platform Name")
        self.submit = Button(self,text="Submit",command=self.add_plat)
        self.platform.pack()
        self.submit.pack()

    def add_plat(self):
        platQ = f"INSERT INTO platform (name) VALUES ('{self.platform.get()}')"
        self.controller.add_to_database(platQ)
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
    def __init__(self,parent,gid,name,dev,pub):
        Frame.__init__(self,parent,highlightbackground="black",highlightthickness=1,width=300)

        self.parent = parent
        self.gid = gid
        self.infoButton = Button(self, text="More info",command=self.showInfo)
        self.nameLab = Label(self,text=name)
        self.devLab = Label(self,text="Developer: " + dev)
        self.pubLab = Label(self,text="Publisher: " + pub)

        self.infoButton.grid(row=0,column=0)
        self.nameLab.grid(row=0,column=1)
        self.devLab.grid(row=0,column=2)
        self.pubLab.grid(row=1,column=2)

    def showInfo(self):
        #Show info for this game listing
        self.parent.controller.gid = self.gid
        self.parent.controller.repop(GamePage)
        
        

# Sets app, and runs the loop 

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
