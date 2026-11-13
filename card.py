#!/usr/bin/env python
from constants import (SUITS, RANKS)

class Card():
    """A class to represent cards in a standard 52 card deck.  

    Attributes:
        none
    """
    def __init__(self,
                 rank: str,
                 suit: str
                 ) -> None:
        """Initializes a card.   

        Attributes:
            rank: The rank of the card. Valid ranks are of the standard 52 card deck. 
            suit: The suit of the card. Valid suits are of the standard 52 card deck. Naming convention is "Hearts" for example.
        """
        self.rank = rank
        self.suit = suit
        self.rank_index = RANKS.index(rank)
        self.suit_index = SUITS.index(suit)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        else: 
           return (self.rank_index == other.rank_index) and (self.suit_index == other.suit_index)

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __lt__(self, other: "Card") -> bool:
        """Compares values of cards based on suit, and rank, determined by
           RANKS and SUITS configurable constants. 
        """
        if self.rank_index == other.rank_index:
            return self.suit_index < other.suit_index
        else:
            return self.rank_index < other.rank_index
        
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        return f"Card({self.rank!r}, {self.suit!r})"
