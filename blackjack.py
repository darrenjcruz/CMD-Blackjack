#!/usr/bin/env python3
# Darren Cruz
# CPSC 386-02
# 2023-02-16
# darrencruz@csu.fullerton.edu
# @darrenjcruz
#
# Lab 02-00
#
# This is the blackjack module for the Blackjack game and it runs the game
#


"""blackjack.py file: runs the game."""


from blackjackgame import game


def main():
    """
    Runs the blackjack game.
    """
    blackjack = game.BlackjackGame()
    blackjack.run()


if __name__ == "__main__":
    main()
