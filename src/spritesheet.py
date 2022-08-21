import pygame
import json

class Spritesheet:
    def __init__(self, filename): # 생성자. 파일 제목을 클래스 매개변수로 받는다. (.png 형식)
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert() # 파일을 불러오고 (Surface 타입 객체) sprite_sheet 변수에 png 파일 로드
        self.meta_data = self.filename.replace('png', 'json')   # 똑같은 이름을 가진 json 파일 제목.
        with open(self.meta_data) as f: # json 파일을 열고, data 변수에 불러온다.
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h): # x, y 위치부터 시작하고 w, h의 크기를 가지는 이미지 파일을 잘라온다.
        sprite = pygame.Surface((w, h)) # 불러올 이미지변수의 크기 설정.
        sprite.set_colorkey((0,0,0)) # 이미지 투명도 설정 (0)
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h)) # 이미지 변수에 스프라이트 파일의 x, y, w, h 위치에 있는 이미지 자르기.
        return sprite

    def parse_sprite(self, name): # json에서 name 이름을 가진 관련 정보를 찾아, 해당 이미지 파일을 잘라 리턴하는 함수.
        sprite = self.data['frames'][name]['frame'] # json에서 해당하는 데이터 찾아오기.
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h) # 이미지 파일 잘라오기.
        return image

    def get_stage_info(self, stage):
        return self.data['meta'][stage]['next_stage'], int(self.data['meta'][stage]['time'])
        
