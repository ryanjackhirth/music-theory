"""
Name: Ryan Hirth
Description: This file contains the data for what notes are in each major scale
and for what the steps and alterations are of different chord types. It also
includes functions that create chords and find the notes given a root and chord
type. The functions can be used by main.py, which runs music theory questions
on pygame.
"""

import random

# Major scales in all 12 keys
CScale = ["C", "D", "E", "F", "G", "A", "B", "C"]
DbScale = ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C", "Db"]
DScale = ["D", "E", "F#", "G", "A", "B", "C#", "D"]
EbScale = ["Eb", "F", "G", "Ab", "Bb", "C", "D", "Eb"]
EScale = ["E", "F#", "G#", "A", "B", "C#", "D#", "E"]
FScale = ["F", "G", "A", "Bb", "C", "D", "E", "F"]
GbScale = ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F", "Gb"]
GScale = ["G", "A", "B", "C", "D", "E", "F#", "G"]
AbScale = ["Ab", "Bb", "C", "Db", "Eb", "F", "G", "Ab"]
AScale = ["A", "B", "C#", "D", "E", "F#", "G#", "A"]
BbScale = ["Bb", "C", "D", "Eb", "F", "G", "A", "Bb"]
BScale = ["B", "C#", "D#", "E", "F#", "G#", "A#", "B"]

# Steps and alterations for 14 different chord types
major = [[1, 3, 5], ["", "", ""]]
minor = [[1, 3, 5], ["", "b", ""]]
dim = [[1, 3, 5], ["", "b", "b"]]
aug = [[1, 3, 5], ["", "", "#"]]
maj7 = [[1, 3, 5, 7], ["", "", "", ""]]
min7 = [[1, 3, 5, 7], ["", "b", "", "b"]]
dom7 = [[1, 3, 5, 7], ["", "", "", "b"]]
maj9 = [[1, 3, 5, 7 , 2], ["", "", "", "", ""]]
min9 = [[1, 3, 5, 7 , 2], ["", "b", "", "b", ""]]
dom9 = [[1, 3, 5, 7 , 2], ["", "", "", "b", ""]]
domb9 = [[1, 3, 5, 7 , 2], ["", "", "", "b", "b"]]
doms9 = [[1, 3, 5, 7 , 2], ["", "", "", "b", "#"]]
min11 = [[1, 3, 5, 7 , 2, 4], ["", "b", "", "b", "", ""]]
doms11 = [[1, 3, 5, 7 , 2, 4], ["", "", "", "b", "", "#"]]

pitchList = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
scaleList = [CScale, DbScale, DScale, EbScale, EScale, FScale,
             GbScale, GScale, AbScale, AScale, BbScale, BScale]
chordList = [major, minor, dim, aug, maj7, min7, dom7,
             maj9, min9, dom9, domb9, doms9, min11, doms11]
chordName = ["major", "minor", "diminished", "augmented", "major seventh",
             "minor seventh", "dominant seventh", "major ninth",
             "minor ninth", "dominant ninth", "dominant flat ninth",
             "dominant sharp ninth", "minor eleventh",
             "dominant sharp eleventh"]

### Functions

def lstToString(lst):
    """
    Converts a list of elements to a string of elements, with commas between
    each element. Returns string of elements.
    """
    result = ""
    for i in range(len(lst)):
        if i != 0:
            result += ", "
        result += lst[i]
    return result

def randReorder(answers):
    """
    Answers is a list of four answers. The first (0-index) item of the list
    is the correct answer. This function randomly reorders the answers
    and returns the reordered list. The function also adds the index of
    the correct answer as the fifth element of the list.
    """
    choice = random.randint(0, 3)
    if choice != 0: # correct answer already in the right spot
        temp = answers[0]
        answers[0] = answers[choice]
        answers[choice] = temp     # swaps answers
    answers.append(choice)
    return answers

def chordGame():
    """
    Main function to play the chord game. Chooses a random chord type in a
    random key and finds the correct note set. Generates three incorrect
    choices for notes by finding the notes for three different chord types
    within the same key. Returns a list of six elements. The first four are the
    four choices. The fifth element is the index of the correct choice, and the
    sixth element is the full name of the chord.
    """
    scale = randScale()
    chords = chordList.copy()
    cindex = random.randrange(0, 14)
    ctype = chords[cindex]
    correct = createChord(scale, ctype) # find the correct notes in the chord
    chords.remove(ctype)
    ctype = random.choice(chords)
    inc1 = createChord(scale, ctype) # first incorrect answer
    chords.remove(ctype)
    ctype = random.choice(chords)
    inc2 = createChord(scale, ctype) # second incorrect answer
    chords.remove(ctype)
    ctype = random.choice(chords)
    inc3 = createChord(scale, ctype) # third incorrect answer
    chords.remove(ctype)
    answers = [correct, inc1, inc2, inc3]
    answers = randReorder(answers) # randomly reorder answers
    for i in range(4):
        answers[i] = lstToString(answers[i]) # convert each answer to string format
    answers.append(chordName[cindex])
    return answers
    
def randChord():
    """
    Chooses a random chord by selecting a random root scale and a random
    chord type. There are 12 * 14 = 168 different possibilities.
    """
    scale= randScale()
    ctype = random.randint(0, 13)
    chord = createChord(root, chordList[ctype])

def randScale():
    """
    Chooses and returns a random major scale from the scaleList.
    """
    return scaleList[random.randint(0, 11)]
    
def createChord(scale, ctype):
    """
    Finds the notes in a certain chord given the chord's root scale and
    chord type (ctype).
    Returns a list with the chord's notes, in ascending order.
    """
    steps = ctype[0]
    alts = ctype[1]
    chord = []
    for i in range(len(steps)):
        new = scale[steps[i]-1]
        alt = new[1::]
        if alts[i] == "b":
            alt = addFlat(alt)
        elif alts[i] == "#":
            alt = addSharp(alt)
        pitch = new[0] + alt #combine letter and alteration to create pitch
        chord.append(pitch)  #append each pitch to chord list
    return chord   

def addSharp(current):
    """
    Adds a sharp to the current accidental. This can either mean adding a
    sharp or deleting a flat, depending on what the current accidental is.
    Returns the new accidental as a string.
    """
    if current == "bb":
        new = "b"
    elif current == "b":
        new = ""
    elif current == "":
        new = "#"
    else:
        new = "x"
    return new

def addFlat(current):
    """
    Adds a flat to the current accidental. This can either mean adding a
    flat or deleting a sharp, depending on what the current accidental is.
    Returns the new accidental as a string. (Inverse of addSharp)
    """
    if current == "x":
        new = "#"
    elif current == "#":
        new = ""
    elif current == "":
        new = "b"
    else:
        new = "bb"
    return new
    


