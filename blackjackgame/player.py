#!/usr/bin/env python3
# Darren Cruz
# CPSC 386-02
# 2023-02-16
# darrencruz@csu.fullerton.edu
# @darrenjcruz
#
# Lab 02-00
#
# This is the player module, it contains the Player class
#


"""players.py file: contains the Player class."""


import locale
import blackjackgame.cards


class Player:
    """
    A class object representing a standard player, including
    its necessary functions.
    """

    def __init__(self, name):
        """
        Initializer for the class Player.
        """
        self._name = name
        self._hand = []
        self._does_hit = False

    @property  # p.name() = p.name -> f"{p.name}, it's your turn."
    def name(self):
        """
        Gets the name of the player.
        """
        return self._name

    def __str__(self):
        """
        Returns the player's name when using the str() method.
        """
        return self._name

    def __repr__(self):
        """
        Returns the both the player's id and name when using the repr() method.
        """
        return f"Player('{self._name}')"

    def take_card(self, card):
        """
        Adds a card to the player's hand.
        """
        self._hand.append(card)

    def get_hand(self):
        """
        Returns the cards in the player's hand.
        """
        return self._hand

    def get_hand_str(self):
        """
        Returns a string containing the cards in the player's hand.
        """
        message = ""
        for card in self._hand:
            message += str(card) + ", "
        return message

    def get_hand_value(self):
        """
        Returns the value of the player's hand.
        """
        total = 0
        for card in self._hand:
            total += blackjackgame.cards.card_value(card)

        for card in self._hand:
            if card.rank == "Ace" and total < 12:
                total += 10

        return total

    def discard_card(self):
        """
        Discards a card to the discard pile.
        """
        return self._hand.pop()


class BlackjackPlayer(Player):
    """
    A class object representing a Blackjack Player, including
    its necessary functions.
    """

    def __init__(self, name, bankroll=10000):
        """
        Initializer for the class BlackjackPlayer.
        """
        super().__init__(name)
        self._balance = bankroll
        self._bet = 0
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    @property
    def bankroll(self):
        """
        Returns the player's balance.
        """
        return locale.currency(self._balance, grouping=True)

    @property
    def bet(self):
        """
        Returns the player's betting amount.
        """
        return locale.currency(self._bet, grouping=True)

    @bet.setter
    def bet(self, wager):
        """
        Sets the player's betting amount.
        """
        self._bet = wager

    def __str__(self):
        """
        Return the player's info when using the str() method.
        """
        return f"{self._name} - {self.bankroll}"

    def __repr__(self):
        """
        Returns the player's id, name and balance when using the repr() method.
        """
        return (
            "BlackjackPlayer("
            + f"'{self._name}', bankroll ="
            + " {self._balance})"
        )

    def get_balance(self):
        """
        Return the player's balance.
        """
        return self._balance

    def set_balance(self, amount):
        """
        Sets the player's balance.
        """
        self._balance = amount

    def get_bet(self):
        """
        Returns the player's bet.
        """
        return self._bet

    def deduct_bet(self):
        """
        Subtracts the player's bet from their balance.
        """
        self._balance = self._balance - self._bet

    def win(self):
        """
        Adds the player's winnings to their balance.
        """
        self._balance = self._balance + (self._bet * 2)

    def push(self):
        """
        Adds the player's bet back to their balance.
        """
        self._balance = self._balance + self._bet
