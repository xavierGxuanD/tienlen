#!/usr/bin/env python

import random
from typing import Iterator
from card import (Card)
from hand import (Hand)
from constants import (SUITS,RANKS)

class Deck():
    """A class to represent a deck of cards, in "new deck order" set by RANK, then SUIT.

    Attributes:
        
    """
    def __init__(self, seed: int | None=None) -> None:
        self.seed = seed

        if seed is None:
            self.seed = random.randint(0,100000000)
        self._rng = random.Random(self.seed)
        
        self.deck_stack: list[Card] = []
        for rank in RANKS:
            for suit in SUITS:
                self.deck_stack.append(Card(rank, suit))

    def __iter__(self) -> Iterator[Card]:
        return iter(self.deck_stack)

    def __len__(self) -> int:
        return len(self.deck_stack)
    
    def __str__(self) -> str:
        stack = ""
        for card in self.deck_stack:
            stack += f"{card}\n"
        return stack

    def shuffle(self):
        self._rng.shuffle(self.deck_stack)

    def deal(self, pile_number: int) -> list[Hand]:
        deck_size = len(self)
        if pile_number == 0:
            raise ZeroDivisionError("Cannot deal cards to 0 piles")
        quarter_deck = (deck_size//pile_number)
        hands = []
        for i in range(0,pile_number):
            hands.append(Hand(self.deck_stack[quarter_deck*i:quarter_deck*(i+1)]))
        return hands

    def __getitem__(self,key):
        return self.deck_stack[key]

def main():
    test = Deck(seed=None)
    test.shuffle()
    hands = test.deal(4)
    for hand in hands:
        print(hand)
        print("\n")
if __name__ == "__main__":
    main()
