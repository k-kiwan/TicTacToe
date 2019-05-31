""" EPR1 - Übungsblatt 9 - Tic Tac Toe
A GUI implementation of Tic Tac Toe using Tkinter.
"""

import tkinter as tk
from tkinter import ttk
from functools import partial

#_____________________________________________________________________________

class TicTacToeWelcome:
    """ Class for the Tic Tac Toe welcome screen.
    Shows a greeting, short instruction and enables the user to
    enter the player's names.
    """

    def __init__(self, parent):

        self.parent = parent
        self.window_style = ttk.Style()
        self.window_style.configure('My.TFrame')
        self.window = ttk.Frame(self.parent, 
                                style='My.TFrame', 
                                padding=(20, 20, 20, 20))

        # define labels
        self.label_title = tk.Label(self.window, 
                                    text="Welcome to Tic Tac Toe", 
                                    fg="#702082", 
                                    font=("arial", 18, "bold"))
        
        self.label_info = tk.Label(self.window, 
                                   text="This is a game of\n" +
                                        "Tic Tac Toe for two players.\n\n" +
                                        "Your goal: get 3 boxes of your\n" +
                                        "color in a row - \n" + 
                                        "either horizontally,\n" +
                                        "vertically or diagonally!\n\n" +
                                        "But first, enter the player's names:", 
                                   fg="#000000", 
                                   font=("arial", 12, "bold"))
        
        self.label_player_1 = tk.Label(self.window, 
                                       text="Player 1: ", 
                                       fg="#C110A0", 
                                       font=("arial", 12))

        self.label_player_2 = tk.Label(self.window, 
                                       text="Player 2: ", 
                                       fg="#00c889", 
                                       font=("arial", 12))

        # define text boxes
        self.enter_players = []
        for i in range(2):
            enter_player = tk.Entry(self.window)
            self.enter_players.append(enter_player)

        
        # define buttons
        self.start_button = ttk.Button(self.window, 
                                 text="Start Game!", 
                                 command=self.start_game)
  
        # place elements in the grid
        self.window.grid(column=0, row=0, sticky="nsew")
        self.label_title.grid(column=0,
                              row=0, 
                              columnspan=3, 
                              sticky="n", 
                              pady=10)
        self.label_info.grid(column=0, 
                             row=1, 
                             columnspan=3, 
                             sticky="n",
                             pady=10)
        self.label_player_1.grid(column=0, row=2, pady=10)
        self.label_player_2.grid(column=0, row=3, pady=10) 
        self.enter_players[0].grid(column=1, row=2, columnspan=2, pady=5)
        self.enter_players[1].grid(column=1, row=3, columnspan=2, pady=5)
        self.start_button.grid(column=2, row=9, pady=10)

    def get_name_players(self):
        """ Returns the name of player 1, that was entered
        into the text box.
        """
        self.name_players = []
        for i in range(2):
            name_player = self.enter_players[i].get()
            self.name_players.append(name_player)
        return self.name_players    
    
    def start_game(self):
        """ Closes the Welcome window and opens the main window.
        Saves the player names in the respective variables.
        """
        self.name_players = self.get_name_players()
        self.parent.destroy()
    
        
class TicTacToeMain:
    """ Main screen of the Tic Tac Toe game. 
    Holds the round and the winner counters as well as the
    game board and the buttons to restart, quit or next round.
    """

    colors = ["#C110A0", "#00c889"]

    def __init__(self, parent, name_players):
        
        self.game = TicTacToeGame()
        self.name_players = name_players
        self.status_label = self.set_status_text()
        self.label_round_text = self.set_label_round_text()
        self.winner_count = [0, 0]
        self.player_1_label_text = self.set_player_1_label_text()
        self.player_2_label_text = self.set_player_2_label_text()

        self.parent = parent
        self.window_style = ttk.Style()
        self.window_style.configure('My.TFrame')
        self.window = ttk.Frame(self.parent, 
                                style='My.TFrame', 
                                padding=(20, 20, 20, 20))

        self.board = ttk.Frame(self.window, 
                               borderwidth=1, 
                               relief="sunken")
        
        # define labels
        self.label_title = tk.Label(self.window, 
                                    text="Let's Play Tic Tac Toe", 
                                    fg="#702082", 
                                    font=("arial", 18, "bold"))

        self.label_round = tk.Label(self.window, 
                                    text=self.label_round_text, 
                                    font=("arial", 12, "bold"))

        self.label_player_1 = tk.Label(self.window, 
                                       text=self.name_players[0] + ": " 
                                            + str(self.winner_count[0]), 
                                       fg="#ffffff",
                                       bg=self.colors[0],
                                       font=("arial", 12, "bold"))

        self.label_player_2 = tk.Label(self.window, 
                                       text=self.name_players[1] + ": " 
                                            + str(self.winner_count[1]), 
                                       fg="#ffffff",
                                       bg=self.colors[1], 
                                       font=("arial", 12, "bold"))

        self.status = tk.Label(self.window,
                               text=self.status_label,
                               font=("arial", 12, "bold"))

        # define buttons
        self.restart = ttk.Button(self.window, 
                                 text="Restart Game", 
                                 command=self.restart_game)

        self.quit = ttk.Button(self.window, 
                               text="Quit", 
                               command=self.quit_game)

        self.new_round = ttk.Button(self.window, 
                               text="Next Round", 
                               command=self.start_new_round)

        self.board_buttons = []
        for i in range(3*3):
            board_button = tk.Button(self.board)
            board_button.grid(column=i%3, row=int(i/3), sticky="nsew")
            board_button["bg"] = "#ffffff"
            board_button["highlightbackground"] = "#ffffff"
            board_button["height"] = 3
            board_button["width"] = 3*2
            board_button["command"] = partial(self.click_play_button, i)
            self.board_buttons.append(board_button)

        
        # place elements 
        self.window.grid(column=0, row=0, 
                         sticky="nsew") 
        self.board.grid(column=0, row=4, 
                        columnspan=3, rowspan=3, 
                        sticky="nsew")
        self.label_title.grid(column=0, row=0, 
                              columnspan=3, 
                              sticky="n", 
                              pady=10)
        self.label_round.grid(column=0, row=1, 
                              columnspan=3, 
                              sticky="n") 
        self.label_player_1.grid(column=0, row=2,
                                 pady=10)
        self.label_player_2.grid(column=2, row=2, 
                                 pady=10) 
        self.status.grid(column=0, row=3, 
                         columnspan=3, pady=10)
        self.restart.grid(column=0, row=9)
        self.quit.grid(column=1, row=9)
        self.new_round.grid(column=2, row=9)

        # resizing configs
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        for x in range(0,3):
            self.window.columnconfigure(x, weight=1)
        for x in range(0,8):
            self.window.rowconfigure(x, weight=1)
        for x in range(0,3):
            self.board.columnconfigure(x, weight=1)
        for x in range(0,3):
            self.board.rowconfigure(x, weight=1)
    

   
    def quit_game(self):
        """ Quits the game by closing the window.
        """
        self.parent.destroy()
    
    def restart_game(self):
        """ Restarts the game by closing the current window
        and opening the Welcome window.
        """
        TicTacToeGame.round_count = 1
        self.parent.destroy()
        main()
    
    def click_play_button(self, board_index):
        """ For the buttons of the grid that make up the game.
        Color changes accoriding to player's turn to red (pink) or green.
        After clicking a button, it will be disabled.
        """
        if self.board_buttons[board_index]["state"] == "normal":
            self.board_buttons[board_index]["bg"] \
                = self.colors[self.game.player_turn]
            self.board_buttons[board_index]["state"] = "disable"
            self.game.player_move(board_index, self.game.symbols)
            self.status["text"] = self.set_status_text()
            #print(self.winner_count)
            if self.game.winning_pattern():
                for i in range(3*3):
                    self.board_buttons[i]["state"] = "disable"

    def get_winner(self):
        """ Determines the winner's name.
        """
        if self.game.winning_pattern():
            if self.game.player_turn == 0:
                self.winner_name = self.name_players[1]
                self.winner_count[1] += 1
            else:
                self.winner_name = self.name_players[0]
                self.winner_count[0] += 1
            return self.winner_name
    
    def start_new_round(self):
        """ Starts a new round of the game by calling a new instance
        and resetting all the colours and states of the boxes.
        """
        self.game = TicTacToeGame()
        TicTacToeGame.round_count += 1
        self.label_round["text"] = self.set_label_round_text()
        self.label_player_1["text"] = self.set_player_1_label_text()
        self.label_player_2["text"] = self.set_player_2_label_text()
        #print(self.game.round_count)
        for i in range(3*3):
            self.board_buttons[i]["state"] = "normal"
            self.board_buttons[i]["bg"] = "#ffffff"

    
    def set_status_text(self):
        """ Dynamically changes the text on the screen to inform the user
        about who's turn it is or if someone won the game
        """
        if self.game.winning_pattern():
            self.status_label = self.get_winner() \
                                + " has won this round!"
        else:
            self.status_label = self.name_players[self.game.player_turn] \
                                + ", it's your turn!"
        return self.status_label
    
    def set_label_round_text(self):
        """ Dynamically changes the label_round with the round counter.
        """
        return "Round: " + str(self.game.round_count)

    def set_player_1_label_text(self):
        """ Dynamically changes the text of player_1_label to 
        update the winner count for player 1.
        """
        return self.name_players[0] + ": " + str(self.winner_count[0])
    
    def set_player_2_label_text(self):
        """ Dynamically changes the text of player_2_label to 
        update the winner count for player 2.
        """
        return self.name_players[1] + ": " + str(self.winner_count[1])
    


class TicTacToeGame:
    """ Tic Tac Toe game logic.
    Defines player moves and winning patterns.
    """

    symbols = ["X", "O"]
    round_count = 1

    def __init__ (self):
        self.turn = 0
        self.symbols = ["X", "O"]
        self.player_turn = 0
        self.board = self.board_setup()
           
    def board_setup(self):
        """ Set's up a list of elements that hold the game moves.
        """
        self.board = ["" for i in range(3*3)]
        return self.board

    def player_move(self, board_index, symbols):
        """ Put's the players symbol into the selected index of the
        board_setup list.
        """
        self.turn += 1
        self.player_turn = self.get_player_turn(self.turn)
        self.board[board_index] = self.symbols[self.player_turn]
        # print(self.winning_pattern())
        # print(self.board)
        # print(self.player_turn)
    
    def get_player_turn(self, turn):
        """ Determines who's turn it is (player 1 or player 2)
        """
        self.player_turn = turn % 2
        return self.player_turn       

    def winning_pattern(self):
        """ Checks for all winning patterns.
        """
        if self.diagonal() or self.horizontal() or self.vertical():
            return True
        else:
            return False
    
    def diagonal(self):
        """ Checks diagonal winning patterns:
            X _ _   OR   _ _ X
            _ X _        _ X _
            _ _ X        X _ _
        """
        if self.board[0] == self.board[4] \
                         == self.board[8] \
                         and self.board[0] != "":
            return True
        elif self.board[2] == self.board[4] \
                           == self.board[6] \
                           and self.board[2] != "":
            return True

    def horizontal(self):
        """ Checks all horizontal winning patterns.
        """
        for i in [0, 3, 6]:
            if self.board[i] == self.board[i+1] \
                             == self.board[i+2] \
                             and self.board[i] != "":
                return True
    
    def vertical(self):
        """ Checks all vertical winning patterns.
        """
        for i in [0, 1, 2]:
            if self.board[i] == self.board[i+3] \
                             == self.board[i+6] \
                             and self.board[i] != "":
                return True


class MainApp:
    """ Regulates the switch between the welcome screen and
    the main screen.
    """

    def __init__(self):
        root = tk.Tk()
        root.geometry("323x484")
        welcome = TicTacToeWelcome(root)
        root.mainloop()
        players = (welcome.name_players[0], welcome.name_players[1])
        
        root = tk.Tk()
        root.geometry("323x484")
        window = TicTacToeMain(root, players)
        root.mainloop()
    

def main():
    MainApp()

 
if __name__ == '__main__':
    main()
