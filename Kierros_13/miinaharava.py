"""
COMP.CS.100 Ohjelmointi 1
Malakias Kosonen
Tehtävä 13.10: Graafinen käyttöliittymä - Miinaharava
"""



from tkinter import *
from tkinter import ttk
from random import randint
import time

font = "Courier"


class Minesweeper:

    def __init__(self, window):
        """
        Initializes parameters and windows for the game.
        :param window: Main window.
        """

        # Player name for future use -> saving high scores
        self.__player_name = None

        # Initialize values for key elements.
        self.__mines = 0
        self.__flags = 0
        self.__correct_flags = 0
        self.__tiles = {}
        self.__found_tiles = 0

        self.__clock = "00:00"
        self.__starttime = None
        self.__endtime = None
        self.__game_end = False
        self.__clock_running = False

        self.__gamepoints = None
        self.__pts_modifier = None
        self.__sessionpoints = {}

        # Tileboard dimensions
        self.__width = 0
        self.__height = 0

        # Main window
        self.window = window

        # Popup window for score saving, after winning or losing a game.
        self.__save_score_window = None

        # Frame for the tileboard, where actual playing happens.
        self.frame = Frame(self.window)

        # Frame for game information, on top of tileboard.
        self.__toprow = Frame(self.window)

        # Configure rows and columns,
        # so they can be resized manually and stay balanced.
        #
        # Manual window resizing needs polishing, but the foundation is there.
        Grid.rowconfigure(self.__toprow, 0, weight=1)
        Grid.columnconfigure(self.__toprow, 1, weight=1)

        Grid.rowconfigure(self.window, 1, weight=1)
        Grid.columnconfigure(self.window, 0, weight=1)

        # Label for points earned for winning or losing.
        self.__points_label = Label(self.window)

        # Button to start a game.
        # Disabled before picking a difficulty.
        self.start_button = Button(self.window, text="Start!",
                                   command=self.start, state=DISABLED,
                                   font=font)
        self.start_button.grid(row=3, pady=10)

        # Game difficulties.
        difficulties = ["Novice", "Intermediate", "Expert"]
        self.difficulty = ttk.Combobox(self.window, values=difficulties,
                                       state="readonly", font=font)
        self.difficulty.set("Pick a difficulty")
        self.difficulty.grid(row=4, pady=5, padx=30)

        # Button that chooses difficulty.
        self.combo_button = Button(self.window, text="Submit",
                                   command=self.getDifficulty, font=font)
        self.combo_button.grid(row=5, pady=5)

        # Quit button, exits the program.
        self.quit_button = Button(self.window, text="Quit",
                                  command=self.quit, font=font)
        self.quit_button.grid(row=8, pady=5)

        # Label for any possible messages.
        self.__message = Label(self.window)

        # Button for displaying high scores.
        # Comes up after the first played game.
        self.__score_button = Button(self.window, text="Session High Scores",
                                     command=self.scores, font=font)

        # Labels that indicate key values during a game. (Mines, Time, Flags)
        self.__mineslabel = Label(self.__toprow,
                                  text=f"Mines: {self.__mines}", font=font)

        self.__flags_label = Label(self.__toprow,
                                   text=f"Flags: {self.__flags}", font=font)

        self.__timer = Label(self.__toprow, text="", font=font)

    def save_score(self):
        """
        This window opens after losing or winning a game.
        Player can enter a name and save their score.
        Or it can be dismissed by pressing "Cancel".
        """

        # Initialize the window.
        self.__save_score_window = Toplevel()

        # Message.
        window_message = Label(self.__save_score_window, text="Save score as:", font=font)
        window_message.grid(row=0, columnspan=2, sticky=NSEW, pady=10)

        # Entry box for a given name.
        self.__player_name = Entry(self.__save_score_window)
        self.__player_name.grid(row=1, columnspan=2, padx=10)

        # Button that saves the name.
        save_button = Button(self.__save_score_window, text="Save", command=self.add_score, font=font)
        save_button.grid(row=2, column=0, sticky=NSEW, pady=10, padx=5)

        # Button that cancels saving.
        cancel_button = Button(self.__save_score_window, text="Cancel", command=self.__save_score_window.destroy, font=font)
        cancel_button.grid(row=2, column=1, sticky=NSEW, pady=10, padx=5)

    def add_score(self):
        """
        Saves a name with points to the database for later viewing.
        """

        # Entered name.
        player_name = self.__player_name.get()

        # Name cannot be empty.
        if player_name != "":

            # If entered name is not in database, enter it with earned points.
            if player_name not in self.__sessionpoints:
                self.__sessionpoints[player_name] = self.__gamepoints

        # Close the window after saving.
        self.__save_score_window.destroy()

    def scores(self):
        """
        Separate window for displaying session high scores. (Top 5)

        Possible future updates: Add difficulty label
        """

        # Initialize window.
        highscorewindow = Toplevel()
        highscorewindow.title("Session High Scores")
        highscorelabel = Label(highscorewindow, text="Session High Scores", font=font)
        highscorelabel.grid(row=0, columnspan=4, pady=10, padx=20)

        # Ranking.
        number_title = Label(highscorewindow, text="#", font=font)
        number_title.grid(row=1, column=0, padx=10, pady=10)

        # Player name.
        name_title = Label(highscorewindow, text="Player", font=font)
        name_title.grid(row=1, column=1, padx=10, pady=10)

        # Points.
        points_title = Label(highscorewindow, text="Points", font=font)
        points_title.grid(row=1, column=2, padx=10, pady=10)

        # Sort points.
        sorted_points = sorted(self.__sessionpoints.values(), reverse=True)
        print(sorted_points)
        sorted_sessionpoints = {}

        for x in sorted_points:
            for y in self.__sessionpoints.keys():
                if self.__sessionpoints[y] == x:
                    sorted_sessionpoints[y] = self.__sessionpoints[y]

        # Displays top 5 points.
        if len(self.__sessionpoints) > 5:
            maximum = 5
        else:
            maximum = len(self.__sessionpoints) + 3

        # Loop that creates the list.
        for row in range(3, maximum):

            # Rankings.
            placement = row - 2
            placements_label = Label(highscorewindow, text=f"{placement}.", font=font)
            placements_label.grid(row=row, column=0, pady=5, sticky=NSEW)

            # Player names.
            player_label = Label(highscorewindow, text=f"{list(sorted_sessionpoints)[row - 3]}", font=font)
            player_label.grid(row=row, column=1, pady=5, sticky=NSEW)

            # Points.
            name = list(sorted_sessionpoints)[row - 3]
            pts_label = Label(highscorewindow, text=f"{int(sorted_sessionpoints[name])}", font=font)
            pts_label.grid(row=row, column=2, pady=5, sticky=NSEW)

    def quit(self):
        """
        Function that quits the program.
        Has a goodbye message and a small delay.
        """
        self.__message.configure(text="Goodbye!", font=("Courier", 15))
        self.__message.grid(pady=10, row=2)
        self.__message.after(2000, lambda: self.window.destroy())

    def getDifficulty(self):
        """
        Gets the selected game difficulty.
        """
        self.start_button.configure(state=NORMAL)
        return self.difficulty.get()

    def updateTimer(self):
        """
        Timer that displays on the top of the window.
        Single game timer.
        Resets after a new game is started.
        Starts after a tile is clicked.
        """

        # If game has ended, stop the timer.
        if self.__game_end:
            return

        time = self.__clock

        (m, s) = time.split(":")

        # Increase seconds, update
        s = int(s) + 1
        m = int(m)
        if int(s) == 60:
            m = int(m) + 1
            s = 0

        # Prevents the game from running forever.
        if int(m) == 59:
            self.gameOver(False)
            return

        if s < 10:
            s = "0" + str(s)

        if m < 10:
            m = "0" + str(m)

        time = str(m) + ":" + str(s)
        self.__clock = time

        # Update timer.
        self.__timer.configure(text=time)
        self.__timer.after(1000, self.updateTimer)



    def start(self):
        """
        Creates the game of minesweeper based on selected difficulty.
        """

        # Clear the board and reset values.
        self.clear()

        # Difficulty values.
        if self.difficulty.get() == "Novice":
            self.__mines = 5
            self.__height = 6
            self.__width = 6
            self.__pts_modifier = 1

        elif self.difficulty.get() == "Intermediate":
            self.__mines = 13
            self.__height = 9
            self.__width = 9
            self.__pts_modifier = 4

        elif self.difficulty.get() == "Expert":
            self.__mines = 22
            self.__height = 9
            self.__width = 12
            self.__pts_modifier = 9

        # Difficulty must be selected to setup a game.
        else:
            return

        # Setup the game.
        self.setup()

        # Refresh game values.
        self.refresh()

        # Message that overlays the gameboard.
        self.__message.configure(text="Good luck!", font=(font, 15))
        self.__message.grid(pady=10, row=2)
        self.__message.after(2000, lambda: self.__message.grid_forget())

    def clear(self):
        """
        Clears the gameboard and values.
        """

        if len(self.__tiles) != 0:
            for x in range(0, self.__height):
                for y in range(0, self.__width):

                    self.__tiles[x][y]["button"].grid_forget()

                    self.__mineslabel.grid_forget()
                    self.__flags_label.grid_forget()
                    self.__timer.grid_forget()

    def setup(self):
        """
        Sets up the game.
        """

        # Introduce game information.
        self.__toprow.grid(row=0, column=0, sticky=NSEW)

        self.__mineslabel.grid(row=0, column=0, padx=20, pady=10, sticky=W)

        self.__flags_label.grid(row=0, column=2, padx=20, pady=10, sticky=E)

        self.__timer.grid(row=0, column=1, sticky=EW)

        self.frame.grid(row=2, column=0, sticky=N + S + E + W, padx=20,
                        pady=10)

        # Generate tiles.
        for x in range(0, self.__height):
            for y in range(0, self.__width):
                if y == 0:
                    self.__tiles[x] = {}

                tile_id = str(x) + "_" + str(y)

                # Tiles don't have bombs by default.
                armed = False

                # Initialize a certain tile.
                tile = {"id": tile_id, "armed": armed, "state": "default",
                        "location": {"x": x, "y": y},
                        "button": Button(self.frame, width=6, height=3, state=NORMAL, bg="snow"),
                        "mines": 0}

                # Place the tile.
                tile["button"].grid(row=x+1, column=y+1, sticky=N+S+E+W)

                Grid.rowconfigure(self.frame, x+1, weight=1)
                Grid.columnconfigure(self.frame, y+1, weight=1)

                self.__tiles[x][y] = tile

                # Left and right-click and their actions.
                tile["button"].bind("<Button-1>", lambda event, clicked_tile=self.__tiles[x][y]: self.LeftClick(clicked_tile))
                tile["button"].bind("<Button-3>", lambda event, clicked_tile=self.__tiles[x][y]: self.RightClick(clicked_tile))

        # Generate mines.
        self.generate_mines()

        # Update mine values based on bomb locations.
        for x in range(0, self.__height):
            for y in range(0, self.__width):
                nearby_mines = 0

                for neighbor in self.neighbors(x, y):
                    if neighbor["armed"]:

                        nearby_mines += 1

                self.__tiles[x][y]["mines"] = nearby_mines

    def neighbors(self, x, y):
        """
        Goes through tile neighbors around a tile in a 3x3 square.
        :param x: int, x location of the center square.
        :param y: int, y location of the center square
        """

        neighbors = []
        neighbor_coords = [{"x": x-1, "y": y-1},  # top left
                           {"x": x-1, "y": y},  # top
                           {"x": x-1, "y": y+1},  # top right
                           {"x": x, "y": y-1},  # center left
                           {"x": x, "y": y+1},  # center right
                           {"x": x+1, "y": y-1},  # bottom left
                           {"x": x+1, "y": y},  # bottom
                           {"x": x+1, "y": y+1}]  # bottom right

        for neighbor in neighbor_coords:
            try:
                neighbors.append(self.__tiles[neighbor["x"]][neighbor["y"]])

            # if center tile is near an edge, there are no tiles over the edge.
            except KeyError:
                pass

        return neighbors

    def generate_mines(self):
        """
        Generates mines, or more precisely updates mines.
        """

        mines = 0

        while True:
            x = randint(0, self.__height - 1)
            y = randint(0, self.__width - 1)

            if self.__tiles[x][y]["armed"]:
                continue

            self.__tiles[x][y]["armed"] = True
            self.__tiles[x][y]["mines"] = -1
            mines += 1

            if mines == self.__mines:
                break

    def refresh(self):
        """
        Refresh game values.
        """
        self.__flags = 0
        self.__correct_flags = 0
        self.__found_tiles = 0

        self.__mineslabel.configure(text=f"Mines: {self.__mines}")
        self.__timer.configure(text="00:00")
        self.__flags_label.configure(text=f"Flags: {self.__flags}")

        self.__points_label.grid_forget()

        self.__game_end = False

    def LeftClick(self, tile):
        """
        Actions that happen when the player clicks a tile with the left click.
        :param tile: tile, tile that is clicked.
        """

        if not self.__clock_running:
            self.__clock = "00:00"
            self.__clock_running = True
            self.updateTimer()

        if self.__starttime == None:
            self.__starttime = time.time()

        if tile["button"]["state"] == "disabled":
            return

        if tile["armed"]:
            self.gameOver(False)
            return

        if tile["mines"] == 0:
            tile["button"].configure(bg="grey", state=DISABLED)
            self.clearSurroundingTiles(tile)

        else:
            if tile["mines"] == 1:
                tile["button"].configure(bg="cyan", text=tile["mines"], state=DISABLED)
            elif tile["mines"] == 2:
                tile["button"].configure(bg="gold", text=tile["mines"], state=DISABLED)
            else:
                tile["button"].configure(bg="firebrick1", text=tile["mines"], state=DISABLED)

        if tile["state"] != "clicked":
            tile["state"] = "clicked"
            self.__found_tiles += 1

        if self.__found_tiles == (self.__height * self.__width - self.__mines):
            self.gameOver(True)

    def RightClick(self, tile):
        """
        Aactions that happen when a tile is clicked with the right click.
        :param tile: tile that is clicked.
        """

        if tile["button"]["state"] == "disabled":
            return

        if tile["state"] != "flagged":
            tile["state"] = "flagged"
            tile["button"].configure(text="!")
            self.__flags += 1
            self.__flags_label.configure(text=f"Flags: {self.__flags}")
            if tile["armed"]:
                self.__correct_flags += 1

        elif tile["state"] == "flagged":
            tile["state"] = "default"
            tile["button"].configure(text="")
            self.__flags -= 1
            self.__flags_label.configure(text=f"Flags: {self.__flags}")
            if tile["armed"]:
                self.__correct_flags -= 1

    def clearSurroundingTiles(self, tile):
        """
        Clears surrounding tiles.
        :param tile: tile that is the center.
        """

        tile_list = [tile]

        while len(tile_list) != 0:

            key = tile_list.pop(0)
            x = key["location"]["x"]
            y = key["location"]["y"]

            for neighbor in self.neighbors(x, y):
                self.clearTile(neighbor, tile_list)

    def clearTile(self, tile, tile_list):
        """
        Clears a single tile.
        """

        if tile["state"] != "default":
            return

        if tile["armed"]:
            return

        if tile["mines"] == 0:
            tile["button"].configure(bg="grey", state=DISABLED)
            tile_list.append(tile)
        else:
            if tile["mines"] == 1:
                tile["button"].configure(bg="cyan", text=tile["mines"], state=DISABLED)
            elif tile["mines"] == 2:
                tile["button"].configure(bg="gold", text=tile["mines"], state=DISABLED)
            elif tile["mines"] >= 3:
                tile["button"].configure(bg="firebrick1", text=tile["mines"], state=DISABLED)

        tile["state"] = "clicked"
        self.__found_tiles += 1

    def gameOver(self, win):

        self.__game_end = True

        self.save_score()

        self.__score_button.grid(row=7, pady=10)

        self.__points_label.configure(text=f"Points: {self.calculatepoints(win)}", font=font)
        self.__points_label.grid(row=1, column=0, pady=5)

        if self.__clock_running:
            self.__clock_running = False

        for x in range(0, self.__height):
            for y in range(0, self.__width):
                if self.__tiles[x][y]["armed"]:
                    self.__tiles[x][y]["button"].configure(text="x", bg="black", fg="snow")

        if not win:
            self.__message.configure(text="You lost. Play again?", font=font)
            self.__message.grid(pady=10, row=2)
            for x in range(0, self.__height):
                for y in range(0, self.__width):
                    self.__tiles[x][y]["button"].configure(state=DISABLED)

        if win:
            self.__message.configure(text="You won! Play again?", font=font)
            self.__message.grid(pady=10, row=2)

    def calculatepoints(self, win):
        """
        Calculates points after winning or losing a game.
        Could possibly use balancing.
        :param win: bool, lost or won the game
        :return: points eraned.
        """

        elapsedtime = 1

        if self.__endtime == None:
            self.__endtime = time.time()
            elapsedtime = self.__endtime - self.__starttime

        if elapsedtime == 0:
            return 0
        else:
            if win:
                self.__gamepoints = self.__pts_modifier * self.__mines / elapsedtime
                self.__gamepoints = self.__gamepoints * 10000
                return int(self.__gamepoints)

            if not win:
                # TODO: Add correct flags for compensation
                # Failing fast yields a greater score.
                self.__gamepoints = self.__pts_modifier * self.__mines / elapsedtime * self.__correct_flags
                if self.__gamepoints == 0:
                    self.__gamepoints = self.__pts_modifier * self.__mines / 10
                self.__gamepoints = self.__gamepoints * 100
                return int(self.__gamepoints)


def main():
    """
    Create the interface.
    :return:
    """
    window = Tk()

    window.title("Minesweeper")

    Minesweeper(window)

    window.mainloop()


if __name__ == "__main__":
    main()
