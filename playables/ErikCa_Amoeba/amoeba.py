import random

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable

class Amoeba(Playable):
    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: GameState) -> int:
        choices = self.best_moves(game_state)
        return random.choice(choices)
    
    def best_moves(self, game_state: GameState):
        scores = []
        for column in game_state.open_columns():
            row = self.get_move_row(column, game_state)
            scores.append(self.get_move_score(row, column, game_state))
        best_score = max(scores)
        best_scores = []
        for index, score in enumerate(scores):
            if score == best_score:
                best_scores.append(index)
        return best_scores
                
            

    @classmethod
    def get_name(cls) -> str:
        return "Erik Carlson's Amoeba Bot"

    def get_move_row(self, column, game_state: GameState) -> int:
        counter = 0
        for row in range(game_state.rows):
            if game_state.state[row][column] == None:
                break
            counter += 1
        return counter
    
    
    def position_matches_color(self, row, column, board: GameState) -> bool:
        if not(row < 0 or row > board.rows - 1 or column < 0 or column > board.columns - 1):
            return board.state[row][column] != None

    def get_move_score(self, row, column, board: GameState) -> int:
        score = 0
        if self.position_matches_color(row - 1, column, board): #north
            score += 1
        if self.position_matches_color(row - 1, column + 1, board): #northeast
            score += 1
        if self.position_matches_color(row, column + 1, board): #east
            score += 1
        if self.position_matches_color(row + 1, column + 1, board): #southeast
            score += 1
        if self.position_matches_color(row + 1, column, board): #south
            score += 1
        if self.position_matches_color(row + 1, column - 1, board): #southwest
            score += 1
        if self.position_matches_color(row, column - 1, board): #west
            score += 1
        if self.position_matches_color(row - 1, column - 1, board): #northwest
            score += 1
        return score




        
        


            
