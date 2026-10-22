#!/usr/bin/env python

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Button constants
BUTTON_TEXT = (255, 255, 255)
BUTTON_HIGHLIGHT = (230, 205, 59)

# Card Constants
CARD_W = 150
CARD_H = round(CARD_W * 7 / 5)
CORNER_RADIUS = round((1/18)*CARD_W)

CARD_RED = (190,30,40)
CARD_BLACK = (25,25,30)
CARD_BACK = (240, 90, 58)

BODY_COLOR = (248,246,240)
OUTLINE_COLOR = (60,60,65)

SUITS: list[str] = ["Spades", "Clubs", "Diamonds", "Hearts"]   
RANKS: list[str] = [
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
    "Ace",
    "2",
]
