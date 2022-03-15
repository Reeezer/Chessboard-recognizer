import cv2 as cv
import matplotlib.pyplot as plt

pieces_names = ['bishop', 'pawn', 'king', 'queen', 'knight', 'rock']

black_pieces_path = [f"pieces/black_{name}.png" for name in pieces_names]
white_pieces_path = [f"pieces/white_{name}.png" for name in pieces_names]
pieces_path = [black_pieces_path, white_pieces_path]

print("Paths:")
print(black_pieces_path)
print(white_pieces_path)

black_pieces_img = [cv.imread(path) for path in black_pieces_path]
white_pieces_img = [cv.imread(path) for path in white_pieces_path]
pieces_img = [black_pieces_img, white_pieces_img]

for color in range(2):
	for img in range(len(black_pieces_img)):
		print(pieces_path[color][img])
		cv.imshow(pieces_path[color][img], pieces_img[color][img])
		
cv.waitKey(0) 
cv.destroyAllWindows()