from tkinter import Canvas
from game import *
from player import *
game = Game()

while game.running:
    # g.playing = True 

    game.curr_menu.display_menu()

    game.game_loop()

    

 
    
