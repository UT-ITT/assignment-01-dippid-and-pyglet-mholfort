import pyglet
from pyglet import window, shapes
from DIPPID import SensorUDP
import random
import os
import math

PORT = 5700
sensor = SensorUDP(PORT)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
win.set_caption("Breakout")

controller = shapes.Rectangle(357, 30, 86, 16, color=(11, 86, 168))
ball = shapes.Circle(400, 55, 8, color=(232, 206, 8))

speed = 5

direction_x = 0
direction_y = 0

move_left = False
move_right = False

game_start = False

def ball_move():
   ball.x += direction_x * speed
   ball.y += direction_y * speed

def reset_game():
    global direction_x, direction_y, game_start

    ball.x = 400
    ball.y = 55

    direction_x = 0
    direction_y = 0

    controller.x = 357

    game_start = False

    blocks.clear()
    create_blocks()

def bounce_edges():
    global direction_x, direction_y

    #left
    if ball.x - ball.radius <= 0:
        ball.x = ball.radius
        direction_x *= -1
        
    #right
    if ball.x + ball.radius >= WINDOW_WIDTH:
        ball.x = WINDOW_WIDTH - ball.radius
        direction_x *= -1
        
    #top
    if ball.y + ball.radius >= WINDOW_HEIGHT:
        ball.y = WINDOW_HEIGHT - ball.radius
        direction_y *= -1

def collison_controller():
    global direction_x, direction_y

    con_left = controller.x
    con_right = controller.x + controller.width
    con_top = controller.y + controller.height

    ball_left = ball.x - ball.radius
    ball_right = ball.x + ball.radius
    ball_bottom = ball.y - ball.radius

    #check if ball is in controller(horizontal) range
    horizontal = (ball_right >= con_left and ball_left <= con_right)

    #check collison on controller top and ball is moving downward
    vertical = (direction_y < 0 and ball_bottom <= con_top)

    if horizontal and vertical:
        ball.y = con_top + ball.radius
        direction_y *= -1

blocks = []
def create_blocks():
    start_x = 20
    start_y = 560
    block_width = 80
    block_height = 30
    gap = 5
    rows = 5
    columns = 9

    for row in range (rows):
        for col in range(columns):
            x = start_x + col * (block_width + gap)
            y = start_y - row * (block_height + gap)
            block = shapes.Rectangle(x, y, block_width, block_height, color=(random.randrange(215, 255), random.randrange(0, 75), random.randrange(105, 150)))
            blocks.append(block) 

def draw_blocks():
    for block in blocks:
        block.draw()

def block_collision():
    global direction_x, direction_y

    for block in blocks:

        block_left = block.x
        block_right = block.x + block.width
        block_top = block.y + block.height
        block_bottom = block.y

        ball_left = ball.x - ball.radius
        ball_right = ball.x + ball.radius
        ball_bottom = ball.y - ball.radius
        ball_top = ball.y + ball.radius

        horizontal = (ball_right >= block_left and ball_left <= block_right)
        vertical = (ball_top >= block_bottom and ball_bottom <= block_top)

        if horizontal and vertical: 
            ball.y = block_bottom + ball.radius
            direction_y *= -1
            blocks.remove(block)
            break


@win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        os._exit(0)

def update(dt):
    global move_right, move_left
    global direction_x, direction_y, game_start

    ball_move()
    bounce_edges()
    collison_controller()
    block_collision()

    #start with button press
    b1 = sensor.get_value("button_1")
    if b1 == 1 and game_start == False:
        game_start = True

        dx = random.uniform(-1.5, 1.5)
        dy = random.uniform(0.5, 1.5)

        length = math.sqrt(dx**2 + dy**2)

        direction_x = dx / length
        direction_y = dy / length

    #move controller - DIPPID
    acc = sensor.get_value("accelerometer")
    
    if acc and game_start == True:
        tilt = acc["x"]

        if abs(tilt) > 0.05:
            controller.x -= tilt * 20

            if controller.x < 0:
                controller.x = 0

            if controller.x + controller.width > WINDOW_WIDTH:
                controller.x = WINDOW_WIDTH - controller.width

    #move controller - keyboard
    """ speed_c = 3
    if move_left == True:
        controller.x -= 1 * speed_c
    if move_right == True:
        controller.x += 1 * speed_c """

    ball_bottom = ball.y - ball.radius
    if ball_bottom <= 0:
        reset_game()
    
    if len(blocks) == 0:
        reset_game()

@win.event
def on_draw():
    win.clear()
    controller.draw()
    ball.draw()
    draw_blocks()

    label = pyglet.text.Label('Press Button 1 to start',
                          font_name='Bauhaus 93',
                          font_size=20,
                          color=(48, 201, 6),
                          x=275, y=WINDOW_HEIGHT/2,)
                          
    if game_start == False:
        label.draw()


pyglet.clock.schedule_interval(update, 1/60)

create_blocks()
pyglet.app.run()
