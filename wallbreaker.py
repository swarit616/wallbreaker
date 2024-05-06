import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_GAP = 5
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
PADDLE_SPEED = 10
BALL_SPEED = 5

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wallbreaker")

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def update(self, direction):
        self.rect.x += direction * PADDLE_SPEED
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, paddle):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(paddle.rect.centerx, paddle.rect.top - BALL_RADIUS))
        self.vel = pygame.math.Vector2(0, -BALL_SPEED)
    
    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0:
            self.vel.y *= -1

# Main function
def main():
    # Create bricks
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    for row in range(3):
        for col in range(WIDTH // (BRICK_WIDTH + BRICK_GAP)):
            color = random.choice(BRICK_COLORS)
            brick = Brick(color, col * (BRICK_WIDTH + BRICK_GAP), row * (BRICK_HEIGHT + BRICK_GAP) + 50)
            all_sprites.add(brick)
            bricks.add(brick)

    # Create paddle and ball
    paddle = Paddle()
    ball = Ball(paddle)
    all_sprites.add(paddle, ball)

    # Game loop
    clock = pygame.time.Clock()
    running = True
    win_message_shown = False  # Flag to indicate if win message is shown
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.update(-1)
        if keys[pygame.K_RIGHT]:
            paddle.update(1)

        ball.update()

        # Check collisions
        collisions = pygame.sprite.spritecollide(ball, bricks, True)
        if collisions:
            ball.vel.y *= -1

        # Check collision with paddle
        if pygame.sprite.collide_rect(ball, paddle):
            ball.rect.bottom = paddle.rect.top  # Ensure the ball is above the paddle
            ball.vel.y *= -1  # Reverse the vertical velocity
            # Adjust horizontal velocity based on where the ball hits the paddle
            offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            ball.vel.x += offset

        # Check if all bricks are broken
        if not bricks and not win_message_shown:
            font = pygame.font.Font(None, 36)
            text = font.render("You won!", True, WHITE)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            win_message_shown = True

        # Draw everything
        win.fill(BLACK)
        all_sprites.draw(win)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
