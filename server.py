import socket
import time
HOST = 'localhost'
PORT = 1337
board = [[0 for _ in range(8)] for _ in range(8)]
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(2)

print("Server started. Waiting for connections...")

# Accept two clients
client1, address1 = server_socket.accept()
print("Player 1 connected:", address1)
client1.send("1".encode())  # Send player number

client2, address2 = server_socket.accept()
print("Player 2 connected:", address2)
client2.send("2".encode())  # Send player number

# Start the game
current_player = client1

def player_move(row, col, playerSymbol):
    if board[row][col] == 3:
        return False
    elif board[row][col] == 0:
        board[row][col] = 1
        # Make adjacent and diagonal cells unplayable
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row+i < 8 and 0 <= col+j < 8:
                    board[row+i][col+j] = 3
        if playerSymbol == 1:
            board[row][col] = 1
        else:
            board[row][col] = 2

def check_winner(current_player):
    if any(0 in row for row in board):
        return None
    else:
        if current_player == client1:
            return 1
        else:
            return 2
        
winner = None
running = True

    
while running:
    try:
        if client1 and client2:
            if winner is not None:
                if winner == 0:
                    print("Tie!")
                elif winner == 1:
                    client1.send("You win!".encode())
                    
                    client2.send("You lose!".encode())
                    running = False
                elif winner == 2:
                    client2.send("You win!".encode())
                    client1.send("You lose!".encode())
                    running = False
            if current_player == client1:
                client1.send("Your turn".encode())
                client2.send("Opponent's turn".encode())
            else:
                client2.send("Your turn".encode())
                client1.send("Opponent's turn".encode())
        # Receive the move from the current player
            move = current_player.recv(1024).decode()
            row,col = move.split(",")
            if client1 == current_player:
                player_move(int(row), int(col), 1)
            else:
                player_move(int(row), int(col), 2)
        # Send the move to the other player
            if current_player == client1:
                client2.send("Board".encode())
                time.sleep(0.1)
                client2.send(str(board).encode())
                time.sleep(0.1)
                winner = check_winner(current_player)
            else:
                client1.send("Board".encode())
                time.sleep(0.1)
                client1.send(str(board).encode())
                time.sleep(0.1)
                winner = check_winner(current_player)
   
            
        # Switch the current player
            if current_player == client1:
                current_player = client2
            else:
                current_player = client1
    except ConnectionResetError:
        
        print("A player left.")
        print("Closing the server...")
        break
# Close the connections
print("Game over.")
print("Closing connections...")
client1.close()
client2.close()
server_socket.close()
