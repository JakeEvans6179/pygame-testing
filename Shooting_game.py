import pygame
import numpy as np
import time

# Initialize pygame
pygame.init()
width, height = 800, 600
player_size = enemy_size = 64
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Arial', 24)
start_time = time.time()  # Start time for enemy spawning
last_enemy_spawn_time = start_time  # Track last spawn time
game_end_time = None

#Upload your own images to make the game custom
icon = pygame.image.load("sample_icon.png")    #icon at the top left of the window
pygame.display.set_icon(icon)
background = pygame.image.load("sample_background.jpg") #upload your own 800x600 pixel image for background of game
player_image = pygame.image.load("sample_player.png") #player icon, upload your own 64x64 pixel image
enemy_image = pygame.image.load("sample_enemy.png")   #enemy icon, 64x64 pixel image
bullet_image = pygame.image.load("bullet.png")
game_over = pygame.image.load("sample_game_over.jpg")      #upload 800x600 image which shows when game is over and prompting you for restart


# Game state
game_active = True
hit_count = 0
font = pygame.font.SysFont('Arial', 24)
game_over_font = pygame.font.SysFont('Arial', 72)
restart_font = pygame.font.SysFont('Arial', 36)
disclaimer_font = pygame.font.SysFont('Arial', 20)


# Player setup
player_x = (width - player_size) / 2
player_y = height - player_size * 2
player_speed = 0.3
player_x_change = player_y_change = 0


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.active = True
        self.rect = pygame.Rect(x, y, 32, 32)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        screen.blit(bullet_image, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.speed_x = 0.3  # Define speed first
        self.speed_y = 0.3
        self.active = True
        self.respawn()  # Then call respawn



    def respawn(self):
        self.active = True
        self.x = np.random.randint(0, width - enemy_size)
        self.y = np.random.randint(0, 50)
        self.x_change = self.speed_x
        self.y_change = self.speed_y
        # Recreate the rect instead of trying to modify it
        self.rect = pygame.Rect(self.x, self.y, enemy_size, enemy_size)
        print(f"Respawned at ({self.x}, {self.y}) - Active: {self.active}")

    def update(self):
        if not self.active:
            if np.random.random() < 1:  # 1% chance to respawn
                self.respawn()
            return

        #Update position
        self.x = self.x + self.x_change
        self.y = self.y + self.y_change
        self.rect.x = self.x
        self.rect.y = self.y

        if self.x <= 0:
            self.x_change = self.speed_x

        elif self.x >= width - enemy_size:
            self.x_change = -self.speed_x

        if self.y <= 0:
            self.y_change = self.speed_y

        elif self.y >= height - enemy_size:
            self.y_change = -self.speed_y



    def draw(self, screen):
        if self.active:
            screen.blit(enemy_image, (self.x, self.y))


# Game objects
bullets = []
enemies = [Enemy()]     #Initialise how many enemies there are


def player(x, y):
    screen.blit(player_image, (x, y))


def check_collisions():
    global hit_count, game_active, game_end_time
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    for enemy in enemies:

        # Player-enemy collision
        if enemy.active and player_rect.colliderect(enemy.rect):
            print("Player hit enemy!")
            game_active = False
            game_end_time = time.time()
            return "player_hit"

        # Bullet-enemy collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.active and enemy.active and bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemy.active = False #Deactivate enemy (respawned later)
                    hit_count = hit_count + 1

                #bullets.remove(bullet)
                #enemy.active = False
                    print("Enemy destroyed!")

                    return "bullet_hit"

    return None

def game_over_screen():
    # Dark overlay


    screen.blit(game_over, (0, 0))


    time_text = game_end_time - start_time

    # Game over text
    game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 100))

    # Score display
    score_text = restart_font.render(f"Final Score: {hit_count}", True, (255, 255, 255))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))

    # Restart prompt
    restart_text = restart_font.render("Press R to Restart", True, (200, 200, 200))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

    #Small text
    disclaimer_line1 = disclaimer_font.render("Well done, you successfully managed to", True, (0, 0, 255))
    disclaimer_line2 = disclaimer_font.render(f"avoid enemies for {round(time_text)}s and killed {hit_count} enemies, would you like to try again?", True,(0, 0, 255))

    screen.blit(disclaimer_line1, (width // 2 - disclaimer_line1.get_width() // 2, height // 2 + 150))
    screen.blit(disclaimer_line2, (width // 2 - disclaimer_line2.get_width() // 2, height // 2 + 180))
# Main game loop
running = True
while running:

    current_time = time.time()
    elapsed_time = current_time - start_time

    screen.blit(background, (0, 0)) #space background



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_y_change = -player_speed
                elif event.key == pygame.K_a:
                    player_x_change = -player_speed
                elif event.key == pygame.K_d:
                    player_x_change = player_speed
                elif event.key == pygame.K_s:
                    player_y_change = player_speed
                elif event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player_x + 16, player_y))
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    player_x_change = 0
                elif event.key in (pygame.K_w, pygame.K_s):
                    player_y_change = 0
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset game
                game_active = True
                player_x = (width - player_size) / 2
                player_y = height - player_size * 2
                player_x_change = player_y_change = 0
                bullets.clear() #reset bullet list
                enemies = [Enemy()]
                hit_count = 0




    if game_active:
        # Update player
        player_x += player_x_change
        player_y += player_y_change
        player_x = max(0, min(width - player_size, player_x))
        player_y = max(0, min(height - player_size, player_y))

        if current_time - last_enemy_spawn_time >= 10:  #new enemy per 10s
            if len(enemies) <= 10:
                enemies.append(Enemy())
                last_enemy_spawn_time = current_time
                print(f"Added new enemy at {elapsed_time:.1f}s. Total enemies: {len(enemies)}")

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            if not bullet.active:
                bullets.remove(bullet)

        # In your enemy update loop:
        for enemy in enemies:
            enemy.update()
            if enemy.active == False:

                if np.random.random() < 1:  # 100% chance

                    print(enemy)
                    enemy.respawn()

        #Draw everything
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player(player_x, player_y)
        #Check collisions
        check_collisions()




        hit_text = font.render(f"Enemies killed: {hit_count}", True, (0, 0, 255))
        screen.blit(hit_text, (20, 20))

    else:
        game_over_screen()

    pygame.display.update()