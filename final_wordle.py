from itertools import count
import random
import sys
import pygame

guess_time=0
game_over = False
pygame.init()
win_played = False
lose_played = False
same_guess=False
count = 0
nice = pygame.mixer.Sound("audio.mp3")
shit = pygame.mixer.Sound("audio3.mp3")
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("Wordle")
running = True
font3 = pygame.font.SysFont("Arial",35)
font = pygame.font.Font(None, 72) #main font for letters
font2 = pygame.font.Font(None, 50) #font for congratulatory message
user_text='' #variable to store the user's input, initialized as an empty string
guess=['','','','',''] #creating a list to store the user's guess, initialized with empty strings
q=0 
keyy = pygame.image.load("raviyellow.png").convert_alpha() #initialise imgs 
keyg = pygame.image.load("ronanshush.png").convert_alpha()
keyw = pygame.image.load("davewinners.png").convert_alpha()
keyb = pygame.image.load("rishabhblack.png").convert_alpha()
keyl = pygame.image.load("banana.png").convert_alpha()
keyg = pygame.transform.scale(keyg, (80, 80))
keyy = pygame.transform.scale(keyy, (80, 80))
keyw = pygame.transform.scale(keyw, (150, 150))
keyb = pygame.transform.scale(keyb, (80, 80))
keyl = pygame.transform.scale(keyl, (80, 80))
animated_letters = {} #list to keep track of letters that have been animated, so that they are not animated again when the user types a new guess 

flag=False
invalid_word=False
invalid_word_time = 0
animating_row=0


user_guesses={} #creating a dictionary to store the user's guesses, where the key is the guess number and the value is the guess itself, initialized as an empty dictionary
with open('answers.txt', 'r') as f:
    words = [line.strip().upper() for line in f]
    #word = list(random.choice(words)) #remove the # for random word selection 
    word = list(random.choice(words)) #current word apple for testing 
animating=True  

while running:
    
    for event in pygame.event.get():
     if event.type == pygame.QUIT:
        running = False

     elif event.type == pygame.KEYDOWN:
        if not game_over:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.unicode.isalpha() and len(user_text) < 5:
                user_text += event.unicode.upper()
        

     elif event.type == pygame.KEYUP:
        if event.key == pygame.K_RETURN and not game_over:
            guess_text = user_text.strip().upper()
            guess_time = pygame.time.get_ticks()
            animating_row=q


            if guess_text not in words or len(guess_text) != 5:
                invalid_word = True
                invalid_word_time = pygame.time.get_ticks()
                user_text = ''
                continue
            if guess_text in user_guesses.values():
                same_guess = True
                invalid_word_time = pygame.time.get_ticks()
                user_text = ''
                continue
                continue

            
            user_guesses[q] = guess_text
            user_text = ''
            q+=1

            if guess_text == ''.join(word):
                game_over = True
                    
                if not win_played:
                  nice.play()
                  win_played = True


            if q >= 6 and guess_text != ''.join(word):
                    game_over = True
                    if not lose_played:
                     shit.play()
                     lose_played = True
    
    

    screen.fill('black')
    current_time = pygame.time.get_ticks()

    if invalid_word:
       error_text = font2.render("Not a valid 5-letter word!",True,"red") 
       screen.blit(error_text, (40, 80))
       if current_time - invalid_word_time > 1000:
          invalid_word = False
    if same_guess:
       error_text = font2.render("You've already guessed that word!",True,"red") 
       screen.blit(error_text, (40, 80))
       if current_time - invalid_word_time > 1000:
          same_guess = False

    x, y = 125, 125
    text2 = font.render("Enter your guess:", True, "white")
    text = font.render(user_text, True, "white")
    screen.blit(text, (500, 20))
    screen.blit(text2, (30, 20))
    
   
    for i in range(6):
        guess = list(user_guesses.get(i, "     "))
        for j in range(5):
            if i==animating_row and current_time - guess_time < j*350 and user_guesses.get(i, '') != '':
                  x+=90
                  continue
            if current_time - guess_time > 1750:
                animating_row = None
                  
            letter = font.render(guess[j], True, "white")
            if guess[j]==word[j]: 
                count += 1 #green letter
                pygame.draw.rect(screen, 'green', (x, y, 80, 80))
                if user_guesses.get(i, '') != '': #so that images dont appear even where there is no guess 
                    screen.blit(keyg,(x,y)) 
            elif guess[j] in word: #yellow letter
                count += 1
                pygame.draw.rect(screen,(214,140,45), (x, y, 80, 80)) 
                if user_guesses.get(i, '') != '':
                    screen.blit(keyy,(x,y))
            else: #grey letter
                pygame.draw.rect(screen,(64,64,64), (x, y, 80, 80,),3) 
                if user_guesses.get(i, '') != '': 
                    screen.blit(keyb,(x,y))
            screen.blit(letter, (x+20, y+20)) #display the letter on top of the colored rectangle, with some padding
            
            x+=90 #move to next rectangle
        if user_guesses.get(i, '') == ''.join(word):
             #if guess=target word
            text3 = font2.render("Congratulations! You guessed the word!", True, "green")
            screen.blit(text3, (30, 700))
            screen.blit(keyw,(600,550))
            break
        y+=90 #move down next row
        x=125 #reset x to start of row
    
    if game_over:

    # Lost after 6 guesses
     if q >= 6 and user_guesses.get(q-1, '') != ''.join(word):
        
        text4 = font3.render(
            f"GAME OVER :( The word was:  {''.join(word)}",
            True,
            "red"
        )
        
        screen.blit(text4, (30,700))
        keyl = pygame.transform.scale(keyl, (150, 150)) 
        screen.blit(keyl,(600,550))
    # Won
    elif any(g == ''.join(word) for g in user_guesses.values()):
        
        text3 = font2.render(
            "Congratulations! You guessed the word!",
            True,
            "green"
        )
        screen.blit(text3, (30,700))

        keyw = pygame.transform.scale(keyw, (150,150))
        screen.blit(keyw, (600,550))
    
    pygame.display.flip()


pygame.quit()
