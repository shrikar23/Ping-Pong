# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
import random

# initialize global variables - position and velocity encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 8
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos =[0,0]
ball_vel = [0,0]
start_flag = "N"
message = "Please press START to start a new game"
message1 = "Use the up and down arrow keys to move the red paddle"
message2 = 'Use "w" and "s" keys to move blue paddle'


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    
    # set the ball position
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    
    #depending on the direction, set the ball velocity. (either upper right or upper left)
    if direction == "right":
        ball_vel[0] = 2
        ball_vel[1] = -1
        
    if direction == "left":
        ball_vel[0] = -2
        ball_vel[1] = -1
        
# define event handlers

# Initialize all the variables and start a new game.
# First time the ball will always move to Upper Right.
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
    paddle2_pos = [WIDTH - (PAD_WIDTH / 2), HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball("right")

# Event handler for draw
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
     
    if start_flag == "N":
        canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
        canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
        canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "red", "white")
        canvas.draw_line([paddle1_pos[0], paddle1_pos[1] + (PAD_HEIGHT / 2)], [paddle1_pos[0], paddle1_pos[1] - (PAD_HEIGHT / 2)], PAD_WIDTH, "blue")
        canvas.draw_line([paddle2_pos[0] ,paddle2_pos[1] + (PAD_HEIGHT / 2)], [paddle2_pos[0], paddle2_pos[1] - (PAD_HEIGHT / 2)], PAD_WIDTH, "Red")
        canvas.draw_text(message, (60,50), 30, "white")
        canvas.draw_text(message1, (60, 80), 20, "white")
        canvas.draw_text(message2, (60, 110), 20, "white")
    else:      
    # draw mid line and gutters
        canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
        canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
        canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position. also check for reflection form top and bottom.
        ball_pos[0] = ball_pos[0] + ball_vel[0]
        ball_pos[1] = ball_pos[1] + ball_vel[1]
    
        if ball_pos[1]  <= BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]
            ball_pos[1] = ball_pos[1] + ball_vel[1]
        
        if ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]
            ball_pos[1] = ball_pos[1] + ball_vel[1]
        
    # draw ball
        canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "red", "white")
    
    # update paddle's vertical position, keep paddle on the screen
        paddle1_pos[1] += paddle1_vel  
        paddle2_pos[1] += paddle2_vel
    
        if paddle1_pos[1] <= 40:
            paddle1_pos[1] = 40
        if paddle1_pos[1] >= 360:
            paddle1_pos[1] = 360
        
        if paddle2_pos[1] <= 40:
            paddle2_pos[1] = 40
        if paddle2_pos[1] >= 360:
            paddle2_pos[1] = 360
        
    # draw paddles
        canvas.draw_line([paddle1_pos[0], paddle1_pos[1] + (PAD_HEIGHT / 2)], [paddle1_pos[0], paddle1_pos[1] - (PAD_HEIGHT / 2)], PAD_WIDTH, "blue")
        canvas.draw_line([paddle2_pos[0] ,paddle2_pos[1] + (PAD_HEIGHT / 2)], [paddle2_pos[0], paddle2_pos[1] - (PAD_HEIGHT / 2)], PAD_WIDTH, "Red")
    
    # determine whether paddle and ball collide
        if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
            if (ball_pos[1] >= (paddle1_pos[1] - 40) and ball_pos[1] <= (paddle1_pos[1] + 40)):
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] = ball_vel[0] + (0.1 * ball_vel[0])
                ball_pos[0] += ball_vel[0]
            else:
                ball_vel[0] = -ball_vel[0]
                ball_pos[0] += ball_vel[0]
                score2 += 1
                spawn_ball("right")
    
        if ball_pos[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
            if (ball_pos[1] >= (paddle2_pos[1] - 40) and ball_pos[1] <= (paddle2_pos[1] + 40)):
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] = ball_vel[0] + (0.1 * ball_vel[0])
                ball_pos[0] += ball_vel[0]
            else:
                ball_vel[0] = -ball_vel[0]
                ball_pos[0] = ball_pos[0] + ball_vel[0]
                score1 += 1
                spawn_ball("left")
    
    # draw scores
        canvas.draw_text(str(score1), (150, 45), 30, "white")
        canvas.draw_text(str(score2), (450, 45), 30, "white")
        
# Event handler for Key down event.
# Keep moving the paddle as long as the key is pressed.
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 4
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 4
    if chr(key) == "S":
        paddle1_vel += 4
    elif chr(key) == "W":
        paddle1_vel -= 4
          
# Event Handler for Key up event.
# Stop moving the paddle as soon as the key is released.
def keyup(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == "S" or chr(key) == "W":
        paddle1_vel = 0
    else:
        paddle2_vel = 0

# Event Handler for the start button    
def start():
    global start_flag
    start_flag = "Y"
    new_game()

def reset():
    global start_flag
    start_flag = 'N'
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
# set the background color to dark green
frame.set_canvas_background("#006400")

# Define the event Handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("START", start,200)
frame.add_label(' ')
frame.add_button("RESET", reset, 200)

# start frame
new_game()
frame.start()