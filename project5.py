# implementation of card game - Memory

import simplegui
import random

list1 = range(0,8)
list2 = range(0,8)
total_list = list1 + list2

random.shuffle(total_list)

exposed = [False] * 16
turn = 0
first_card = None
second_card = None

# helper function to initialize globals
def new_game():
    global exposed, state, turn
    random.shuffle(total_list)
    state = 0
    turn = 0
    exposed = [False] * 16
    label.set_text("Turn = " + str(turn))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turn, first_card, second_card, success
    index = pos[0] / 50
    
    if state == 0:
        state = 1
        first_card = index
        if exposed[first_card] == False:
            exposed[first_card] = True
    elif state == 1 and index != first_card and exposed[index] == False:
        turn += 1
        if exposed[index] == False:
            second_card = index
            if exposed[second_card] == False:
                exposed[second_card] = True
                if total_list[first_card] == total_list[second_card]:
                    exposed[first_card] = True
                    exposed[second_card] = True
        state = 2
        label.set_text("Turn = " + str(turn))
    elif state == 2 and index != first_card and index != second_card and exposed[index] == False:
        if total_list[first_card] != total_list[second_card]:
            exposed[first_card] = False
            exposed[second_card] = False
        state = 1
        first_card = index
        if exposed[first_card] == False:
            exposed[first_card] = True
             
# cards are logically 50x100 pixels in size    
def draw(canvas):
    slot = 0
    for i in total_list:
        canvas.draw_text(str(i), [18 + 50 * slot, 60], 30, "White")
        slot += 1
    for i in range(16):
        if exposed[i] == False:
            canvas.draw_polygon([[50*i, 0], [50*(i+1), 0], [50*(i+1), 100], [50*(i), 100]], 1, 'Yellow', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turn = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric