#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IS211_Assignment8
Game: Pig Proxy
"""
import argparse
import time
import random

class Die:
    def __init__(self):
        self.rolled = 0
        self.values = [1, 2, 3, 4, 5, 6]
        random.seed(0)
    def roll_die(self):
        self.rolled = random.choice(list(range(1, 7)))
        return self.rolled
    
class Player:
    def __init__(self):
        self.hold = False
        self.roll = False
        self.score = 0
        self.running_score = 0
    def win(self):
        if self.score >= 100:
            return True
        
class ComputerPlayer(Player):
    def __init__(self, name):
        Player.__init__(self)
        self.name = name + " COMP"
    def hold_or_roll(self):
        if (self.running_score >= 25) or self.running_score >= (100 - self.score):
            print('\n\t{} holds.'.format(self.name))
            self.hold = True
            self.roll = False
        else:
            print('\n\t{} rolls.'.format(self.name))
            self.roll = True
            self.hold = False

        
class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self)
        self.name = name + " HUMAN"
    def hold_or_roll(self):
        choice = input('\nIf you want to roll, enter "r". If you want to hold, enter "h": ')
        if choice.lower() == 'h':
            self.hold = True
            self.roll = False
        elif choice.lower() == 'r':
            self.roll = True
            self.hold = False
        else:
            print('\n\tPlease enter either"r" or "h". All other entries are invalid.')
            self.hold_or_roll()

    
class PlayerFactory:
    def getPlayer(self, arg, name):
        if arg == "c":
            return ComputerPlayer(name)
        if arg == "h":
            return HumanPlayer(name)
        else:
            print('Please enter "c" for a Computer and "h" for Human.')

class Pig:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.die = Die()
        self.max_score = 100
        self.running_score = 0
        for num in range(1, total_players + 1):
            self.players.append(Player('Player {}'.format(num)))
        self.counter = 0
        self.current_player = self.players[self.counter]
        while not self.current_player.win():
            print('=======================')
            print('\n{}\'s turn'.format(self.current_player.name))
            print('=======================')
            print('SCORES:')
            print('Points for this turn: {}'.format(self.running_score))
            for player in self.players:
                print('\n   {}\'s Score: {}'.format(player.name, player.score))
            self.current_player.hold_or_roll()
            if self.current_player.roll:
                self.die.roll_die()
                print('\n\n\n{} ROLLED A {}! '.format(self.current_player.name, self.die.rolled))
                if self.die.rolled == 1:
                    self.running_score = 0
                    self.counter += 1
                    if self.counter < len(self.players):
                        self.current_player = self.players[self.counter]
                        print('YOUR TURN ENDED BECAUSE YOU ROLLED A ONE!'.format(self.current_player.name))
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]
                        print('YOUR TURN ENDED BECAUSE YOU ROLLED A ONE!'.format(self.current_player.name))
                else:
                    self.running_score += self.die.rolled
                    print('IF YOU HOLD NOW, YOU CAN ADD {} TO YOUR SCORE.'.format(self.running_score))
            else:
                self.current_player.score += self.running_score
                self.current_player.running_score = 0
                if self.current_player.score > self.max_score:
                    self.max_score = self.current_player.score

                if self.current_player.win():
                    print('\n\tGAME OVER, {} WINS!!'.format(
                        self.current_player.name))
                    exit()
                else:
                    self.counter += 1
                    if self.counter < len(self.players):
                        self.current_player = self.players[self.counter]
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]

class TimedGameProxy(Pig):
    def __init__(self):
        self.start_time = time.time()
        self.end_time = self.start_time + 60

    def check_time(self):
        if time.time() <= self.end_time:
            pass
        else:
            if player1.score > player2.score:
                print('\n\tTime has expired!\n\t{} wins with a score of {}'.format(player1.name, player1.score))
                exit()
            elif player2.score > player1.score:
                print('\n\tTime has expired!\n\t{} wins with a score of {}'.format(player2.name, player2.score))
                exit()
            elif player1.score == player2.score:
                print('\n\tTime has expired!\n\tHowever, a winner can\'t be determined.')
                exit()
    def time_left(self):
        return round(self.end_time - time.time(), 2)


class ProxyPig:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.die = Die()
        self.max_score = 100
        self.running_score = 0
        self.counter = 0
        self.current_player = self.players[self.counter]
        self.proxy = TimedGameProxy()
        
        while not self.current_player.win():
            print('=======================')
            print('\n{}\'s turn'.format(self.current_player.name))
            print('=======================')
            print('\n {} seconds are left on the clock!'.format(self.proxy.time_left()))
            print('SCORES:')
            print('Points for this turn: {}'.format(self.running_score))
            for player in self.players:
                print('{}\'s Score: {}'.format(player.name, player.score))
            
            
            self.current_player.hold_or_roll()
            self.proxy.check_time()
            
            if self.current_player.roll:
                self.die.roll_die()
                print('\n\n\n{} ROLLED A {}! '.format(self.current_player.name, self.die.rolled))
                self.proxy.check_time()
                
                if self.die.rolled == 1:
                    self.running_score = 0
                    self.counter += 1
                    if self.counter < len(self.players):
                        self.proxy.check_time()
                        
                        self.current_player = self.players[self.counter]
                        print('YOUR TURN ENDED BECAUSE YOU ROLLED A ONE!'.format(self.current_player.name))
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]
                        print('YOUR TURN ENDED BECAUSE YOU ROLLED A ONE!'.format(self.current_player.name))
                        self.proxy.check_time()
                        
                else:
                    self.running_score += self.die.rolled
                    print('IF YOU HOLD NOW, YOU CAN ADD {} TO YOUR SCORE.'.format(self.running_score))
                    self.proxy.check_time()
                    
            else:
                self.current_player.score += self.running_score
                self.current_player.running_score = 0
                self.proxy.check_time()
                
                if self.current_player.score > self.max_score:
                    self.max_score = self.current_player.score

                if self.current_player.win():
                    print('\n\tGAME OVER, {} WINS!!'.format(
                        self.current_player.name))
                    exit()
                else:
                    self.counter += 1
                    if self.counter < len(self.players):
                        self.current_player = self.players[self.counter]
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]

                        
def main():
    parser = argparse.ArgumentParser(description='Parser for number of players playing the Pig game.')
    parser.add_argument('--player1', default='h', type=str, help='Player type. Enter "h" for Human, "c" for computer')
    parser.add_argument('--player2', default='h', type=str, help='Player type. Enter "h" for Human, "c" for computer')
    parser.add_argument('--timed', default='y', type=str, help='Timed Game. Enter "y" for Yes and "n" for No')
    args = parser.parse_args()
    arg_vals = ('c', 'h', 'y', 'n')
    if (args.player1.lower() not in arg_vals) or (args.player2.lower() not in arg_vals) or (args.timed.lower() not in arg_vals):
        print('Please enter valid inputs for the game.')
    else:
        factory = PlayerFactory()
        player1 = factory.getPlayer(args.player1.lower(), 'Player 1')
        player2 = factory.getPlayer(args.player2.lower(), 'Player 2')
        if args.timed.lower() == "y":
            ProxyPig(player1, player2)
        else:
            Pig(player1, player2)


if __name__ == '__main__':
    main()
