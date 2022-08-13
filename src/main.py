from game import Game

game = Game()



while game.running:
    # g.playing = True
    game.curr_menu.display_menu()
    game.game_loop()