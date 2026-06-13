import pygame
import random

# 희범님 메인 코드와 층을 맞추기 위해 바닥 기준점(GROUND_Y)을 똑같이 가져옵니다.
GROUND_Y = 620

class Obstacle:
    def __init__(self, x, kind):
        self.kind = kind # "Stone", "Military", "Tax"
        self.rect = pygame.Rect(x, GROUND_Y-40, 40, 40)
        
        # 하늘에서 떨어지는 기믹 전용 (입영통지서, 세금)
        if self.kind in ["Military", "Tax"]:
            # 더 갑작스럽게 떨어지도록 화면 위쪽 무작위 위치에서 시작
            self.rect.y = random.randint(-400, -100)
            self.fall_speed = random.randint(7, 12) # 기존보다 떨어지는 속도 살짝 증가
            
            # 바닥에 경고 마크(!)를 띄우기 위한 스위치
            self.show_warning = True if self.kind == "Military" else False
        else:
            self.fall_speed = 0

    def update(self):
        # 하늘에서 떨어지는 물체일 경우
        if self.fall_speed > 0:
            self.rect.y += self.fall_speed
            
            # 땅(GROUND_Y)에 닿으면 고정되고 경고 마크 꺼짐
            if self.rect.y >= GROUND_Y - 40:
                self.rect.y = GROUND_Y - 40
                self.fall_speed = 0
                self.show_warning = False

    def draw(self, surf, cam):
        # 1. 일반 장애물: 삼각형 돌멩이
        if self.kind == "Stone":
            pygame.draw.polygon(
                surf, (100,100,100),
                [(self.rect.x-cam+20, self.rect.y),
                 (self.rect.x-cam, self.rect.y+40),
                 (self.rect.x-cam+40, self.rect.y+40)]
            )
            
        # 2. 1학년의 최대 시련: 입영통지서 (업그레이드 완료!)
        elif self.kind == "Military":
            # 물체가 아직 하늘에 있을 때 바닥에 빨간색 경고(!) 표시
            if self.show_warning and self.rect.y < GROUND_Y - 100:
                warning_font = pygame.font.SysFont("malgungothic", 30, bold=True)
                warn_txt = warning_font.render("!", True, (255, 0, 0))
                surf.blit(warn_txt, (self.rect.x - cam + 15, GROUND_Y - 40))

            # 리얼한 국방색 편지봉투 디자인
            pygame.draw.rect(surf, (80, 100, 70), (self.rect.x-cam, self.rect.y, 60, 40))
            pygame.draw.rect(surf, (55, 75, 45), (self.rect.x-cam, self.rect.y, 60, 40), 3)
            
            # 글씨 디테일 추가
            font = pygame.font.SysFont("malgungothic", 14, bold=True)
            txt1 = font.render("8/25", True, (255, 255, 255))
            txt2 = font.render("35사단", True, (255, 255, 255))
            surf.blit(txt1, (self.rect.x-cam+15, self.rect.y+5))
            surf.blit(txt2, (self.rect.x-cam+10, self.rect.y+20))

        # 3. 사회인의 시련: 세금 폭탄
        elif self.kind == "Tax":
            pygame.draw.rect(surf, (220, 20, 20), (self.rect.x-cam, self.rect.y, 50, 40), border_radius=5)
            pygame.draw.rect(surf, (0, 0, 0), (self.rect.x-cam, self.rect.y, 50, 40), 2, border_radius=5)
            txt = pygame.font.SysFont("malgungothic", 18, bold=True)
            tax_txt = txt.render("TAX", True, (255, 255, 0))
            surf.blit(tax_txt, (self.rect.x-cam+8, self.rect.y+10))
