import pygame
import sys
from cardrender import CardRenderer
from deck import Deck
from constants import (SCREEN_HEIGHT, SCREEN_WIDTH, CARD_W, CARD_H)
from hand import (Hand)
from rules import (beats)
from bot import choose_play

from logger import (log_state, log_event)
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()

    temp0 = CardRenderer(CARD_W,CARD_H)
    #Building new deck
    #seeded for development purposes
    originaldeck = Deck(seed=4)

    # render faces
    faces = {card: temp0.render(card) for card in originaldeck}
    originaldeck.shuffle()
    print(len(faces), faces[originaldeck[0]].get_size())

    # card back render
    card_back = temp0.back()
    card_back_sideways = pygame.transform.rotate(card_back, 90)
    
    #init game
    card_piles = originaldeck.deal(4)
    game = Game(card_piles)

    # bot runner

    def bot_move():
        current_player = game.current
        bot_play = choose_play(game.hands[current_player], game.pile)
        if bot_play is None:
            game.pass_turn()
            print(f"bot {current_player} passed the turn")
        else:
            if not game.play(bot_play): 
                game.pass_turn()
                print(f"bot {current_player} passed the turn")
            else:
                print(f"bot {current_player} played {bot_play}")
        

    def run_bots():
        while game.current != 0 and (not game.check_game_over()):
            bot_move()

    def player_can_act() -> bool:
        return game.current == 0 and (not game.check_game_over())
    
    #drawing hands
    max_width = 990
    max_step = 160

    # helper function for updating player_hand rects
    def layout_player():
        return game.hands[0].layout((CARD_W,CARD_H),
                                  max_width,
                                  max_step,
                                  screen_rect.centerx,
                                  SCREEN_HEIGHT - 20)

    # center pile setup
    def layout_center_pile():
        return game.pile.layout((CARD_W, CARD_H),
                                  500,
                                  max_step,
                                  screen_rect.centerx,
                                  screen_rect.centery + (CARD_H // 2))

    # layout top opponent hand 
    def layout_top_opponent():
        return game.hands[2].layout((CARD_W, CARD_H),
                                    700,
                                    max_step,
                                    screen_rect.centerx,
                                    230)

    #layot side opponents
    side_margin = 20
    side_max_height = 430

    # helper functions for the side opponents (seat 1 left, seat 3 right)
    def layout_left_opponent():
        return game.hands[1].column(card_back_sideways.get_size(),
                                    side_max_height,
                                    max_step,
                                    245,
                                    side_margin)

    def layout_right_opponent():
        return game.hands[3].column(card_back_sideways.get_size(),
                                    side_max_height,
                                    max_step,
                                    245,
                                    SCREEN_WIDTH - side_margin - card_back_sideways.get_width())
    
    # game running basics
    clock = pygame.time.Clock()
    dt = 0.0
    DELAY = 0.6
    timer = 0.0
    #tracks selected cards
    selected_cards = set()

    #card lift
    selected_card_lift = 25

    #layout helper
    layout = {}
    def relayout():
        layout["player"] = layout_player()
        layout["pile"] = layout_center_pile()
        layout["top"] = layout_top_opponent()
        layout["left"] = layout_left_opponent()
        layout["right"] = layout_right_opponent()
    relayout()
    # Game Loop
    while True:
        log_state() 
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for card, area in reversed(layout["player"]):
                            if card in selected_cards:
                                if area.move(0,-selected_card_lift).collidepoint(event.pos):
                                    selected_cards.remove(card) 
                                    print(f"removed: {card}")
                                    break
                            else:
                                if area.collidepoint(event.pos):     
                                    selected_cards.add(card)
                                    print(f"selected: {card}")
                                    break 
                case pygame.KEYDOWN if player_can_act():
                    if event.key == pygame.K_RETURN:
                        if selected_cards:
                            if game.play(selected_cards):  
                                relayout()
                                selected_cards = set()
                            else:
                                print("selection does not beat pile")
                    elif event.key == pygame.K_p:
                        game.pass_turn() 
                        relayout()
                        selected_cards = set()
        #bot move area
        if game.current != 0 and not game.check_game_over():
            timer += dt
            if timer >= DELAY:
                timer = 0
                bot_move()
                relayout()
                

        #draw table color
        screen.fill((20, 80, 50))
    
        #blit player hand
        for card, rect in layout["player"]:
            if card in selected_cards:
                screen.blit(faces[card], rect.move(0, -selected_card_lift))
            else:
                screen.blit(faces[card], rect)

        #blit center pile
        for card, rect in layout["pile"]:
            screen.blit(faces[card], rect)

        #blit top opponent hand, showing card back
        for _, rect in layout["top"]:
            screen.blit(card_back, rect)

        #blit side opponents
        for _, rect in layout["left"]:
            screen.blit(card_back_sideways, rect)
        for _, rect in layout["right"]:
            screen.blit(card_back_sideways, rect)
            
        pygame.display.flip()

        

        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()
