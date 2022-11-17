from collections import deque
import random

class Card:
    """French playing cards.

    Class attributes:
    suit_names -- the four suits Clubs, Diamonds, Hearts, Spades
    rank_names -- the 13 ranks in each suit: Two--Ten, Jack, Queen, King, Ace

    Data attributes:
    suit, rank -- the Card's suit and rank, as indices into the lists above
    """

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
             'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank):
        # assert 0 <= suit < 4, "suit must be between 0 and 3"
        # assert 0 <= rank < 13, "rank must be between 0 and 12"
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{Card.rank_names[self.rank]} of {Card.suit_names[self.suit]}"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        elif self.rank == other.rank:
            return self.suit > other.suit
        else:
            return False
    
class Deck:
    """A deck of Cards.

    Data attributes:
    cards -- a list of all Cards in the Deck
    """

    def __init__(self, minrank):
        self.cards = list()
        for suit in range(4):
            for rank in range(minrank, 13):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

    def pop(self):
        """Remove and return last card from deck."""
        return self.cards.pop()

    def popleft(self):
        """Remove and return first card from deck."""
        # This is extremely inefficient, but it's the only way to do it
        temp = self.cards[0]
        self.cards = self.cards[1:]
        return temp

    def add(self, card):
        """Add a card to the deck."""
        self.cards.append(card)

    def number_of_cards(self):
        """Return the number of cards in the deck."""
        return len(self.cards)
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def is_empty(self):
        """Return True if the deck is empty."""
        return self.number_of_cards() == 0
    
class Player:
    """A player of the card game.

    Data attributes:
    name -- the name of the player
    hand -- a Deck containing composed of the player's cards (their "hand")
    """

    def __init__(self, name):
        self.name = name
        self.hand = Deck(13)

    def __str__(self):
        if self.hand.is_empty():
            return f"Player {self.name} has no cards"
        else:
            return f"Player {self.name} has: {self.hand}"

    def add_card(self, card):
        """Add card to this player's hand."""
        self.hand.add(card)

    def num_cards(self):
        """Return the number of cards in this player's hand."""
        return self.hand.number_of_cards()

    def remove_card(self):
        """Remove the first card from this player's hand and return it."""
        return self.hand.popleft()

class CardGame:
    """A class for playing card games.

    Data attributes:
    players -- a list of Player objects which participate in the game
    deck -- a Deck of Cards used for playing
    numcards -- the number of Cards in the game
    """

    def __init__(self, player_names, minrank):
        self.players = list()
        for name in player_names:
            player = Player(name)
            self.players.append(player)
        self.deck = Deck(minrank)
        self.numcards = self.deck.number_of_cards()

    def __str__(self):
        res = []
        for player in self.players:
            res.append(str(player))
        return '\n'.join(res)

    def burn_card(self, card):
        """Remove the card 'card' from this game's deck if it exists,
        and update the number of cards in the deck accordingly"""
        if card in self.deck.cards:
            self.deck.cards.remove(card)
            self.numcards -= 1
    
    def shuffle_deck(self):
        """Shuffle this game's deck."""
        self.deck.shuffle()

    def deal_cards(self):
        """Deal all of the cards in the deck to the players, round-robin."""
        while not self.deck.is_empty():
            for player in self.players:
                if not self.deck.is_empty():
                    player.add_card(self.deck.pop())

    def simple_turn(self):
        """Play a very simple game.
        For each player, play the first card.
        The winner is the player with the highest cards.
        """
        first_cards_players = [(player, player.remove_card()) for player in self.players]
        trick = []
        for player, card in first_cards_players:
            print(f"{player.name}: {card}")
            trick.append(card)
        winner = max(first_cards_players, key=lambda x: x[1])
        winner_name = winner[0].name
        return winner_name, trick
