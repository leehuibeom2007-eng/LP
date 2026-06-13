import pygame
import random

class FallingObject:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 아이템 종류 확률 (A+ 40%, F학점 50%, 극악의 확률 10%로 보스 등장)
        self.type = random.choices(["A+", "F", "BOSS"], weights=[40, 50, 10])[0]
        
        # 종류별 설정 (색상, 크기, 떨어지는 속도)
        if self.type == "A+":
            self.color = (0, 0, 255) # 파란색 (점수 획득)
            self.size = 30
            self.speed = random.randint(3, 6)
        elif self.type == "F":
            self.color = (255, 0, 0) # 빨간색 (피해야 함)
            self.size = 40
            self.speed = random.randint(5, 8)
        else: 
            # BOSS: 8월 25일 35사단 입영통지서 (최악의 시련)
            self.color = (0, 0, 0) # 검은색 (절망)
            self.size = 60
            self.speed = random.randint(10, 16) # 피하기 힘들게 미친 속도로 떨어짐
            
        # 화면 맨 위(y=0)의 무작위 x 좌표에서 스폰
        self.x = random.randint(0, screen_width - self.size)
        self.y = -self.size
        
    def drop(self):
        # 매 프레임마다 아래로 떨어짐
        self.y += self.speed
        
    def draw(self, screen):
        # 일단은 네모 박스로 구현 (나중에 진짜 입영통지서나 F학점 이미지로 교체 가능)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
