# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [-1, -3]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    # ball_pos[0] horizontal velocity: random.randrange(120, 240)
    # ball_pos[1] vertical velocity: random.randrange(60, 180)
    if direction == "Right":
        ball_vel[0] = random.random()*2 + 2
        ball_vel[1] = -(random.random()*2 + 1)
    elif direction == "Left":
        ball_vel[0] = -(random.random()*2 + 2)
        ball_vel[1] = -(random.random()*2 + 1)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball("Right")

def button_handler():
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS - 1)):
        ball_vel[1] = - ball_vel[1]
    
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) and ball_pos[1] <= (paddle1_pos + 40) and ball_pos[1] >= (paddle1_pos - 40):
        ball_vel[0] = - (ball_vel[0] * 1.1)
    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        spawn_ball("Right")
        score2 += 1
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS - 1 - PAD_WIDTH) and ball_pos[1] <= (paddle2_pos + 40) and ball_pos[1] >= (paddle2_pos - 40):
        ball_vel[0] = - (ball_vel[0] * 1.1)
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS - 1 - PAD_WIDTH):
        spawn_ball("Left")
        score1 += 1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Pink", "Pink")

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel >= 40) and (paddle1_pos + paddle1_vel <= HEIGHT - 40):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel >= 40) and (paddle2_pos + paddle2_vel <= HEIGHT - 40):
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polyline([(4, paddle1_pos - 40), (4, paddle1_pos + 40)], 8, 'White')
    
    canvas.draw_polyline([(596, paddle2_pos - 40), (596, paddle2_pos + 40)], 8, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), (200,50), 40, "Teal")
    canvas.draw_text(str(score2), (375,50), 40, "Teal")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", button_handler, 50)

# start frame
new_game()
frame.start()