import pygame
import random
import socket
import threading
import time
# Initialize Pygame
pygame.init()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 1337
s.connect((HOST, PORT))
# Set up the game window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Obstruction")

# Set up the game board
BOARD_SIZE = 8
CELL_SIZE = 80
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
msg =""
# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
playerSymbol = 0
FONT = pygame.font.SysFont("Arial", 72)
# Draw the game board on the screen
# Draw the game board on the screen
# Draw the game board on the screen
def draw_board():
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Draw the cell
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(screen, BLACK, cell_rect, 1)
            if board[row][col] == 3:
                pygame.draw.rect(screen, GREY, cell_rect.inflate(-10, -10))

            # Draw the player symbol
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, cell_rect.center, CELL_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.rect(screen, BLUE, cell_rect.inflate(-10, -10))

def player_move(row, col, playerSymbol):
    if board[row][col] == 3:
        return False
    elif board[row][col] == 0:
        board[row][col] = 1
        # Make adjacent and diagonal cells unplayable
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < BOARD_SIZE and 0 <= col+j < BOARD_SIZE:
                    board[row+i][col+j] = 3
        if playerSymbol == 1:
            board[row][col] = 1
        else:
            board[row][col] = 2
        return True
    else:
        return False
def printText(text):
    text = FONT.render(text, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    quit()
# Check for a winner
def check_winner(player_turn):
    if any(0 in row for row in board):
        return None
    else:
        if player_turn:
            return 1
        else:
            return 2

def receive_msg():
    global msg
    global playerSymbol
    global board
    while True: 
        try:
            msg = s.recv(1024).decode()
            print("msg received: " + msg)
            if msg == "Board":
                print("Board received")
                
                data = s.recv(1024).decode()
                print("data received: " + data)
                board = eval(data)
            if msg == "1":
                print("You are player 1")
                playerSymbol = 1
            if msg == "2":
                print("You are player 2")
                playerSymbol = 2
            if msg == "You win!":
                print("You win!")
                s.close()
                break
            if msg == "You lose!":
                print("You lose!")
                s.close()
                break
            
        except Exception as e:
            print(e)
            print("An error occured!")
            s.close()
            break

# Initialize the winner variable
winner = None
receiving_thread = threading.Thread(target=receive_msg)
receiving_thread.start()
# Create a game loop to keep the game running
running = True
player_turn = True
while running:

    if msg == "You win!":
        
        print("You win!")
        pygame.display.set_caption("Obstruction - You win!")
        printText("You win!")
        running = False
    if msg == "You lose!":
        pygame.display.set_caption("Obstruction - Opponent wins!")
        printText("Opponent wins!")
        running = False
        
    if msg == "Your turn":
        pygame.display.set_caption("Obstruction - Your turn")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and player_turn:
            # Get the row and column of the clicked cell
                row = event.pos[1] // CELL_SIZE
                col = event.pos[0] // CELL_SIZE
                if player_move(row, col, playerSymbol):
                    winner = check_winner(player_turn)
                    s.send(str(f"{row},{col}").encode())
                    if winner is not None:
                        running = False
                    else:
                        player_turn = False
                        pygame.display.set_caption("Obstruction - Opponent's turn")
             
                        
                winner = check_winner(player_turn)
                if winner is not None:
                    running = False
                else:
                    player_turn = True
            if winner is not None:
                if winner == 0:
                    print("Tie!")
                elif winner == 1:
                    print("You win!")
                    pygame.display.set_caption("Obstruction - You win!")
                    printText("You win!")
                else:
                    print("Opponent wins!")
                    pygame.display.set_caption("Obstruction - Opponent wins!")
                    printText("Opponent wins!")
                running = False
    if msg == "Opponent's turn":
        pygame.display.set_caption("Obstruction - Opponent's turn")
    # Draw the game board on the screen
    draw_board()

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()