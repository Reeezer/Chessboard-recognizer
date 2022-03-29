import os
import shutil
from PIL import Image

def get_images(pieces_path, backgrounds_path):
    pieces_paths = [piece_path for piece_path in os.listdir(pieces_path)]
    pieces_img = [Image.open(os.path.join(pieces_path, piece_path)) for piece_path in pieces_paths]
    
    backgrounds_paths = [background_path for background_path in os.listdir(backgrounds_path)]
    backgrounds_img = [Image.open(os.path.join(backgrounds_path, background_path)) for background_path in backgrounds_paths]
    
    return pieces_img, pieces_paths, backgrounds_img, backgrounds_paths

def create_pieces(pieces_img, pieces_path, backgrounds_img, backgrounds_path):
    created_pieces_img = []
    created_pieces_path = []
    
    for bg_i in range(len(backgrounds_img)):
        for piece_i in range(len(pieces_img)):
            new_path = f"{pieces_path[piece_i][:-4]}_{backgrounds_path[bg_i][:-4]}.png"
            
            background = backgrounds_img[bg_i]
            piece = pieces_img[piece_i]
            
            new_image = background.copy()
            new_image.paste(piece, (0,0), mask=piece.convert('RGBA'))
            
            created_pieces_img.append(new_image)
            created_pieces_path.append(new_path)
            
    return created_pieces_img, created_pieces_path

def save_pieces(pieces_img, pieces_path, path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)

    [pieces_img[i].save(os.path.join(path, pieces_path[i])) for i in range(len(pieces_img))]

if __name__ == '__main__':
    pieces_path = 'pieces_screens/pieces/'
    backgrounds_path = 'pieces_screens/backgrounds/'
    path = 'pieces/'
    
    pieces_img, pieces_paths, backgrounds_img, backgrounds_paths = get_images(pieces_path, backgrounds_path)
    created_pieces_img, created_pieces_path = create_pieces(pieces_img, pieces_paths, backgrounds_img, backgrounds_paths)
    save_pieces(created_pieces_img, created_pieces_path, path)