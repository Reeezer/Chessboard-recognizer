from piece_recognizer import *
from labeler import *

def get_files_in_dir(inputDir):
    filesArray = []

    for _root, dirs, _files in os.walk(inputDir):
        for dir in dirs:
            for _root, _dirs, files in os.walk(inputDir + dir):
                for file in files:
                    filesArray.append(inputDir + dir + '/' + file)
    
    return filesArray

def getFiles(inputDir):
    filesArray = []

    for _root, _dirs, files in os.walk(inputDir):
        for file in files:
            filesArray.append(inputDir + file)
    
    return filesArray

if __name__ == '__main__':
    output_dir = 'labeledConstSize/'
    input_dir = 'unlabeled_boards/'
    piece_path = 'pieces/'
    counter = 0
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        filesArray = []
        for root, dirs, files in os.walk(output_dir):
            counter += len(files)
    
    boards_path = getFiles(input_dir)
    
    for board_path in boards_path:
        board_img = imageResize(cv.imread(board_path), 0.5)

        board_cells_img = getBoardCoords(board_img)
        
        pieces_path, pieces_img = get_pieces_images(piece_path)
        
        for cell_img in board_cells_img:
            piece_name = recognize_piece(pieces_path, pieces_img, cell_img, labeling=True)
            
            cv.imwrite(f"{output_dir}{piece_name[:-4]}/{counter}.png", cell_img)
            counter += 1
    