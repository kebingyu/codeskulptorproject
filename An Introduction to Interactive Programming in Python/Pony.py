###################################
# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
INIT_VEL = 5
INCRE_VEL = 1

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]



# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH/2
    ball_pos[1] = random.randrange(0 + BALL_RADIUS/2, HEIGHT - BALL_RADIUS/2)
    if (direction):
        ball_vel[0] = random.randrange(1, INIT_VEL)
    else:
        ball_vel[0] = random.randrange(-INIT_VEL, -1)
    ball_vel[1] = random.randrange(-INIT_VEL, -1)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(random.randrange(0, 2))
    # reset paddle
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    #reset score
    score1 = score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS/2, BALL_RADIUS, 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[0] = paddle1_pos[0] + paddle1_vel[0]
    paddle1_pos[1] = paddle1_pos[1] + paddle1_vel[1]
    paddle2_pos[0] = paddle2_pos[0] + paddle2_vel[0]
    paddle2_pos[1] = paddle2_pos[1] + paddle2_vel[1]
    
    # reflection detection
    ## if touch top and bottom line
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = reflect(ball_vel[1])
    elif (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    ## if touch left paddle
    if (ball_pos[0] <= PAD_WIDTH):
        if (ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
        else:
            score2 += 1
            spawn_ball(1)
    ## if touch right paddle
    elif (ball_pos[0] >= WIDTH - PAD_WIDTH):
        if (ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = reflect(ball_vel[0])
        else:
            score1 += 1
            spawn_ball(0)
    
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT], 
        [paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]-HALF_PAD_HEIGHT],
        [paddle1_pos[0]+HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT], 
        [paddle1_pos[0]-HALF_PAD_WIDTH, paddle1_pos[1]+HALF_PAD_HEIGHT]], 1, 'White', 'White')
    canvas.draw_polygon([[paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT], 
        [paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]-HALF_PAD_HEIGHT],
        [paddle2_pos[0]+HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT], 
        [paddle2_pos[0]-HALF_PAD_WIDTH, paddle2_pos[1]+HALF_PAD_HEIGHT]], 1, 'White', 'White')    
    
    # draw scores   
    canvas.draw_text(str(score1), [0.25*WIDTH, 0.25*HEIGHT], 50, 'White')
    canvas.draw_text(str(score2), [0.75*WIDTH, 0.25*HEIGHT], 50, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if (chr(key) == '&'):
        paddle2_vel[1] = -INIT_VEL
    if (chr(key) == '('):
        paddle2_vel[1] = INIT_VEL
    if (chr(key) == 'W'):
        paddle1_vel[1] = -INIT_VEL
    if (chr(key) == 'S'):
        paddle1_vel[1] = INIT_VEL
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (chr(key) == '&'):
        paddle2_vel[1] = 0
    if (chr(key) == '('):
        paddle2_vel[1] = 0
    if (chr(key) == 'W'):
        paddle1_vel[1] = 0
    if (chr(key) == 'S'):
        paddle1_vel[1] = 0

def restart():
    new_game()
    
def reflect(v):
    if (v >= 0):
        return -(v+INCRE_VEL)
    else:
        return INCRE_VEL-v
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 100)


# start frame
new_game()
frame.start()
###################################
