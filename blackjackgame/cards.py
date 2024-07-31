#!/usr/bin/env python3
# Darren Cruz
# CPSC 386-02
# 2023-02-16
# darrencruz@csu.fullerton.edu
# @darrenjcruz
#
# Lab 02-00
#
# This is the cards module for the Blackjack game, it contains the Deck class
#


"""cards.py file: contains the Deck class."""


from collections import namedtuple
import random


Card = namedtuple("Card", ("rank", "suit"))


def _str_card(card):
    """
    Changes the way Card objects are written as strings.
    """
    return f"{card.rank} of {card.suit}s"


Card.__str__ = _str_card


def is_ace(card):
    """
    Determines if the card is an Ace or not.
    """
    return card.rank == "Ace"


Card.is_ace = is_ace


def card_value(card):
    """
    Determines the value of the card.
    """
    return Deck.values_dict[card.rank]


Card.value = card_value


class Deck:
    """
    A class object representing a deck of cards, including
    its necessary functions.
    """

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Club Heart Spade Diamond".split()
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))

    def __init__(self):
        """
        Initializer for the class Deck.
        """
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]
        self._cut_card = (len(self._cards) / 4) + random.randint(
            -((len(self._cards) / 4) // 4), ((len(self._cards) / 4) // 4)
        )

    def get_cards(self):
        """
        Gets the ._cards data member.
        """
        return self._cards

    def get_cut_card(self):
        """
        Returns the cut card position
        """
        return self._cut_card

    def size(self):
        """
        Returns the size of the deck.
        """
        return len(self._cards)

    def deal(self):
        """
        Deals a single card from the deck.
        """
        return self._cards.pop()

    def merge(self, other_deck):
        """
        Merges a deck of cards with another deck of cards.
        """
        self._cards = self._cards + other_deck.get_cards()
        self._cut_card = (len(self._cards) / 4) + random.randint(
            -((len(self._cards) / 4) // 4), ((len(self._cards) / 4) // 4)
        )

    def shuffle(self):
        """
        Shuffles the deck of cards, then cuts it.
        """
        random.shuffle(self._cards)

    def cut(self):
        """
        Cuts the deck of cards.
        """
        deck_half = len(self._cards) / 2
        self._cards = (
            self._cards[int(deck_half) :] + self._cards[: int(deck_half)]
        )

    def reshuffle(self, discard_pile):
        """
        Reshuffles a fresh stack of cards to be added back into the deck.
        """
        random.shuffle(discard_pile)
        self._cards = self._cards + discard_pile
        self._cut_card = (len(self._cards) / 4) + random.randint(
            -((len(self._cards) / 4) // 4), ((len(self._cards) / 4) // 4)
        )
