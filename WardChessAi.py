import chess
import random
import Chess
from functools import cache, lru_cache

pieceScore = {
    'K' : 0, 'Q' : 9, 'R' : 5, "B" : 3, "N" : 3, "P" : 1,
    'k' : 0, 'q' : -9, 'r' : -5, "b" : -3, "n" : -3, "p" : -1,
    'None' : 0
}

blackKnightScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 2, 2, 2, 2, 2, 0],
                    [0, 2, 3, 3, 3, 3, 2, 0],
                    [0, 2, 4, 4, 4, 4, 2, 0],
                    [0, 2, 3, 4, 4, 3, 2, 0],
                    [0, 2, 4, 3, 3, 4, 2, 0],
                    [0, 2, 2, 2, 2, 2, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
whiteKnightScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 2, 2, 2, 2, 2, 0],
                    [0, 2, 4, 3, 3, 4, 2, 0],
                    [0, 2, 4, 4, 4, 4, 2, 0],
                    [0, 2, 3, 4, 4, 3, 2, 0],
                    [0, 2, 4, 3, 3, 4, 2, 0],
                    [0, 2, 2, 2, 2, 2, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
blackPawnScores = [[15, 15, 15, 15, 15, 15, 15, 15],
                    [8, 10, 10, 10, 10, 10, 10, 8],
                    [5, 5, 5, 7, 7, 5, 5, 5],
                    [5, 4, 5, 6, 6, 5, 4, 5],
                    [4, 3, 4, 5, 5, 4, 3, 4],
                    [3, 2, 2, 4, 4, 2, 2, 3],
                    [2, 2, 2, 1, 1, 2, 2, 2],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
whitePawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [2, 2, 2, 1, 1, 2, 2, 2],
                    [3, 3, 3, 4, 4, 3, 3, 3],
                    [4, 3, 4, 5, 5, 4, 3, 4],
                    [5, 4, 5, 6, 6, 5, 4, 5],
                    [5, 5, 5, 7, 7, 5, 5, 5],
                    [8, 10, 10, 10, 10, 10, 10, 8],
                    [15, 15, 15, 15, 15, 15, 15, 15]]
blackBishopScores = [[5, 4, 3, 1, 1, 1, 4, 5],
                    [4, 5, 4, 3, 2, 4, 5, 4],
                    [3, 4, 5, 4, 4, 5, 4, 1],
                    [1, 3, 4, 4, 5, 4, 2, 1],
                    [1, 2, 4, 5, 4, 4, 3, 1],
                    [1, 4, 5, 4, 4, 5, 4, 3],
                    [4, 5, 4, 2, 3, 4, 5, 4],
                    [5, 4, 1, 1, 1, 3, 4, 5]]
whiteBishopScores = [[5, 4, 3, 1, 1, 1, 4, 5],
                    [4, 5, 4, 3, 2, 4, 5, 4],
                    [3, 4, 5, 4, 4, 5, 4, 1],
                    [1, 3, 4, 4, 5, 4, 2, 1],
                    [1, 2, 4, 5, 4, 4, 3, 1],
                    [1, 4, 5, 4, 4, 5, 4, 3],
                    [4, 5, 4, 2, 3, 4, 5, 4],
                    [5, 4, 1, 1, 1, 3, 4, 5]]
blackRookScores = [[4, 4, 4, 4, 4, 4, 4, 4],
                    [7, 7, 7, 7, 7, 7, 7, 7],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [6, 6, 6, 6, 6, 6, 6, 6],
                    [5, 5, 6, 8, 8, 6, 5, 5]]
whiteRookScores = [[5, 5, 6, 8, 8, 6, 5, 5],    
                    [6, 6, 6, 6, 6, 6, 6, 6],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [7, 7, 7, 7, 7, 7, 7, 7],
                    [4, 4, 4, 4, 4, 4, 4, 4]]
blackQueenScores = [[3, 3, 3, 3, 3, 3, 3, 3],
                    [3, 4, 4, 5, 5, 4, 4, 3],
                    [3, 4, 5, 6, 6, 5, 4, 3],
                    [3, 4, 4, 6, 6, 4, 4, 3],
                    [4, 5, 5, 6, 6, 5, 5, 4],
                    [3, 4, 5, 5, 5, 5, 4, 3],
                    [2, 3, 3, 4, 4, 3, 3, 2],
                    [1, 2, 2, 2, 2, 2, 2, 1]]
whiteQueenScores = [[1, 2, 2, 2, 2, 2, 2, 1],
                    [2, 3, 3, 4, 4, 3, 3, 2],
                    [3, 4, 5, 5, 5, 5, 4, 3],
                    [4, 5, 5, 6, 6, 5, 5, 4],
                    [3, 4, 4, 6, 6, 4, 4, 3],
                    [3, 4, 5, 6, 6, 5, 4, 3],
                    [3, 4, 4, 5, 5, 4, 4, 3],
                    [3, 3, 3, 3, 3, 3, 3, 3]]
whiteKingOpeningScores = [[3, 8, 0, 0, 0, 0, 8, 3],
                        [1, 0, -1, -1, -1, -1, 0, 1],
                        [-2, -4, -4, -4, -4, -4, -4, -2],
                        [-1, -4, -4, -4, -4, -4, -4, -5],
                        [-1, -2, 3, -4, -4, -3, -2, -1],
                        [-1, -2, -3, -3, -3, -3, -2, 1],
                        [-10, -7, -7, -7, -7, -7, -7, -7],
                        [-10, -10, -10, -10, -10, -10, -10, -10]]
whiteKingEndGameScores = [[-3, -1, -3, -3, -3, -3, -3, -3],
                        [-3, 2, 2, 2, 2, 2, 2, -3],
                        [-3, 2, 3, 3, 3, 3, 2, -3],
                        [-3, 2, 3, 4, 4, 3, 2, -3],
                        [-3, 2, 3, 4, 4, 3, 2, -3],
                        [-1, 2, 3, 3, 3, 3, 2, -3],
                        [-1, 2, 2, 2, 2, 2, 2, -3],
                        [-1, -1, -1, -1, -1, -1, -1, -3]]
blackKingOpeningScores = [[-10, -10, -10, -10, -10, -10, -10, -10],
                        [-10, -7, -7, -7, -7, -7, -7, -7],
                        [-1, -2, -3, -3, -3, -3, -2, 1],
                        [-1, -2, 3, -4, -4, -3, -2, -1],
                        [-1, -2, -3, -4, -4, -3, -5, -5],
                        [-2, -2, -1, -3, -3, -1, -2, -2],
                        [1, 0, -1, -1, -1, -1, 0, 1],
                        [3, 8, 0, 0, 0, 0, 8, 3]]
blackKingEndGameScores = [[-3, -3, -3, -3, -3, -3, -3, -3],
                        [-3, 2, 2, 2, 2, 2, 2, -3],
                        [-3, 2, 3, 3, 3, 3, 2, -3],
                        [-3, 2, 3, 4, 4, 3, 2, -3],
                        [-3, 2, 3, 4, 4, 3, 2, -3],
                        [-3, 2, 3, 3, 3, 3, 2, -3],
                        [-3, 2, 2, 2, 2, 2, 2, -3],
                        [-3, -3, -3, -3, -3, -3, -3, -3]]



piecePositions = {
    "N" : whiteKnightScores, "n": blackKnightScores,  "B" : whiteBishopScores, "b" : blackBishopScores,
    "R" : whiteRookScores, "r" : blackRookScores,  "Q" : whiteQueenScores, "q" : blackQueenScores,
    "P" : whitePawnScores, "p" : blackPawnScores, "oK" : whiteKingOpeningScores, "ok" : blackKingOpeningScores,
    "ek" : blackKingEndGameScores, "eK" : whiteKingEndGameScores
}

CHECKMATE = float('inf')
STALEMATE = 0
DEPTH = 3


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMoveGreedy(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
    
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            gs.getValidMoves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if(score > opponentMaxScore):
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentsMinMaxScore:
            opponentsMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    print("+")
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove() 
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, - turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move


        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE

    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta,  -alpha, - turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# postive is good for white

def scoreBoard(gs):
    if gs.board.is_checkmate():
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    if gs.board.is_stalemate():
        return STALEMATE
    pawnStructureScore = evaluatePawns(gs)
    blackPawnStructureScore = pawnStructureScore[1]
    whitePawnStructureScore = pawnStructureScore[0]
    score = 0
    for row in range(8):
        for col in range(8):
            piecePositionScore = 0
            square = gs.board.piece_at(row*8 + col)
            color = gs.board.color_at(row*8 +col)
            piece = str(square)

            if piece != 'None':
                if not gs.isEndGame:
                    if piece == 'K' or piece == 'k':
                        repiece = "o" + piece
                        piecePositionScore = piecePositions[repiece][row][col]
                if gs.isEndGame:
                    if piece == 'K' or piece == 'k':
                        repiece = "e" + piece
                        piecePositionScore = piecePositions[repiece][row][col]
                if piece != 'k' and piece != 'K':
                    piecePositionScore += piecePositions[piece][row][col]
                if color == True:
                    score += pieceScore[piece] + piecePositionScore *.1 
                if color == False:
                    score += pieceScore[piece] - piecePositionScore*.1 
    score += (whitePawnStructureScore - blackPawnStructureScore)*.1

    return score

def evaluatePawns(gs):
    whitePawnStructureScore = 0
    blackPawnStructureScore = 0
    for row in range(8):
        for col in range(8):
            row = Chess.numberConvert[row]
            if 0 < col < 7:
                if gs.board.piece_at(row*8 + col) == chess.Piece(1, True):
                    whitePossiblePawnLeft = gs.board.piece_at((row-1)*8 + col - 1)
                    whitePossiblePawnRight = gs.board.piece_at((row-1)*8 + col + 1)
                    if str(whitePossiblePawnLeft) == 'None' and str(whitePossiblePawnRight) == 'None':
                        whitePawnStructureScore += 0
                    if whitePossiblePawnLeft == chess.Piece(1, True):
                            whitePawnStructureScore += 3
                    if whitePossiblePawnRight == chess.Piece(1, True):
                            whitePawnStructureScore += 3
                if gs.board.piece_at(row*8 + col) == chess.Piece(1, False):
                    blackPossiblePawnLeft = gs.board.piece_at((row+1)*8 + col - 1)
                    blackPossiblePawnRight = gs.board.piece_at((row+1)*8 + col + 1)
                    if str(blackPossiblePawnLeft) == 'None' and str(blackPossiblePawnRight) == 'None':
                        blackPawnStructureScore += 0
                    if blackPossiblePawnLeft == chess.Piece(1, True):
                        whitePawnStructureScore += 3
                    if blackPossiblePawnRight == chess.Piece(1, True):
                        whitePawnStructureScore += 3
    return whitePawnStructureScore, blackPawnStructureScore
