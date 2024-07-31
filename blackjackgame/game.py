#!/usr/bin/env python3
# Darren Cruz
# CPSC 386-02
# 2023-02-16
# darrencruz@csu.fullerton.edu
# @darrenjcruz
#
# Lab 02-00
#
# This is the game module, it contains the BlackjackGame class.
#


"""game.py file: containins the BlackjackGame class."""

import locale
import os
import os.path
import pickle
from blackjackgame.player import Player, BlackjackPlayer
from blackjackgame.cards import Deck


class BlackjackGame:
    """
    A class object representing a Blackjack game,
    including its necessary functions.
    """

    def __init__(self):
        """
        Initializer for the class BlackjackGame.
        """
        self._dealer = Player("dealer")
        self._players = []
        self._deck = Deck()
        self._discard_pile = []

    def start(self):
        """
        The starting function which asks for how many player and player info.
        """
        main_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(main_dir, "data")
        pickle_file = os.path.join(data_dir, "players.pkl")
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        for _ in range(7):
            deck = Deck()
            self._deck.merge(deck)
        self._deck.shuffle()
        self._deck.cut()

        num_players = 0

        while num_players > 4 or num_players < 1:
            num_players = int(
                input("Welcome to Blackjack!" + "\n\nHow many players? ")
            )
            if num_players > 4 or num_players < 1:
                print(f"Please select a number between 1 and 4")

        for _ in range(num_players):
            name = input("\nEnter player's name: ")
            if os.path.exists(pickle_file):
                with open(pickle_file, "rb") as opened:
                    player_list = pickle.load(opened)
                for old_player in player_list:
                    if name == old_player.name:
                        self._players.append(old_player)
                        print(f"Found {name}'s profile in the save file.\n")

                if len(self._players) == 0 or self._players[-1].name != name:
                    self._players.append(BlackjackPlayer(name))

            else:
                self._players.append(BlackjackPlayer(name))

    def end(self):
        """
        The ending phase of the game.
        """
        print(
            "\n\nThank you for playing, hope you had fun!"
            + "\nSaving all the player's profile to a file."
        )
        main_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(main_dir, "data")
        pickle_file = os.path.join(data_dir, "players.pkl")
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        with open(pickle_file, "wb") as opened:
            pickle.dump(self._players, opened, pickle.HIGHEST_PROTOCOL)

    def wager(self):
        """
        Collects the player's bets.
        """
        print("\n\n==========\n  WAGERS  \n==========\n")
        for i in self._players:
            wager = 0
            while wager > i.get_balance() or wager < 1:
                print(str(i))
                wager = int(input(f"How much would you like to wager? "))
                if wager > i.get_balance() or wager < 1:
                    print(
                        "Please enter a number between 0 and "
                        + f"{i.get_balance()}"
                    )
            i.bet = wager
            print()
            i.deduct_bet()

    def discard_hand(self, player):
        """
        Discard's the player's hand.
        """
        for _ in range(len(player.get_hand())):
            self._discard_pile.append(player.discard_card())

    def first_deal(self):
        """
        First round blackjackgame.cards dealt.
        """
        print("\n\n=================\n  DEALING CARDS  \n=================\n")
        for i in self._players:
            print(str(i))
            print(f"Wager: {i.bet}")
            self.discard_hand(i)
            i.take_card(self._deck.deal())
            print("Hand: " + i.get_hand_str())
            print()

        print("Dealer:")
        print("Hand: ___ of ___s\n")
        self.discard_hand(self._dealer)
        self._dealer.take_card(self._deck.deal())

    def second_deal(self):
        """
        Second round blackjackgame.cards dealt.
        """
        for i in self._players:
            print(str(i))
            print(f"Wager: {i.bet}")
            i.take_card(self._deck.deal())
            print("Hand: " + i.get_hand_str())
            print()

        print("Dealer:")
        self._dealer.take_card(self._deck.deal())
        print("Hand: ___ of ___s, " + str(self._dealer.get_hand()[1]))
        print()

    def turn(self):
        """
        Individual turns after the inital two blackjackgame.cards dealt.
        """
        for i in self._players:
            print(f"\n{i.name}'s turn\n---------------")
            print(f"Balance: {i.bankroll}\nWager: {i.bet}")
            print("Hand: " + i.get_hand_str())
            double_down = ""

            while double_down not in ("yes", "no"):
                double_down = str(input("\nWould you like to double-down? "))
                print(double_down)
                if double_down not in ("yes", "no"):
                    print('\nPlease enter either "yes" or "no"')

            if double_down == "yes" and (i.get_balance() < i.get_bet()):
                print("\nSorry, you do not have the funds to double-down.\n")

            elif double_down == "yes":
                i.deduct_bet()
                i.bet = i.get_bet() * 2
                print(f"\nBalance: {i.bankroll}\nWager: {i.bet}")
                i.take_card(self._deck.deal())
                print("Hand: " + i.get_hand_str())
                if i.get_hand_value() > 21:
                    print(f"\n{i.name}, you bust!")
                print()
                continue

            choice = ""

            while choice not in ("hit", "stand"):
                choice = input("\nWould you like to hit or stand? ")
                if choice not in ("hit", "stand"):
                    print('\nPlease enter either "hit" or "stand"')

                elif choice == "hit":
                    i.take_card(self._deck.deal())
                    print("Hand: " + i.get_hand_str())

                    if i.get_hand_value() > 21:
                        print(f"\n{i.name}, you bust!")
                        break

                else:
                    print(f"\n{i.name}, you stand")
                    print()
                    break

                choice = ""

    def dealer_turn(self):
        """
        Dealer's turn.
        """
        print("Dealer flips face-down card:")
        print("Hand: " + self._dealer.get_hand_str())
        print()
        hand_value = self._dealer.get_hand_value()

        while hand_value < 22:
            if hand_value < 17:
                print("\nDealer hits -")
                self._dealer.take_card(self._deck.deal())
                print("Hand: " + self._dealer.get_hand_str())
                hand_value = self._dealer.get_hand_value()

            else:
                print("\nDealer stands -")
                print()
                break

        if hand_value >= 22:
            print("\nDealer busts!")
            print()

    def result_of_round(self):
        """
        Results of the round.
        """
        print("\n\n=========\nResults\n=========\n")
        dealer_value = self._dealer.get_hand_value()
        print("Dealer\n---------------")
        print(
            "Hand: " + self._dealer.get_hand_str() + " -> " + str(dealer_value)
        )
        if dealer_value > 21:
            print("Dealer busts!")

        print()
        for player in self._players:
            print(f"{player.name}\n---------------")
            print(f"Balance: {player.bankroll}")
            print(f"Wager: {player.bet}")
            player_value = player.get_hand_value()
            print("Hand: " + player.get_hand_str() + " -> " + str(player_value))
            if player_value > 21:
                print(f"{player.name} busts!\n")
                player.bet = 0

            elif (player_value > dealer_value) or (
                player_value <= 21 < dealer_value
            ):
                print(f"{player.name} wins!\n")
                player.win()
                player.bet = 0

            elif player_value == dealer_value:
                print(f"{player.name} pushed!\n")
                player.push()
                player.bet = 0

            else:
                print(f"{player.name} lost!\n")
                player.bet = 0

    def round(self):
        """
        Plays a round of Blackjack.
        """
        self.wager()
        self.first_deal()
        self.second_deal()
        self.turn()
        self.dealer_turn()
        self.result_of_round()

        for player in self._players:
            if player.get_balance() == 0:
                print(
                    "An anonymous donation of $10,000.00 has "
                    + f"been given to {player.name}"
                )
                player.set_balance(10000)
        if self._deck.size() < self._deck.get_cut_card():
            self._deck.reshuffle(self._discard_pile)

    def run(self):
        """
        Runs the game of Blackjack.
        """
        self.start()
        print("\n\n---------- Round 1 ----------\n")
        match = 1
        self.round()
        cont = ""

        while cont not in ("yes", "no"):
            cont = input("Would the group like to play another round? ")
            if cont not in ("yes", "no"):
                print('\nPlease enter either "yes" or "no"')
            elif cont == "yes":
                match += 1
                print(f"\n\n---------- Round {match} ----------\n")
                self.round()
            else:
                break
            cont = ""

        self.end()
