import pygame
import sys

WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()


FONT = pygame.font.SysFont(None, 40)

# Board
board = [['' for _ in range(COLS)] for _ in range(ROWS)]

def draw_board():
    WIN.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            if board[row][col] == 'X':
                pygame.draw.line(WIN, RED, (col*SQUARE_SIZE + 10, row*SQUARE_SIZE + 10), 
                                 (col*SQUARE_SIZE + SQUARE_SIZE - 10, row*SQUARE_SIZE + SQUARE_SIZE - 10), 3)
                pygame.draw.line(WIN, RED, (col*SQUARE_SIZE + 10, row*SQUARE_SIZE + SQUARE_SIZE - 10), 
                                 (col*SQUARE_SIZE + SQUARE_SIZE - 10, row*SQUARE_SIZE + 10), 3)
            elif board[row][col] == 'O':
                pygame.draw.circle(WIN, BLUE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//2 - 10, 3)
    pygame.display.update()

def is_winner(board, player):
    for row in range(ROWS):
        if all(cell == player for cell in board[row]):
            return True
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    
    if all(board[i][i] == player for i in range(ROWS)):
        return True
    if all(board[i][COLS-i-1] == player for i in range(ROWS)):
        return True
    return False

def is_board_full(board):
    return all(cell != '' for row in board for cell in row)

def get_empty_cells(board):
    return [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == '']

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'X'):
        return -10 + depth, None
    elif is_winner(board, 'O'):
        return 10 - depth, None
    elif is_board_full(board):
        return 0, None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for row, col in get_empty_cells(board):
            board[row][col] = 'O'
            score, _ = minimax(board, depth + 1, False)
            board[row][col] = ''
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for row, col in get_empty_cells(board):
            board[row][col] = 'X'
            score, _ = minimax(board, depth + 1, True)
            board[row][col] = ''
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move

def main():
    turn = 'X'
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 'X':
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // SQUARE_SIZE
                    col = mouse_pos[0] // SQUARE_SIZE
                    if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == '':
                        board[row][col] = turn
                        if is_winner(board, turn):
                            draw_board()
                            print("You win!")
                            game_over = True
                        elif is_board_full(board):
                            draw_board()
                            print("It's a tie!")
                            game_over = True
                        else:
                            turn = 'O'
                        draw_board()
        if turn == 'O' and not game_over:
            _, (row, col) = minimax(board, 0, True)
            board[row][col] = turn
            if is_winner(board, turn):
                draw_board()
                print("AI wins!")
                game_over = True
            elif is_board_full(board):
                draw_board()
                print("It's a tie!")
                game_over = True
            else:
                turn = 'X'
            draw_board()
main()
