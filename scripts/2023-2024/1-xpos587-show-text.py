# from threading import Thread
import random

# import pandas as pd
from psychopy import core, event, visual

win = visual.Window([800, 600], units="norm")

quired_port_type = "Arduino Mega 2560"

phrase = "Я - скрипт, и я вывожу на экран буквы"
start_pos_x = -len(phrase) * 0.025
letters = [
    visual.TextStim(
        win, text=char, pos=(start_pos_x + i * 0.05, 0), color="black"
    )
    for i, char in enumerate(phrase)
]

square = visual.Rect(  # type: ignore
    win,
    width=0.1,
    height=0.1,
    fillColor="black",
    lineColor="black",
    pos=(0.9, -0.9),
)


def redraw():
    for letter in letters:
        letter.draw()
    square.draw()
    win.flip()


def change_state(index, move):
    letters[index].color = "red"
    original_pos = letters[index].pos
    if move:
        letters[index].pos = (
            letters[index].pos[0] + random.uniform(-0.05, 0.05),
            letters[index].pos[1] + random.uniform(-0.05, 0.05),
        )
    square.fillColor = "white"
    redraw()
    core.wait(0.5)
    letters[index].color = "black"
    if move:
        letters[index].pos = original_pos
    square.fillColor = "black"
    redraw()


redraw()

move = False
while True:
    key = event.waitKeys()
    if key:
        if key[0] == "escape":
            win.close()
            core.quit()

        if key[0] == "space":
            move = not move

        while True:
            index = random.randint(0, len(letters) - 1)
            if str(letters[index].text) in [" ", "-", ","]:
                continue

            change_state(index, move)
            if event.getKeys(keyList=["escape"]):
                win.close()
                core.quit()
            if event.getKeys(keyList=["space"]):
                move = not move
            core.wait(0.5)
