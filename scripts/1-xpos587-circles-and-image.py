#!/usr/bin/env python
# coding: utf-8

# In[1]:


from psychopy import visual, event, core

win = visual.Window(size=(600, 800))


# In[2]:


circle = visual.Circle(  # type: ignore
    win,
    units="pix",
    radius=150,
    fillColor=[0, 0, 0],
    lineColor=[-1, -1, -1],
)
circle.colorSpace = "rgb255"
circle.color = (255, 255, 255)

circle.draw()
win.flip()

core.wait(2)

image = visual.ImageStim(win, image="../data/raw/cat.jpg")
image.ori = 45
image.size *= 0.272
image.draw()
win.flip()

keys = event.waitKeys(keyList=["d"])
win.close()

