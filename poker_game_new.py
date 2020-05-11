"""
poker_game
==========
Simulates basic poker game.
"""
from itertools import cycle
from random import sample
from time import sleep

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
    pot = 0

    def __init__(self, name, controller='CPU'):
        self.name = name
        self.controller = controller
        self.chips = 200
        self.bet = 0
        self.bet_add = 0
        self.in_game = True
        self.in_hand = True
        self.betting = True

        self.hand = []
        self.hand_ranks = []
        self.hand_suits = []
        self.hand_rank_vals = []
        self.combos = {}
        self.hand_score = 0

    def score_hand(self):
        self.hand_ranks = [card[0] for card in self.hand]
        self.hand_suits = [card[1] for card in self.hand]
        self.hand_rank_vals = sorted([rank_levels[rank] for rank in self.hand_ranks])
        # Change value of ace if used in 5-high straight
        if self.hand_rank_vals == [2, 3, 4, 5, 14]:
            self.hand_rank_vals = [1, 2, 3, 4, 5]
        self.combos = {self.hand_rank_vals.count(rank): rank for rank in set(self.hand_rank_vals)}

        # Define hand score
        # Royal flush
        if len(set(self.hand_suits)) == 1 \
                and self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)) \
                and max(self.hand_rank_vals) == 14:
            self.hand_score = (possible_scores[9], self.hand_rank_vals[4])
        # Straight flush
        elif len(set(self.hand_suits)) == 1 \
                and self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)):
            self.hand_score = (possible_scores[8], self.hand_rank_vals[4])
        # Four of a kind
        elif 4 in self.combos:
            self.hand_score = (possible_scores[7], self.combos[4])
        # Full house
        elif 2 in self.combos and 3 in self.combos:
            self.hand_score = (possible_scores[6], self.combos[3])
        # Flush
        elif len(set(self.hand_suits)) == 1:
            self.hand_score = (possible_scores[5], self.hand_rank_vals[4])
        # Straight
        elif self.hand_rank_vals == list(range(self.hand_rank_vals[0], self.hand_rank_vals[4] + 1)):
            self.hand_score = (possible_scores[4], self.hand_rank_vals[4])
        # Three of a kind
        elif 3 in self.combos.keys():
            self.hand_score = (possible_scores[3], self.combos[3])
        # Pair
        elif 2 in self.combos.keys():
            self.hand_score = (possible_scores[1], self.combos[2])
        # High card
        else:
            self.hand_score = (possible_scores[0], self.hand_rank_vals[4])

        self.hand_score_rank = possible_scores.index(self.hand_score[0])

    def __str__(self):
        return self.name

    def make_bet(self):
        global possible_scores
        if self.controller == 'CPU':
            if self.hand_score[0] in possible_scores[2:]:
                sleep(2)
                self.all_in()
            elif self.hand_score[0] == possible_scores[1]:
                sleep(2)
                self.call()
            else:
                sleep(2)
                self.fold()

        elif self.controller == 'User':
            move_complete = False
            while not move_complete:
                move = input('Choose your move - press 1 for call, 2 for raise, 3 for all-in, or 4 for fold: ')
                if int(move) == 1:
                    self.call()
                    move_complete = True
                elif int(move) == 2:
                    try:
                        raise_amt = int(input('How much do you want to raise by? '))
                        if int(raise_amt) > 0:
                            self.raise_(int(raise_amt))
                            move_complete = True
                        else:
                            raise Exception('Please enter a positive number.')
                    except Exception as e:
                        print(e)
                elif int(move) == 3:
                    self.all_in()
                    move_complete = True
                elif int(move) == 4:
                    self.fold()
                    move_complete = True
                else:
                    raise Exception('Please enter 1, 2, 3 or 4.')    # TODO: ensure retry after incorrect entry

        self.bet += self.bet_add
        self.chips -= self.bet_add

        if self.bet > self.__class__.game_bet:
            self.__class__.game_bet = self.bet
        self.__class__.pot += self.bet_add

    def call(self):
        print('Call')
        print(f'Game bet: {self.__class__.game_bet}')
        if self.__class__.game_bet >= self.chips:
            print('Not enough chips to call')
            self.all_in()
        else:
            self.bet_add = self.__class__.game_bet - self.bet

    def raise_(self, amount):
        if amount > self.__class__.game_bet:
            if amount == self.chips:
                self.all_in()
            elif amount < self.chips:
                print(f'Raise: {str(amount)}')
                self.bet_add = amount
            else:
                raise Exception('Cannot raise amount greater than remaining chips.')
        else:
            raise Exception('Must raise by more than current bet.')

    def all_in(self):
        print('All in')
        self.bet_add = self.chips
        self.betting = False

    def fold(self):
        print('Fold')
        self.bet_add = 0
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
                self.deck.remove(self.hand[-1], self.hand[-2])

            else:
                raise Exception('Please enter 0, 1 or 2.')


def poker_game(players = [Player('Player 1', controller='User'), Player('Player 2'), Player('Player 3')]):
    in_game = players.copy()
    in_hand = players.copy()
    in_betting = players.copy()
    dealer_tracker = iter(in_game)
    dealer = cycle(dealer_tracker)
    hand_winner = 0

    deck = cards.copy()
    ante = 5
    blind = 10

    def deal():
        nonlocal deck, players
        for i, player in enumerate(players):
            if i == 0:
                player.hand = [('Ace', 'Hearts'), ('Ace', 'Clubs'), ('Ace', 'Spades'), ('5', 'Spades'), ('9', 'Diamonds')]
            else:
                player.hand = sample(deck, 5)

            player.score_hand()
            deck = [card for card in deck if card not in player.hand]

    def betting_round():
        nonlocal in_betting, in_hand, in_game
        while len(in_betting) > 1:
            for player in in_betting:
                if len(in_hand) > 1:  # If all the first n-1 players fold, then nth player wins by default.
                    print(player.name + '\n')
                    sleep(2)
                    print(*player.hand, sep = ', ')
                    print(f'Score: {player.hand_score[0]}, {player.hand_score[1]}')
                    print(f'Chips: {player.chips}')
                    print(f'Player bet: {player.bet}')
                    print(f'Game bet: {Player.game_bet}\n')
                    player.make_bet()
                    print(f'\nPlayer bet: {player.bet}')
                    print(f'Game bet: {Player.game_bet}')
                    print(f'Chips: {player.chips}')
                    print(f'Pot: {Player.pot}\n')
                    sleep(2)
            in_hand = [player for player in in_game if player.in_hand]
            in_betting = [player for player in in_hand if player.betting]
            if len(in_betting) > 0:
                print('Betting: ', [player.name for player in in_betting], '\n')
            else:
                print('Betting finished')

    def draw_round():
        pass

    def winning_hand():
        nonlocal in_hand
        scores = {player: player.hand_score_rank for player in in_hand}
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

    while len(in_game) > 1:
        print('NEW HAND\n')
        sleep(2)
        deck = cards.copy()
        in_hand = in_game.copy()
        in_betting = in_game.copy()
        if len(in_game) <= 2:
            blind = 20
            ante = 10
        dealer = cycle(dealer_tracker)
        Player.pot = 0
        Player.game_bet = 0
        for player in in_game:
            player.in_hand = True
            player.betting = True
            player.chips -= ante
            player.bet = ante
            Player.game_bet = blind
            Player.pot += ante

        deal()
        betting_round()
        draw_round()
        # betting_round()
        hand_winner = winning_hand()
        print('Hand winner: ' + hand_winner.name)
        hand_winner.chips += Player.pot

        Player.pot = 0
        for player in players:
            if player.chips <= 0:
                player.in_game = False
                player.in_hand = False
                player.betting = False
            else:
                player.in_hand = True
                player.betting = True
        in_game = [player for player in players if player.in_game]
        print('\nIn game: ', *in_game, sep = ', ')
        for player in players:
            print(f'{player} chips: {player.chips}')
        print('\nEND OF HAND\n\n')
    print('Game winner: ', [player.name for player in in_game])
    print('GAME OVER')

if __name__ == "__main__":
    poker_game()

