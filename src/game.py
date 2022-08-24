from operator import truediv
import pygame
from menu import *
from tiles import *
from player import *
from spritesheet import Spritesheet

from object import *

# cat = Player()
# cat.update()
# cat.keyboard()
# cat.draw(map)


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False    # 2가지 Loop
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False  # player가 눌렀을 때 True로
        self.DISPLAY_W, self.DISPLAY_H = 800, 600   # width, height (canvas size)
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        # self.font_name = 'DungGeunMo.ttf'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE, self.BLUE = (0, 0, 0), (255, 255, 255), (0, 0, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.spritesheet = Spritesheet('./sprite/temp_sheet.png')
        self.map = TileLayerMap('./map/level1/', self.spritesheet)

        ## 몬스터 ____________
        self.monster_spr = pygame.image.load("./images/monster.png")
        self.monster = MonsterObject(spr=self.monster_spr, coord=(200,300), hp_max=100, speed=0.01)
        ########### _____________

        self.next_map_name, self.stage_time = self.spritesheet.get_stage_info('./map/level1/')
        print("[LOG] loading start map... & next map is [{}]".format(self.next_map_name))
        self.time_check = 0


        self.player = Player()
        

    def game_loop(self):
        self.time_check = pygame.time.get_ticks()
        while self.playing: # Loop
            self.check_events() # event 확인, 아래 def로 지정한 함수
        
            if self.BACK_KEY:
                self.playing = False
            # if map2.collsion_tiles(player_rect) :
            #     # 맵 충돌처리, 플레이어가 더 이상 가지못하도록 막기.
            #     pass
            curr_time = pygame.time.get_ticks()
            #print("time is {0}\n", curr_time)
            if (curr_time - self.time_check) > self.stage_time:
                print("[LOG] time is over {}-{} > {}".format(curr_time, self.time_check, self.stage_time))
                self.change_screen()
                print("[LOG] complete changed map & next map is [{}]".format(self.next_map_name))
                
            
            self.map.draw_map(self.display)
            
           
            self.player.update()
            self.player.updatekeyboard()
            self.player.draw(self.display)
            self.window.blit(self.display, (0, 0))
            
             ## 몬스터 ____________
            self.monster.x_pos += self.monster.speed
            self.monster.draw(self.window)
            ########### _____________
            
            pygame.display.update()

          
            # self.reset_keys()   # 다시 모든key False로, def지정 함수
    #########추가###########
    # def new(self):
    #     self.all_sprites = pygame.sprite.LayeredUpdates() # 모든 스프라이트 효과를 한번에 업데이트
    #     self.blocks = pygame.sprite.LayeredUpdates() # 블럭 업데이트 / config.py에 BLOCK_LAYER 가 지정되어있습니다.
    # def update(self):
    #     self.all_sprites.update()
    #################################################        
    # make game loop
    # check the player inputs and button press
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    
    # reset variables
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('./font/8BITWONDER.TTF', size)
        text_surface = font.render(text, True, self.WHITE)  # 글자 나타내기
        text_rect = text_surface.get_rect() # 사각형틀 잡기
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    # Game Start 누르면 화면 전환



    def change_screen(self, alive = True):
        self.display.fill((0, 0, 0))

        if not alive:
            self.draw_text("you died", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            changing = True
            while changing:
                self.check_events()
                if self.START_KEY:
                    changing = False
                    self.playing = False
                    self.curr_menu = self.main_menu
                    # 게임 정보 초기화
                    #continue
                #pygame.display.update()
                self.reset_keys()
            return
        else:
            if (self.next_map_name == 'end'):
                self.playing = False
                self.curr_menu = self.credits
                return
            
            self.draw_text("press start key to go to the Next stage", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            changing = True
            while changing:
                self.check_events()
                if self.START_KEY:
                    changing = False
                    self.change_stage()
                    #continue
                #pygame.display.update()
                self.reset_keys()
                


    def change_map(self, levelpath):
        return TileLayerMap(levelpath, self.spritesheet)

    def change_stage(self):
        self.display.fill((255, 255, 255))
        self.map = self.change_map(self.next_map_name)
        self.next_map_name, self.stage_time = self.spritesheet.get_stage_info(self.next_map_name)
        self.time_check = pygame.time.get_ticks()
        # 플레이어 상태 초기화 (무기활성화 등..)
        # 몬스터들 비우기


