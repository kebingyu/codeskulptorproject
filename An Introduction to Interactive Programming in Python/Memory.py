###################################
# implementation of card game - Memory
import simplegui
import random

TOTAL_CARDS = 8
turns = 0

# helper function to initialize globals
def new_game():
    global cards, card_status, state, clicked, exposed, turns
    cards = range(TOTAL_CARDS) + range(TOTAL_CARDS)
    random.shuffle(cards)
    card_status = []
    state = 0
    clicked = []
    exposed = []
    turns = 0
    for i in cards:
        card_status.append(False)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    idx = pos[0] // 50
    global state, card_status, clicked, exposed, turns
    if state == 0:
        state = 1
        clicked.append(idx)
        card_status[idx] = True
    elif state == 1:
        state = 2
        #if idx != clicked[0] and card_status[idx] != True:
        clicked.append(idx)
        card_status[idx] = True
        turns += 1
    else:
        state = 1
        #if len(clicked) == 2:
        if clicked[0] != clicked[1] and cards[clicked[0]] == cards[clicked[1]]:
            exposed.append(clicked[0])
            exposed.append(clicked[1])                
        else:
            if clicked[0] not in exposed:
                card_status[clicked[0]] = False
            if clicked[1] not in exposed:
                card_status[clicked[1]] = False
        clicked = [idx]
        card_status[idx] = True    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    i = 0
    for num in cards:
        if card_status[i]:
            canvas.draw_text(str(num), (12.5+i*50, 62.5), 50, 'Green')
        else:
            canvas.draw_polygon([(i*50, 0), ((i+1)*50, 0), ((i+1)*50, 100), (i*50, 100)], 1, 'Black', 'Green')
        i += 1
    global label
    label.set_text("Turs = %d" % turns)

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
###################################
