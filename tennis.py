import random
import numpy as np
from enum import Enum
from player import Player
from point import Point
import types

class GameStates(Enum):
    SCORE00_00 = 1
    SCORE15_00 = 2
    SCORE30_00 = 3
    SCORE40_00 = 4
    SCORE00_15 = 5
    SCORE15_15 = 6
    SCORE30_15 = 7
    SCORE40_15 = 8
    SCORE00_30 = 9
    SCORE15_30 = 10
    SCORE30_30 = 11
    SCORE40_30 = 12
    SCORE00_40 = 13
    SCORE15_40 = 14
    SCORE30_40 = 15
    SCORE40_40 = 16
    SCOREAD_40 = 17
    SCORE40_AD = 18

class Match:
    best_of = 5

    def __init__(self, player_one, player_two):
        # Initialize instance variables (not class variables)
        self.sets = []
        self.player_one = player_one
        self.player_two = player_two
        self.player_one_sets_won = 0
        self.player_two_sets_won = 0
        self.winner = None
        self.current_game = 0
        self.current_game_state = GameStates.SCORE00_00
        self.current_set = 0
        self.total_games_played = 0

        self.server = random.choice([self.player_one, self.player_two])

        # Initialize first set and first game
        first_set = Set()
        first_game = Game()
        self.sets.append(first_set)
        self.sets[0].games.append(first_game)
    
    def toggle_server(self):
        self.server = self.player_one if self.server == self.player_two else self.player_two
    
    def get_server_and_receiver(self):
        if self.server == self.player_one:
            return self.player_one, self.player_two
        else:
            return self.player_two, self.player_one

    def set_player_one(self, name: str):
        self.player_one = name
    
    def set_player_two(self, name: str):
        self.player_two = name

    def set_players(self, names: list[str,str]):
        self.player_one, self.player_two = names

    def set_winner(self, name):
        if name == self.player_one: self.winner = self.player_one
        if name == self.player_two: self.winner = self.player_two

    def add_point(self, point):
        self.sets[self.current_set].games[self.current_game].points.append(point)
        if self.sets[self.current_set].games[self.current_game].is_tiebreaker:
            if(point.winner == self.player_one):
                self.sets[self.current_set].player_one_tiebreaker_points += 1
            else:
                self.sets[self.current_set].player_two_tiebreaker_points += 1

            if (self.sets[self.current_set].player_one_tiebreaker_points + self.sets[self.current_set].player_two_tiebreaker_points) % 2 == 1:
                self.toggle_server()

            if self.sets[self.current_set].player_one_tiebreaker_points - self.sets[self.current_set].player_two_tiebreaker_points >= 2 and \
               self.sets[self.current_set].player_one_tiebreaker_points >= 7:
                self.add_game(self.player_one)
            elif self.sets[self.current_set].player_two_tiebreaker_points - self.sets[self.current_set].player_one_tiebreaker_points >= 2 and \
                 self.sets[self.current_set].player_two_tiebreaker_points >= 7:
                self.add_game(self.player_two)
        else:
            match self.current_game_state:
                case GameStates.SCORE00_00:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE15_00
                    else:
                        self.current_game_state = GameStates.SCORE00_15
                case GameStates.SCORE15_00:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE30_00
                    else:
                        self.current_game_state = GameStates.SCORE15_15
                case GameStates.SCORE30_00:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE40_00
                    else:
                        self.current_game_state = GameStates.SCORE30_15
                case GameStates.SCORE40_00:
                    if(point.winner == self.player_one):
                        # Player one wins the game
                        self.add_game(self.player_one)
                    else:
                        self.current_game_state = GameStates.SCORE40_15
                case GameStates.SCORE00_15:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE15_15
                    else:
                        self.current_game_state = GameStates.SCORE00_30
                case GameStates.SCORE15_15:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE30_15
                    else:
                        self.current_game_state = GameStates.SCORE15_30
                case GameStates.SCORE30_15:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE40_15
                    else:
                        self.current_game_state = GameStates.SCORE30_30
                case GameStates.SCORE40_15:
                    if(point.winner == self.player_one):
                        # Player one wins the game
                        self.add_game(self.player_one)
                    else:
                        self.current_game_state = GameStates.SCORE40_30
                case GameStates.SCORE00_30:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE15_30
                    else:
                        self.current_game_state = GameStates.SCORE00_40
                case GameStates.SCORE15_30:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE30_30
                    else:
                        self.current_game_state = GameStates.SCORE15_40
                case GameStates.SCORE30_30:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE40_30
                    else:
                        self.current_game_state = GameStates.SCORE30_40
                case GameStates.SCORE40_30:
                    if(point.winner == self.player_one):
                        # Player one wins the game
                        self.add_game(self.player_one)
                    else:
                        self.current_game_state = GameStates.SCORE40_40 
                case GameStates.SCORE00_40:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE15_40
                    else:
                        # Player two wins the game
                        self.add_game(self.player_two)
                case GameStates.SCORE15_40:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE30_40
                    else:
                        # Player two wins the game
                        self.add_game(self.player_two)
                case GameStates.SCORE30_40:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE40_40
                    else:
                        # Player two wins the game
                        self.add_game(self.player_two)
                case GameStates.SCORE40_40:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCOREAD_40
                    else:
                        self.current_game_state = GameStates.SCORE40_AD
                case GameStates.SCOREAD_40:
                    if(point.winner == self.player_one):
                        # Player one wins the game
                        self.add_game(self.player_one)
                    else:
                        self.current_game_state = GameStates.SCORE40_40
                case GameStates.SCORE40_AD:
                    if(point.winner == self.player_one):
                        self.current_game_state = GameStates.SCORE40_40
                    else:
                        # Player two wins the game
                        self.add_game(self.player_two)
    
    def add_game(self, player):
        self.toggle_server()
        self.total_games_played = self.total_games_played + 1
        cur_set = self.sets[self.current_set]
        if player == self.player_one:
            cur_set.score[0] += 1
        else:
            cur_set.score[1] += 1

        # Reset game state for next game
        self.current_game_state = GameStates.SCORE00_00

        def _start_new_set():
            self.current_game = 0
            self.current_set += 1
            new_set = Set()
            new_game = Game(False)
            self.sets.append(new_set)
            self.sets[self.current_set].games.append(new_game)

        s0, s1 = cur_set.score
        # just win by two for now, will impl tiebreakers later
        if s0 >= 6 and (s0 - s1) >= 2 or (s0 == 7 and s1 == 6):
            # Player one wins the set
            self.player_one_sets_won += 1
            if not self.check_win():
                _start_new_set()
        elif s1 >= 6 and (s1 - s0) >= 2 or (s1 == 7 and s0 == 6):
            # Player two wins the set
            self.player_two_sets_won += 1
            if not self.check_win():
                _start_new_set()
        else:
            self.current_game += 1
            is_tiebreaker = (s0 == 6 and s1 == 6)
            new_game = Game(is_tiebreaker)
            cur_set.games.append(new_game)

    def check_win(self):
        if self.player_one_sets_won > self.best_of // 2:
            self.set_winner(self.player_one)
        elif self.player_two_sets_won > self.best_of // 2:
            self.set_winner(self.player_two)

        return self.winner is not None

    def print_score(self):
        for i, set in enumerate(self.sets):
            print(f"Set {i+1}: {set.score[0]} - {set.score[1]}")


class Set:
    def __init__(self):
        self.games = []
        self.first_to = 6
        self.is_win_by_2 = True
        self.has_tiebreaker = True
        self.score = [0, 0]
        self.player_one_tiebreaker_points = 0
        self.player_two_tiebreaker_points = 0

class Game:
    def __init__(self, is_tiebreaker=False):
        self.points = []
        self.is_tiebreaker = is_tiebreaker
