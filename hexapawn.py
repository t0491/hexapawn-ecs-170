import sys

'''
PROGRAM IS NOT 100% ACCURATE. THERE ARE SOME MISCALCULATIONS IT MAKES.
ALL MOVEMENT OPERATORS AND STATIC BOARD EVALUATION IS CORRECT + FUNCTIONAL.
MINIMAX ALGORITHM IS PROPERLY USED. MY ONLY PROBLEM PERHAPS IS
SOMEWHERE DEEP WITHIN THE RECURSION AND CHOOSING THE RESULTING
SBE VALUES AMONG THE MANY THAT WERE CALCULATED. PROGRAM
CAN 100% FIND THE NEXT BEST MOVE FOR A SINGLE PAWN, BUT
NOT THE ENTIRE BOARD. IF YOU COULD UNIT TEST AND CHECK ALL
THE INDIVIDUAL COMPONENTS, MOST OF IT SHOULD BE CORRECT.
'''

'''
/////////////////////
/// MAIN FUNCTION ///
/////////////////////
'''

# Hexapawn function will be called with all the information regarding the board
# that is being played, e.g. piece locations, size, color and how far the user
# wants the program to search ahead for evaluating the minimax alg.
def hexapawn(bd_state, bd_size, my_color, minimax_depth):

    print("Current Board State:")
    print_board(bd_state)
    print("\n------------\n ")
    # Convert the board into a list for easier parsing on my end.
    bd_state = str_to_list(bd_state)
    
    # Check if the arguments are valid. Terminate the program if it isn't.
    check_args(bd_state, bd_size, my_color)
                    
    # Sub function to call and recurse.
    current_depth = 0
    best_next_move = find_best_move(bd_state, bd_size, my_color, minimax_depth, current_depth)
    bd_state = best_next_move.new_board
    
    bd_state = list_to_str(bd_state)
    print("The Next Best Move/State:")
    print_board(bd_state)

def find_best_move(bd_state, bd_size, my_color, minimax_depth, current_depth):

    # Copy over the bd_state to a mutable variable.
    # Convert bd_state to a str instead so that it isn't accidentally mutated.
    bd_state = list_to_str(bd_state)
    
    current_depth += 1
    
    curr_best_node = Node(static_board_evaluator(bd_state, bd_size, my_color),0,0,bd_state)
    # Once we have reached the deepest part, return the state's sbe.
    if current_depth > minimax_depth:
        return curr_best_node
    else:
        row_index = 0
        for row in bd_state:
            col_index = 0
            for col in row:
                ''' ## REMINDER: EVERYTHING WE DO IN HERE IS FOR A SINGLE PAWN OUT OF N MANY ## '''
                # Make a new frontier for every pawn. It has its own "expansion" and will have its own best choice.
                frontier = []
                
                # We only want to move my colors on MAX turn.
                if col == my_color and current_depth % 2 == 1:
                    # print("MAX'S TURN")
                    # print(current_depth)
                    # print(str(row_index) + str(col_index))
                    # Iterate and check all of MAX's possible moves.
                    # Add all the moves' sbe value to the frontier.
                    # Choose the highest value for MAX.

                    # print(col_index)
                    # Frontier [0]
                    new_bd = move_forward(bd_state,bd_size,row_index,col_index)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # Frontier [1]
                    new_bd = capture_left(bd_state,bd_size,row_index,col_index)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # Frontier [2]
                    new_bd = capture_right(bd_state,bd_size,row_index,col_index)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # Because the input is a list, the bd_state input should be mutable.
                    # This means that it will make the best move, it will "save" for the current "find_best_move" it is in.
                    # Once we propagate back up to the original "find_best_move" we should have made a single choice/move rather
                    # than an culmination of many. make_best_move will choose our best result from the frontier given we are MAX
                    # or MIN.

                    # Figure out which move is the best for this individual pawn.
                    # Then check if that best move for the pawn is the best move overall. Every pawn is a "node".
                    move_index = choose_best(frontier, "MAX")
                    # print("Move index: " + str(move_index))

                    # Default movement.
                    next_board = move_forward(bd_state,bd_size,row_index,col_index)
                    
                    if move_index == 0:
                        next_board = move_forward(bd_state,bd_size,row_index,col_index)
                    elif move_index == 1:
                        next_board = capture_left(bd_state,bd_size,row_index,col_index)
                    elif move_index == 2:
                        next_board = capture_right(bd_state,bd_size,row_index,col_index)
                    else:
                        # Perform a default and move forward the first possible piece of your color.
                        r=0
                        for i in bd_state:
                            c=0
                            for j in row:
                                if col == 'w' and next_board == str_to_list(bd_state):
                                    next_board = move_forward(bd_state,bd_size,r,c)
                                c += 1
                            r += 1

                   
                    new_node = Node(frontier[move_index], row_index, col_index, next_board)

                    # If this pawn's move is better than any other we've gotten so far, update our current best move.
                    if new_node.sbe_val >= curr_best_node.sbe_val:
                        curr_best_node = new_node

                # Only move opposing color on MIN turn.
                elif col != my_color and col != '-' and current_depth % 2 == 0:
                    # print("MIN'S TURN")
                    # print(current_depth)
                    # Iterate and check opposing player's moves if you
                    # are on MIN's turn depthwise. Add the values to their frontier.
                    # Determine the lowest value and that's MIN's choice.

                    # print(col_index)
                    # Frontier [0]
                    new_bd = move_forward(bd_state,bd_size,row_index,col_index)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # Frontier [1]
                    new_bd = capture_left(bd_state,bd_size,row_index,col_index)
                    # print(new_bd)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # Frontier [2]
                    new_bd = capture_right(bd_state,bd_size,row_index,col_index)
                    new_sbe = find_best_move(new_bd, bd_size, my_color, minimax_depth, current_depth)
                    frontier.append(static_board_evaluator(new_sbe.new_board, bd_size, my_color))

                    # print(frontier)
                    move_index = choose_best(frontier, "MIN")
                     #print("Move index: " + str(move_index))

                    # Default movement.
                    next_board = move_forward(bd_state,bd_size,row_index,col_index)
                    if move_index == 0:
                        next_board = move_forward(bd_state,bd_size,row_index,col_index)
                    elif move_index == 1:
                        next_board = capture_left(bd_state,bd_size,row_index,col_index)
                    elif move_index == 2:
                        next_board = capture_right(bd_state,bd_size,row_index,col_index)
                    else:
                        # Perform a default and move forward the first possible piece of your color.
                        r=0
                        for i in bd_state:
                            c=0
                            for j in row:
                                if j == 'w' and next_board == str_to_list(bd_state):
                                    next_board = move_forward(bd_state,bd_size,r,c)
                                c += 1
                            r += 1
                    

                    new_node = Node(frontier[move_index], row_index, col_index, next_board)

                    # If this pawn's move is better than any other we've gotten so far, update our current best move.
                    if new_node.sbe_val >= curr_best_node.sbe_val:
                        curr_best_node = new_node
                        
                col_index += 1
            row_index += 1

    return curr_best_node

def make_best_move(bd_state, frontier, max_or_min):
    # Iterate through frontier and find the best MAX value.
    # Our choice will be the index corresponding to that value.
    # 0 = Forward, 1 = Cap Left, 2 = Cap Right
    OUR_CHOICE = -1
    OUR_VALUE = frontier[0]
    f_index = 0
    for i in frontier:
        if i >= OUR_VALUE and max_or_min == "MAX":
            OUR_VALUE = i
            OUR_CHOICE = f_index
        elif i <= OUR_VALUE and max_or_min == "MIN":
            OUR_VALUE = i
            OUR_CHOICE = f_index
        f_index += 1
        

    # Make the best move with the bd_state being edited.
    if OUR_CHOICE == 0:
        move_forward(bd_state,bd_size,row_index,col_index)
    elif OUR_CHOICE == 1:
        capture_left(bd_state,bd_size,row_index,col_index)
    elif OUR_CHOICE == 2:
        capture_right(bd_state,bd_size,row_index,col_index)
    else:
        print("No proper MAX/MIN choice. Error along the way.")

    # Return nothing since only the list has been changed due to mutability.
    return

'''
///////////////////
/// NODE OBJECT ///
///////////////////
'''

class Node:
    def __init__(this, sbe_val, r_index, c_index, board):
        this.sbe_val = sbe_val
        this.r_index = r_index
        this.c_index = c_index
        this.new_board = board
    

'''
////////////////////////
/// HELPER FUNCTIONS ///
////////////////////////
'''
def print_board(bd_state):
    for row in bd_state:
        print(row)
        
def check_args(bd_state, bd_size, my_color):
    # Check if the color input is even a valid one, e.g. white or black.
    if my_color != 'w' and my_color != 'b':
        # print(my_color)
        print ("Invalid color input. Please choose 'w' or 'b'.")
        exit()
        
    # Checking if the board has a false input somewhere by checking board size.
    col_count = 0
    for row in bd_state:
        for col in row:
            col_count += 1
        if col_count != bd_size:
            print("Board state and board size given are incompatible.")
            exit()
        else:
            col_count = 0

def choose_best(frontier, max_or_min):
    OUR_CHOICE = -1
    OUR_VALUE = frontier[0]
    f_index = 0
    for i in frontier:
        if i > OUR_VALUE and max_or_min == "MAX":
            OUR_VALUE = i
            OUR_CHOICE = f_index
        elif i < OUR_VALUE and max_or_min == "MIN":
            OUR_VALUE = i
            #print(OUR_VALUE)
            OUR_CHOICE = f_index
        f_index += 1
    if OUR_CHOICE == -1:
        # No "best" move has been found, so return -1 and perform a "default".
        return OUR_CHOICE
        
    return OUR_CHOICE

'''
///////////////////////
/// PIECE OPERATORS ///
///////////////////////
'''

def move_forward(bd_state, bd_size, row_index, col_index):
    # If the moving piece is white, then move down.
    temp_bd = bd_state.copy()
    temp_bd = str_to_list(temp_bd)
    if temp_bd[row_index][col_index] == 'w':
        # Check to make sure it isn't going out of bounds and there is space.
        if row_index < bd_size - 2 and temp_bd[row_index+1][col_index] == '-':
            temp_bd[row_index + 1][col_index] = 'w'
            temp_bd[row_index][col_index] = '-'
            
    # If the moving piece is black, then move up.
    elif temp_bd[row_index][col_index] == 'b':
        # Basically same comments as above.
        if row_index > 0 and temp_bd[row_index-1][col_index] == '-':
            temp_bd[row_index - 1][col_index] = 'b'
            temp_bd[row_index][col_index] = '-'
            
    return temp_bd

def capture_left(bd_state, bd_size, row_index, col_index):
    temp_bd = bd_state.copy()
    temp_bd = str_to_list(temp_bd)
    # White moves diagonally downwards.
    if temp_bd[row_index][col_index] == 'w':
        # Unlike move forward we also want to be sure that
        # we are within the horizontal boundaries as well.
        if row_index < bd_size - 2 and col_index > 0 and temp_bd[row_index+1][col_index-1] == 'b':
            temp_bd[row_index+1][col_index-1] = 'w'
            temp_bd[row_index][col_index] = '-'
            
    # Black moves diagonally upwards.
    elif temp_bd[row_index][col_index] == 'b':
        if row_index > 0 and col_index > 0 and temp_bd[row_index-1][col_index-1] == 'w':
            temp_bd[row_index-1][col_index-1] = 'b'
            temp_bd[row_index][col_index] = '-'
            
    return temp_bd

# Operates nearly identical to capture left but it will
# be checking col_index+1 instead since that is to the right.
def capture_right(bd_state, bd_size, row_index, col_index):
    temp_bd = bd_state.copy()
    temp_bd = str_to_list(temp_bd)
    # White moves diagonally downwards.
    if temp_bd[row_index][col_index] == 'w':
        # Unlike move forward we also want to be sure that
        # we are within the horizontal boundaries as well.
        if row_index < bd_size - 2 and col_index < bd_size - 2 and temp_bd[row_index+1][col_index+1] == 'b':
            temp_bd[row_index+1][col_index-1] = 'w'
            temp_bd[row_index][col_index] = '-'
            
    # Black moves diagonally upwards.
    elif temp_bd[row_index][col_index] == 'b':
        if row_index > 0 and col_index < bd_size - 2 and temp_bd[row_index-1][col_index+1] == 'w':
            temp_bd[row_index-1][col_index-1] = 'b'
            temp_bd[row_index][col_index] = '-'
            
    return temp_bd

'''
//////////////////////
/// BOARD EVALUTOR ///
//////////////////////
'''

# It reads the current board state and returns a value indicating who is in
# the current lead, either white or black. It takes in all the board information
# e.g. the piece locations, size of the board, and what color the player is.
def static_board_evaluator(bd_state, bd_size, my_color):
    # Check if either white or black has won and return a value accordingly.
    winning_color = 'n'
    white_count = 0
    black_count = 0
    row_index = 0
    for row in bd_state:
        for col in row:
            # Black wins if any of its pawns are at the top row.
            if row_index == 0 and col == 'b':
                winning_color = 'b'
            # White wins if any of its pawns are at the bottom row.
            elif row_index == bd_size - 1 and col == 'w':
                winning_color = 'w'

            # Keep track of the # of colored pawns there are for the board val.
            if col == 'w':
                white_count += 1
            elif col == 'b':
                black_count += 1
                
        row_index += 1

    # Using the default sbe given in lecture ep 13. Changed "10" to bd_size.
    if winning_color == my_color:
        return bd_size
    elif winning_color != 'n':
        return 0 - bd_size
    else:
        if my_color == 'w':
            return white_count - black_count
        elif my_color == 'b':
            return black_count - white_count

    print("Error while executing sbe.")
    return -999

'''
///////////////////////////////////
/////// PARSING THE BOARD /////////
///////////////////////////////////
'''

# Converts the rows (strings) in our board to lists so that they can become mutable.
def str_to_list(board):
    new_board = []
    for row in board:
        temp = []
        temp[:0] = row
        new_board.append(temp)
    return new_board

# Converts list back into strings so printing the board looks cleaner/readable.
def list_to_str(board):
    new_board = []
    for row in board:
        temp = ''
        for i in row:
            temp += i
        new_board.append(temp)
    return new_board
