import sys
import time
import random
import pygame
pygame.init()
sound_effect = pygame.mixer.Sound("audio.mp3")
nice = pygame.mixer.Sound("audio2.mp3")
shit = pygame.mixer.Sound("audio3.mp3")
with open('answers.txt') as f:
    answers = [line.strip().upper() for line in f]
word = random.choice(answers)
guess = ''
attempts,count = 0,0
while guess != word and attempts < 5:
    guess = input("Enter your guess #" + str(attempts + 1) + ": ")
    guess = guess.upper()
    if len(guess) != 5:
        print("Invalid guess. Please enter a 5-letter word.")
        continue
    attempts += 1
    feedback = ''
    for i in range(5):
        if guess[i] == word[i]:
            feedback += '\033[32m' + guess[i] + " " + '\033[0m'
            count += 1
        elif guess[i] in word:
            feedback += '\033[33m' + guess[i] + " " + '\033[0m'
            count += 1
        else:
            feedback += '\033[0m' + guess[i] + " " + '\033[0m'
    print(feedback)
    if count >= 2 and attempts !=5:
        nice.play()
    count = 0    
if guess == word:
    print("Congratulations! You've guessed the word!")
    sound_effect.play()
else:
    print("Game over :( The word was: " + '\033[32m' + word + '\033[0m')    
    shit.play()
    time.sleep(10)