import chess
import numpy
from functools import lru_cache


startPosition = chess.STARTING_FEN
stalematePosition = "8/8/8/8/8/3K4/3Q4/k7 w - - 0 1"
testPosition = "8/8/p2BKP2/7p/7k/8/8/1r6 w - - 1 2"

class gameState():
    def __init__(self):
        self.board = chess.Board(startPosition)
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = { 'p' : self.getPawnMoves, 'P' : self.getPawnMoves, 
        'r' : self.getRookMoves, 'R' : self.getRookMoves, 'q' : self.getQueenMoves,
        'Q' : self.getQueenMoves, 'n' : self.getKnightMoves, 'N' : self.getKnightMoves, 
        'k' : self.getKingMoves, 'K' : self.getKingMoves,
        'b' : self.getBishopMoves, 'B' : self.getBishopMoves}

        self.whiteKingLocation = (0,4)
        self.blackKingLocation = (7,4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.isOpening = True
        self.isEndGame = False
        self.whiteIsWinning = False
        self.blackIsWinning = False
        if len(self.moveLog) > 6:
            self.isOpening = False




        #castling
               
        self.currentCastlingRights = CastleRights(None, True, True, True, True)
        self.castlingRightsLog = [CastleRights(None, self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs )]
        



        


        
    def makeMove(self, move):
        self.board.remove_piece_at((move.startRow*8) + move.startCol)
        self.board.set_piece_at(((move.endRow*8) + move.endCol), move.pieceMoved)
        self.moveLog.append(move)
        self.board.turn = not self.board.turn
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'K':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'k':
            self.blackKingLocation = (move.endRow, move.endCol)
       #promotion
        if move.isPawnPromotion:
            if not self.whiteToMove:
                self.board.set_piece_at(((move.endRow*8) + move.endCol), chess.Piece(5, True))
            if self.whiteToMove:
                self.board.set_piece_at(((move.endRow*8) + move.endCol), chess.Piece(5, False))
        #enpassant
        if move.isEnpassantMove:
            self.board.remove_piece_at((move.startRow)*8 + move.endCol)
        if (move.pieceMoved == chess.Piece(1, False)) or (move.pieceMoved == chess.Piece(1, True)):
            if abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ((move.endRow + move.startRow)//2, move.endCol)
            else:
                self.enpassantPossible = ()
        else:
            self.enpassantPossible = ()
        self.enpassantPossibleLog.append(self.enpassantPossible)

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                if move.endRow == 0:
                    self.board.set_piece_at((move.endRow*8 + move.endCol - 1), chess.Piece(4 , True))
                    self.board.remove_piece_at(move.endRow * 8 + move.endCol + 1)
                if move.endRow == 7:
                    self.board.set_piece_at((move.endRow*8 + move.endCol - 1), chess.Piece(4 , False))
                    self.board.remove_piece_at(move.endRow * 8 + move.endCol + 1)
            elif move.endCol - move.startCol == -2:
                if move.endRow == 0:
                    self.board.set_piece_at(move.endRow * 8 + move.endCol + 1, chess.Piece(4 , True))
                    self.board.remove_piece_at(move.endRow * 8 + move.endCol - 2)
                if move.endRow == 7:
                    self.board.set_piece_at(move.endRow * 8 + move.endCol + 1, chess.Piece(4 , False))
                    self.board.remove_piece_at(move.endRow * 8 + move.endCol - 2)
        self.updateCastlingRights(move)
        self.castlingRightsLog.append(CastleRights(move, self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

        


        

    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board.set_piece_at((move.endRow*8) + move.endCol, move.peiceCaptured)
            self.board.set_piece_at((move.startRow*8) + move.startCol, move.pieceMoved)
            self.whiteToMove = not self.whiteToMove
            self.board.turn = not self.board.turn
            if move.pieceMoved == 'K':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'k':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board.remove_piece_at(move.endRow * 8 + move.endCol)
                self.board.set_piece_at(move.startRow * 8 + move.endCol, move.peiceCaptured)
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            self.checkmate = False
            self.stalemate = False
            self.castlingRightsLog.pop()
            self.currentCastlingRights = self.castlingRightsLog[-1]
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    if move.endRow == 0:
                        self.board.set_piece_at(move.endRow * 8 + move.endCol + 1, chess.Piece(4, True))
                        self.board.remove_piece_at(move.endRow * 8 + move.endCol - 1)
                    if move.endRow == 7:
                        self.board.set_piece_at(move.endRow * 8 + move.endCol + 1, chess.Piece(4, False))
                        self.board.remove_piece_at(move.endRow * 8 + move.endCol - 1)
                else:
                    self.board.set_piece_at(move.endRow * 8 + move.endCol - 2, self.board.piece_at(move.endRow * 8 + move.endCol + 1))
                    self.board.remove_piece_at(move.endRow * 8 + move.endCol + 1)
            self.checkmate = False
            self.stalemate = False
            

    
    def updateCastlingRights(self, move):
        if move.pieceMoved == chess.Piece(6, True):
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == chess.Piece(6, False):
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == chess.Piece(4, True):
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == chess.Piece(4, False):
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.bks = False
        if move.peiceCaptured == chess.Piece(4, True):
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.peiceCaptured == chess.Piece(4, False):
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.bks = False




    
    def getValidMoves(self):
        tempcastle = CastleRights(None, self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        tempEnpasssantMove = self.enpassantPossible
        testMoves = self.getAllPossibleMoves()
        captureMoves = []
        for i in range(len(testMoves) -1, -1, -1):
            self.makeMove(testMoves[i])
            self.whiteToMove = not self.whiteToMove
            self.board.turn = not self.board.turn
            if self.board.is_check() == True:
                testMoves.remove(testMoves[i])
            elif testMoves[i].isCapture:
                captureMoves.append(testMoves[i])
                testMoves.remove(testMoves[i])
            self.whiteToMove = not self.whiteToMove
            self.board.turn = not self.board.turn
            self.undoMove()
      
        if self.board.is_checkmate() == True:
            self.checkmate = True
        if self.board.is_stalemate() == True:
            self.stalemate = True
        self.enpassantPossible = tempEnpasssantMove
        self.currentCastlingRights = tempcastle
        testMoves = captureMoves + testMoves
        return testMoves
        
           

    def getAllPossibleMoves(self):
        moves = []
        queenCount = 0
        whitePieceCount = 0
        blackPieceCount = 0
        for r in range(8):
            for c in range(8):
                pos = r * 8 + c
                pieceColor = self.board.color_at(pos)
                pieceAt = self.board.piece_at(pos)
                if pieceAt == chess.Piece(5, True) or pieceAt == chess.Piece(5, False):
                    queenCount += 1
                if pieceAt == chess.Piece(5, True) or pieceAt == chess.Piece(4, True) or pieceAt == chess.Piece(3, True) or pieceAt == chess.Piece(2, True):
                    whitePieceCount += 1
                if pieceAt == chess.Piece(5, False) or pieceAt == chess.Piece(4, False) or pieceAt == chess.Piece(3, False) or pieceAt == chess.Piece(2, False):
                    blackPieceCount += 1
                if str(pieceColor) != 'None':
                    if ((pieceColor) == True and self.whiteToMove) or ((pieceColor) == False and not self.whiteToMove):
                        piece = self.board.piece_at(pos)
                        self.moveFunctions[str(piece)](r, c, moves)
        if queenCount == 0:
            self.isEndGame = True
        if blackPieceCount - whitePieceCount > 1:
            self.blackIsWinning = True
        if whitePieceCount - blackPieceCount > 1:
            self.whiteIsWinning = True

        return moves

    
 




    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if str(self.board.piece_at((r + 1)* 8 + c)) == 'None':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and str(self.board.piece_at((r + 2)*8 + c)) == 'None':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if str(self.board.piece_at((r + 1)*8 + c - 1)) != 'None':
                    if (self.board.color_at((r + 1) * 8 + c - 1)) == False:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove = True))
            if c + 1 <= 7:
                if str(self.board.piece_at((r + 1) * 8 + c + 1)) != 'None':
                    if (self.board.color_at((r + 1) * 8 + c + 1)) == False:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove = True))
        else:
            if str(self.board.piece_at((r - 1)* 8 + c)) == 'None':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and str(self.board.piece_at((r - 2)*8 + c)) == 'None':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if str(self.board.piece_at((r - 1)*8 + c - 1)) != 'None':
                    if (self.board.color_at((r - 1) * 8 + c - 1)) == True:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove = True))
            if c + 1 <= 7:
                if str(self.board.piece_at((r - 1) * 8 + c + 1)) != 'None':
                    if (self.board.color_at((r - 1) * 8 + c + 1)) == True:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove = True))


                

        

    
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = False if self.whiteToMove else True
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board.piece_at(endRow * 8 + endCol)
                    if str(endPiece) == 'None':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board.color_at(endRow * 8 + endCol) == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

                    


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, 1), (2, 1), (-1, 2), (1, 2), (-1, -2), (2, -1), (-2, -1), (1, -2))
        enemyColor = False if self.whiteToMove else True
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board.piece_at(endRow * 8 + endCol)
                if str(endPiece) == 'None':
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif self.board.color_at(endRow * 8 + endCol) == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    



    def getKingMoves(self, r, c, moves):
        kingMoves = ((1,0), (1, 1), (1, -1), (0, -1), (0, 1), (-1, -1), (-1, 1), (-1, 0))
        enemyColor = False if self.whiteToMove else True
        allyColor = not enemyColor
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board.piece_at(endRow * 8 + endCol)
                if str(endPiece) == 'None':
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif self.board.color_at(endRow * 8 + endCol) == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board)) 
        self.getCastleMoves(r, c, moves, allyColor)

    def getCastleMoves(self, r, c, moves, allyColor):
        if self.board.is_check():
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves, allyColor)
    
    def getKingsideCastleMoves(self, r, c, moves, allyColor):
        if (r*8 + c + 2) < 63:
            if str(self.board.piece_at(r*8 + c + 1)) == 'None' and str(self.board.piece_at(r*8 + c +2)) == 'None':
                if (len(self.board.attackers(not self.whiteToMove, (r * 8 + c + 1))) == 0) and (len(self.board.attackers(not self.whiteToMove, (r * 8 + c + 2))) == 0):
                    new_move = Move((r, c), (r, c + 2), self.board, isCastleMove = True)
                    moves.append(new_move)
                
        

    
    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        if str(self.board.piece_at(r*8 + c - 1)) == 'None' and str(self.board.piece_at(r*8 + c - 2)) == 'None' and str(self.board.piece_at(r * 8 + c - 3)) == 'None':
            if (len(self.board.attackers(not self.whiteToMove, (r * 8 + c - 1))) == 0) and (len(self.board.attackers(not self.whiteToMove, (r * 8 + c - 2))) == 0) and (len(self.board.attackers(not self.whiteToMove, (r * 8 + c - 3))) == 0):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))



    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemyColor = False if self.whiteToMove else True
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board.piece_at(endRow * 8 + endCol)
                    if str(endPiece) == 'None':
                          moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board.color_at(endRow * 8 + endCol) == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break





class CastleRights():
    def __init__(self, move, wks, bks, wqs, bqs):
        self.move = move
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

    def __str__(self):
        buf = ""
        if self.move is not None:
            buf = self.move.__str__()
        else:
            buf = "No move object present"
        buf += str(self.wks) + "," + str(self.bks) + "," + str(self.wqs) + "," + str(self.bqs)
        return buf







class Move():
    ranksToRows = {
        "8" : 7, "7": 6, "6" : 5, "5": 4,
        "4" : 3, "3": 2, "2" : 1, "1": 0 }
    rowsToRanks = { v: k for k, v in ranksToRows.items()}
    
    filesToCols = {
        "h" : 7, "g": 6, "f" : 5, "e": 4,
        "d" : 3, "c": 2, "b" : 1, "a": 0
    }
    colsToFiles = { v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board.piece_at(self.startRow*8 + self.startCol)
        self.peiceCaptured = board.piece_at(self.endRow*8 + self.endCol)
        self.newFen = board.board_fen
        self.originalSquare = startSq
        self.compareSquare = endSq
       # promotion

        self.isPawnPromotion = (str(self.pieceMoved) == 'P' and self.endRow == 7) or (str(self.pieceMoved) == 'p' and self.endRow == 0)

        # en passant

        self.isEnpassantMove = isEnpassantMove

        if self.isEnpassantMove == True:
            self.peiceCaptured = chess.Piece(1, False) if str(self.pieceMoved) == 'P' else chess.Piece(1, True)
          
        self.isCapture = str(self.peiceCaptured) != 'None'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        #castle

        self.isCastleMove = isCastleMove
    
    def __str__(self):
        return 'move: {} {} -> {} {}'.format(self.startRow, self.startCol, self.endRow, self.endCol)

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        

    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSqaure = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved == chess.Piece(1, True):
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSqaure
            else:
                return endSqaure
        if self.pieceMoved == chess.Piece(1, False):
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSqaure
            else:
                return endSqaure

        moveString = str(self.pieceMoved)
        if self.isCapture:
            moveString += "x"
        return moveString + endSqaure
        

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False


class translate():
    pass


    