import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
GROUND_Y = 620

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("학점 방어전 : 한성부기의 모험")
clock = pygame.time.Clock()

font = pygame.font.SysFont("malgungothic", 32)
big_font = pygame.font.SysFont("malgungothic", 90)

STAGE1_LEN = 12000
STAGE2_LEN = 15000

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 100
        self.y = GROUND_Y - 90
        self.w = 60
        self.h = 90
        self.vy = 0
        self.speed = 7
        self.hp = 10
        self.score = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.vy += 0.8
        self.y += self.vy

        if self.y + self.h >= GROUND_Y:
            self.y = GROUND_Y - self.h
            self.vy = 0

        self.x = max(0, self.x)

    def jump(self):
        if self.y + self.h >= GROUND_Y:
            self.vy = -16

    def draw(self, surf, cam, stage):
        x = self.x - cam
        if stage == 1:
            # 기본 대학생 부기 모습
            pygame.draw.circle(surf, (0,80,220), (int(x+30), int(self.y+22)), 25)
            pygame.draw.circle(surf, (255,255,255), (int(x+30), int(self.y+22)), 17)
            pygame.draw.rect(surf, (0,80,220), (x+10, self.y+40, 40, 40))
            pygame.draw.circle(surf, (120,180,255), (int(x+48), int(self.y+58)), 15)
        else:
            # Stage 2: 정장을 입은 사회인 모습
            pygame.draw.circle(surf, (0,80,220), (int(x+30), int(self.y+22)), 25)
            pygame.draw.circle(surf, (255,255,255), (int(x+30), int(self.y+22)), 17)
            # 검은색 정장 상의와 흰색 셔츠 깃 표현
            pygame.draw.rect(surf, (30,30,30), (x+10, self.y+40, 40, 40))
            pygame.draw.polygon(surf, (255,255,255), [(x+22, self.y+40), (x+30, self.y+55), (x+38, self.y+40)])
            pygame.draw.polygon(surf, (200,0,0), [(x+28, self.y+43), (x+30, self.y+52), (x+32, self.y+43)]) # 빨간 넥타이

class Item:
    def __init__(self, x, kind, stage):
        self.kind = kind
        self.stage = stage
        self.rect = pygame.Rect(x, GROUND_Y-45, 40, 40)

    def draw(self, surf, cam):
        if self.stage == 1:
            colors = {"A+":(0,180,0), "F":(180,0,0), "R":(0,0,0)}
            pygame.draw.rect(surf, colors[self.kind], (self.rect.x-cam, self.rect.y, 40, 40))
            txt = pygame.font.SysFont(None, 28).render(self.kind, True, (255,255,255))
            surf.blit(txt, (self.rect.x-cam+4, self.rect.y+8))
        else:
            # Stage 2: 코인 형태로 렌더링
            if self.kind == "Gold":
                pygame.draw.circle(surf, (255,215,0), (self.rect.x-cam+20, self.rect.y+20), 20)
                pygame.draw.circle(surf, (200,165,0), (self.rect.x-cam+20, self.rect.y+20), 20, 2)
                txt = pygame.font.SysFont(None, 24).render("+5", True, (0,0,0))
                surf.blit(txt, (self.rect.x-cam+11, self.rect.y+13))
            elif self.kind == "Red":
                pygame.draw.circle(surf, (230,30,30), (self.rect.x-cam+20, self.rect.y+20), 20)
                pygame.draw.circle(surf, (150,10,10), (self.rect.x-cam+20, self.rect.y+20), 20, 2)
                txt = pygame.font.SysFont(None, 24).render("-5", True, (255,255,255))
                surf.blit(txt, (self.rect.x-cam+13, self.rect.y+13))

class Obstacle:
    def __init__(self, x, kind):
        self.kind = kind # "Stone", "Military", "Tax"
        self.rect = pygame.Rect(x, GROUND_Y-40, 40, 40)
        
        # 하늘에서 떨어지는 기믹 전용 변수 설정
        if self.kind in ["Military", "Tax"]:
            self.rect.y = random.randint(-150, -50)
            self.fall_speed = random.randint(5, 9)
        else:
            self.fall_speed = 0

    def update(self):
        if self.fall_speed > 0:
            self.rect.y += self.fall_speed
            # 땅에 닿으면 고정
            if self.rect.y >= GROUND_Y - 40:
                self.rect.y = GROUND_Y - 40
                self.fall_speed = 0

    def draw(self, surf, cam):
        if self.kind == "Stone":
            pygame.draw.polygon(
                surf, (100,100,100),
                [(self.rect.x-cam+20, self.rect.y),
                 (self.rect.x-cam, self.rect.y+40),
                 (self.rect.x-cam+40, self.rect.y+40)]
            )
        elif self.kind == "Military":
            # 군대색 입영통지서 (국방색 편지봉투 모양)
            pygame.draw.rect(surf, (55, 75, 45), (self.rect.x-cam, self.rect.y, 44, 30))
            pygame.draw.polygon(surf, (80, 100, 70), [(self.rect.x-cam, self.rect.y), (self.rect.x-cam+22, self.rect.y+15), (self.rect.x-cam+44, self.rect.y)])
            txt = pygame.font.SysFont(None, 22).render("M", True, (255,255,255))
            surf.blit(txt, (self.rect.x-cam+16, self.rect.y+12))
        elif self.kind == "Tax":
            # 하늘에서 떨어지는 빨간 Tax 글씨 폭탄
            pygame.draw.rect(surf, (180, 40, 40), (self.rect.x-cam, self.rect.y, 45, 35), border_radius=4)
            txt = pygame.font.SysFont(None, 24).render("Tax", True, (255,255,255))
            surf.blit(txt, (self.rect.x-cam+8, self.rect.y+8))

def make_stage(stage_num, length, count_items, count_obs):
    items = []
    obstacles = []
    
    def is_safe_zone(x_pos, existing_list, min_dist=300):
        for existing in existing_list:
            if abs(existing.rect.x - x_pos) < min_dist:
                return False
        return True

    if stage_num == 1:
        # Stage 1: R 아이템 존재
        gap = max(1200, length // 6)
        for i in range(5):
            x = 1000 + i * gap
            items.append(Item(x, "R", 1))

        attempts = 0
        while len(items) < count_items and attempts < 2000:
            x = random.randint(400, length - 600)
            attempts += 1
            if is_safe_zone(x, items, min_dist=320):
                kind = random.choice(["A+", "A+", "A+", "F", "F"])
                items.append(Item(x, kind, 1))
                
        # Stage 1 장애물 배정 (삼각형 돌 + 하늘에서 떨어지는 입영통지서)
        last_x = 600
        for _ in range(count_obs):
            last_x += random.randint(250, 450)
            if last_x < length - 300:
                obs_kind = random.choice(["Stone", "Military"])
                obstacles.append(Obstacle(last_x, obs_kind))
    else:
        # Stage 2: R 없이 Gold와 Red 코인만 배치
        attempts = 0
        while len(items) < count_items and attempts < 2000:
            x = random.randint(400, length - 600)
            attempts += 1
            if is_safe_zone(x, items, min_dist=320):
                kind = random.choice(["Gold", "Gold", "Gold", "Red", "Red"])
                items.append(Item(x, kind, 2))

        # Stage 2 장애물 배정 (삼각형 돌 + 하늘에서 떨어지는 Tax)
        last_x = 600
        for _ in range(count_obs):
            last_x += random.randint(230, 420)
            if last_x < length - 300:
                obs_kind = random.choice(["Stone", "Tax"])
                obstacles.append(Obstacle(last_x, obs_kind))

    return items, obstacles

player = Player()
stage = 1
camera_x = 0

items, obstacles = make_stage(1, STAGE1_LEN, 45, 38)

state = "game"
transition_timer = 0

def restart_stage(target_stage):
    global player, stage, items, obstacles, camera_x, state
    saved_score = player.score if target_stage == 2 else 0 # 스테이지 2면 스코어 복구 메커니즘을 두거나 초기화 조율 가능
    player = Player()
    stage = target_stage
    camera_x = 0
    if target_stage == 1:
        items, obstacles = make_stage(1, STAGE1_LEN, 45, 38)
    else:
        player.score = saved_score
        items, obstacles = make_stage(2, STAGE2_LEN, 55, 48)
    state = "game"

running = True
while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == "game":
                player.jump()

    if state == "game":
        player.update()
        length = STAGE1_LEN if stage == 1 else STAGE2_LEN
        p_rect = player.rect()

        # 장애물 위치 업데이트 루프
        for obs in obstacles:
            obs.update()

        # 아이템 충돌 확인
        for item in items[:]:
            if p_rect.colliderect(item.rect):
                if item.kind in ["A+", "Gold"]:
                    player.score += 5
                elif item.kind in ["F", "Red"]:
                    player.score -= 5
                elif item.kind == "R":
                    # Stage 1에서 R을 먹으면 Stage 1부터 다시 시작
                    restart_stage(1)
                    break
                items.remove(item)

        # 장애물 충돌 확인
        for obs in obstacles[:]:
            if p_rect.colliderect(obs.rect):
                player.hp -= 1
                obstacles.remove(obs)
                if player.hp <= 0:
                    state = "fail"
                break

        if player.x >= length:
            if stage == 1:
                state = "transition"
                transition_timer = pygame.time.get_ticks()
            else:
                state = "clear"

        camera_x = max(0, player.x - WIDTH//3)

    screen.fill((0,0,0))

    if state == "game":
        if stage == 1:
            screen.fill((175, 220, 245))
            pygame.draw.rect(screen, (110, 160, 110), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))
            
            for bg_i in range(0, STAGE1_LEN, 1600):
                bx = bg_i - camera_x
                if -400 < bx < WIDTH + 400:
                    pygame.draw.rect(screen, (150, 150, 160), (bx, GROUND_Y-250, 320, 250))
                    pygame.draw.rect(screen, (100, 100, 110), (bx+110, GROUND_Y-320, 100, 70))
                    pygame.draw.polygon(screen, (80, 80, 90), [(bx+110, GROUND_Y-320), (bx+160, GROUND_Y-370), (bx+210, GROUND_Y-320)])
                    for wx in range(20, 300, 60):
                        for wy in range(40, 200, 60):
                            pygame.draw.rect(screen, (220, 240, 255), (bx+wx, GROUND_Y-250+wy, 30, 40))
                    
                    pygame.draw.rect(screen, (100, 65, 30), (bx+450, GROUND_Y-120, 20, 120))
                    pygame.draw.circle(screen, (45, 120, 65), (bx+460, GROUND_Y-130), 50)
                    
                    pygame.draw.rect(screen, (140, 90, 40), (bx+650, GROUND_Y-45, 90, 15))
                    pygame.draw.rect(screen, (80, 80, 80), (bx+660, GROUND_Y-30, 10, 30))
                    pygame.draw.rect(screen, (80, 80, 80), (bx+720, GROUND_Y-30, 10, 30))

            pygame.draw.rect(screen, (125, 95, 70), (0, GROUND_Y, WIDTH, 20))
        else:
            # Stage 2: 웅장한 대도시 야경 배경 빌드
            screen.fill((20, 25, 45)) # 깊은 밤하늘색
            pygame.draw.rect(screen, (50, 50, 55), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y)) # 보도블록 도로 느낌
            
            for bg_i in range(0, STAGE2_LEN, 1200):
                bx = bg_i - camera_x
                if -500 < bx < WIDTH + 500:
                    # 초고층 빌딩 1
                    pygame.draw.rect(screen, (35, 40, 60), (bx, GROUND_Y-430, 220, 430))
                    for hx in range(20, 180, 45):
                        for hy in range(30, 400, 50):
                            pygame.draw.rect(screen, (255, 240, 150), (bx+hx, GROUND_Y-430+hy, 15, 20))
                    
                    # 현대식 대형 빌딩 2
                    pygame.draw.rect(screen, (45, 50, 75), (bx+280, GROUND_Y-320, 300, 320))
                    for hx in range(30, 260, 50):
                        for hy in range(40, 280, 60):
                            pygame.draw.rect(screen, (180, 230, 255), (bx+hx, GROUND_Y-320+hy, 25, 25))

                    # 안테나 타워 랜드마크 3
                    pygame.draw.rect(screen, (25, 25, 35), (bx+680, GROUND_Y-500, 40, 500))
                    pygame.draw.line(screen, (255, 100, 100), (bx+700, GROUND_Y-500), (bx+700, GROUND_Y-560), 3)
                    pygame.draw.circle(screen, (255, 50, 50), (bx+700, GROUND_Y-560), 6)

            pygame.draw.rect(screen, (30, 30, 35), (0, GROUND_Y, WIDTH, 15))

        for item in items:
            item.draw(screen, camera_x)

        for obs in obstacles:
            obs.draw(screen, camera_x)

        player.draw(screen, camera_x, stage)

        flag_x = (STAGE1_LEN if stage == 1 else STAGE2_LEN) - camera_x
        pygame.draw.line(screen, (255,255,255), (flag_x, 300), (flag_x, GROUND_Y), 5)
        pygame.draw.polygon(screen, (255,255,0), [(flag_x,300),(flag_x+60,330),(flag_x,360)])

        screen.blit(font.render(f"점수: {player.score}", True, (255,255,255)), (20,20))
        screen.blit(font.render(f"HP: {player.hp}", True, (255,255,255)), (20,60))
        screen.blit(font.render(f"STAGE {stage}", True, (255,255,0)), (20,100))

    elif state == "transition":
        screen.fill((0,0,0))
        txt = big_font.render("STAGE 2 (사회인 진출)", True, (255,255,255))
        screen.blit(txt, (WIDTH//2-txt.get_width()//2, HEIGHT//2-50))

        if pygame.time.get_ticks() - transition_timer > 2500:
            stage = 2
            player.x = 100
            camera_x = 0
            items, obstacles = make_stage(2, STAGE2_LEN, 55, 48)
            state = "game"

    elif state == "fail":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # 실패 창에서 재시작할 때 현재 소속되어 있던 스테이지 정보대로 부활
            restart_stage(stage)

        screen.fill((0,0,0))
        txt = big_font.render("GAME OVER", True, (255,255,255))
        sub = font.render("ENTER 키를 눌러 이번 스테이지 재시작", True, (255,255,255))
        screen.blit(txt, (WIDTH//2-txt.get_width()//2, HEIGHT//2-50))
        screen.blit(sub, (WIDTH//2-sub.get_width()//2, HEIGHT//2+60))

    elif state == "clear":
        if player.score >= 80: grade = "A"
        elif player.score >= 60: grade = "B"
        else: grade = "F"

        if grade in ("A", "B"):
            screen.fill((0,0,0))
            for _ in range(60):
                pygame.draw.circle(screen, random.choice([(255,0,0),(0,255,0),(0,0,255),(255,255,0)]),
                                   (random.randint(0, WIDTH), random.randint(0, HEIGHT)), random.randint(2,6))
            t1 = big_font.render("인생 승리! 졸업 및 취업 성공", True, (255,255,255))
            t2 = font.render(f"최종 자산 점수: {player.score}  등급: {grade}", True, (255,255,255))
            screen.blit(t1, (WIDTH//2-t1.get_width()//2, 220))
            screen.blit(t2, (WIDTH//2-t2.get_width()//2, 350))
        else:
            screen.fill((30,30,30))
            t1 = big_font.render("GAME OVER", True, (255,255,255))
            t2 = font.render(f"최종 점수: {player.score}  등급: 신용불량(F)", True, (255,255,255))
            screen.blit(t1, (WIDTH//2-t1.get_width()//2, 220))
            screen.blit(t2, (WIDTH//2-t2.get_width()//2, 350))

    pygame.display.flip()

pygame.quit()
sys.exit()