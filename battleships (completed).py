import random
import time


# Initializing variables/lists

playboard = ['X'] * 25
botboard = ['?'] * 25

coords = ('A1','A2','A3','A4','A5','B1','B2','B3','B4','B5','C1','C2','C3','C4','C5','D1','D2','D3','D4','D5','E1','E2','E3','E4','E5')
playships = []
botships = []
attacked_bcoords = []
attacked_bships = []
attacked_pcoords = []
attacked_pships = []

playship_coord = None
botship_coord = None
play_atk = None
bot_atk = None
play_victory = None

playships_left = 5
index = 0
turns = 1


# Defining functions

def intro():

    print('Greetings! Welcome to the Battleship Game!')
    print("\nBasically, you'll have to select 5 coordinates to place your ships.")
    print('There will be an enemy with an equal number of ships.')
    print('\nAfter you have selected the coordinates for your ships,')
    print("You will have to guess where your enemy's ships are and attack that coordinate.")
    print('\nYour enemy will do the same, and this will continue until either you or your enemy will only have one ship left.')
    print("First one to destroy four of the other team's ships wins! Good luck!")
    
    input('\nPress enter to start...')
    time.sleep(1)


def display_board(board):   # displays board

    print(f"\nA   {board[0]} | {board[1]} | {board[2]} | {board[3]} | {board[4]}")
    print("    -----------------")
    print(f"B   {board[5]} | {board[6]} | {board[7]} | {board[8]} | {board[9]}")
    print("    -----------------")
    print(f"C   {board[10]} | {board[11]} | {board[12]} | {board[13]} | {board[14]}")
    print("    -----------------")
    print(f"D   {board[15]} | {board[16]} | {board[17]} | {board[18]} | {board[19]}")
    print("    -----------------")
    print(f"E   {board[20]} | {board[21]} | {board[22]} | {board[23]} | {board[24]}")
    print('\n    1   2   3   4   5\n')


def player_set():   # sets player ships

    playships_left = 5   # sets num of ship placements

    print('\n------------------------------------------------------------------------')
    print('(Setting up ships)')

    while playships_left > 0:   # runs until player runs out of ship placements
        
        playship_coord = str(input(f'Enter a ship coordinate (A1 - E5) [{playships_left} left]: ')).strip().upper()

        while playship_coord not in coords or playship_coord in playships:
            playship_coord = str(input(f'INVALID! Enter a ship coordinate (A1 - E5) [{playships_left} left]: ')).strip().upper()

        index = coords.index(playship_coord)    # finds the index number of player ship coord in coords
        playboard[index] = 'O'                  # and replaces it with O
        
        playships.append(playship_coord)   # adds player ship coord to a list

        playships_out = str(playships).replace("'","")   # makes player ships suitable for output

        print("Your ships:", playships_out)

        display_board(playboard)

        playships_left -= 1


def bot_set():  # sets bot ships

    for x in range(5):                           # bot chooses 5 random coords for ships
        botship_coord = random.choice(coords)

        while botship_coord in botships:
            botship_coord = random.choice(coords)

        botships.append(botship_coord)      


def player_attack():    # player's turn to attack

    global turns, play_victory

    print('\n------------------------------------------------------------------------')
    print(f'(Turn #{turns})')
    
    play_atk = str(input('Which square to attack? (A1 - E5): ')).strip().upper()

    while play_atk not in coords or play_atk in attacked_bcoords:
        play_atk = str(input('INVALID! Which square to attack? (A1 - E5): ')).strip().upper()

    index = coords.index(play_atk)
        
    attacked_bcoords.append(play_atk)

    if play_atk in botships:   # if player hits an enemy ship
        
        botships.remove(play_atk)
        attacked_bships.append(play_atk)    # updates lists

        botboard[index] = 'Ø'   # updates botboard
        
        print(f"\nWell done! You've successfully landed an attack on an enemy ship at {play_atk}!")

    else:   # if player doesnt hit a ship

        botboard[index] = 'X'

        print("\nNothing there, captain! Keep firing away at our enemy!")

    attacked_bcoords_out = str(attacked_bcoords).replace("'","")   # suitable for output
    attacked_bships_out = str(attacked_bships).replace("'","")

    print('\nCoordinates you have attacked:', attacked_bcoords_out)

    if attacked_bships != []:                                       # only shows after player attacks a ship
        print('Ships you have taken down:', attacked_bships_out)

    display_board(botboard)     # displays bot_board

    
    if len(botships) == 1:   # if player eliminates almost all enemy ships
        
        play_victory = 'Y'
        return                  # exits player_attack()

    turns += 1   # increases turns

def bot_attack():   # bot's turn to attack

    global play_victory

    if play_victory != None:
        return                  # exits bot_attack() if player wins/loses

    print('\n------------------------------------------------------------------------')
    print('The enemy is thinking of a square to attack\n...')

    bot_atk = random.choice(coords)

    while bot_atk in attacked_pcoords:   # only attacks coords it hasnt attacked
        bot_atk = random.choice(coords)

    index = coords.index(bot_atk)

    attacked_pcoords.append(bot_atk)
    time.sleep(1.25)


    if bot_atk in playships:        # if bot attacks a player ship
        
        playships.remove(bot_atk)

        playboard[index] = 'Ø'

        print(f'The enemy has attacked your ship on {bot_atk}!')

    else:   # if bot didnt attack a ship

        print(f'The enemy has attacked {bot_atk}! No ships there!')

    playships_out = str(playships).replace("'","")   # suitable for output

    print('\nYour remaining ships:', playships_out)

    display_board(playboard)

    if len(playships) == 1:   # if almost all player ships are destroyed

        play_victory = 'N'
        return                  # exits bot_attack()

    time.sleep(1)
        

def game():

    bot_set()
    player_set()

    while play_victory == None:    # runs until one side wins
        
        player_attack()
        bot_attack()

    time.sleep(1)

    print('\n------------------------------------------------------------------------')
    print('(End Result)\n')
    time.sleep(1)

    if play_victory == 'Y':   # if player wins

        if len(playships) == 5:     # if player doesnt lose any ships
            print('Congratulations! You won without losing any ships! Crazy luck!')

        elif len(playships) == 2:   # if player nearly loses
            print('Close call! You won with only 2 ships left!')

        else:
            print(f'Great job! You won with {len(playships)} ships left!')

    else:   # if player loses

        print('Game over! Nearly all of your ships have sunk.')
        

# Running game

intro()

game()











