from cmath import inf
import cv2 as cv
import matplotlib.pyplot as plt
import os

from board_finder import getBoardCoords, imageResize

# https://python-chess.readthedocs.io/en/latest/
# To output again the board

methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
meth = 'cv.TM_CCORR_NORMED'

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
    
def recognize_piece(paths, pieces, cell):  
    max_value = float('-inf')
    max_image_path = ''
    max_image = None
    
    for i in range(len(pieces)):
        piece = pieces[i]
        path = paths[i]
        
        for scale in range(20):
            cell_copy = cell.copy()
            cell_copy = imageResize(cell_copy, 0.1*(scale+1))
            
            # Apply template Matching
            method = eval(meth)
            result = cv.matchTemplate(cell_copy, piece, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv.TM_SQDIFF]:
                max = min_val
            else:
                max = max_val
                
            if max > max_value:
                max_value = max
                max_image = piece
                max_image_path = path
                
    print()
    print(max_image_path)
    print(f"Best: {max_value:.3f}")
    cv.imshow("Board's cell", cell)
    cv.imshow(max_image_path, max_image)
    cv.waitKey(0) 
    cv.destroyAllWindows()

if __name__ == '__main__':
    piece_path = 'pieces/'
    board_path = 'Board_Examples/medium2.png'
    
    board_img = imageResize(cv.imread(board_path), 0.5)
    board_cells_img = getBoardCoords(board_img)
    
    pieces_path, pieces_img = get_pieces_images(piece_path)
    
    # display_pieces(pieces_img, pieces_path)
    
    for cell_img in board_cells_img:
        recognize_piece(pieces_path, pieces_img, cell_img)
