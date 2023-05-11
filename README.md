# Chess.com Board Recognizer

In this image processing project, our goal is to develop an algorithm capable of detecting and recognizing the state of a chessboard found on chess.com. Users can provide a screenshot of the board (with proper shapes and colors of the pieces for our program) to obtain its current state.

By leveraging board recognition from a screenshot, users can employ a bot to play on their behalf, among other potential applications.

## Steps

The first step of the project involves extracting the chessboard from an image and dividing it into individual squares in row-major format. To accomplish this, we apply thresholding on the image in the HSV color space to isolate the chessboard. Then, using Canny edge detection, we can identify the board's contour based on its expected size. Once we know the position and size of the chessboard, we extract it from the image. Subsequently, we repeat the previous steps on the extracted board to extract each square individually. Once all the pieces are found and extracted, we store them in a list to be used in subsequent scripts.

After successfully finding and extracting the individual squares of the board, the next step is to recognize the chess pieces present on each square. Initially, we attempted to use template matching, but it did not yield sufficient accuracy. Instead, we switched to utilizing a deep learning model for piece recognition.

Once the algorithm recognizes the chessboard, we need to display it to the user for analysis or further use. For this purpose, we offer three different display options. The simple display shows the board as a grid of letters in the console, with each letter representing the first letter of the piece's name. The Forsyth-Edwards Notation (FEN) display follows the same rules as the simple display but represents the board state on a single line. Lastly, the image recreation display reconstructs the board by placing the piece and background images next to each other.

## Conclusion

This project enables accurate recognition of the state of a chessboard from a screenshot obtained from chess.com. We implemented multiple methods to continually improve the accuracy of the recognition process, allowing users to nearly perfectly recreate the board state. The various ways of presenting the board state enable users to utilize the code, such as providing the current board state to a bot.

![](https://i.imgur.com/IMjzDgY.png)

![](https://i.imgur.com/hC5M3ez.png)

![](https://i.imgur.com/ghMvc5f.png)
