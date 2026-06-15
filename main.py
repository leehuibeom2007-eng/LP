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
small_font = pygame.font.SysFont("malgungothic", 24)

STAGE1_LEN = 12000
STAGE2_LEN = 15000

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 100
        self.y = GROUND_Y - 110
        self.w = 70
        self.h = 110
        self.vy = 0
        self.speed = 7
        self.hp = 10
        self.score = 0

    def rect(self):
        return pygame.Rect(self.x + 10, self.y, self.w - 10, self.h)

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
        y = self.y

        pygame.draw.circle(surf, (160, 215, 245), (int(x + 15), int(y + 75)), 22)
        pygame.draw.circle(surf, (100, 160, 210), (int(x + 15), int(y + 75)), 22, 2)
        pygame.draw.line(surf, (100, 160, 210), (x + 5, y + 63), (x + 28, y + 85), 2)
        pygame.draw.line(surf, (100, 160, 210), (x + 3, y + 78), (x + 25, y + 70), 2)

        pygame.draw.circle(surf, (255, 255, 255), (int(x + 32), int(y + 102)), 10)
        pygame.draw.circle(surf, (0, 40, 100), (int(x + 32), int(y + 102)), 10, 2)
        pygame.draw.circle(surf, (255, 255, 255), (int(x + 52), int(y + 102)), 10)
        pygame.draw.circle(surf, (0, 40, 100), (int(x + 52), int(y + 102)), 10, 2)

        if stage == 1:
            pygame.draw.rect(surf, (0, 43, 106), (x + 25, y + 55, 38, 42), border_bottom_left_radius=8, border_bottom_right_radius=8)
            pygame.draw.circle(surf, (255, 255, 255), (int(x + 58), int(y + 70)), 7)
            pygame.draw.circle(surf, (0, 43, 106), (int(x + 58), int(y + 70)), 7, 2)
            f_small = pygame.font.SysFont("arial", 12, bold=True)
            logo_txt = f_small.render("HSU", True, (255, 255, 255))
            surf.blit(logo_txt, (x + 34, y + 74))
            pygame.draw.circle(surf, (255, 255, 255), (int(x + 40), int(y + 64)), 2)
            pygame.draw.circle(surf, (255, 255, 255), (int(x + 46), int(y + 64)), 2)
        else:
            pygame.draw.rect(surf, (25, 25, 25), (x + 25, y + 55, 38, 42), border_bottom_left_radius=4, border_bottom_right_radius=4)
            pygame.draw.polygon(surf, (255, 255, 255), [(x + 38, y + 55), (x + 44, y + 68), (x + 50, y + 55)])
            pygame.draw.polygon(surf, (210, 20, 20), [(x + 42, y + 58), (x + 44, y + 72), (x + 46, y + 58)])

        if stage == 1:
            pygame.draw.circle(surf, (0, 43, 106), (int(x + 44), int(y + 32)), 32)
        else:
            pygame.draw.circle(surf, (40, 40, 40), (int(x + 44), int(y + 32)), 32)

        pygame.draw.circle(surf, (255, 255, 255), (int(x + 46), int(y + 35)), 26)
        pygame.draw.circle(surf, (175, 215, 250), (int(x + 30), int(y + 40)), 6)
        pygame.draw.circle(surf, (175, 215, 250), (int(x + 58), int(y + 40)), 6)
        pygame.draw.circle(surf, (0, 0, 0), (int(x + 38), int(y + 30)), 2.5)
        pygame.draw.circle(surf, (0, 0, 0), (int(x + 54), int(y + 30)), 2.5)

        pygame.draw.line(surf, (0, 0, 0), (x + 42, y + 38), (x + 44, y + 41), 2)
        pygame.draw.line(surf, (0, 0, 0), (x + 44, y + 41), (x + 46, y + 38), 2)
        pygame.draw.line(surf, (0, 0, 0), (x + 46, y + 38), (x + 48, y + 41), 2)
        pygame.draw.line(surf, (0, 0, 0), (x + 48, y + 41), (x + 50, y + 38), 2)
        pygame.draw.line(surf, (0, 0, 0), (x + 40, y + 15), (x + 44, y + 19), 2)
        pygame.draw.line(surf, (0, 0, 0), (x + 44, y + 19), (x + 48, y + 15), 2)

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
        self.kind = kind
        self.rect = pygame.Rect(x, GROUND_Y-40, 40, 40)
        self.is_falling = False
        if self.kind in ["Military", "Tax"]:
            self.rect.y = -100
            self.max_speed = random.randint(11, 16)
        else:
            self.max_speed = 0

    def check_trigger(self, player_x):
        if self.max_speed > 0 and not self.is_falling:
            if self.rect.x - player_x < 620:
                self.is_falling = True

    def update(self):
        if self.is_falling and self.max_speed > 0:
            self.rect.y += self.max_speed
            if self.rect.y >= GROUND_Y - 40:
                self.rect.y = GROUND_Y - 40
                self.is_falling = False
                self.max_speed = 0

    def draw(self, surf, cam):
        if self.kind == "Stone":
            pygame.draw.polygon(surf, (100,100,100), [(self.rect.x-cam+20, self.rect.y), (self.rect.x-cam, self.rect.y+40), (self.rect.x-cam+40, self.rect.y+40)])
        elif self.kind == "Military":
            pygame.draw.rect(surf, (55, 75, 45), (self.rect.x-cam, self.rect.y, 44, 30))
            pygame.draw.polygon(surf, (80, 100, 70), [(self.rect.x-cam, self.rect.y), (self.rect.x-cam+22, self.rect.y+15), (self.rect.x-cam+44, self.rect.y)])
            txt = pygame.font.SysFont(None, 22).render("M", True, (255,255,255))
            surf.blit(txt, (self.rect.x-cam+16, self.rect.y+12))
        elif self.kind == "Tax":
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
                
        last_x = 600
        for _ in range(count_obs):
            last_x += random.randint(250, 450)
            if last_x < length - 300:
                obs_kind = random.choice(["Stone", "Military", "Military"])
                obstacles.append(Obstacle(last_x, obs_kind))
    else:
        attempts = 0
        while len(items) < count_items and attempts < 2000:
            x = random.randint(400, length - 600)
            attempts += 1
            if is_safe_zone(x, items, min_dist=320):
                kind = random.choice(["Gold", "Gold", "Gold", "Red", "Red"])
                items.append(Item(x, kind, 2))

        last_x = 600
        for _ in range(count_obs):
            last_x += random.randint(230, 420)
            if last_x < length - 300:
                obs_kind = random.choice(["Stone", "Tax", "Tax"])
                obstacles.append(Obstacle(last_x, obs_kind))

    return items, obstacles

player = Player()
stage = 1
camera_x = 0
items, obstacles = make_stage(1, STAGE1_LEN, 45, 38)
state = "intro"
transition_timer = 0

def restart_stage(target_stage):
    global player, stage, items, obstacles, camera_x, state
    saved_score = player.score if target_stage == 2 else 0
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
            elif event.key == pygame.K_RETURN and state == "intro":
                state = "game"

    if state == "intro":
        screen.fill((15, 25, 45))
        
        title_txt = big_font.render("학점 방어전 : 한성부기의 모험", True, (255, 255, 0))
        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 50))
        
        pygame.draw.rect(screen, (30, 45, 75), (60, 160, 1160, 440), border_radius=15)
        pygame.draw.rect(screen, (0, 43, 106), (60, 160, 1160, 440), 3, border_radius=15)
        
        lines = [
            (font, "[ 게임 조작법 ]", (175, 220, 245), 185),
            (small_font, "- 좌우 방향키 (◀ , ▶) : 한성부기 캐릭터 이동", (255, 255, 255), 225),
            (small_font, "- 스페이스바 (SPACE) : 위험물 회피용 점프 유도", (255, 255, 255), 255),
            
            (font, "[ 게임 규칙 및 기믹 ]", (175, 220, 245), 305),
            (small_font, "- 스테이지 1 (대학생): A+ 습득 시 점수 가산, F는 감점 처리됩니다.", (255, 255, 255), 345),
            (small_font, "  특히 R(재수강) 박스는 해당 스테이지가 처음부터 강제 리셋되니 주의하세요.", (255, 120, 120), 375),
            (small_font, "- 스테이지 2 (사회인): 황금 코인은 자산 점수가 추가되며, 빨간 코인은 자산이 차감됩니다.", (255, 255, 255), 415),
            (small_font, "- ★실시간 돌발 기믹★: 입영통지서(M)와 세금 폭탄(Tax)은 부기 전방 접근 시 기습 낙하합니다!", (255, 200, 100), 455),
            (small_font, "- 맵의 굴러오는 돌맹이나 기습 낙하물에 충돌할 경우 하트 생명력(HP)이 감소합니다.", (255, 255, 255), 495),
            (small_font, "- 총 10개의 기본 HP가 모두 소진되면 최종 게임 오버(패배) 처리됩니다.", (255, 255, 255), 525)
        ]
        
        for f_obj, text_str, color_rgb, y_pos in lines:
            rendered_text = f_obj.render(text_str, True, color_rgb)
            screen.blit(rendered_text, (90, y_pos))
        
        start_txt = font.render("ENTER 키를 누르면 게임이 시작됩니다!", True, (0, 255, 120))
        screen.blit(start_txt, (WIDTH // 2 - start_txt.get_width() // 2, 635))

    elif state == "game":
        player.update()
        length = STAGE1_LEN if stage == 1 else STAGE2_LEN
        p_rect = player.rect()

        for obs in obstacles:
            obs.check_trigger(player.x)
            obs.update()

        for item in items[:]:
            if p_rect.colliderect(item.rect):
                if item.kind in ["A+", "Gold"]:
                    player.score += 5
                elif item.kind in ["F", "Red"]:
                    player.score -= 5
                elif item.kind == "R":
                    restart_stage(1)
                    break
                items.remove(item)

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
            screen.fill((20, 25, 45))
            pygame.draw.rect(screen, (50, 50, 55), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))
            for bg_i in range(0, STAGE2_LEN, 1200):
                bx = bg_i - camera_x
                if -500 < bx < WIDTH + 500:
                    pygame.draw.rect(screen, (35, 40, 60), (bx, GROUND_Y-430, 220, 430))
                    for hx in range(20, 180, 45):
                        for hy in range(30, 400, 50):
                            pygame.draw.rect(screen, (255, 240, 150), (bx+hx, GROUND_Y-430+hy, 15, 20))
                    pygame.draw.rect(screen, (45, 50, 75), (bx+280, GROUND_Y-320, 300, 320))
                    for hx in range(30, 260, 50):
                        for hy in range(40, 280, 60):
                            pygame.draw.rect(screen, (180, 230, 255), (bx+hx, GROUND_Y-320+hy, 25, 25))
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
