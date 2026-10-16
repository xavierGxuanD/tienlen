#!/usr/bin/env python

import pygame
from typing import NamedTuple
from card import Card
from constants import(BODY_COLOR, CARD_BACK, CARD_RED,CARD_BLACK, OUTLINE_COLOR, SUITS, RANKS)


rank_map: dict[str, str] = {
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
    "Jack": "J",
    "Queen": "Q",
    "King": "K",
    "Ace": "A",
    "2": "2"
}

class Suit(NamedTuple):
    letter: str
    color: tuple[int, int, int]

suit_map: dict[str, Suit] = {
    "Spades": Suit("S", CARD_BLACK),
    "Clubs": Suit("C", CARD_BLACK),
    "Diamonds": Suit("D", CARD_RED),
    "Hearts": Suit("H", CARD_RED)
}

class CardRenderer():
    def __init__(self, width: int, height: int, font_path: str | None = None) -> None:
        self.width = width
        self.height = height
        self.radius = width // 18
        self.inset = width // 15
        self.outline_width = max(1, width // 75)
        self.font = pygame.font.Font(font_path, height // 5)

        missing_ranks = set(RANKS) - set(rank_map)
        missing_suits = set(SUITS) - set(suit_map)
        if missing_ranks:
            raise ValueError(f"rank_map has no entry for {sorted(missing_ranks)}")
        if missing_suits:
            raise ValueError(f"suit_map has no entry for {sorted(missing_suits)}")

    def render(self, card: Card) -> pygame.Surface:
        base = self._blank_card()
        suit_color = suit_map[card.suit].color
        rank_surface = self.font.render(rank_map[card.rank], True, suit_color)
        suit_surface = self.font.render(suit_map[card.suit].letter, True, suit_color)
        rank_rect = rank_surface.get_rect(topleft=(self.inset, self.inset))
        suit_rect = suit_surface.get_rect(midtop=rank_rect.midbottom)
        base.blit(rank_surface, rank_rect)
        base.blit(suit_surface, suit_rect)
        return base.convert_alpha()

    def _blank_card(self) -> pygame.Surface:
        surf = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf,
                         BODY_COLOR,
                         surf.get_rect(),
                         border_radius=self.radius)
        pygame.draw.rect(surf,
                         OUTLINE_COLOR,
                         surf.get_rect(),
                         border_radius=self.radius,
                         width=self.outline_width)
        return surf
    
    def back(self) -> pygame.Surface:
        base = self._blank_card()
        margin = self.inset
        border_inset = base.get_rect().inflate(-2*margin, -2*margin)
        pygame.draw.rect(base,
                         CARD_BACK,
                         border_inset,
                         border_radius=max(1,self.radius - 3))
        return base.convert_alpha()
        
        
