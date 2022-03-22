from cmath import inf
import cv2 as cv
import matplotlib.pyplot as plt
import os

# https://python-chess.readthedocs.io/en/latest/
# To output again the board

methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
meth = 'cv.TM_CCORR_NORMED'
pieces_names = ['bishop', 'pawn', 'king', 'queen', 'knight', 'rock']

def get_pieces_images(path):
    black_pieces_path = [f"{path}black_{name}.png" for name in pieces_names]
    white_pieces_path = [f"{path}white_{name}.png" for name in pieces_names]
    pieces_path = [black_pieces_path, white_pieces_path]

    black_pieces_img = [cv.imread(path) for path in black_pieces_path]
    white_pieces_img = [cv.imread(path) for path in white_pieces_path]
    pieces_img = [black_pieces_img, white_pieces_img]
 
    return pieces_path, pieces_img

def get_boards_images(path):
    board_cells_path = [f"{path}{x}" for x in os.listdir(path)]
    board_cells_img = [cv.imread(path) for path in board_cells_path]
    
    return board_cells_path, board_cells_img

def display_pieces(pieces, path):
    print("Pieces:")
    for color in range(2):
        for img in range(6):
            print(path[color][img])
            cv.imshow(path[color][img], pieces[color][img])
    cv.waitKey(0) 
    cv.destroyAllWindows()
    
def recognize_piece(paths, pieces, cell):  
    max_value = float('-inf')
    max_method = ''
    max_image_path = ''
    max_image = None
    
    for color in range(2):
        for img in range(6):
            piece = pieces[color][img]
            # piece = cv.cvtColor(piece, cv.COLOR_BGR2GRAY)
            path = paths[color][img]
            w, h = piece.shape[:-1]
            
            # cell_copy = cv.cvtColor(cell, cv.COLOR_BGR2GRAY)
            cell_copy = cell.copy()
            
            # Apply template Matching
            method = eval(meth)
            result = cv.matchTemplate(cell_copy, piece, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv.TM_SQDIFF]:
                top_left = min_loc
                max = min_val
            else:
                top_left = max_loc
                max = max_val
                
            if max > max_value:
                max_value = max
                max_method = meth
                max_image = piece
                max_image_path = path
                
            # Display the result
            # bottom_right = (top_left[0] + w, top_left[1] + h)
            # cv.rectangle(img, top_left, bottom_right, 255, 2)
            # plt.subplot(221), plt.imshow(res, cmap='gray')
            # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            # plt.subplot(222), plt.imshow(img, cmap='gray')
            # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            # plt.subplot(223), plt.imshow(piece, cmap='gray')
            # plt.title('Piece'), plt.xticks([]), plt.yticks([])
            # plt.suptitle(f"{meth} - {path}")
            # plt.show()
                
    print()
    print(max_image_path)
    print(max_value)
    print(max_method)
    cv.imshow("board's cell", cell)
    cv.imshow(max_image_path, max_image)
    cv.waitKey(0) 
    cv.destroyAllWindows()

if __name__ == '__main__':
    piece_path = 'pieces/'
    board_path = 'board/'
    
    pieces_path, pieces_img = get_pieces_images(piece_path)
    board_cells_path, board_cells_img = get_boards_images(board_path)
    
    # display_pieces(pieces_img, pieces_path)
    
    for cell_img in board_cells_img:
        recognize_piece(pieces_path, pieces_img, cell_img)
