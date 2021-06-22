import os
import random
import string
import sys
import re

import numpy as np


class HiddenPrints:
    """
    A class used to prevent prints
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class Fleet:
    """
    A class used to track a fleet
    """
    def __init__(self, size):
        self.fleet_dict = {
            5: [['b', 1], ['c', 1], ['d', 2]],
            8: [['a', 1], ['b', 2], ['c', 1], ['s', 1], ['d', 2]],
            10: [['a', 1], ['b', 2], ['c', 1], ['s', 2], ['d', 4]]
        }

        self.ships = {}
        for item in self.fleet_dict[size]:
            temp = []
            for x in range(item[1]):
                if item[0] == 'a':
                    temp.append(AircraftCarrier())
                    self.ships[item[0] + str(x)] = temp[x]
                elif item[0] == 'b':
                    temp.append(Battleship())
                    self.ships[item[0] + str(x)] = temp[x]
                elif item[0] == 'c':
                    temp.append(Cruiser())
                    self.ships[item[0] + str(x)] = temp[x]
                elif item[0] == 's':
                    temp.append(Submarine())
                    self.ships[item[0] + str(x)] = temp[x]
                elif item[0] == 'd':
                    temp.append(Destroyer())
                    self.ships[item[0] + str(x)] = temp[x]


class AircraftCarrier:
    def __init__(self):
        self.health = [1] * 5
        self.name = 'Aircraft Carrier'
        self.size = 5


class Battleship:
    def __init__(self):
        self.health = [1] * 4
        self.name = 'Battleship'
        self.size = 4


class Cruiser:
    def __init__(self):
        self.health = [1] * 3
        self.name = 'Cruiser'
        self.size = 3


class Submarine:
    def __init__(self):
        self.health = [1] * 3
        self.name = 'Submarine'
        self.size = 3


class Destroyer:
    def __init__(self):
        self.health = [1] * 2
        self.name = 'Destroyer'
        self.size = 2


class Battleships:
    def __init__(self, random_board='y', size=10, mines='n', name=''):
        self.size = size
        self.board = np.array([['  '] * size] * size)
        self.attempts = np.array([[' '] * size] * size)
        self.name = name

        board_cols = string.ascii_lowercase[:size]
        board_col_first = board_cols[0]
        board_col_last = board_cols[size - 1]
        self.coord_regex = f"[{board_col_first}-{board_col_last}]([1-9]|10)" if size == 10 else \
            f"[{board_col_first}-{board_col_last}]([1-{size}])"

        self.fleet = Fleet(size)
        self.fleet_size = len(self.fleet.ships)

        # current status message
        self.status = ''
        self.status_messages = []

        if random_board.lower() == 'y':
            # loop through each ship to initialise
            for s in self.fleet.ships.keys():
                while True:
                    # generate a random co-ordinate
                    c = self.random_coordinate()
                    # validate that co-ordinate for current ship is valid
                    with HiddenPrints():
                        valid = self.validate_placement(s, c[0], c[1])

                    if valid:
                        self.place_ship(s, c[0], c[1])
                        break

        if mines.lower() == 'y':
            if size == 5:
                num_mines = 1
            elif size == 8:
                num_mines = 2
            else:
                num_mines = 3

            for i in range(num_mines):
                while True:
                    # generate a random co-ordinate
                    c = self.random_coordinate()
                    # validate co-ordinate is not occupied
                    with HiddenPrints():
                        valid = self.validate_placement('m', c[0], '')

                    if valid:
                        self.place_ship('m', c[0], '')
                        break

    # todo: salvo scenario

    def get_status(self):
        """ Getter method to return current status of player. Used in State of Play method

        :return: Returns string current status message
        :rtype: str
        """
        return self.status

    def set_status(self, status):
        """ Setter method for updating player status message

        :param status: Status message to be set
        :type status: list
        :return: None
        """
        self.status = '\n'.join([msg for msg in status])

    def set_fleet_size(self):
        """ Setter method for updating fleet size

        :return: None
        """
        self.fleet_size = len(self.fleet.ships)

    def validate_coordinate(self, coord):
        """ Validate that provided coordinate is formatted correctly and valid for current board size

        :param coord: Co-ordinate to validate
        :type coord: str
        :return: True for valid coordinate, False otherwise
        :rtype: bool
        """
        return True if re.fullmatch(self.coord_regex, coord) is not None else False

    def build_positions(self):
        """Take user input and place ships on the board

        :return: None
        """
        for s in self.fleet.ships.keys():
            while True:
                self.print_board()
                print(f"Enter starting co-ordinate for {self.fleet.ships[s].name} ({self.fleet.ships[s].size})")
                print(f"e.g a1")
                while True:
                    coord = input("Enter co-ordinate:")
                    if self.validate_coordinate(coord):
                        break
                    else:
                        print('Co-ordinate error! Enter a grid reference as <letter><number> e.g. a1')

                while True:
                    alignment = input(f"Enter 'h' or 'v' to place ship horizontally or vertically:")
                    if alignment.lower() in ('v', 'h'):
                        break
                    else:
                        print('Alignment error! Enter either "v" or "h" to place ship')

                if self.validate_placement(s, coord.lower(), alignment.lower()):
                    self.place_ship(s, coord.lower(), alignment.lower())
                    break

    def print_board(self):
        """Display player board

        :return: None
        """
        print(f"{self.name}'s Fleet:")
        print(f"    {'    '.join(string.ascii_uppercase[:self.size])}")
        for row in range(1, self.size + 1):
            print(f"{str(row).rjust(2)} {str(self.board[row - 1]).replace('[', '').replace(']', '')}")

    def random_coordinate(self):
        """Generate a random ship co-ordinate

        :return: a tuple of strings representing generated co-ordinate
        :rtype: tuple
        """
        letters = string.ascii_lowercase[:self.size]
        return f"{letters[random.randint(0, self.size - 1)]}" \
               f"{random.randint(1, self.size)}", f"{'h' if random.randint(1, 2) == 1 else 'v'}"

    def place_ship(self, ship, coord, alignment):
        """Place a ship on the board

        :param ship: ship to place
        :type ship: str
        :param coord: co-ordinate of starting position of ship
        :type coord: str
        :param alignment: alignment of ship (vertical or horizontal)
        :type alignment: str
        :return: None
        """
        col = ord(coord[:1]) - 97
        row = int(coord[1:]) - 1

        if ship == 'm':
            self.board[row][col] = f'm '
        else:
            for i in range(self.fleet.ships[ship].size):
                if alignment == 'h':
                    self.board[row][col + i] = f'{ship}'
                else:
                    self.board[row + i][col] = f'{ship}'

    def validate_placement(self, ship, coord, alignment):
        """Validate that ship can be placed in the co-ordinates provided

        :param ship: ship to place
        :type ship: str
        :param coord: starting co-ordinate of ship
        :type coord: str
        :param alignment: alignment of ship (horizontal or vertical)
        :type alignment: str
        :return: bool to indicate if ship placement is valid
        :rtype: bool
        """
        col = ord(coord[:1]) - 97
        row = int(coord[1:]) - 1

        valid = True

        if ship == 'm':  # mines
            if self.board[row][col] != '  ':
                valid = False
        else:
            for i in range(self.fleet.ships[ship].size):
                if alignment == 'h':
                    try:
                        if self.board[row][col + i] != '  ':
                            print('####################################################')
                            print('Cannot place ship here. Intersects with another ship')
                            print('####################################################')
                            valid = False
                            break
                    except IndexError:
                        print('#######################################')
                        print('Cannot place ship here. Outside of grid')
                        print('#######################################')
                        valid = False
                        break
                else:
                    try:
                        if self.board[row + i][col] != '  ':
                            print('####################################################')
                            print('Cannot place ship here. Intersects with another ship')
                            print('####################################################')
                            valid = False
                            break
                    except IndexError:
                        print('#######################################')
                        print('Cannot place ship here. Outside of grid')
                        print('#######################################')
                        valid = False
                        break

        return valid

    def play(self, coord, target):
        """Take a target and determine if a enemy ship has been hit

        :param coord: coordinates of shot (e.g. 'a1')
        :type coord: str
        :param target: other player instance to fire against
        :type target: Battleships
        :return: None
        """
        col = ord(coord[:1].lower()) - 97
        row = int(coord[1:]) - 1

        if self.attempts[row][col] == 'X':
            print('You have already fired at this location')
        elif target.board[row][col] == 'm ':  # hit a MINE
            self._mine(coord, target)
        elif target.board[row][col] != '  ':  # if target is not empty (HIT a ship)
            # update player attempt array with successfully hit (X)
            self.attempts[row][col] = 'X'
            # update fleet health
            target.fleet.ships[target.board[row][col]].health.pop()

            # alter status message if a ship has been sunk
            if len(target.fleet.ships[target.board[row][col]].health) == 0:
                self.status_messages.append(f"{coord} : Hit! {target.fleet.ships[target.board[row][col]].name} "
                                            f"({target.fleet.ships[target.board[row][col]].size}) has been sunk!")
                # remove ship from fleet
                target.fleet.ships.pop(target.board[row][col])
            else:
                self.status_messages.append(f"{coord} : Hit!")

        else:  # target is empty (MISS)
            self.attempts[row][col] = 'O'
            self.status_messages.append(f"{coord} : Miss!")

        # set status ready for print
        self.set_status(self.status_messages)
        # clear status_messages list
        self.status_messages.clear()
        # update fleet size
        self.set_fleet_size()

    def _mine(self, coord, target):
        # mine damage radius
        mine_radius = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]

        col = ord(coord[:1].lower()) - 97
        row = int(coord[1:]) - 1

        self.attempts[row][col] = 'M'
        # loop through mine range
        self.status_messages.append(f"{coord} : Hit a mine!")
        for i in range(len(mine_radius)):
            new_row = row + mine_radius[i][0]
            new_col = col + mine_radius[i][1]
            new_coord = chr(new_col + 97) + str(new_row + 1)
            # if mine in first or last row or column then ignore as outside of grid
            # or if mine already discovered
            if new_row < 0 or new_row >= self.size or new_col < 0 or new_col >= self.size \
                    or self.attempts[new_row][new_col] != ' ':
                pass
            else:
                try:
                    if target.board[new_row][new_col] == '  ':  # Nothing
                        self.attempts[new_row][new_col] = 'O'
                    elif target.board[new_row][new_col] == 'm ':  # Hit another mine
                        self._mine(new_coord, target)
                    elif target.board[new_row][new_col] != '  ':  # Ship
                        self.attempts[new_row][new_col] = 'X'
                        self.status_messages.append(f'{new_coord} : Hit from mine!')
                        target.fleet.ships[target.board[new_row][new_col]].health.pop()
                        if len(target.fleet.ships[target.board[new_row][new_col]].health) == 0:
                            self.status_messages.append(f"{target.fleet.ships[target.board[new_row][new_col]].name} "
                                                        f"({target.fleet.ships[target.board[new_row][new_col]].size}) "
                                                        f"has been sunk!")
                            # remove ship from fleet
                            target.fleet.ships.pop(target.board[new_row][new_col])
                except IndexError:
                    pass
        pass

    @staticmethod
    def state_of_play(player1, player2):
        """Print current status of game

        :param player1: Player 1 Battleships instance
        :type player1: Battleships
        :param player2: Player 2 Battleships instance
        :type player2: Battleships
        :return: None
        """
        if player1.fleet_size == 0:
            print()
            print('**************')
            print(f'{player2.name} WINS!')
            print('**************')
            print()
            print(f': {player1.name} Fleet :')
            print()
            player1.print_board()
            print()
            print(f': {player2.name} Fleet :')
            print()
            player2.print_board()
            print()
        elif player2.fleet_size == 0:
            print()
            print('**************')
            print(f'{player1.name} WINS!')
            print('**************')
            print()
            print(f': {player1.name} Fleet :')
            print()
            player1.print_board()
            print()
            print(f': {player2.name} Fleet :')
            print()
            player2.print_board()
            print()
        else:
            print('#############')
            print('State of Play')
            print('#############')
            print()
            print(f'{player1.name} Status ...')
            print(f'{player1.get_status()}')
            player1.print_attempts_board()
            print()
            print(f'{player2.name} Status ...')
            print(f'{player2.get_status()}')
            player2.print_attempts_board()

    def print_attempts_board(self):
        """ Print player previous shots

        :return: None
        """
        print(f"    {'   '.join(string.ascii_uppercase[:self.size])}")
        for row in range(1, self.size + 1):
            print(f"""{str(row).rjust(2)} {str(self.attempts[row - 1]).replace(
                '[', '').replace(']', '').replace("'", " ")}""")
