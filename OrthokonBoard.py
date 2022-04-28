# Author: Brian Chamberlain
# Date: 6/1/2021
# Description: Game between two players where each player represents
#              a color on the board and attempts to change all other
#              players pieces to their color

class OrthokonBoard:
    """OrthokonBoard is a game between two players where one player starts
    with 4 red pieces and the other starts with 4 yellow pieces. Players attempt
    to flip the other players pieces to their color. Colors are flipped when
    a player moves their piece next to (orthogonally) the other players piece.
    A player has won when all pieces are their color or a player cannot
    move their piece"""

    def __init__(self):
        """Create parameters for game such as current state of game and the
        game board for the game to be played on"""
        self._current_state = 'UNFINISHED'
        self._game_board = [
            ['r', 'r', 'r', 'r'],
            ['', '', '', ''],
            ['', '', '', ''],
            ['y', 'y', 'y', 'y']
        ]

    def get_current_state(self):
        """Returns the current state of the game - UNFINISHED, RED_WON OR
        YELLOW_WON"""
        return self._current_state

    def _print_board(self):
        """Prints the 4x4 game board at current state of the game"""
        print(self._game_board)

    def make_move(self, row_current, col_current, row_new, col_new):
        """Make_move takes the current location of the piece to be moved
        and the location of the piece to be moved to. It determines if the
        move is valid and if it is will move the piece"""

        move_loc = self._game_board[row_new][col_new]
        # available_moves is called to make sure that each player in the game has moves
        # that can be made prior to attempting to make the move
        self._current_state = self._available_moves()
        # check to make sure move location is within board boundary
        if 3 < row_new < 0 or 3 < col_new < 0:
            return False
        # verify that player is moving a piece and not a blank square
        elif self._game_board[row_current][col_current] == '':
            return False
        # verify the piece is not being moved to a square with a piece already there
        elif move_loc == 'y' or move_loc == 'r':
            return False
        # verify that the piece is actually moved
        elif row_new == row_current and col_new == col_current:
            return False
        # verify that the game is still in an UNFINISHED state to make a move
        elif self._current_state != 'UNFINISHED':
            return False
        else:
            # _valid_move is called to verify the move is valid for more complicated scenarios
            valid_move = self._valid_move(row_current, col_current, row_new, col_new)
            if valid_move == False:
                return False
            # if the all checks are complete, the move is valid and the move location
            # is set to the current location color
            self._game_board[row_new][col_new] = self._game_board[row_current][col_current]
            # set the current location to blank
            self._game_board[row_current][col_current] = ''
            # determine if colors need to be flipped from the move by calling _flip_colors
            self._flip_colors(row_new, col_new)
            # set the current state to determine if a player has won
            self._current_state = self._set_current_state()
            # return true to signify a valid move
            return True

    def _available_moves(self):
        """Private method _available_moves loops through the board and verifies that each
        player has a move they can make - meaning their pieces are not blocked by the
        opposing player. If a player has no possible moves the current state of the
        game is updated accordingly"""

        # direction list is used to check all surrounding squares around the piece to be checked
        direction_list = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        possible_y_moves = 0
        possible_r_moves = 0
        # row_num will keep track of the row in the board
        row_num = 0
        # a double for loop is used to loop through each square in the game
        for row in self._game_board:
            #col_num will keep track of the column in the board
            col_num = 0
            for col in row:
                # if statement checks to make sure the square has a piece
                if self._game_board[row_num][col_num] != '':
                    # another for loop is entered to check all surrounding directions of piece
                    for dir in direction_list:
                        # if statements verify that the directions being checked are within the
                        # boundary of the board
                        if 0 <= row_num + dir[0] <= 3:
                            if 0 <= col_num + dir[1] <= 3:
                                # if a surrounding square is blank, there is a possible move
                                if self._game_board[row_num + dir[0]][col_num + dir[1]] == '':
                                    if self._game_board[row_num][col_num] == 'y':
                                        possible_y_moves += 1
                                    else:
                                        possible_r_moves += 1
                # iterate through column in inner loop
                col_num += 1
            # iterate through row in outer loop
            row_num += 1

        # if a blank square wasn't found around one of the players, the current state is updated
        # to show the other player won
        if possible_y_moves == 0:
            return 'RED_WON'
        elif possible_r_moves == 0:
            return 'YELLOW_WON'
        else:
            return 'UNFINISHED'

    def _valid_move(self, row_current, col_current, row_new, col_new):
        """_valid_move is a private function to make sure the piece is moved as far
        orthogonally or diagonally as it can go and that the player is not making
        a move through another piece"""

        # row move and col move will check how far the piece is moved
        row_move = row_new - row_current
        col_move = col_new - col_current
        # the first conditional checks if the piece is moved up and down validly
        if row_move != 0 and col_move == 0:
            # if the piece was moved up and the above square is blank, the piece did not move
            # as far as possible
            if row_move > 0 and row_new != 3 and self._game_board[row_new + 1][col_new] == '':
                return False
            # the same check is made if the piece is moved down and the square below is blank
            elif row_move < 0 and row_new != 0 and self._game_board[row_new - 1][col_new] == '':
                return False
            # verify if the move was more than 1 square that the square it moved through was blank
            if row_move > 1:
                if self._game_board[row_new - 1][col_new] != '':
                    return False
                # if move was 3 squares verify all squares moved through were blank
                if row_move > 2:
                    if self._game_board[row_new - 2][col_new] != '':
                        return False
            # the same check is performed for pieces moving down
            elif row_move < -1:
                if self._game_board[row_new + 1][col_new] != '':
                    return False
                if row_move < -2:
                    if self._game_board[row_new + 2][col_new] != '':
                        return False
        # the same series of checks is performed for pieces moving side to side to make sure
        # the piece moved in a valid way, for left and right moving pieces
        elif col_move != 0 and row_move == 0:
            if col_move > 0 and col_new != 3 and self._game_board[row_new][col_new + 1] == '':
                return False
            elif col_move < 0 and col_new != 0 and self._game_board[row_new][col_new - 1] == '':
                return False
            if col_move > 1:
                if self._game_board[row_new][col_new - 1] != '':
                    return False
                if col_move > 2:
                    if self._game_board[row_new][col_new - 2] != '':
                        return False
            elif col_move < -1:
                if self._game_board[row_new][col_new + 1] != '':
                    return False
                if col_move < -2:
                    if self._game_board[row_new][col_new + 2] != '':
                        return False
        else:
            # This if statement verifies that they moved to a valid location
            # so for example, they cannot move from 0, 0 to 1, 2 or 2, 1 'diagonally'
            # in all diagonal moves the amount of rows moved must equal amount of columns moved
            if abs(row_move) != abs(col_move):
                return False
            # the same check is made for all diagonal moves to verify that it was moved as far as
            # possible and a piece was not moved through to get there. There are 4 possible directions
            # a piece can be moved diagonally so the check is done 4 times
            if col_move > 0 and row_move > 0:
                if col_new != 3 or row_new != 3:
                    if self._game_board[row_new + 1][col_new + 1] == '':
                        return False
                # since row_move and col_move should be equal, only row move needs to be checked in
                # conditional
                if row_move > 1:
                    if self._game_board[row_new - 1][col_new - 1] != '':
                        return False
                    if row_move > 2:
                        if self._game_board[row_new - 2][col_new - 2] != '':
                            return False
            elif col_move < 0 and row_move > 0:
                if col_new != 0 or row_new != 3:
                    if self._game_board[row_new + 1][col_new - 1] == '':
                        return False
                if row_move > 1:
                    if self._game_board[row_new - 1][col_new + 1] != '':
                        return False
                    if row_move > 2:
                        if self._game_board[row_new - 2][col_new + 2] != '':
                            return False
            elif col_move > 0 and row_move < 0:
                if col_new != 3 or row_new != 0:
                    if self._game_board[row_new - 1][col_new + 1] == '':
                        return False
                if row_move < -1:
                    if self._game_board[row_new + 1][col_new - 1] != '':
                        return False
                    if row_move < -2:
                        if self._game_board[row_new + 2][col_new - 2] != '':
                            return False
            elif col_move < 0 and row_move < 0:
                if col_new != 0 or row_new != 0:
                    if self._game_board[row_new - 1][col_new - 1] == '':
                        return False
                if row_move < -1:
                    if self._game_board[row_new + 1][col_new + 1] != '':
                        return False
                    if row_move < -2:
                        if self._game_board[row_new + 2][col_new + 2] != '':
                            return False

    def _flip_colors(self, x_coord, y_coord):
        """Private function _flip_colors is used to determine if the location that the
        player has moved to has pieces of the other color next to it (orthogonally) and
        flips those colors"""

        # direction list checks all squares orthogonally next to the square where the player moved
        direction_list = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        # a for loop is entered to check all squares next to the move location
        for dir in direction_list:
            # if statements verify that the square to be checked is within the game board boundary
            if 0 <= x_coord + dir[0] <= 3:
                if 0 <= y_coord + dir[1] <= 3:
                    # initialize surrounding_square to the direction we are checking
                    surrounding_square = self._game_board[x_coord + dir[0]][y_coord + dir[1]]
                    # if the square isn't blank or the same value as the square that was just moved to
                    # the square will be flipped to the other color
                    if surrounding_square != self._game_board[x_coord][y_coord] and surrounding_square != '':
                        self._game_board[x_coord + dir[0]][y_coord + dir[1]] = self._game_board[x_coord][y_coord]

    def _set_current_state(self):
        """Private method set_current_state verifies that the players have pieces left. If they
        do not, the other team wins"""
        r_count = 0
        y_count = 0
        # loop through all squares in the board and keep track of the count of red and yellow pieces
        for row in self._game_board:
            for element in row:
                if element == 'r':
                    r_count += 1
                elif element == 'y':
                    y_count += 1
        # if there are no pieces of one color, update the game state to the other player winning.
        # otherwise the game state remains unfinished
        if r_count == 0:
            return 'YELLOW_WON'
        elif y_count == 0:
            return 'RED_WON'
        else:
            return 'UNFINISHED'
