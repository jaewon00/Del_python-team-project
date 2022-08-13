import pygame, os, csv

class Tile(pygame.sprite.Sprite): # 타일 본인의 이미지 파일과, 위치를 지닌 클래스
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, filename, spritesheet):  # 생성자. 파일 이름과 Spritesheet 타입의 시트를 받아옴. 해당 변수들로 맵이 그려진 map_surface를 만든다.
        self.tile_size = 30 # 타일 하나의 사이즈
        self.start_x, self.start_y = 0, 0 # 임시 시작 위치
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename) # csv 파일을 읽고, 각각에 해당하는 Tile 객체를 지닌 list(맵)를 리턴하는 함수. 호출
        self.map_surface = pygame.Surface((self.map_w, self.map_h)) # 맵 표면 변수 생성.
        self.map_surface.set_colorkey((0, 0, 0)) # 투명도 설정
        self.load_map() # Tile타입을 가진 list를 map_surface 에 반영.

    def draw_map(self, surface): # 메인 함수에서 쓰임. surface(=screen)에 map_surface를 그린다.
        surface.blit(self.map_surface, (0, 0))

    def load_map(self): # 각각의 Tile 들을 map_surface 변수에 그린다.
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename): # csv 파일을 읽는 함수. list 타입 리턴.
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename): # csv 파일을 읽고, 각각에 해당하는 Tile 객체를 지닌 list(맵)를 리턴하는 함수.
        tiles = []
        map = self.read_csv(filename) # csv 함수를 읽어옴.
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '-1': # x, y 위치의 값이 -1 이라면 플레이어 시작 위치
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('floor1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('floor2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '11':
                    tiles.append(Tile('round1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '12':
                    tiles.append(Tile('round2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '21':
                    tiles.append(Tile('wall1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '22':
                    tiles.append(Tile('wall2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '23':
                    tiles.append(Tile('wall3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '24':
                    tiles.append(Tile('wall4.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '25':
                    tiles.append(Tile('wall5.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '31':
                    tiles.append(Tile('cream_wall1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '32':
                    tiles.append(Tile('cream_wall2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
    
    def collsion_tiles(self, rect):
        for tile in self.tiles:
            if rect.colliderect(tile):
                return True
        return False        

class TileLayerMap():
    def __init__(self, dir_name, spritesheet):
        self.layer = []
        # layer에 TileMap 객체를 차곡차곡.
        dir_list = os.listdir(dir_name)
        dir_list.sort(reverse=True)
        for file in dir_list:
            ext = os.path.splitext(file)[-1]	# 확장자 이름만 가지고 오게 한다.
            if ext == '.csv':
                self.layer.append(TileMap(os.path.join(dir_name, file), spritesheet))
        # 그 중 가장 첫번째 타일맵은 바닥 타일로, 플레이어의 위치 정보가 포함되어 있음. (3->2->1 : file 숫자 낮을수록 위의 레이어.)
        self.start_x, self.start_y = self.layer[0].start_x, self.layer[0].start_y

    def draw_map(self, surface):
        # layer 순서대로 캔버스에 업데이트. # layer[1].draw_map(canvas)
        for map in self.layer:
            map.draw_map(surface)





