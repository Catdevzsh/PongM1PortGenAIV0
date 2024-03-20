import pygame
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)  # Mono channel for retro sound

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# Game variables
paddle_width, paddle_height = 15, 80
ball_diameter = 15
ball_radius = ball_diameter // 2
paddle_speed = 10
ball_speed = [5, -5]
paddle1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle2 = pygame.Rect(SCREEN_WIDTH - 50 - paddle_width, SCREEN_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(SCREEN_WIDTH // 2 - ball_radius, SCREEN_HEIGHT // 2 - ball_radius, ball_diameter, ball_diameter)
score1 = 0
score2 = 0

# Sound generation function for retro-style effects
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
hit_sound = generate_square_wave(660, 0.1, 0.1)
score_sound = generate_square_wave(440, 0.1, 0.1)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    paddle1.y += (keys[pygame.K_s] - keys[pygame.K_w]) * paddle_speed
    paddle2.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * paddle_speed

    # Keep paddles inside the screen
    paddle1.y = max(0, min(paddle1.y, SCREEN_HEIGHT - paddle_height))
    paddle2.y = max(0, min(paddle2.y, SCREEN_HEIGHT - paddle_height))

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Wall collision
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
        hit_sound.play()

    # Paddle collision
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed[0] = -ball_speed[0]
        hit_sound.play()

    # Score update
    if ball.left <= 0:
        score2 += 1
        score_sound.play()
        ball.x, ball.y = SCREEN_WIDTH // 2 - ball_radius, SCREEN_HEIGHT // 2 - ball_radius
        ball_speed[0] = -ball_speed[0]
    elif ball.right >= SCREEN_WIDTH:
        score1 += 1
        score_sound.play()
        ball.x, ball.y = SCREEN_WIDTH // 2 - ball_radius, SCREEN_HEIGHT // 2 - ball_radius
        ball_speed[0] = -ball_speed[0]

    # Check for win/lose condition
    if score1 == 5:
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", 1, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    elif score2 == 5:
        font = pygame.font.Font(None, 74)
        text = font.render("You Lose!", 1, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Display scores
    font = pygame.font.Font(None, 74)
    text = font.render(str(score1), 1, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 4, 50))
    text = font.render(str(score2), 1, WHITE)
    screen.blit(text, (SCREEN_WIDTH * 3 // 4, 50))

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
