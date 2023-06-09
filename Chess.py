# import chess
import pygame as p
import ChessEngine
import WardChessAi


p.init()
board_width = board_height = 512
move_log_panel_width = 250
move_log_panel_height = board_height
dimension = 8
sq_Size = board_height // dimension
max_FPS = 15
images = {}


def loadImages():
    pieces = ['wp', 'wK', 'wR', 'wB', 'wQ', 'wN', 'p', 'k', 'r', 'b', 'q', 'n']
    for piece in pieces:
        images[piece] = p.image.load(f'ChessPieces/{piece}.png')


def main():
    p.init()
    loadImages()
    screen = p.display.set_mode(
        (board_width + move_log_panel_width, board_height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Helvetica", 12, False, False)
    gs = ChessEngine.gameState()
    running = True
    animate = False
    sq_Selected = ()
    player_Clicked = []
    validMoves = gs.getValidMoves()
    stockfish_bool = False  # True if you want to play against stockfish
    moveMade = False
    gameOver = False
    playerOne = True  # human = white if true
    playerTwo = False  # human = black if true

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (
            not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//sq_Size
                    row = location[1]//sq_Size
                    if row in numberConvert:
                        newrow = numberConvert[row]
                    if sq_Selected == (newrow, col) or col >= 8:
                        sq_Selected == ()
                        player_Clicked == []
                    else:
                        sq_Selected = (newrow, col)
                        player_Clicked.append(sq_Selected)
                    if len(player_Clicked) == 2:
                        move = ChessEngine.Move(
                            player_Clicked[0], player_Clicked[1], gs.board)
                        if str(move.pieceMoved) != "None":
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sq_Selected = ()
                                    player_Clicked = []
                            if not moveMade:
                                player_Clicked = [sq_Selected]
                        else:
                            sq_Selected = ()
                            player_Clicked = []
                    check = gs.board.piece_at(newrow * 8 + col)
                    if str(check) == 'None':
                        sq_Selected = ()
                        player_Clicked = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    animate = False
                    moveMade = True
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.gameState()
                    validMoves = gs.getValidMoves()
                    sq_Selected = ()
                    player_Clicked = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI
        if not gameOver and not humanTurn:
            if stockfish_bool == False:
                aiMove = WardChessAi.findBestMove(gs, validMoves)
                if aiMove == None:
                    aiMove = WardChessAi.findRandomMove(validMoves)
                gs.makeMove(aiMove)
                moveMade = True
                animate = True
            else:
                print('stockfish')

        if moveMade:
            validMoves = gs.getValidMoves()
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sq_Selected, moveLogFont)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "BLACK WINS BY CHECKMATE")
            if not gs.whiteToMove:
                drawText(screen, "WHITE WINS BY CHECKMATE")
        if gs.stalemate:
            gameOver = True
            drawText(screen, "STALEMATE")
        clock.tick(max_FPS*3)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sq_Selected):
    if sq_Selected != ():
        r, c = sq_Selected
        if gs.board.color_at(r * 8 + c) == (True if gs.whiteToMove else False):
            s = p.Surface((sq_Size, sq_Size))
            s.set_alpha(255)
            s.fill(p.Color('light blue'))
            newr = numberConvert[r]
            screen.blit(s, (c * sq_Size, newr * sq_Size))
            s.set_alpha(100)
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    newEndRow = numberConvert[move.endRow]

                    screen.blit(
                        s, (move.endCol * sq_Size, newEndRow * sq_Size))


def animateMove(move, screen, board, clock):
    global colors
    dR = numberConvert[move.endRow] - numberConvert[move.startRow]
    dC = move.endCol - move.startCol
    if abs(dR) != 0 and abs(dC) != 0:
        framesPerSquare = 2
    else:
        framesPerSquare = 3
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (numberConvert[move.startRow] + dR * frame /
                frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(numberConvert[move.endRow] + move.endCol) % 2]
        endSqaure = p.Rect(
            move.endCol * sq_Size, numberConvert[move.endRow] * sq_Size, sq_Size, sq_Size)
        p.draw.rect(screen, color, endSqaure)
        if str(move.peiceCaptured) != 'None':
            if str(move.peiceCaptured) in convert:
                imagePieceCaptured = convert[str(move.peiceCaptured)]
                screen.blit(images[imagePieceCaptured], endSqaure)
            if move.peiceCaptured in images:
                screen.blit(images[move.peiceCaptured], endSqaure)
        if str(move.pieceMoved) in convert:
            imagePieceMoved = convert[str(move.pieceMoved)]
            screen.blit(images[imagePieceMoved], p.Rect(
                c*sq_Size, r * sq_Size, sq_Size, sq_Size))
        if str(move.pieceMoved) in images:
            screen.blit(images[str(move.pieceMoved)], p.Rect(
                c*sq_Size, r * sq_Size, sq_Size, sq_Size))
        p.display.flip()
        clock.tick(60)


def drawGameState(screen, gs, validMoves, sq_Selected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sq_Selected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    global colors
    #colors = [p.Color("WhiteSmoke"), p.Color(165, 175, 180)]

    # brown colors
    colors = [p.Color(245+10, 222+10, 179+10), p.Color(160+10, 100+10, 45+15)]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*sq_Size, r*sq_Size, sq_Size, sq_Size))


convert = {
    'R': 'wR',
    'P': 'wp',
    'N': 'wN',
    'Q': 'wQ',
    'B': 'wB',
    'K': 'wK'
}

numberConvert = {
    0: 7,
    1: 6,
    2: 5,
    3: 4,
    4: 3,
    5: 2,
    6: 1,
    7: 0,

}


def drawPieces(screen, board):
    for r in range(0, 8, 1):
        for c in range(0, 8, 1):
            piece = board.piece_at(r*8 + c)
            pp = str(piece)
            if pp in convert:
                pp = convert[pp]
            if pp != 'None':
                screen.blit(images[pp], p.Rect(
                    c*sq_Size, (7-r)*sq_Size, sq_Size, sq_Size))


def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 16, True, False)
    textObject = font.render(text, 0, p.Color('black'))
    textLocation = p.Rect(0, 0, board_width, board_height).move(
        board_width/2 - textObject.get_width()/2, board_height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(
        board_width, 0, move_log_panel_width, move_log_panel_height)
    p.draw.rect(screen, p.Color(180, 200, 175), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    padding = 5
    textY = padding
    lineSpacing = 2
    movesPerRow = 3
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + "  "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "   "
        moveTexts.append(moveString)
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]

        textObject = font.render(text, True, p.Color('black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


if __name__ == "__main__":
    main()
