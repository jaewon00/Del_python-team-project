import pygame

objects = []

class BaseObject:
    
    def __init__(self, spr, coord):
        # spr : 스프라이트
        self.spr = spr
        #self.spr_index = 0
        self.width = spr.get_width()
        self.height = spr.get_height()
        self.x_pos = coord[0]
        self.y_pos = coord[1]
        
        self.direction = True
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, self.width, self.height)
        
    def draw(self, screen):
        # flip : 진행방향에 따라 이미지 방향 바꾸기
        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, self.width, self.height)
        screen.blit(pygame.transform.flip(self.spr, self.direction, False), (self.rect.x, self.rect.y))
    
    def destroy(self):
        objects.remove(self)
        del(self)
        
class MonsterObject(BaseObject):
    
    def __init__(self, spr, coord, hp_max, speed):
        super().__init__(spr, coord)
        self.speed = speed
        self.hp_max = hp_max
        self.hp = hp_max
        objects.append(self)
        
        
        
        