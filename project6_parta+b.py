# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

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
        self.cards = []	# create Hand object

    def __str__(self):
        to_print = ""
        for card in self.cards:
            to_print += (card.suit + card.rank + " ") 
        return "Hand contains: " + to_print # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        has_ace = False
        for card in self.cards:
            hand_value += VALUES[card.rank]
            if card.rank == 'A':
                has_ace = True # compute the value of the hand, see Blackjack video
        if has_ace == False:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
            # draw a hand on the canvas, use the draw method for cards
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank)) # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        self.dealt_card = self.cards[random.randrange(len(self.cards)-1)]
        return self.dealt_card
        self.cards.remove(self.dealt_card) # deal a card object from the deck
    
    def __str__(self):
        to_print = ""
        for card in self.cards:
            to_print += (card.suit + card.rank + " ")
        return "Deck contains: " + to_print # return a string representing the deck

deck = Deck()
dealer_hand = Hand()
player_hand = Hand()

#define event handlers for buttons
def deal():
    global outcome, score, in_play, deck, dealer_hand, player_hand

    deck = Deck()
    deck.shuffle()
    
    # deals to dealer (a hand)
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "dealer hand", dealer_hand
    print "dealer hand value", dealer_hand.get_value()
    # deals to player
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "player hand", player_hand
    print "player hand value", player_hand.get_value()
    
    if in_play:
        score -= 1
        outcome = "You lost!"
    else:
        in_play = True
        outcome = "Hit or Stand?"

def hit():
    global outcome, in_play, score
    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        outcome = "Hit or Stand?"
        print "player hand", player_hand
        print "player hand value", player_hand.get_value()
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = "You have busted! New Deal?"
        print "You have busted!"
        print player_hand.get_value()
        in_play = False
        score -= 1
        
def stand():
    global in_play, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        print "dealer hand", dealer_hand
        print "dealer hand value", dealer_hand.get_value()
    in_play = False
    if dealer_hand.get_value() > 21:
        outcome = "Dealer busted! You win! New Deal?"
        print "Dealer busted! You win!"
        score += 1
        print score
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "Dealer wins! New Deal?"
        print "Dealer wins!"
        score -= 1
        print score
    elif dealer_hand.get_value() < player_hand.get_value():
        outcome = "You win! New Deal?"
        print "You win!"
        score += 1
        print score
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (200, 60), 50, 'White')
    dealer_hand.draw(canvas, [70, 150])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [70 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    player_hand.draw(canvas, [70, 450])
    canvas.draw_text(outcome, (80,350), 30, 'White')
    canvas.draw_text(("score: "+str(score)),(200,100), 20, 'White')

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