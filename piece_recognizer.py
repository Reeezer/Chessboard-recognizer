from cmath import inf
import cv2 as cv
import matplotlib.pyplot as plt
import os
import numpy as np

from board_finder import getBoardCoords, imageResize

# https://python-chess.readthedocs.io/en/latest/
# To output again the board

methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
meth = 'cv.TM_CCOEFF_NORMED'
nb_resize = 30


def get_pieces_images(path):
    pieces_path = [piece_path for piece_path in os.listdir(path)]
    pieces_img = [cv.imread(os.path.join(path, piece_path)) for piece_path in pieces_path]
    return pieces_path, pieces_img


def display_pieces(pieces, paths):
    print("Pieces:")
    for i in range(len(pieces)):
        print(paths[i])
        cv.imshow(paths[i], pieces[i])
    cv.waitKey(0)
    cv.destroyAllWindows()


def recognize_piece(paths, pieces, cell, labeling=False):
    max_value = float('-inf')
    max_image_path = ''
    max_image = None

    for i in range(len(pieces)):
        piece = pieces[i]
        path = paths[i]

        wC, hC, _ = cell.shape
        w, h, _ = piece.shape
        for scale in range(nb_resize):
            cell_copy = cell.copy()
            piece_copy = piece.copy()

            ratio = wC / (w - (nb_resize/2) + scale)
            piece_copy = imageResize(piece_copy, ratio)

            # Apply template Matching
            try:
                method = eval(meth)
                result = cv.matchTemplate(cell_copy, piece_copy, method)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if method in [cv.TM_SQDIFF]:
                    max = min_val
                else:
                    max = max_val

                if max > max_value:
                    max_value = max
                    max_image_path = path
                    max_image = piece_copy
            except Exception:
                pass

    if max_value > 0.38:
        if labeling:
            split = max_image_path.split('_')
            return split[0] + '_' + split[1]
        else:
            return from_piece_to_name(max_image_path)
    else:
        if labeling:
            return 'empty'
        else:
            return from_piece_to_name(max_image_path)


def from_piece_to_name(piece_name):
    if piece_name == 'empty':
        return '-'
    else:
        split = piece_name.split('_')

        if split[0] == 'knight':
            piece_letter = 'n'
        else:
            piece_letter = split[0][0]

        if split[1] == 'white':
            return piece_letter.upper()
        else:
            return piece_letter.lower()


def simple_display_board(board):
    print('Simple board display:')
    i = 0
    for piece in board:
        i += 1
        print(f"{piece} ", end="")
        if i % 8 == 0:
            print()
    print()


def forsyth_edward_display_board(board):
    print('Forsyth Edward Notation (FEN) board display:')
    i = 0
    j = 0
    nb_space = 0
    for piece in board:
        i += 1

        if piece == '-':
            nb_space += 1
        else:
            if nb_space > 0:
                print(f"{nb_space}", end="")
                nb_space = 0
            print(f"{piece}", end="")

        if i % 8 == 0:
            j += 1
            if nb_space > 0:
                print(f"{nb_space}", end="")
            nb_space = 0

            if j % 8 != 0:
                print("/", end="")
    print('\n')


def display_recognized_board(board):
    recognized_board = None
    line_image = None
    for i in range(len(board)):
        if i % 8 == 0 and i != 0:
            recognized_board = np.concatenate((recognized_board, line_image), axis=1)
            line_image = None

        print(f"pieces_screens/pieces/{board[i]}.png")
        piece = cv.imread(f"pieces_screens/pieces/{board[i]}.png")
        line_image = np.concatenate((line_image, piece), axis=0)

    cv.imshow('Recognized board', recognized_board)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    piece_path = 'all_pieces/'
    board_path = 'Board_Examples/medium2.png'

    print('Loarding images...')
    board_img = imageResize(cv.imread(board_path), 0.5)
    board_cells_img = getBoardCoords(board_img)

    pieces_path, pieces_img = get_pieces_images(piece_path)

    # display_pieces(pieces_img, pieces_path)

    recognized_board = list()
    print('Recognizing pieces on board...\n')
    for cell_img in board_cells_img:
        recognized_board.append(recognize_piece(
            pieces_path, pieces_img, cell_img))

    simple_display_board(recognized_board)
    forsyth_edward_display_board(recognized_board)

    cv.imshow('Board', board_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
