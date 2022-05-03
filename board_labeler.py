from piece_recognizer import *
from labeler import *
from tensorflow import keras
import numpy as np

dictClasses = {
    "empty": 0,
    "bishop_black": 1,
    "bishop_white": 2,
    "king_black": 3,
    "king_white": 4,
    "knight_black": 5,
    "knight_white": 6,
    "pawn_black": 7,
    "pawn_white": 8,
    "queen_black": 9,
    "queen_white": 10,
    "rook_black": 11,
    "rook_white": 12,
}

# Inverse dictionary with 0=>empty, 1=>black_bishop, 2=>white_bishop, etc.
dctInv = {v: k for k, v in dictClasses.items()}


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
    piece_path = 'all_pieces/'
    counter = 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        for k, v in dictClasses.items():
            os.makedirs(output_dir + k)
    else:
        filesArray = []
        for root, dirs, files in os.walk(output_dir):
            counter += len(files)

    boards_path = getFiles(input_dir)

    pieces_path, pieces_img = get_pieces_images(piece_path)

    model = keras.models.load_model('models/secondmodel')
    for board_path in boards_path:
        board_img = imageResize(cv.imread(board_path), 0.5)

        board_cells_img = getBoardCoords(board_img)
        predictions = model.predict(np.array(board_cells_img))

        for i, im in enumerate(board_cells_img):
            predictionClassName = dctInv[predictions[i].argmax()]

            cv.imwrite(f"{output_dir}{predictionClassName}/{counter}.png", im)
            counter += 1
