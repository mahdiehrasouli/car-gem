import pygame
import random

# مقداردهی اولیه pygame
pygame.init()

# ابعاد صفحه بازی
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("car gem")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# متغیرها
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5  # سرعت اولیه بازیکن

obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5  # سرعت اولیه موانع

# لیست‌ها برای موانع
obstacles = []  # موانع قرمز
green_obstacles = []  # موانع سبز

font = pygame.font.SysFont("Arial", 32)

# متغیر شمارش موانع سبز
green_obstacles_collected = 0

# تابع رسم بازیکن
def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

# تابع رسم موانع قرمز
def draw_red_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

# تابع رسم موانع سبز
def draw_green_obstacles(green_obstacles):
    for obs in green_obstacles:
        pygame.draw.rect(screen, GREEN, obs)

# تابع ایجاد موانع قرمز
def create_red_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

# تابع ایجاد موانع سبز
def create_green_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

# تابع بررسی برخورد
def check_collision(player_rect, obstacles):
    for obs in obstacles:
        if player_rect.colliderect(obs):
            return True
    return False

# حلقه بازی
def game_loop():
    global player_speed, obstacle_speed, green_obstacles_collected  # استفاده از متغیرهای جهانی

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    obstacles[:] = []  # لیست موانع قرمز رو خالی می‌کنیم
    green_obstacles[:] = []  # لیست موانع سبز رو خالی می‌کنیم
    score = 0
    game_over = False

    while not game_over:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # کنترل بازیکن
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # ایجاد و حرکت موانع
        if random.random() < 0.05:
            obstacles.append(create_red_obstacle())  # ایجاد مانع قرمز
        if random.random() < 0.02:
            green_obstacles.append(create_green_obstacle())  # ایجاد مانع سبز

        # حرکت موانع
        for obs in obstacles:
            obs.y += obstacle_speed
        for obs in green_obstacles:
            obs.y += obstacle_speed

        # حذف موانع خارج از صفحه
        obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]
        green_obstacles[:] = [obs for obs in green_obstacles if obs.y < HEIGHT]

        # بررسی برخورد با موانع قرمز
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if check_collision(player_rect, obstacles):
            game_over = True

        # بررسی برخورد با موانع سبز (افزایش سرعت و حذف مانع سبز)
        for obs in green_obstacles[:]:
            if player_rect.colliderect(obs):
                player_speed += 1  # افزایش سرعت ماشین (بازیکن)
                obstacle_speed += 1  # افزایش سرعت موانع
                green_obstacles.remove(obs)  # حذف مانع سبز از لیست
                green_obstacles_collected += 1  # افزایش تعداد موانع سبز گرفته شده

        # نمایش اطلاعات
        draw_player(player_x, player_y)
        draw_red_obstacles(obstacles)
        draw_green_obstacles(green_obstacles)

        score_text = font.render(f"emtiaz: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # نمایش تعداد موانع سبز گرفته شده
        green_count_text = font.render(f"benzin: {green_obstacles_collected}", True, WHITE)
        screen.blit(green_count_text, (10, 50))

        pygame.display.update()

        # افزایش امتیاز
        score += 1

        pygame.time.Clock().tick(60)  # سرعت فریم

        # نمایش پیام پایان بازی
    screen.fill(BLACK)
    game_over_text = font.render("bazi tmam shod!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    score_text = font.render(f"emtiaz nahai: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    pygame.time.delay(3000)  # نمایش نتیجه برای 3 ثانیه


# اجرای بازی
def main():
    for _ in range(3):  # بازی در 3 مرحله
        game_loop()

    pygame.quit()


# اجرای بازی
main()