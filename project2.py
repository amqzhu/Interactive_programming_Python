# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

#secret_number = 0
#guess_count = 2

# helper function to start and restart the game
def new_game(x,y):
    # initialize global variables used in your code here
    global secret_number 
    secret_number = random.randrange(x,y)
    global guess_count
    guess_count = math.ceil(math.log(y-x,2))


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number
    secret_number = random.randrange(0,100)
    print "Range is [0,100)"
    new_game(0,100)

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    secret_number = random.randrange(0,1000)
    print "Range is [0,1000)"
    new_game(0,1000)
    
def input_guess(guess):
    # main game logic goes here	
    
    global guess_count
    
    print "Number of remaining guesses is", int(guess_count)
    
    print "Guess was", guess
    guess = int(guess)
    
    if guess == secret_number:
        print "Correct"
    elif guess < secret_number:
        print "Higher"
    else:
        print "Lower"
        
    if guess_count > 1:
        guess_count = guess_count - 1
    else:
        print "You have no more guesses left"
        new_game(0,100)
  
    
# create frame
frame = simplegui.create_frame("Game", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100)
frame.add_button("Range: 0 - 1000", range1000)
frame.add_input("New Guess",input_guess,100)



# call new_game 
new_game(0,100)
frame.start()

# always remember to check your completed program against the grading rubric
