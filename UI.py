from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

PIT_O = Path("Gabata Images/Pit.png")
PIT_TURN_O = Path("Gabata Images/Pit_turn.png")
PIT_NOT_TURN_O = Path("Gabata Images/Pit_not_turn.png")
DEPOSIT_O = Path("Gabata Images/Deposit.png")
DEPOSIT_HOVER_O = Path("Gabata Images/Deposit_hover.png")
BAR_O = Path("Gabata Images/Bar.png")
PLAYER_O = Path("Gabata Images/Player.png")
MARBLE_O = Path("Gabata Images/Large Marble.png")


def image_preprocess(images: list):
    """
    Function processes images so that they are all the needed size for the app

    Inputs: images (list) -> Pathes to images

    Output: final_images (list) -> list of resized images
    """

    final_images = []
    for i in images:
        image = Image.open(i)
        if i != BAR_O and i != PLAYER_O and i != MARBLE_O:
            final_image = image.resize(
                (150, int(150 * (image.height / image.width))), Image.LANCZOS
            )
        elif i == BAR_O:
            final_image = image.resize(
                (1200, int(1200 * (image.height / image.width))), Image.LANCZOS
            )
        elif i == MARBLE_O:
            final_image = image.resize((80, 80), Image.LANCZOS)
        else:
            final_image = image.resize(
                (900, int(900 * (image.height / image.width))), Image.LANCZOS
            )
        final_images.append(final_image)
    return final_images


final_images = image_preprocess(
    [
        PIT_O,
        PIT_TURN_O,
        PIT_NOT_TURN_O,
        DEPOSIT_O,
        DEPOSIT_HOVER_O,
        BAR_O,
        PLAYER_O,
        MARBLE_O,
    ]
)


PIT, PIT_TURN, PIT_NOT_TURN, DEPOSIT, DEPOSIT_HOVER, BAR, PLAYER, MARBLE = final_images


class Bar:
    """
    Bar class is for the bar at the bottom where marbles in a pit can be viewed
    """

    def __init__(self, root) -> None:
        self.final_image = BAR
        self.marble_im = MARBLE
        self.image_tk = ImageTk.PhotoImage(self.final_image)
        self.marble_tk = ImageTk.PhotoImage(self.marble_im)
        self.canvas = Canvas(
            root, width=self.final_image.width, height=self.final_image.height
        )
        self.c_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.canvas.grid(row=4, column=0, columnspan=8)
        self.showing = False
        self.marbles = []

    def show_marbles(self, num_marbles: int):
        self.showing = True

        for marble in range(num_marbles):
            if marble < 12:
                element = self.canvas.create_image(
                    20 + (marble * 90), 20, anchor=NW, image=self.marble_tk
                )
                self.canvas.update_idletasks()
                self.marbles.append(element)

            else:
                element = self.canvas.create_text(
                    25 + (marble * 90),
                    37,
                    anchor=NW,
                    text="+ " + str(num_marbles - 12),
                    font=("Helvetica", 27, "bold"),
                )
                self.canvas.update_idletasks()
                self.marbles.append(element)
                break

    def erase(self):
        self.showing = False

        for widget in self.marbles:
            self.canvas.delete(widget)
        self.marbles.clear()
        """
        displays all the marbles in the bottom bar
        """


class Players:
    """
    Players class is for the player images that are used to indicate player side and turn
    """

    def __init__(self, root, player: int, board, player_name: str) -> None:
        self.image = PLAYER
        self.canvas = Canvas(root, width=self.image.width, height=self.image.height)

        self.player = player
        self.player_name = player_name
        if player == 1:
            row = 3
            self.text = self.canvas.create_text(
                self.image.width / 2,
                self.image.height / 2 - 20,
                text=player_name,
                anchor=CENTER,
                font=("Helvetica", 14, "bold"),
            )
            self.image_tk = ImageTk.PhotoImage(self.image)

        elif player == 2:
            row = 0
            self.text = self.canvas.create_text(
                self.image.width / 2,
                self.image.height / 2 + 20,
                text=player_name,
                anchor=CENTER,
                font=("Helvetica", 14, "bold"),
            )
            self.image_tk = ImageTk.PhotoImage(self.image.rotate(180))

        self.c_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.canvas.grid(row=row, column=1, columnspan=6)

        self.board = board
        self.update()

    def update(self):
        """
        Updates the color of the player text depending on whose turn it is in the game.
        This is called by the updater class object
        """
        if self.board.get_player() == self.player:
            self.canvas.itemconfig(self.text, fill="green")
        else:
            self.canvas.itemconfig(self.text, fill="red")

    def modify_text(self, new_name):
        self.canvas.itemconfig(self.text, text=new_name)
        self.canvas.update_idletasks()


class Updater:
    """
    Class for updating the values on the pits, deposit slots, and the color of the player text
    depending on the status of the game. An object of the Updater class is called whenever a
    valid move is made
    """

    def __init__(self, slots, players):
        self.slots = slots
        self.players = players

    def update_value(self):
        for slot in self.slots:
            slot.value = slot.board.score[slot.id]
            slot.canvas.itemconfig(slot.text, text=str(slot.value))

        for player in self.players:
            player.update()


class Pit:
    """
    Pit objects are the playable pits which the players make moves on. They are ovals with
    3 different states: stationary (when no interaction), invalid (when hovering over a pit
    which is not a valid move), and valid. Moves are made by left clicking on the valid pits.

    The important object variables are:
        id (int): which relates to the position of the pit on the board
        value (int): which is the score at the id position on the board
        updater (Updater): used to update the value
    """

    def __init__(
        self,
        root,
        location: tuple,
        value: int,
        id: int,
        board,
        updater: Updater,
        bar: Bar,
    ):
        self.root = root
        self.final_image = PIT
        self.image_tk = ImageTk.PhotoImage(self.final_image)
        self.canvas = Canvas(
            root, width=self.final_image.width, height=self.final_image.height
        )
        self.c_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.text = self.canvas.create_text(
            self.final_image.width / 2,
            self.final_image.height / 2,
            anchor=CENTER,
            text=str(value),
            fill="black",
            font=("Helvetica", 12, "bold"),
        )
        self.canvas.grid(row=location[0], column=location[1])

        self.hover_true = PIT_TURN
        self.hover_true_tk = ImageTk.PhotoImage(self.hover_true)

        self.hover_false = PIT_NOT_TURN
        self.hover_false_tk = ImageTk.PhotoImage(self.hover_false)

        self.id = id
        self.board = board

        self.updater = updater
        self.bar = bar

        self.enable()

    def enable(self):
        """
        This method is used to bind all the required hover and press events to the pits
        """
        self.canvas.bind("<Enter>", self.configure_slot)
        self.canvas.bind("<Leave>", self.reset_slot)
        self.canvas.bind("<Button-1>", self.button_press)

    def button_press(self, event):
        self.board.move(self.id)
        self.updater.update_value()
        self.configure_slot("<Enter>")
        self.bar.erase()
        self.canvas.update_idletasks()

        # sometimes the pit is not valid for the next move so needs to be rechecked

    def configure_slot(self, event):
        """
        Assigns the state of the pit to valid or invalid. If invalid, the button press event is unbounded.
        """
        if self.id in self.board.valid_moves(self.board.get_player()):
            self.canvas.itemconfig(self.c_image, image=self.hover_true_tk)
            self.bar.show_marbles(self.board.score[self.id])
        else:
            self.canvas.itemconfig(self.c_image, image=self.hover_false_tk)
            self.canvas.itemconfig(self.text, fill="red")
            self.canvas.unbind("<Button-1>")

        # display available marbles

    def reset_slot(self, event):
        """
        Resets to stationary state when hovered away. Need to rebind the button press event incase it was unbounded earlier
        """
        if self.bar.showing:
            self.bar.erase()

        self.canvas.bind("<Button-1>", self.button_press)
        self.canvas.itemconfig(self.c_image, image=self.image_tk)
        self.canvas.update_idletasks()
        self.canvas.itemconfig(self.text, fill="black")
        self.canvas.update_idletasks()

    def disable(self):
        self.canvas.itemconfig(self.c_image, image=self.image_tk)
        self.canvas.itemconfig(self.text, fill="black")
        self.canvas.unbind("<Enter>")
        self.canvas.unbind("<Leave>")
        self.canvas.unbind("<Button-1>")

    def bot_move(self):
        self.canvas.itemconfig(self.c_image, image=self.hover_true_tk)
        self.canvas.update_idletasks()
        self.bar.show_marbles(self.board.score[self.id])
        self.board.move(self.id)
        self.updater.update_value()
        self.root.after(2000)
        self.canvas.itemconfig(self.c_image, image=self.image_tk)
        self.bar.erase()

    def move_for_bot_display(self):
        self.canvas.itemconfig(self.c_image, image=self.hover_true_tk)
        self.bar.show_marbles(self.board.score[self.id])
        self.canvas.bind("<Button-1>", self.press_for_bot)

    def press_for_bot(self, event):
        self.board.move(self.id)
        self.updater.update_value()
        self.canvas.itemconfig(self.c_image, image=self.image_tk)
        self.bar.erase()
        self.canvas.update_idletasks()


class Deposit:
    """
    Deposit class is for the deposit/collection slots in on the board. Moves can not be made on the slots.
    They are also updated after every valid button press of a pit.

    The important object variables are:
        id (int): which relates to the position of the deposit on the board
        value (int): which is the score at the id position on the board
        updater (Updater): used to update the value to the current state of the board
    """

    def __init__(
        self,
        root,
        location: tuple,
        value: int,
        id: int,
        board,
        updater: Updater,
        bar: Bar,
    ) -> None:
        self.final_image = DEPOSIT
        self.image_tk = ImageTk.PhotoImage(self.final_image)
        self.canvas = Canvas(
            root, width=self.final_image.width, height=self.final_image.height
        )
        self.c_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.text = self.canvas.create_text(
            self.final_image.width / 2,
            self.final_image.height / 2,
            anchor=CENTER,
            text=str(value),
            fill="black",
            font=("Helvetica", 12, "bold"),
        )
        self.canvas.grid(row=location[0], column=location[1], rowspan=2)

        self.hover = DEPOSIT_HOVER
        self.hover_tk = ImageTk.PhotoImage(self.hover)

        self.id = id
        self.board = board

        self.bar = bar
        self.updater = updater
        self.title_name = None

        if self.id == 6:
            self.title = self.canvas.create_text(
                self.final_image.width / 2,
                self.final_image.height - 60,
                anchor=CENTER,
                fill="black",
                font=("Helvetica", 12, "bold"),
            )
        else:
            self.title = self.canvas.create_text(
                self.final_image.width / 2,
                60,
                anchor=CENTER,
                fill="black",
                font=("Helvetica", 12, "bold"),
            )

        self.functions()

    def functions(self):
        """
        Similar to the pit class, this function makes the initial bindings of the hovering events
        to the deposit slot.
        """
        self.canvas.bind("<Enter>", self.configure_slot)
        self.canvas.bind("<Leave>", self.reset_slot)

    def configure_slot(self, event):
        self.canvas.itemconfig(self.c_image, image=self.hover_tk)
        if self.board.score[self.id] > 0:
            self.bar.show_marbles(self.board.score[self.id])

    def reset_slot(self, event):
        if self.bar.showing:
            self.bar.erase()
        self.canvas.itemconfig(self.c_image, image=self.image_tk)

    def update_title(self, name: str):
        self.title_name = name
        if name.split(" ")[0] == "Level":
            indent = " " * ((len(self.title_name) // 2))
        else:
            indent = " " * ((len(self.title_name) // 2) - 2)

        self.canvas.itemconfig(
            self.title, text=self.title_name + "\n" + indent + "Score"
        )


# ovals at the bottom surrounded by some shape with the same revealing feature

"""

"""
