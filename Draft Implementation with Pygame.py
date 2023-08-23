#Nathnael Bekele
#Gabata
#5/25/2023


#gabata  implementation using array

import copy
import pygame

class gabata_board():
    
    def __init__(self):
        self.score = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
        self.sequence = [1]

    def get_player(self):
        return self.sequence[-1]

    def get_sequence(self):
        return self.sequence
    
    def set_sequence(self,sequence):
        self.sequence = sequence

    def set_score(self,score_list):
        self.score = score_list

    def get_score(self):
        return self.score

    def valid_moves(self, player_turn):
        valid_move = []
        player = player_turn

        if(player == 1):
            for i in range(7):
                if self.score[i]!=0:
                    valid_move.append(i+1)
        
        elif(player == 2):
            for i in range(7,14):
                if self.score[i]!=0:
                    valid_move.append(i+1)
        return valid_move
    
    def copy(self):
        new_copy = gabata_board()
        new_copy.set_score(copy.deepcopy(self.get_score()))
        new_copy.set_sequence(copy.deepcopy(self.get_sequence()))
    
        return new_copy

    def points(self, player):
        player = player

        if(player == 1):
            return self.score[6]
        else:
            return self.score[13]
    
    def empty(self, player):
        if player == 1:
            if sum(self.score[0:6]) == 0:
                return True
            else:
                return False
        else:
            if sum(self.score[7:13]) == 0:
                return True  
            else:
                return False

    def move(self, pos):
        change = {key: value for key, value in zip(range(1, 14), range(13, 0, -1))}
        seq_switch = {1:2,2:1}
        player = self.sequence[-1]

        if pos in self.valid_moves(player):

            while player == self.sequence[-1]:

                hand = self.score[pos-1]
                self.score[pos-1] = 0

                for i in range(hand):
                    if (pos == 6 and player == 2) or (pos == 13 and player == 1):
                        pos += 1
                    if pos == 14:
                        pos = 0
                    self.score[pos] = self.score[pos] + 1
                    pos = pos + 1
                
                if self.empty(player):
                    self.sequence.append(seq_switch[player])
                    break
                elif (pos == 7 and player ==1) or (pos == 14 and player ==2):        
                    self.sequence.append(player)
                    break
                elif (pos == 7 and player ==2) or (pos == 14 and player ==1):
                    self.sequence.append(seq_switch[player])
                    break
                elif self.score[pos-1] == 1:
                    if (1<=pos<7 and player ==1) or (8<=pos<14 and player == 2):
                        if self.score[change[pos]-1] != 0:
                            self.score[pos-1] = 0
                            pos = change[pos]
                            self.score[pos -1] = self.score[pos -1] + 1 
                        else:
                            self.sequence.append(seq_switch[player])
                            break
                    else:
                        self.sequence.append(seq_switch[player])
                        break

        if self.empty(2):
            self.sequence.append(1)
        elif self.empty(1):
            self.sequence.append(2)

    def get_winner(self):
        if self.points(1) > self.points(2):
            return 1 
        elif self.points(2) > self.points(1):
            return 2
        else:
            return 0
        
    def game_over(self):
        if self.empty(1) and self.empty(2): 
            return True
        else:
            return False
        

class Node:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

        if len(board.sequence) == 1:
            self.player = board.sequence[-1]
        else:
            self.player = board.sequence[-2]

        self.children = []
        self.move_made = None
        self.value = None

class Bot:

    def __init__(self, depth):
        self.depth = depth
        self.head = None
        self.player = None

    def gen_head(self, board):
        self.head = Node(board, 0)
        self.player = board.get_player()
        self.gen_tree(self.head,board)

    def gen_tree(self, node, board):
        if node.depth >= self.depth:
            node.value = node.board.points(self.player)
            return
        else:
            moves = board.valid_moves(board.get_player())

            for move in moves:
                tempboard = board.copy()
                tempboard.move(move)
                new_node = Node(tempboard,node.depth+1)
                new_node.move_made = move                    
                node.children.append(new_node)
                self.gen_tree(new_node,tempboard)
    
    def recommend(self):
        score = []
        for child in self.head.children:
            stack = [child]
            move_score = []

            while stack:
                node = stack.pop()

                if  node.depth == self.depth:
                    move_score.append(node.value)
                else:
                    stack.extend(node.children)

            score.append((child.move_made,max(move_score)))

        max_tuple = max(score, key=lambda x: x[1])
        return max_tuple[0]     

pygame.init()
screen = pygame.display.set_mode((1350,720))
#screen.fill((160, 120, 80))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 50)
text_color = (255, 255, 255) 
e_width = 100
e_height = 80
game_player = None

location_dict = {1:(250, 320, 100, 80) , 2: (400, 320, 100, 80), 3:(550, 320, 100, 80) , 4: (700, 320, 100, 80), 5:(850, 320, 100, 80), 6: (1000, 320, 100, 80), 7:(1180,120,100,260), 8:(1000, 100, 100, 80), 9:(850, 100, 100, 80), 10:(700, 100, 100, 80), 11:(550, 100, 100, 80), 12:(400, 100, 100, 80), 13:(250, 100, 100, 80), 14:(70,120,100,260)}
location_dict_text = {1:(300, 360) , 2: (450, 360), 3:(600, 360) , 4: (750, 360), 5:(900, 360), 6: (1050, 360), 7:(1230,250), 8:(1050, 140), 9:(900, 140), 10:(750, 140), 11:(600, 140), 12:(450, 140), 13:(300, 140), 14:(120,250)}
location = [(300, 360) , (450, 360),(600, 360) , (750, 360), (900, 360), (1050, 360), (1050, 140), (900, 140), (750, 140), (600, 140), (450, 140), (300, 140)]
location_valid = {(300, 360):1 , (450, 360):2,(600, 360):3 , (750, 360):4, (900, 360):5, (1050, 360):6, (1050, 140):8, (900, 140):9, (750, 140):10, (600, 140):11, (450, 140):12, (300, 140):13}


def restart():
    pygame.draw.rect(screen, 'blue', (1,1,100,40))

    home = font.render('Restart', True, text_color)
    rect_home = home.get_rect()
    rect_home.center = (50.5,20.5)
    screen.blit(home,rect_home)

    if ((1 <= pygame.mouse.get_pos()[0] <= 101) and (1 <= pygame.mouse.get_pos()[1] <= 41)):
        pygame.draw.rect(screen, 'white', (1,1,100,40),2)
        
    if pygame.mouse.get_pressed()[0]:
        if ((1 <= pygame.mouse.get_pos()[0] <= 101) and (1 <= pygame.mouse.get_pos()[1] <= 41)):
            screen.fill((160, 120, 80))
            player_choice()

def player_choice():

    running = True
    while running:
        screen.fill((160, 120, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.draw.rect(screen, 'blue', (screen.get_width()/2 -400,screen.get_height()/2,300,150))
        pygame.draw.rect(screen, 'blue', (screen.get_width()/2 +100,screen.get_height()/2,300,150))

        
        t_choose = font.render('Who do you want to play as?', True, text_color)
        t_rect_c = t_choose.get_rect()
        t_rect_c.center = (screen.get_width()/2,screen.get_height()/2 - 100)

        t_p1 = font.render('Player 1', True, text_color)
        t_rect_p1 = t_p1.get_rect()
        t_rect_p1.center = (screen.get_width()/2-250,screen.get_height()/2+75)

        t_p2 = font.render('Player 2', True, text_color)
        t_rect_p2 = t_p2.get_rect()
        t_rect_p2.center = (screen.get_width()/2+250,screen.get_height()/2+75)

        screen.blit(t_choose, t_rect_c)
        screen.blit(t_p1, t_rect_p1)
        screen.blit(t_p2, t_rect_p2)

        if ((screen.get_width()/2 +100 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 +400) and
            (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
            pygame.draw.rect(screen, 'white', (screen.get_width()/2 +100,screen.get_height()/2,300,150),2)

        if ((screen.get_width()/2 -400 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 -100) and
            (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
            pygame.draw.rect(screen, 'white', (screen.get_width()/2 -400,screen.get_height()/2,300,150),2)
        
        if pygame.mouse.get_pressed()[0]:
            if ((screen.get_width()/2 -400 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 -100) and
                (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
                game_player = 1
                pygame.time.wait(100)
                opponent(game_player)

            if ((screen.get_width()/2 +100 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 +400) and
                (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
                pygame.draw.rect(screen, 'white', (screen.get_width()/2 +100,screen.get_height()/2,300,150),2)
                game_player = 2
                pygame.time.wait(100)
                opponent(game_player)

        pygame.display.flip()
        clock.tick(60)

def opponent(game_player):
    screen.fill((160, 120, 80)) 
    pygame.time.wait(100)

    running = True
    while running:
        screen.fill((160, 120, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.draw.rect(screen, 'blue', (screen.get_width()/2 -400,screen.get_height()/2,300,150))
        pygame.draw.rect(screen, 'blue', (screen.get_width()/2 +100,screen.get_height()/2,300,150))

        
        t_choose = font.render('Who do you want to as your opponent?', True, text_color)
        t_rect_c = t_choose.get_rect()
        t_rect_c.center = (screen.get_width()/2,screen.get_height()/2 - 100)

        t_bot = font.render('Bot', True, text_color)
        t_rect_bot = t_bot.get_rect()
        t_rect_bot.center = (screen.get_width()/2-250,screen.get_height()/2+75)

        t_2p = font.render('Second player', True, text_color)
        t_rect_2p = t_2p.get_rect()
        t_rect_2p.center = (screen.get_width()/2+250,screen.get_height()/2+75)

        screen.blit(t_choose, t_rect_c)
        screen.blit(t_bot, t_rect_bot)
        screen.blit(t_2p, t_rect_2p)

        if ((screen.get_width()/2 +100 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 +400) and
            (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
            pygame.draw.rect(screen, 'white', (screen.get_width()/2 +100,screen.get_height()/2,300,150),2)

        if ((screen.get_width()/2 -400 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 -100) and
            (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
            pygame.draw.rect(screen, 'white', (screen.get_width()/2 -400,screen.get_height()/2,300,150),2)
        
        if pygame.mouse.get_pressed()[0]:
            if ((screen.get_width()/2 -400 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 -100) and
                (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
                #display(create_board_with_bot())
                pygame.time.wait(100)
                display(create_board(game_player, 'Bot'))

            if ((screen.get_width()/2 +100 <= pygame.mouse.get_pos()[0] <= screen.get_width()/2 +400) and
                (screen.get_height()/2 <= pygame.mouse.get_pos()[1] <= screen.get_height()/2 +150)):
                pygame.draw.rect(screen, 'white', (screen.get_width()/2 +100,screen.get_height()/2,300,150),2)
                pygame.time.wait(100)
                display(create_board(game_player, '2 Player'))

        restart()
        pygame.display.flip()
        clock.tick(60)

def create_board(game_player, typ):
    board = gabata_board()
    if typ == 'Bot':
        bot = Bot(5)
        return (board, game_player, typ, bot)    
    elif typ == '2 Player':
        return (board, game_player, typ)
    
def display(tup):
    board = tup[0]
    game_player = tup[1]
    typ = tup[2]
    
    if typ == 'Bot':
        bot = tup[3]
    
    running = True

    while running:
        screen.fill((160, 120, 80))
        restart()
        
        if board.get_player() == 2:
            text_surface_turn2 = font.render("Player 2's Turn",True, 'Green')
            text_rect_turn2 = text_surface_turn2.get_rect()
            text_rect_turn2.center = (1350/2,50)
            screen.blit(text_surface_turn2, text_rect_turn2)
        else:
            text_surface_turn1 = font.render("Player 1's Turn",True, 'Green')
            text_rect_turn1 = text_surface_turn1.get_rect()
            text_rect_turn1.center = (1350/2,450)
            screen.blit(text_surface_turn1, text_rect_turn1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        for i in range(1,15):
            if i != 7 and i != 14:
                pygame.draw.ellipse(screen, 'blue',location_dict[i])
                text_surface = font.render(str(board.get_score()[i-1]), True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = location_dict_text[i]
                screen.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(screen, 'blue', location_dict[i])
                text_surface = font.render(str(board.get_score()[i-1]), True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = location_dict_text[i]
                screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0,100,100), (70, 500, 1210, 200))
        
        for i in range(20):
            if i < 10:
                pygame.draw.ellipse(screen,'white',(80+i*120,510,e_width,e_height),2)
            elif i < 19:
                pygame.draw.ellipse(screen,'white',(80+(i-10)*120,600,e_width,e_height),2)
        
        cursor_position = pygame.mouse.get_pos()
        for loc in location:
            if (loc[0]-50 < cursor_position[0] < loc[0]+50) and (loc[1]-40 < cursor_position[1] < loc[1]+40):
                if (location_valid[loc] in board.valid_moves(board.get_player())):
                    pygame.draw.ellipse(screen, 'green',(loc[0]-50,loc[1]-40,100,80),2)
                    expand(board.get_score()[location_valid[loc]-1])
                else:
                    pygame.draw.ellipse(screen, 'red',(loc[0]-50,loc[1]-40,100,80),2)
            elif(70 < cursor_position[0] < 170) and (120 < cursor_position[1] < 380):
                expand(board.get_score()[13])
            elif(1180 < cursor_position[0] < 1280) and (120 < cursor_position[1] < 380):
                expand(board.get_score()[6])

        if typ == "Bot" and game_player != board.get_player():
            
            bot.gen_head(board)
            move = bot.recommend()

            pygame.time.wait(1000)

            pygame.draw.ellipse(screen, 'green',(location_dict_text[move][0]-50,location_dict_text[move][1]-40,100,80),2)
            pygame.display.flip()
            pygame.time.wait(1000)
            board.move(move)
            
            #elif (typ == "Bot" and game_player == board.get_player()) or typ != "Bot":
        if pygame.mouse.get_pressed()[0]:
            for loc in location:    
                if (loc[0]-50 < cursor_position[0] < loc[0]+50) and (loc[1]-40 < cursor_position[1] < loc[1]+40):
                        if (location_valid[loc] in board.valid_moves(board.get_player())):
                            board.move(location_valid[loc])
                            pygame.time.wait(100)
        
        if board.game_over():
            win_page(board)

        pygame.display.flip()
        clock.tick(60)
    
def expand(score):
    for i in range(score):
        if i < 10:
            pygame.draw.ellipse(screen,'blue',(80+i*120,510,e_width,e_height))
            pygame.draw.ellipse(screen,'white',(80+i*120,510,e_width,e_height),2)

        elif i < 19:
            pygame.draw.ellipse(screen,'blue',(80+(i-10)*120,600,e_width,e_height))
            pygame.draw.ellipse(screen,'white',(80+(i-10)*120,600,e_width,e_height),2)
        else:
            string_score = "+ "+str(score-19)
            text_surface_box = font.render(string_score, True, text_color)
            text_surface2 = pygame.Surface(text_surface_box.get_size(), pygame.SRCALPHA)
            text_surface2.blit(text_surface_box, (0, 0))
            text_rect_box = text_surface2.get_rect(center = (1200,640))
            screen.blit(text_surface2, text_rect_box)
    
def win_page(board):
    screen.fill((160, 120, 80))

    if board.get_winner() == 1:
        win = "PLAYER 1 WON"
    elif board.get_winner() ==2:
        win = "PLAYER 2 WON"
    else:
        win = "PLAYERS TIED"

    t_win = font.render(win,True, 'Green')
    t_win_rect = t_win.get_rect()
    t_win_rect.center = (screen.get_width()/2,screen.get_height()/2)
    screen.blit(t_win,t_win_rect)
    restart()
    
player_choice()
