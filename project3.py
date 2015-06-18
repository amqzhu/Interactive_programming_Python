# template for "Stopwatch: The Game"

import simplegui

# define global variables
time = 0
success = 0
total = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t / 600
    rest1 = t - minute*600
    second1 = rest1 / 100
    rest2 = rest1 - second1*100
    second2 = rest2 / 10
    last_digit = t - minute*600 - second1*100 - second2*10
    formatted = str(minute)+":"+str(second1)+str(second2)+"."+str(last_digit)
    return formatted
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    timer.start()   

def stop_button():
    global total
    global success
    if timer.is_running() == True:
        total += 1
        if time % 10 == 0:
            success += 1
    timer.stop()
    
def reset_button():
    timer.stop()
    global time
    time = 0
    global total
    total = 0
    global success
    success = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    time_displayed = format(time)
    canvas.draw_text(str(time_displayed),[90,160],50,"White","serif")
    display_text = str(success) + "/" + str(total)
    canvas.draw_text(display_text,[250,30],25,"Grey")
    
    
# create frame
frame = simplegui.create_frame("Timer",300,300)

# register event handlers
frame.set_draw_handler(draw_handler)

frame.add_button("Start", start_button,50)
frame.add_button("Stop", stop_button,50)
frame.add_button("Reset", reset_button,50)
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
