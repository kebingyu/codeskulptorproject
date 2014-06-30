# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        s = "Hand contains"
        for card in self.cards:
            s += ' ' + str(card)
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_aces = False
        for card in self.cards:
            r = card.get_rank()
            value += VALUES[r]
            if ('A' == r):
                has_aces = True
        if has_aces and value + 10 <= 21:
            return value + 10
        else:
            return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards:
            card.draw(canvas, (pos[0] + i*CARD_SIZE[0]*1.2, pos[1]))
            i += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        s = "Deck contains"
        for card in self.cards:
            s += ' ' + str(card)
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    outcome = ''
    in_play = True

def hit():
    # if the hand is in play, hit the player
    global player, deck, outcome, score, in_play
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())   
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = 'Player busted'
            score -= 1
            in_play = False
       
def stand():
    global player, dealer, deck, outcome, score, in_play
    player_value = player.get_value()
    if in_play and player_value > 21:
        outcome = 'Player busted'
        score -= 1
        in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        # assign a message to outcome, update in_play and score
        dealer_value = dealer.get_value()    
        player_won = False
        if dealer_value > 21:
            player_won = True
        else:
            if player_value > dealer_value:
                player_won = True
        if player_won:
            outcome = 'Player won'
            score += 1
        else:
            outcome = 'Dealer won'
            score -= 1
        in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_text('Dealer hand', (50, 50), 40, 'Black')
    canvas.draw_text('Player hand', (50, 350), 40, 'Black')
    dealer.draw(canvas, [50, 100])
    player.draw(canvas, [50, 400])
    canvas.draw_text(outcome, (400, 250), 30, 'Black')
    canvas.draw_text("score: %d" % score, (400, 300), 30, 'Black')
    # block the first card of dealer
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
            [50 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

