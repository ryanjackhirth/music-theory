"""
Name: Ryan Hirth
Sources: https://pythonprogramming.net/pygame-python-3-part-1-intro/
This pygame tutorial helped me understand how to create centered text and
buttons in pygame. The "text_objects" and "text_creator" functions are from
this source (which centers text), and the "button" function is also from this
source (which creates a button with an active and inactive color based on
whether the cursor is hovering over it, and an optional action.
"""

import pygame
import time
import random
from theory import *

# The qstatus is a list of the statuses of the four answer choices for a question.
# -1 means unanswered, 0 means answered and incorrect, 1 means answered and correct.
qstatus = [-1, -1, -1, -1]
CORRECT = 0

pygame.init()

# screen size
WIDTH = 1200
HEIGHT = 800

# basic colors
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
green2 = (0,200,0)
red = (255,0,0)
red2 = (200,0,0)
blue = (120,250,255)
blue2 = (100,200,255)

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
cs = "comicsansms"

### Buttons and text functions ###

def text_objects(text, font):
    """
    Renders font in pygame. This function is from this source:
    https://pythonprogramming.net/pygame-python-3-part-1-intro/
    """
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text_creator(message,font,size,w,h):
    """
    Creates and centers text. This function is from this source:
    https://pythonprogramming.net/pygame-python-3-part-1-intro/
    """
    text = pygame.font.SysFont(font,size)
    TextSurf, TextRect = text_objects(message,text)
    TextRect.center = (w,h)
    return TextSurf,TextRect

def act(action):
    """
    Different actions that lead to calling different functions. This
    function is called by the button function when a button is pressed.
    """
    global qstatus, CORRECT
    if type(action) == list:
        qstatus[action[0]] = action[1]
        if action[1] == 1:
            CORRECT = 1
    elif action == "chordQuiz":
        chordQuiz()
    elif action == "mainMenu":
        mainMenu()
    elif action == "quit":
        pygame.quit()
        quit()
        
def button(msg,x,y,w,h,ic,ac, action=None):
    """
    Generic button function with paramters: message, x value, y value,
    width, height, inactive color, active color, action.
    This function is from this source:
    https://pythonprogramming.net/pygame-python-3-part-1-intro/
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (x+w > mouse[0] > x) and (y+h > mouse[1] > y):
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] and action != None:
            act(action)
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))       

    smallText = pygame.font.SysFont(cs,30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x+(w/2),y+(h/2))
    gameDisplay.blit(textSurf, textRect)

### Score and message display functions ###

def score():
    """
    Returns score of a question by looking at the qstatus.
    Correct in 1 try: 10 points
    Correct in 2 tries: 5 points
    Correct in 3 tries: 2 points
    Correct in 4 tries / never correct: 0 points
    """
    correct = 0
    incorrect = 0
    for status in qstatus:
        if status == 1:
            correct = 1
        elif status == 0:
            incorrect += 1
    if correct == 0 or incorrect == 3:
        return 0
    elif incorrect == 2:
        return 2 #2 points for getting anser in 3 tries
    elif incorrect == 1:
        return 5 #5 points for getting answer in 2 tries
    elif incorrect == 0:
        return 10 #10 points for getting answer in 1 try

def displayScore(qnum, score):
    """
    Displays question number and current points within a game.
    """
    font = pygame.font.SysFont(cs,30)
    text1 = font.render("Question: "+str(qnum), True, black)
    text2 = font.render("Points: "+str(score)+"/"+str(qnum*10-10), True, black)
    gameDisplay.blit(text1, (10,10))
    gameDisplay.blit(text2, (10,45))

def correctMsg(points):
    """
    Displays message when correct answer is chosen.
    """
    text = "Correct!"
    TextSurf,TextRect = text_creator(text,cs,70,WIDTH/2,HEIGHT*.15)
    gameDisplay.blit(TextSurf,TextRect)
    text = "Press space to continue"
    TextSurf,TextRect = text_creator(text,cs,30,WIDTH/2,HEIGHT*.25)
    gameDisplay.blit(TextSurf,TextRect)

### Main game screen loop functions ###

def mainMenu():
    """
    Main menu for the game. Currently has one button for the chord game quiz.
    """
    gameDisplay.fill(white)
    TextSurf,TextRect = text_creator("Music Theory",cs,120,WIDTH/2,HEIGHT*.4)
    gameDisplay.blit(TextSurf,TextRect)
    TextSurf,TextRect = text_creator("Intervals, Scales, & Chords Training",cs,35,WIDTH/2,HEIGHT*.55)
    gameDisplay.blit(TextSurf,TextRect)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    chordQuiz()
        button("Chord Quiz",475,600,250,100,green2,green,"chordQuiz")

        pygame.display.update()
        clock.tick(15)
        
def chordQuiz():
    """
    This function calls chordQuestion() ten times to ask ten questions and
    then calls displayFScore() to display the final score.
    """
    score = 0
    for i in range(1, 11):
        score += chordQuestion(i, score)
    displayFScore(score)    
    
def chordQuestion(qnum, points):
    """
    Loop for answering question within a chord quiz. There are always
    four buttons to choose, with one correct answer.
    """
    global qstatus, CORRECT
    qstatus = [-1, -1, -1, -1] # all questions are initally unanswered
    CORRECT = 0 # the correct answer is initially unanswered
    answers = chordGame()
    root = str.replace(answers[0][0:2], ",", "")
    correct = answers[4]
    ctype = answers[5]

    gameDisplay.fill(white)
    displayScore(qnum,points) # display question number and current points
    
    question = f"What are the notes in a {root} {ctype} chord?"
    TextSurf,TextRect = text_creator(question,cs,30,WIDTH/2,HEIGHT*.4)
    gameDisplay.blit(TextSurf,TextRect)

    ic = blue2
    ac = blue

    ics = [red, green2, blue2] # button colors when cursor is not on them
    acs = [red, green2, blue] # button colors when cursor is hovered over them

    q0 = [0,0] # Index 0 is answer #, index 1 is whether it is correct
    q1 = [1,0]
    q2 = [2,0]
    q3 = [3,0]
    questions = [q0, q1, q2, q3]
    questions[correct][1] = 1 # index 1 of correct answer will be 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return score()

        if CORRECT == 1:
            correctMsg(10)

        # Buttons for the four possible answers       
        button(answers[0],125,400,450,150,ics[qstatus[0]], acs[qstatus[0]], q0)
        button(answers[1],625,400,450,150,ics[qstatus[1]], acs[qstatus[1]], q1)
        button(answers[2],125,600,450,150,ics[qstatus[2]], acs[qstatus[2]], q2)
        button(answers[3],625,600,450,150,ics[qstatus[3]], acs[qstatus[3]], q3)

        pygame.display.update()
        clock.tick(15)

def displayFScore(score):
    """
    Displays final score after a game is over. User can play again or go
    back to the main menu from here.
    """
    gameDisplay.fill(white)

    text = "Final Score:"
    TextSurf,TextRect = text_creator(text,cs,80,WIDTH/2,HEIGHT*.2)
    gameDisplay.blit(TextSurf,TextRect)
    
    score = str(score)+"%"
    TextSurf,TextRect = text_creator(score,cs,200,WIDTH/2,HEIGHT*.5)
    gameDisplay.blit(TextSurf,TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    chordQuiz()
        button("Play Again",275,600,250,100,green2,green,"chordQuiz")
        button("Main Menu", 675,600,250,100,green2,green,"mainMenu")

        pygame.display.update()
        clock.tick(15)

        
# Start at main menu    
mainMenu()

