from UI import Pit, Deposit, Updater, Bar, Players

# rom Instructions import Instructions
from Board import Board
from Bot import Bot
from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import webbrowser

ROOT = Tk()
ROOT.minsize(800, 208)
ROOT.maxsize(1232, 659)
ROOT.title("Gabata Game")

GABATA_CLAEAR = Image.open(Path("Gabata Images/Gabata_vclear.png"))
GABATA_CLAEAR = GABATA_CLAEAR.resize(
    (800, int(800 * GABATA_CLAEAR.height / GABATA_CLAEAR.width)), Image.LANCZOS
)
iamge = CLEAR_TK = ImageTk.PhotoImage(GABATA_CLAEAR)

GABATA_IM = Image.open(Path("Gabata Images/Gabata_text.png"))
GABATA_IM = GABATA_IM.resize(
    (800, int(800 * GABATA_IM.height / GABATA_IM.width)), Image.LANCZOS
)
GABATA_IK = ImageTk.PhotoImage(GABATA_IM)

BOT_LEVEL = None
BOT_NAME = None
BOT_NAME_MENU = IntVar(ROOT)
DUMB_BOT = False
COUNT_SWITCHES = 0
PLAYER_LIST = []
BOT_LIST = []
BOT_FUNCTION = None
RADIOVAR = StringVar(ROOT)
RADIOVAR.set("Auto")


def clear_page():
    for widget in ROOT.winfo_children():
        widget.destroy()


def set_bot_level(level, player=None, bot=None, player2=None, slot_options=None):
    global BOT_LEVEL, DUMB_BOT, BOT_NAME, BOT_NAME_MENU
    if level == -1:
        BOT_LEVEL = 5
        DUMB_BOT = True
        BOT_NAME = -1
    else:
        BOT_LEVEL = level
        BOT_NAME = level
        DUMB_BOT = False

    BOT_NAME_MENU.set(BOT_NAME)

    if player != None and bot != None:
        bot.depth = BOT_LEVEL
        global COUNT_SWITCHES
        if COUNT_SWITCHES % 2 == 0:
            player.modify_text("Level " + str(BOT_NAME) + " Bot")
        else:
            player2.modify_text("Level " + str(BOT_NAME) + " Bot")

        if bot.player == 2:
            slot_options[13].update_title("Level " + str(BOT_NAME) + " Bot")
        else:
            slot_options[6].update_title("Level " + str(BOT_NAME) + " Bot")


def menu_bar():
    menu = Menu(ROOT, tearoff=0)
    play_menu = Menu(menu, tearoff=0)
    play_menu.add_command(label="Versus human", command=game_play)
    bot_menu = Menu(play_menu, tearoff=0)

    for i in range(0, 9):
        if i == 0:
            bot_menu.add_command(
                label="Level: " + str(-1), command=lambda level=-1: bot_setting(level)
            )
        else:
            bot_menu.add_command(
                label="Level: " + str(i), command=lambda level=i: bot_setting(level)
            )

    play_menu.add_cascade(label="Versus bot", menu=bot_menu)
    menu.add_cascade(label="Play", menu=play_menu)
    menu.add_command(label="Learn to Play", command=instructions)

    bot_settings = Menu(menu, tearoff=0)
    bot_settings.add_radiobutton(
        label="Bot Automove",
        value="Auto",
        var=RADIOVAR,
        command=lambda: bot_move("Auto"),
    )
    bot_settings.add_radiobutton(
        label="Player Makes Bot Move",
        value="Player",
        var=RADIOVAR,
        command=lambda: bot_move("Player"),
    )

    menu.add_cascade(label="Bot Settings", menu=bot_settings)

    ROOT.config(menu=menu)


def bot_move(motion: str):
    global BOT_FUNCTION
    if motion == "Auto":
        BOT_FUNCTION = make_bot_move
    elif motion == "Player":
        BOT_FUNCTION = move_for_bot


def home():
    clear_page()
    menu_bar()
    home_page = Canvas(ROOT, width=GABATA_IM.width, height=GABATA_IM.height)
    home_page.create_image(0, 0, anchor=NW, image=GABATA_IK)
    home_page.pack(expand=True)

    ROOT.mainloop()


def instructions():
    webbrowser.open("https://natibek.github.io/Gabata-App/Gabata_webpage.html")
    """
    web_alert = Toplevel(ROOT)
    web_alert.title("Page not found")
    web_alert.minsize(400, 200)
    web_alert.maxsize(400, 200)

    label = Label(
        web_alert,
        text="Website is under developed. Apologies.\nConsult the README document for game rules and features",
    )
    label.pack(padx=20, pady=20)

    close_button = Button(web_alert, text="Back to Game", command=web_alert.destroy)
    close_button.pack(pady=20)

    ROOT.mainloop()
    """


def bot_menus(
    player=None,
    bot=None,
    switch=False,
    human_player=None,
    player_num=None,
    slot_options=None,
):
    bot_menu = Menu(ROOT)
    bot_menu.add_command(label="Home", command=home)
    bot_level = Menu(bot_menu, tearoff=0)

    for i in range(0, 9):
        if i == 0:
            bot_level.add_radiobutton(
                label="Level: " + str(-1),
                value=-1,
                var=BOT_NAME_MENU,
                command=lambda level=-1: set_bot_level(
                    level, player, bot, human_player, slot_options
                ),
            )
        else:
            bot_level.add_radiobutton(
                label="Level: " + str(i),
                value=i,
                var=BOT_NAME_MENU,
                command=lambda level=i: set_bot_level(
                    level, player, bot, human_player, slot_options
                ),
            )

    bot_menu.add_cascade(label="Reset Bot level", menu=bot_level)

    bot_settings = Menu(bot_menu, tearoff=0)
    bot_settings.add_radiobutton(
        label="Bot Automove",
        value="Auto",
        var=RADIOVAR,
        command=lambda: bot_move("Auto"),
    )
    bot_settings.add_radiobutton(
        label="Player Makes Bot Move",
        value="Player",
        var=RADIOVAR,
        command=lambda: bot_move("Player"),
    )

    bot_menu.add_cascade(label="Bot Settings", menu=bot_settings)

    if switch:
        bot_menu.add_command(
            label="Restart", command=lambda: bot_setting(BOT_LEVEL))

        bot_menu.add_command(
            label="Switch players",
            command=lambda: switch_players(
                player, human_player, bot, player_num, slot_options
            ),
        )

    ROOT.config(menu=bot_menu)


def switch_players(player, human_player, bot, player_num, slot_options):
    switch = {1: 2, 2: 1}
    global COUNT_SWITCHES, BOT_LIST, PLAYER_LIST
    temp = BOT_LIST
    BOT_LIST = PLAYER_LIST
    PLAYER_LIST = temp

    player2_name = slot_options[13].title_name
    player1_name = slot_options[6].title_name

    slot_options[13].update_title(player1_name)
    slot_options[6].update_title(player2_name)

    if COUNT_SWITCHES % 2 == 0:
        bot.player = switch[player_num]
        player.modify_text("Player " + str(player_num))
        human_player.modify_text("Level " + str(BOT_NAME) + " Bot")
    else:
        bot.player = player_num
        human_player.modify_text("Player " + str(switch[player_num]))
        player.modify_text("Level " + str(BOT_NAME) + " Bot")

    COUNT_SWITCHES += 1


def bot_setting(level):
    global COUNT_SWITCHES
    COUNT_SWITCHES = 0

    clear_page()
    set_bot_level(level)
    bot_menus()

    choice_player = Canvas(ROOT, width=GABATA_CLAEAR.width,
                           height=GABATA_CLAEAR.height)
    choice_player.pack()

    choice_image = choice_player.create_image(0, 0, anchor=NW, image=CLEAR_TK)
    choice_text = choice_player.create_text(
        GABATA_CLAEAR.width / 2,
        GABATA_CLAEAR.height / 2,
        text="Play as:",
        anchor=CENTER,
        font=("Helvetica", 14),
    )
    player1_button = choice_player.create_rectangle(
        (GABATA_CLAEAR.width / 2) - 40,
        285 - 15,
        (GABATA_CLAEAR.width / 2) + 40,
        285 + 15,
        fill="white",
    )

    player2_button = choice_player.create_rectangle(
        (GABATA_CLAEAR.width / 2) - 40,
        35 - 15,
        (GABATA_CLAEAR.width / 2) + 40,
        35 + 15,
        fill="white",
    )

    player1_text = choice_player.create_text(
        (GABATA_CLAEAR.width / 2),
        285,
        anchor=CENTER,
        text="Player 1",
        fill="black",
        font=("Helvetica", 12),
    )

    player2_text = choice_player.create_text(
        (GABATA_CLAEAR.width / 2),
        35,
        anchor=CENTER,
        text="Player 2",
        fill="black",
        font=("Helvetica", 12),
    )

    def hover(event, element):
        choice_player.itemconfig(element, fill="gray")

    def reset(event, element):
        choice_player.itemconfig(element, fill="white")

    choice_player.tag_bind(
        player1_button, "<Enter>", lambda event: hover(event, player1_button)
    )
    choice_player.tag_bind(
        player2_button, "<Enter>", lambda event: hover(event, player2_button)
    )
    choice_player.tag_bind(
        player1_button, "<Leave>", lambda event: reset(event, player1_button)
    )
    choice_player.tag_bind(
        player2_button, "<Leave>", lambda event: reset(event, player2_button)
    )
    choice_player.tag_bind(player1_button, "<Button-1>",
                           lambda event: bot_game(2))
    choice_player.tag_bind(player2_button, "<Button-1>",
                           lambda event: bot_game(1))

    choice_player.tag_bind(
        player1_text, "<Enter>", lambda event: hover(event, player1_button)
    )
    choice_player.tag_bind(
        player2_text, "<Enter>", lambda event: hover(event, player2_button)
    )
    choice_player.tag_bind(
        player1_text, "<Leave>", lambda event: reset(event, player1_button)
    )
    choice_player.tag_bind(
        player2_text, "<Leave>", lambda event: reset(event, player2_button)
    )
    choice_player.tag_bind(player1_text, "<Button-1>",
                           lambda event: bot_game(2))
    choice_player.tag_bind(player2_text, "<Button-1>",
                           lambda event: bot_game(1))


def bot_game(player: int):
    clear_page()

    global BOT_LIST, PLAYER_LIST
    bot = Bot(BOT_LEVEL, player)
    board = Board()  # board for the game
    slot_options = [None] * 14  # used to store all the pits and deposits

    if bot.player == 2:
        player1 = Players(ROOT, 1, board, "Player 1")
        player2 = Players(ROOT, 2, board, "Level " + str(BOT_NAME) + " Bot")
        BOT_LIST = range(7, 13)
        PLAYER_LIST = range(0, 6)
        bot_menus(player2, bot, True, player1, player, slot_options)
    else:
        player1 = Players(ROOT, 1, board, "Level " + str(BOT_NAME) + " Bot")
        player2 = Players(ROOT, 2, board, "Player 2")
        BOT_LIST = range(0, 6)
        PLAYER_LIST = range(7, 13)
        bot_menus(player1, bot, True, player2, player, slot_options)

    back = list(range(7, 13))

    updater = Updater(
        slot_options, [player1, player2]
    )  # updater is initialized with the pits and deposits, and the players
    bar = Bar(ROOT)

    for col in range(0, 8):
        # this nested for loop is used for displaying the pits and deposits as well as adding them to the slot_option list in the correct order
        if col == 0:
            deposit = Deposit(
                ROOT, (1, col), board.score[13], 13, board, updater, bar)
            deposit.update_title(player2.player_name)
            slot_options[13] = deposit
        elif col == 7:
            deposit = Deposit(
                ROOT, (1, col), board.score[6], 6, board, updater, bar)
            deposit.update_title(player1.player_name)
            slot_options[6] = deposit
        else:
            for row in range(1, 3):  # (2,4)
                if row == 2:
                    pit = Pit(
                        ROOT,
                        (row, col),
                        board.score[col - 1],
                        col - 1,
                        board,
                        updater,
                        bar,
                    )
                    slot_options[col - 1] = pit
                else:
                    ind = back.pop()
                    pit = Pit(
                        ROOT, (row,
                               col), board.score[ind], ind, board, updater, bar
                    )
                    slot_options[ind] = pit

    for i in BOT_LIST:
        slot_options[i].disable()

    ROOT.after(1000, BOT_FUNCTION, slot_options, bot, board, player)
    ROOT.mainloop()


def move_for_bot(slot_options, bot, board, player):
    if board.get_player() == bot.player and not board.game_over():
        for i in PLAYER_LIST:
            slot_options[i].disable()

        bot.gen_head(board)

        if DUMB_BOT:
            move = bot.recommend_worst()
        else:
            move = bot.recommend_best()

        slot_options[move].move_for_bot_display()

        ROOT.after(20, BOT_FUNCTION, slot_options, bot, board, player)

    elif board.game_over():
        for i in PLAYER_LIST:
            slot_options[i].disable()
        for i in BOT_LIST:
            slot_options[i].disable()

        bot_game_over(board, slot_options)

    else:
        for i in PLAYER_LIST:
            try:
                slot_options[i].enable()
            except:
                pass
        for i in BOT_LIST:
            try:
                slot_options[i].disable()
            except:
                pass

        ROOT.after(20, BOT_FUNCTION, slot_options, bot, board, player)


def make_bot_move(slot_options, bot, board, player):
    if board.get_player() == bot.player and not board.game_over():
        for i in PLAYER_LIST:
            slot_options[i].disable()

        bot.gen_head(board)

        if DUMB_BOT:
            move = bot.recommend_worst()
        else:
            move = bot.recommend_best()

        slot_options[move].bot_move()

        ROOT.after(20, BOT_FUNCTION, slot_options, bot, board, player)

    elif board.game_over():
        for i in PLAYER_LIST:
            slot_options[i].disable()
        for i in BOT_LIST:
            slot_options[i].disable()

        bot_game_over(board, slot_options)

    else:
        for i in PLAYER_LIST:
            try:
                slot_options[i].enable()
            except:
                pass
        for i in BOT_LIST:
            try:
                slot_options[i].disable()
            except:
                pass

        ROOT.after(20, BOT_FUNCTION, slot_options, bot, board, player)


def bot_game_over(board, slot_options):
    if board.get_winner() == 1:
        if slot_options[6].title_name.split(" ")[0] == "Level":
            winner = slot_options[6].title_name + " Won!!"
        else:
            if BOT_LEVEL != 8:
                winner = (
                    "You beat the "
                    + slot_options[13].title_name
                    + "!!\nTry a tougher bot?!"
                )
            else:
                winner = (
                    "You beat the "
                    + slot_options[13].title_name
                    + "!!\nYou beat my toughest bot!!"
                )
    elif board.get_winner() == 2:
        if slot_options[13].title_name.split(" ")[0] == "Level":
            winner = "The " + slot_options[13].title_name + " Won!!"
        else:
            if BOT_LEVEL != 8:
                winner = (
                    "You beat the "
                    + slot_options[6].title_name
                    + "!!\nTry a tougher bot?!"
                )
            else:
                winner = (
                    "You beat the "
                    + slot_options[6].title_name
                    + "!!\nYou beat my toughest bot!!"
                )
    else:
        winner = "You TIED with the Level " + str(BOT_LEVEL) + " BOT"

    game_over = Toplevel(ROOT)
    game_over.title("Game Over")
    game_over.minsize(width=260, height=150)
    game_over.maxsize(width=260, height=150)
    label = Label(game_over, text=winner, font=("Helvetica", 12))
    label.pack(padx=20, pady=20)

    close_button = Button(game_over, text="Return to Game",
                          command=game_over.destroy)
    close_button.pack(pady=10)


def play_menu():
    menu = Menu(ROOT)
    menu.add_command(label="Home", command=home)
    menu.add_command(label="Restart", command=game_play)
    ROOT.config(menu=menu)


def game_play():  # the method for 2 player game play
    clear_page()
    play_menu()

    board = Board()  # board for the game

    slot_options = [None] * 14  # used to store all the pits and deposits
    back = list(range(7, 13))

    player1 = Players(ROOT, 1, board, "Player 1")
    player2 = Players(ROOT, 2, board, "Player 2")

    updater = Updater(
        slot_options, [player1, player2]
    )  # updater is initialized with the pits and deposits, and the players
    bar = Bar(ROOT)

    for col in range(0, 8):
        # this nested for loop is used for displaying the pits and deposits as well as adding them to the slot_option list in the correct order
        if col == 0:
            deposit = Deposit(
                ROOT, (1, col), board.score[13], 13, board, updater, bar)
            deposit.update_title(player2.player_name)
            slot_options[13] = deposit
        elif col == 7:
            deposit = Deposit(
                ROOT, (1, col), board.score[6], 6, board, updater, bar)
            deposit.update_title(player1.player_name)
            slot_options[6] = deposit
        else:
            for row in range(1, 3):
                if row == 2:
                    pit = Pit(
                        ROOT,
                        (row, col),
                        board.score[col - 1],
                        col - 1,
                        board,
                        updater,
                        bar,
                    )
                    slot_options[col - 1] = pit
                else:
                    ind = back.pop()
                    pit = Pit(
                        ROOT, (row,
                               col), board.score[ind], ind, board, updater, bar
                    )
                    slot_options[ind] = pit

    ROOT.after(1000, check_game_state, board, slot_options)
    ROOT.mainloop()


def check_game_state(board, slot_options):
    if board.game_over():
        for i in PLAYER_LIST:
            slot_options[i].disable()
        for i in BOT_LIST:
            slot_options[i].disable()

        if board.get_winner() == 1:
            winner = "Player 1 Won!!"
        elif board.get_winner() == 2:
            winner = "Player 2 Won!!"
        else:
            winner = "Players Tied!!"

        game_over = Toplevel(ROOT)
        game_over.title("Game Over")
        game_over.minsize(width=260, height=200)
        game_over.maxsize(width=260, height=200)

        label = Label(game_over, text=winner, font=("Helvetica", 12))
        label.pack(padx=20, pady=20)

        close_button = Button(
            game_over, text="Return to Game Page", command=game_over.destroy
        )
        close_button.pack(pady=20)
    else:
        ROOT.after(1000, check_game_state, board, slot_options)


if __name__ == "__main__":
    BOT_FUNCTION = make_bot_move
    home()
