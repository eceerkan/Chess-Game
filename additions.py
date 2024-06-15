import pygame
pygame.init()

from constants import *

#draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'pink', [700 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'pink', [600 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'black', [0,800, WIDTH,100], 5)
        pygame.draw.rect(screen, 'black', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820))
        for i in range(9):
            pygame.draw.line(screen, 'white', (0,100*i), (WIDTH-200, 100*i))
            pygame.draw.line(screen, 'white', (100*i,0), (100*i, HEIGHT-100))
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830)) 
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'white', [0, 800, WIDTH - 200, 100])
            pygame.draw.rect(screen, 'black', [0, 800, WIDTH - 200, 100], 5)
            screen.blit(big_font.render('Promote Pawn', True, 'black'), (20, 820)) 
              
# draw pieces onto board
def draw_pieces():
    
    for i in range(len(white_pieces)):
        
        # display the white pieces
        index = piece_list.index(white_pieces[i])
        if white_pieces[i]=='pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 16, white_locations[i][1] * 100 + 15))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10 ))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'black', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)
                
        # display the black pieces 
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i]=='pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 16, black_locations[i][1] * 100 + 15))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step > 2:
            if selection == i:
                pygame.draw.rect(screen, 'black', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)
                

# function to check all pieces' valid options on board    
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)    
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)  
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn) 
        all_moves_list.append(moves_list)      
    return all_moves_list
       
# check valid rook moves
def check_rook(position,colour):
    moves_list= []
    if colour == 'white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        
        enemies_list=white_locations
        friends_list=black_locations

    for i in range(4):  # down, up, right, left
        # if we have a clear path, chain is 1
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check valid knight moves
def check_knight(position, colour):
    moves_list = []
    if colour == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check valid bishop moves
def check_bishop(position,colour):
    moves_list= []
    if colour == 'white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        
        enemies_list=white_locations
        friends_list=black_locations

    for i in range(4):  # up-right, up-left, down-right, down-left
        # if we have a clear path, chain is 1
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check valid pawn moves
def check_pawn(position, colour):
    moves_list = []
    if colour == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # check en passant move
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # check en passant move
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list
    
# check valid queen moves
def check_queen(position, colour):
    # queen's movement is a combination of bishop's and rook's
    moves_list = check_bishop(position, colour)
    second_list = check_rook(position, colour)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

# check valid king moves
def check_king(position, colour):
    moves_list = []
    if colour == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen, "gold", (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
      
# draw captures pieces on the side of the screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50*i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


# check en passant 
def check_enpassant(old_coords, new_coords):
    if turn_step<=1:
        index= white_locations.index(old_coords)
        ep_coords=(new_coords[0], new_coords[1]-1)
        piece=white_pieces[index]
    else:
        index= black_locations.index(old_coords)
        ep_coords=(new_coords[0], new_coords[1]+1)
        piece=black_pieces[index]  
    if piece == 'pawn' and abs(old_coords[1]-new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        ep_coords=(100,100)
    return ep_coords

# pawn promotion
def check_pawnpromotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index= 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index
            
def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
    if white_promote:
        colour= 'white'
        index= piece_list.index('queen')
        screen.blit(white_images[index], (860, 5 + 100))   
    elif black_promote:
        colour= 'black'
        index= piece_list.index('queen')
        screen.blit(black_images[index], (860, 5 + 100)) 
    pygame.draw.rect(screen, colour, [800, 0, 200, 420], 8)   
 
def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = 'queen'
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = 'queen'    
        
            
# main game loop
black_options = check_options(black_pieces,black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run=True

while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter=0

    screen.fill('white')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if not game_over:
        white_promote, black_promote, promo_index= check_pawnpromotion()
        if white_promote or black_promote:
            draw_promotion() 
            check_promo_select()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # x coordinate of the click divided by 100, due to the size of each square
            x_coord = event.pos[0] // 100
            # y coordinate of the click divided by 100, due to the size of each square
            y_coord = event.pos[1] // 100
            click_coords=(x_coord,y_coord)
            
            if turn_step <= 1:
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'black'
                # if statement runs when the whites' player selects a white piece
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step== 0:
                        turn_step=1
                # if statement runs when the whites' player selects a destination square for the selected white piece
                if click_coords in valid_moves and selection != 100 :
                    white_ep = check_enpassant(white_locations[selection], click_coords)
                    white_locations[selection]=click_coords
                    if click_coords in black_locations:
                        # get the index of the captured black piece in the black_pieces
                        black_piece=black_locations.index(click_coords)
                        # add the captured black pieces into captured_pieces_white and remove the piece from list of black pieces and their locations
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece]== 'king':
                            winner='white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    # en passant piece capture
                    if click_coords == black_ep:
                        # get the index of the captured black piece in the black_pieces
                        black_piece=black_locations.index((black_ep[0], black_ep[1]-1))
                        # add the captured black pieces into captured_pieces_white and remove the piece from list of black pieces and their locations
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        
                    black_options = check_options(black_pieces,black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    # now it is black's turn
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            
            if turn_step > 1:
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'white'
                # if statement runs when the blacks' player selects a black piece
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step== 2:
                        turn_step=3
                # if statement runs when the blacks' player selects a destination square for the selected black piece
                if click_coords in valid_moves and selection != 100 :
                    black_ep = check_enpassant(black_locations[selection], click_coords)
                    black_locations[selection]=click_coords
                    if click_coords in white_locations:
                        # get the index of the captured white piece in the white_pieces
                        white_piece=white_locations.index(click_coords)
                        # add the captured white pieces into captured_pieces_black and remove the piece from list of white pieces and their locations
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece]== 'king':
                            winner='black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    # en passant piece capture
                    if click_coords == white_ep:
                        # get the index of the captured white piece in the white_pieces
                        white_piece=white_locations.index((white_ep[0], white_ep[1]+1))
                        # add the captured white pieces into captured_pieces_black and remove the piece from list of white pieces and their locations
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces,black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    # now it is white's turn
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                # game variables and images
                white_pieces = ['rook', 'knight','bishop','king','queen','bishop','knight','rook', 
                                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

                black_pieces = ['rook', 'knight','bishop','king','queen','bishop','knight','rook', 
                                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves=[]
                black_options = check_options(black_pieces,black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
    
    if winner != '':
        game_over = True
        draw_game_over()   
            
    pygame.display.flip()
    
pygame.quit()
