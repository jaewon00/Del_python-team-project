
import pygame
from spritesheet import Spritesheet
from game import * 
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
    
    
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_RIGHT = False, False, False
        self.UP_KEY, self.DOWN_KEY = False, False 
        self.load_frames()
        self.rect = self.idle_frames_right[0].get_rect() # idle_frames_right에서 랜덤으로 이미지 지정
        self.rect.midbottom = (240, 244)  # player 시작 위치
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.updown = 0 
        self.state = 'idle' # 상태 
        self.current_image = self.idle_frames_right[0]
      

    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self):
            self.velocity =0
            self.updown = 0 
            if self.LEFT_KEY:
                self.velocity = -2
                
            elif self.RIGHT_KEY:
                self.velocity = 2    
            self.rect.x += self.velocity
            if self.UP_KEY:
                self.updown = -2
            elif self.DOWN_KEY:
                self.updown = 2  
            self.rect.y += self.updown 
                  
            self.set_state()
            self.animate()    
    def updatekeyboard(self): 
        self.keyboard()       

    def keyboard(self): #키보드 입력했을때 캐릭터의 이동을 나타냅니다. 
        
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type ==pygame.QUIT:
                        running = False 

                    if event.type == pygame.KEYDOWN:
                        if event.key ==pygame.K_LEFT: #캐릭터를 왼쪽으로
                            self.LEFT_KEY, self.FACING_RIGHT = True, False
                        
                            
                        elif event.key == pygame.K_RIGHT:#캐릭터를 오른쪽으로
                            self.RIGHT_KEY,self.FACING_RIGHT = True , True
                        elif event.key ==pygame.K_UP: #캐릭터를 위로 
                            self.UP_KEY,self.FACING_RIGHT = True , False
                        elif event.key ==pygame.K_DOWN:#캐릭터를 아래로
                            self.DOWN_KEY,self.FACING_RIGHT = True , True
                    

                    if event.type == pygame.KEYUP: #방향키를 떼면 멈춤   
                        if event.key ==pygame.K_LEFT :
                            self.LEFT_KEY =False 
                        elif event.key ==pygame.K_RIGHT:
                            self.RIGHT_KEY =False 
                        elif event.key ==pygame.K_UP:
                            self.UP_KEY = False
                        elif event.key == pygame.K_DOWN:
                            self.DOWN_KEY = False
                    
    def set_state(self):
            self.state = 'idle'
            if self.velocity >0 or self.updown >0 :
                self.state = 'moving right'
            elif self.velocity <0 or self.updown <0:
                self.state = 'moving left'    
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated >200 : 
                self.last_updated = now
                self.current_frame = (self.current_frame +1)%len(self.idle_frames_right)

                if self.FACING_RIGHT:
                    self.current_image = self.idle_frames_right[self.current_frame]
                elif not self.FACING_RIGHT:
                    self.current_image = self.idle_frames_left[self.current_frame] 
        else:
            if now - self.last_updated >100:
                self.last_updated = now
                self.current_frame =  (self.current_frame +1)%len(self.walking_frames_right) 
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]                   
    def load_frames(self):
        my_spritesheet = Spritesheet("./sprite/character_sheet.png")
        self.idle_frames_right = [my_spritesheet.parse_sprite("player2.png"), 
                                 my_spritesheet.parse_sprite("player4.png")]
        self.walking_frames_right = [my_spritesheet.parse_sprite("player5.png"), 
                                 my_spritesheet.parse_sprite("player6.png"),
                                 my_spritesheet.parse_sprite("player7.png")
                                 ]                        
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append(pygame.transform.flip(frame,True,False))
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pygame.transform.flip(frame,True,False))
