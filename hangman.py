from tkinter import *
import random
from functools import partial 

#Choose a random word of a certain length, from a list of words (Merriam-Webster dictionary).
word_file = open("words.txt")
word_text = word_file.read()
word_file.close()
word_list_org = word_text.split(" ")
word_list = []

word_chosen = ""
word_chosen_backup = ""

def choose_word():
    global word_chosen
    global word_chosen_backup
    word_chosen = random.choice(word_list_org)
    word_chosen_backup = word_chosen[:]
    if(
        len(word_chosen) < 5 or len(word_chosen) > 12
       or "\n" in word_chosen or " " in word_chosen
       or "." in word_chosen or "," in word_chosen
        or word_chosen[0].isupper()
       ):
        choose_word()
    else:
        pass

choose_word()
word_incomplete = "_ " * len(word_chosen)

root = Tk()
root.title("Hangman")
frame1 = Frame(root)
frame2 = Frame(root)

word_displayed = StringVar()
word_displayed.set(word_incomplete)

word_label = Label(frame1, textvariable = word_displayed)
word_label.grid(row = 0, column = 0)

guesses = len(word_chosen) + 5
guesses_text = "Tries Left: " + str(guesses)

guesses_displayed = StringVar()
guesses_displayed.set(guesses_text)

guesses_label = Label(frame1, textvariable = guesses_displayed)
guesses_label.grid(row = 0, column = 1)

def alert_switch():
    global alert_on
    if alert_on == True:
        alert_on = False
        alert_switch_text.set("Alerts Off")
    else:
        alert_on = True
        alert_switch_text.set("Alerts On")

alert_on = True
alert_switch_text = StringVar()
alert_switch_text.set("Alerts On")
alert_switch_label = Button(frame1, textvariable = alert_switch_text, command = alert_switch)
alert_switch_label.grid(row = 0, column = 2)

letters_guessed = 0



def submit_letter(char, i):
    global guesses
    guesses -= 1

    guesses_text = "Tries Left: " + str(guesses)
    guesses_displayed.set(guesses_text)

    global word_chosen
    if char in word_chosen:
        
        global letters_guessed
        letters_guessed += 1
        
        index = word_chosen.find(char)
        
        word_chosen = word_chosen.replace(char, "_", 1)

        global word_incomplete
        word_incomplete_list = list(word_incomplete)
        word_incomplete_list[index*2] = char
        word_incomplete = ""
        
        for letter in word_incomplete_list:
            word_incomplete += letter

        word_displayed.set(word_incomplete)

        if("_" not in word_incomplete):
            root.destroy()
            root3 = Tk()
            root3.title("Congratulations!")
            congrats_label = Label(root3, text = "Congratulations! You won!\nThe correct word was: " + word_chosen_backup, width = 30, height = 5)
            congrats_label.pack()


        if("_" in word_incomplete and guesses <= 0):
            root.destroy()
            root3 = Tk()
            root3.title("Game Over!")
            gameover_label = Label(
                root3,
                text = "Game Over!\nThe correct word is: {0}\nYou guessed {1} letters: {2}".format(word_chosen_backup, letters_guessed, word_incomplete),
                width = 30,
                height = 5,
                justify = "center"
                )
            gameover_label.pack()
                
    else:
        global alert_on 
        if(alert_on == True):
            
            root2 = Tk()
            root2.title("Alert")
            frame2_1 = Frame(root2)
            warning_label = Label(frame2_1, text = "Wrong letter! Guess again!", width = 30, height = 5)
            warning_label.pack()
            frame2_1.pack()

        character_displayed_list[i].set("")

        if(guesses<=0):
            root.destroy()
            root3 = Tk()
            root3.title("Game Over!")
            gameover_label = Label(
                root3,
                text = "Game Over!\nThe correct word is: {0}\nYou guessed {1} letters: {2}".format(word_chosen_backup, letters_guessed, word_incomplete),
                width = 30,
                height = 5,
                justify = "center"
                )
            gameover_label.pack()
    

character_displayed_list = []

for i in range(97, 123):
    character = chr(i)
    character_displayed = StringVar()
    character_displayed.set(character)
    character_displayed_list.append(character_displayed)
    
    character_label = Button(frame2, textvariable = character_displayed, justify = "center", width = 3, height = 2, command = partial(submit_letter, character, i-97))
    
    if(i>=97 and i<=114):
        character_label.grid(row = int((i-97)/6), column = i - 96 - int((i-97)/6) * 6)
    if(i>=115 and i<=122):
        character_label.grid(row = 3, column = i - 115)


frame1.pack()
frame2.pack()


