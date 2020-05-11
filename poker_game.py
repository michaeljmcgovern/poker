"""
poker_game
==========
Simulates basic poker game.
"""
from itertools import cycle
from random import sample

# TODO: maximum 2 consecutive calls before cards are played.
# TODO: calculate odds from perspective of Player 1.
# TODO: Incorporate card swaps in gameplay
# TODO: Incorporate Texas Hold'Em gameplay
# TODO: Calculate odds conditional on moves in Texas Hold'Em


suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
rank_levels = dict(zip(ranks, range(2, 15)))
cards = [(rank, suit) for rank in ranks for suit in suits]

possible_scores = ('High card', 'Pair', 'Two pair', 'Three of a kind', 'Straight', 'Flush',
                   'Full house', 'Four of a kind', 'Straight flush', 'Royal flush')


class Player:
    deck = cards.copy()
    game_bet = 0

    def __init__(self, name, controller='CPU', chips=200):
        self.name = name
        self.controller = controller
        self.chips = chips
        self.bet = 0
        self.in_game = True
        self.in_hand = True
        self.betting = True
        self.hand = sample(cards, 5)

        self.hand_ranks = [card[0] for card in self.hand]
        self.hand_suits = [card[1] for card in self.hand]
        self.hand_rank_vals = sorted([rank_levels[rank] for rank in self.hand_ranks])
        # Change value of ace if used in 5-high straight
        if self.hand_rank_vals == [2, 3, 4, 5, 14]:
            self.hand_rank_vals = [1, 2, 3, 4, 5]
        self.combos = {self.hand_rank_vals.count(rank): rank for rank in set(self.hand_rank_vals)}

        # Define hand score
        if len(set(self.hand_suits)) == 1 \
                and self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)) \
                and max(self.hand_rank_vals) == 14:
            self.hand_score = (possible_scores[9], self.hand_rank_vals[4])
        elif len(set(self.hand_suits)) == 1 \
                and self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)):
            self.hand_score = (possible_scores[8], self.hand_rank_vals[4])
        elif 4 in self.combos:
            self.hand_score = (possible_scores[7], self.combos[4])
        elif 2 and 3 in self.combos:
            self.hand_score = (possible_scores[6], self.combos[3])
        elif len(set(self.hand_suits)) == 1:
            self.hand_score = (possible_scores[5], self.hand_rank_vals[4])
        elif self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)):
            self.hand_score = (possible_scores[4], self.hand_rank_vals[4])
        elif 3 in self.combos.keys():
            self.hand_score = (possible_scores[3], self.combos[3])
        elif 2 in self.combos.keys():
            self.hand_score = (possible_scores[1], self.combos[2])
        else:
            self.hand_score = (possible_scores[0], self.hand_rank_vals[4])

        self.hand_score_rank = possible_scores.index(self.hand_score[0])

    def make_bet(self):
        if self.controller == 'CPU':
            if self.hand_score[0] in possible_scores[2:]:
                self.all_in()
            elif self.hand_score[0] == possible_scores[1]:
                self.call()
            else:
                self.fold()

        elif self.controller == 'User':
            move = input('Choose your move - press 1 for call, 2 for raise, 3 for all-in, or 4 for fold: ')
            if int(move) == 1:
                self.call()
            elif int(move) == 2:
                try:
                    raise_amt = input('How much do you want to raise by? ')
                    if int(raise_amt) > 0:
                        self.raise_(int(raise_amt))
                    else:
                        raise Exception('Please enter a positive number.')
                except Exception as e:
                    print(e)
            elif int(move) == 3:
                self.all_in()
            elif int(move) == 4:
                self.fold()
            else:
                raise Exception('Please enter 1, 2, 3 or 4.')
                # TODO: ensure retry after incorrect entry
        self.chips -= self.bet

    def call(self):
        if self.game_bet >= self.chips:
            self.all_in()
        else:
            print('Call')
            self.bet = self.game_bet

    def raise_(self, amount):
        if amount > self.game_bet:
            if amount >= self.chips:
                self.all_in()
            elif amount < self.chips:
                print('Raise: ' + str(amount))
                self.bet = amount
                game_bet = self.bet
            else:
                raise Exception('Cannot raise amount greater than remaining chips.')
        else:
            raise Exception('Must raise by more than current bet.')

    def all_in(self):
        print('All in')
        self.bet = self.chips
        self.game_bet = self.bet
        self.betting = False

    def fold(self):
        print('Fold')
        self.betting = False
        self.in_hand = False

    def draw(self):
        if self.controller == 'CPU':
            self.hand.remove(self.hand[0])
            self.hand.append(sample(cards, 1))
            self.deck.remove(self.hand[-1])

        elif self.controller == 'User':
            n_draws = input('How many cards would you like to draw? Enter 0, 1 or 2:')

            if n_draws == 0:
                pass

            if n_draws == 1:
                for i, card in enumerate(self.hand):
                    print(i, ': ', card)
                draw_card = input('Select the card you want to replace - enter a number from 1 to 5:')
                self.hand.remove(draw_card)
                self.hand.append(sample(cards, 1))
                self.deck.remove(self.hand[-1])

            elif n_draws == 2:
                for i, card in enumerate(self.hand):
                    print(i, ': ', card)
                draw_card_1 = input('Select the card you want to replace - enter a number from 1 to 5:')
                draw_card_2 = input('Select the card you want to replace - enter a number from 1 to 5:')
                self.hand.remove(draw_card_1, draw_card_2)
                self.hand.append(sample(cards, 2))
                self.deck.remove(self.hand[-1], self.hand[-2])  # ???: OK?

            else:
                raise Exception('Please enter 0, 1 or 2.')

class GameState:
    ...

class PokerGame:
    def __init__(self, player_list):
        self.players = player_list
        self.in_game = self.players.copy()
        self.in_hand = self.players.copy()
        self.in_betting = self.players.copy()
        self.dealer_tracker = iter(self.in_game)
        self.dealer = cycle(self.dealer_tracker)
        self.hand_winner = 0

        self.state = GameState()        # setters

        self.deck = cards.copy()
        self.pot = 0
        self.game_bet = 0
        self.ante = 5
        self.blind = 10

    def deal(self):
        for player in self.players:
            player.hand = sample(self.deck, 5)
            self.deck = [card for card in self.deck if card not in player.hand]

    def betting_round(self):
        while len(self.in_betting) > 1:
            for player in self.in_betting:
                if len(self.in_hand) > 1:  # If all the first n-1 players fold, then nth player wins by default.
                    print(player.name)
                    print(player.hand)
                    print('Score: ' + player.hand_score[0] + ', ' + str(player.hand_score[1]))
                    print('Chips: ' + str(player.chips))
                    player.make_bet()
                    self.pot += player.chips
                    print('Chips: ' + str(player.chips))
                    print('Pot: ' + str(self.pot) + '\n')
            self.in_hand = [player for player in self.in_game if player.in_hand]
            self.in_betting = [player for player in self.in_hand if player.betting]
            if len(self.in_betting) > 0:
                print('Betting: ', [player.name for player in self.in_betting], '\n')
            else:
                print('Betting finished')

    def draw_round(self):
        pass

    def winning_hand(self):
        scores = {player: player.hand_score[1] for player in self.in_hand}
        # List of all players with highest scoring hand (e.g. all full-houses).
        high_scorers = [player for player, score in scores.items() if score == max(scores.values())]

        # If e.g. multiple players have pair, pick highest scoring pair (King pair beats Queen pair).
        if len(high_scorers) > 1:
            high_cards = {player: player.hand_score[1] for player in high_scorers}
            return max(high_cards, key = high_cards.get)
        elif len(high_scorers) == 1:
            return high_scorers[0]
        else:
            print('No winners') # ???: Only a test - delete when no longer needed

    def poker_game(self):
        self.pot = 0
        self.in_game = self.players.copy()

        while len(self.in_game) > 1:
            print('NEW HAND\n')

            self.in_hand = self.in_game.copy()
            self.in_betting = self.in_game.copy()

            if len(self.in_game) <= 2:
                self.blind = 20
                self.ante = 10
            self.dealer = cycle(self.dealer_tracker)

            for player in self.in_game:
                player.in_hand = True
                player.betting = True
                player.chips -= self.ante
                self.pot += self.ante

            self.game_bet = self.blind

            self.deal()
            self.betting_round()
            self.draw_round()
            self.betting_round()
            self.hand_winner = self.winning_hand()
            print('Hand winner: ' + self.hand_winner.name)
            self.hand_winner.chips += self.pot

            self.pot = 0
            for player in self.players:
                if player.chips <= 0:
                    player.in_game = False
                    player.in_hand = False
                    player.betting = False
                else:
                    player.in_hand = True
                    player.betting = True
            self.in_game = [player for player in self.players if player.in_game]
            print('\nIn game: ', [player.name for player in self.in_game])
            print('\nEND OF HAND\n\n')
        print('Game winner: ', [player.name for player in self.in_game])
        print('GAME OVER')

if __name__ == "__main__":
    # Initiate card deck
    playing = [Player('Player 1', controller='User'), Player('Player 2'), Player('Player 3')]
    PokerGame(playing).poker_game()
