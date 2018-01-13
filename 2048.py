"""
Jack Shea
1/13/2018

2048 game

"""
import random

class Game:
    """ Class for the actual game of 2048 """

    def __init__(self):
        """ Initialization method for the 2048 game """

        self.board = Board()
        self.score = 0
        self.moves = 0

    def play_random(self):
        """ Plays a game where move decisions are completely random """
        
        game_over = False
        
        while not game_over:

            move = random.randint(0,3)
            
            if move == 0:
                (made_move,d_score) = self.board.down()
            elif move == 1:
                (made_move,d_score) = self.board.up()
            elif move == 2:
                (made_move,d_score) = self.board.right()
            else:
                (made_move,d_score) = self.board.left()

            if made_move:
                self.moves += 1
                self.score += d_score
                self.board.new_piece()
                if self.board.no_more_moves():
                    game_over = True
                


class Board:
    """ Class for the 2048 board """
    
    def __init__(self):
        """ Initialization method for the 2048 board """
        
        self.board = [[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]

        # random positions for the first 2 pieces
        a,b = random.randint(0,3),random.randint(0,3)
        c,d = random.randint(0,3),random.randint(0,3)

        # ensures the 2 piece locations are not the same
        while a == c and b == d:
            c,d = random.randint(0,3),random.randint(0,3)

        self.board[a][b] = 2
        self.board[c][d] = 2


    def down(self):
        """ Method to update board when the player moves down """
        """ Returns tuple (was anything moved? , score change) """

        # when a piece is doubled, it should not be redoubled.
        # this keeps a list of piece locations that have been doubled to prevent redoubling
        dont_change = []
        
        d_score = 0    # score change from this move
        made_move = False   # keeps track of anything changing

        # loops through the top 3 rows working upwards
        for i in [2,1,0]:
            # loops through the 4 columns in each row
            for j in range(4):
                
                if self.board[i][j] != 0:
                    
                    move_complete = False # is this piece's motion complete?
                    move_count = 0        # how many places has this piece moved?
                    
                    while not move_complete:
                        
                        piece = self.board[i+move_count][j]
                        piece_below = self.board[i+move_count+1][j]

                        # if the location below is empty, moves the piece down
                        if piece_below == 0:
                            self.board[i+move_count][j] = 0
                            self.board[i+move_count+1][j] = piece
                            move_count += 1
                            made_move = True
                            # loop is done if it's reached the bottom
                            if i+move_count == 3:
                                move_complete = True

                        # if the location below has the same number, it doubles that piece
                        elif piece_below == piece:
                            # checks if piece to change is changable
                            if (i+move_count+1,j) not in dont_change:
                                self.board[i+move_count][j] = 0
                                self.board[i+move_count+1][j] = piece*2
                                d_score += piece*2
                                move_complete = True
                                made_move = True
                                # adds the changed location to a list of unchangable locations
                                dont_change.append((i+move_count+1,j))
                            else:
                                move_complete = True

                        # if the piece below is nonzero but not the same type
                        else:
                            move_complete = True

        # returns whether or not a move was made along with the score change
        return (made_move,d_score)
                            

    def up(self):
        """ Method to update board when the player moves up """
        """ Returns tuple (was anything moved? , delta_score) """
        
        dont_change = []
        d_score = 0
        made_move = False
        
        for i in [1,2,3]:
            for j in range(4):
                if self.board[i][j] != 0:
                    
                    move_complete = False
                    move_count = 0
                    
                    while not move_complete:
                        piece = self.board[i-move_count][j]
                        piece_above = self.board[i-move_count-1][j]
                        if piece_above == 0:
                            self.board[i-move_count][j] = 0
                            self.board[i-move_count-1][j] = piece
                            move_count += 1
                            made_move = True
                            if i-move_count == 0:
                                move_complete = True
                        elif piece_above == piece:
                            if (i-move_count-1,j) not in dont_change:
                                self.board[i-move_count][j] = 0
                                self.board[i-move_count-1][j] = piece*2
                                d_score += piece*2
                                move_complete = True
                                made_move = True
                                dont_change.append((i-move_count-1,j))
                            else:
                                move_complete = True
                        else:
                            move_complete = True
        return (made_move,d_score)


    def right(self):
        """ Method to update board when the player moves right """
        """ Returns tuple (was anything moved? , delta_score) """
        
        dont_change = []
        d_score = 0
        made_move = False
        for j in [2,1,0]:
            for i in range(4):
                if self.board[i][j] != 0:
                    
                    move_complete = False
                    move_count = 0
                    
                    while not move_complete:
                        piece = self.board[i][j+move_count]
                        piece_right = self.board[i][j+move_count+1]
                        if piece_right== 0:
                            self.board[i][j+move_count] = 0
                            self.board[i][j+move_count+1] = piece
                            move_count += 1
                            made_move = True
                            if j+move_count == 3:
                                move_complete = True
                        elif piece_right == piece:
                            if (i,j+move_count+1) not in dont_change:
                                self.board[i][j+move_count] = 0
                                self.board[i][j+move_count+1] = piece*2
                                d_score += piece*2
                                move_complete = True
                                made_move = True
                                dont_change.append((i,j+move_count+1))
                            else:
                                move_complete = True
                        else:
                            move_complete = True
        return (made_move,d_score)


    def left(self):
        """ Method to update board when the player moves left """
        """ Returns tuple (was anything moved? , delta_score) """
        
        dont_change = []
        d_score = 0
        
        made_move = False
        for j in [1,2,3]:
            for i in range(4):
                if self.board[i][j] != 0:
                    
                    move_complete = False
                    move_count = 0
                    
                    while not move_complete:
                        piece = self.board[i][j-move_count]
                        piece_left = self.board[i][j-move_count-1]
                        if piece_left == 0:
                            self.board[i][j-move_count] = 0
                            self.board[i][j-move_count-1] = piece
                            move_count += 1
                            made_move = True
                            if j-move_count == 0:
                                move_complete = True
                        elif piece_left == piece:
                            if (i,j-move_count-1) not in dont_change:
                                self.board[i][j-move_count] = 0
                                self.board[i][j-move_count-1] = piece*2
                                d_score += piece*2
                                move_complete = True
                                made_move = True
                                dont_change.append((i,j-move_count-1))
                            else:
                                move_complete = True
                                
                        else:
                            move_complete = True
        return (made_move,d_score)


    def new_piece(self):
        """ adds a new piece to a random spot on the board """

        # compiles list of empty locations
        empty_spots = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    empty_spots.append((i,j))

        # if no empty locations, we're done
        if len(empty_spots) == 0:
            return

        # chooses a random empty spot. 1/10 chance it's a 4
        spot = empty_spots[random.randint(0,len(empty_spots)-1)]
        is_4 = random.randint(0,9) == 0

        if is_4:
            self.board[spot[0]][spot[1]] = 4
        else:
            self.board[spot[0]][spot[1]] = 2


    def no_more_moves(self):
        """ checks if there are any more possible moves """
        
        temp = Board()

        # copies board to temp, returns False if move causes any change
        for i in range(4):
            for j in range(4):
                temp.board[i][j] = self.board[i][j]
        if temp.up()[0]:
            return False
        
        for i in range(4):
            for j in range(4):
                temp.board[i][j] = self.board[i][j]
        if temp.down()[0]:
            return False
        
        for i in range(4):
            for j in range(4):
                temp.board[i][j] = self.board[i][j]               
        if temp.right()[0]:
            return False
        
        for i in range(4):
            for j in range(4):
                temp.board[i][j] = self.board[i][j]              
        if temp.left()[0]:
            return False

        # if no move causes change, returns True
        return True
        

    def __str__(self):
        """ Nice printing method for the board class """
        
        print(self.board[0][0],self.board[0][1],self.board[0][2],self.board[0][3])
        print(self.board[1][0],self.board[1][1],self.board[1][2],self.board[1][3])
        print(self.board[2][0],self.board[2][1],self.board[2][2],self.board[2][3])
        print(self.board[3][0],self.board[3][1],self.board[3][2],self.board[3][3])
        return ""















    
