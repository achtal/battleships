import battleships as b
import os


if __name__ == '__main__':
    # todo: welcome message. ascii art?
    # todo: colour text printing
    # todo: check computer will place mines when user places ships
    # game options
    size = input('What size board would you like to play? (5/8/10)')
    random = input("Would you like the computer to randomise your ship placements? (y/N)")
    mines = input('Would you like to play the mine variant? (y/N)')
    p1_name = input("What is Player 1's name?")
    p2_name = input("What is Player 2's name?")
    # build game instances for each player
    p1 = b.Battleships(random, int(size), mines, p1_name)
    p2 = b.Battleships(random, int(size), mines, p2_name)

    if random.lower() != 'y':
        # get fleet positions from players and build the game board
        p1.build_positions()
        p2.build_positions()

    print(f"{p1.name}'s Board:")
    p1.print_attempts_board()
    print()
    print(f"{p2.name}'s Board:")
    p2.print_attempts_board()
    print()

    # play!
    while p1.fleet_size != 0 and p2.fleet_size != 0:
        # get each players shot co-ordinates and execute shot
        # validate co-ordinates before progressing
        while True:
            p1_coord = input(f"{p1.name} - Enter co-ordinate for shot:")
            if p1.validate_coordinate(p1_coord):
                p1.play(p1_coord, p2)
                break
            else:
                print('####################')
                print('Invalid co-ordinate.')
                print('####################')

        while True:
            p2_coord = input(f"{p2.name} - Enter co-ordinate for shot:")
            if p2.validate_coordinate(p2_coord):
                p2.play(p2_coord, p1)
                break
            else:
                print('####################')
                print('Invalid co-ordinate.')
                print('####################')

        # show attempts boards
        os.system('cls')
        b.Battleships.state_of_play(p1, p2)
