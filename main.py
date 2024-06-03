import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
# control the frame rate
clock = pygame.time.Clock()

# coin
coin = pygame.image.load('images/coin.png')
coin = pygame.transform.scale(coin, (16, 16))
# background
bg = pygame.image.load('images/BG.png')
# knight
knight = pygame.image.load('images/knight.png')
knight = pygame.transform.scale(knight, (55, 55))
# ground platform
ground = pygame.image.load('images/2.png')
ground = pygame.transform.scale(ground, (850, 64))
# platform
platform_img = pygame.image.load('images/2.png')
platform_img = pygame.transform.scale(platform_img, (150, 32))
# door
door = pygame.image.load('images/door.png')
door = pygame.transform.scale(door, (128, 128))

# platforms
platforms = [
    pygame.Rect(0, 536, 850, 64),
    pygame.Rect(50, 400, 128, 32),
    pygame.Rect(600, 450, 128, 32),
    pygame.Rect(200, 120, 128, 32),
    pygame.Rect(500, 200, 128, 32),
    pygame.Rect(700, 100, 128, 32),
    pygame.Rect(300, 300, 128, 32)
]


def draw_text(text, font_name, font_size, color, surface, x, y):
    font = pygame.font.SysFont(font_name, font_size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


click = False


def main_menu():
    while True:
        screen.fill("chartreuse3")
        draw_text('Main Menu', 'arial', 36, "black", screen, 320, 50)

        mx, my = pygame.mouse.get_pos()

        # Start button
        start_button = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(screen, "black", start_button)
        draw_text('Start', 'arial', 36, "white", screen, 350, 210)

        # Exit button
        exit_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(screen, "black", exit_button)
        draw_text('Exit', 'arial', 36, "white", screen, 355, 310)

        # checking whether the mouse collides with the buttons
        if start_button.collidepoint((mx, my)):
            if click:
                game()
        if exit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        # checks whether the buttons have been clicked
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # checks if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks if the left pad was clicked
                if event.button == 1:
                    click = True

        pygame.display.flip()
        clock.tick(60)


def game():
    knight_x = 400
    knight_y = 480
    knight_height = 55
    speed = 0
    accel = 0.1
    velocity = 3

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        new_knight_x = knight_x
        new_knight_y = knight_y
        # player input
        keys = pygame.key.get_pressed()
        # moving left and checks character stays within boundaries of the screen
        if keys[pygame.K_LEFT] and knight_x > velocity:
            new_knight_x -= velocity
        # moving right and checks character doesn't go off the screen
        if keys[pygame.K_RIGHT] and knight_x < 800 - knight_height - velocity:
            new_knight_x += velocity
        # jump
        if keys[pygame.K_SPACE] and knight_y > 55 + knight_height + velocity:
            speed = -5

        # horizontal movement

        new_knight_rect = pygame.Rect(new_knight_x, knight_y, 55, 55)
        x_collision = False

        # check player-platform collision
        for platform in platforms:
            if platform.colliderect(new_knight_rect):
                x_collision = True
                break

        if not x_collision:
            knight_x = new_knight_x

        # vertical movement
        speed += accel
        new_knight_y += speed

        new_knight_rect = pygame.Rect(knight_x, new_knight_y, 55, 55)
        y_collision = False

        # check player-platform collision
        for platform in platforms:
            if platform.colliderect(new_knight_rect):
                y_collision = True
                speed = 0
                break

        if not y_collision:
            knight_y = new_knight_y

        # background
        screen.blit(bg, (0, 0))
        # knight
        screen.blit(knight, (knight_x, knight_y))
        # coin
        screen.blit(coin, (240, 104))
        # door
        screen.blit(door, (715, 10))
        # ground platform
        screen.blit(ground, (0, 536))
        # drawing each platform
        for platform in platforms:
            screen.blit(platform_img, platform)

        pygame.display.update()
        clock.tick(60)


main_menu()
