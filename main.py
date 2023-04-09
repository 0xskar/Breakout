import random
import pygame

# pygame main window setup
window_width = 1280
window_height = 720
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True

# border
border_width = 5
border_color = (255, 0, 0)
border_rects = [
    pygame.Rect(0, 0, window_width, border_width),
    pygame.Rect(0, 0, border_width, window_height),
    pygame.Rect(window_width - border_width, 0, border_width, window_height)
]


class Ball:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed_x = 10  # initial x speed
        self.speed_y = -10  # initial y speed
        # load ball sound
        self.hit_sound = pygame.mixer.Sound("assets/ball_blip.mp3")
        self.lose_life_sound = pygame.mixer.Sound("assets/lose_life.mp3")

    def update(self):
        # update ball position
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)

        # handle collision with walls
        global player_lives
        if self.rect.left < 0 or self.rect.right > window_width:
            self.speed_x *= -1
            self.hit_sound.play()
        if self.rect.top < 0:
            self.speed_y *= -1
            self.hit_sound.play()
        if self.rect.bottom > window_height:
            # if ball hits bottom wall, reset ball position and speed
            self.x = random.randint(0, window_width)
            self.y = 400
            self.rect.center = (self.x, self.y)
            self.speed_x = random.choice([-5, 5])
            self.speed_y = -5
            player_lives -= 1
            self.lose_life_sound.play()

        # handle paddle collision
        if self.rect.colliderect(player_rect):
            # calculate position of ball relative to paddle
            ball_pos = self.rect.centerx - player_rect.left
            # calculate percentage of paddle hit (between 0 and 1)
            hit_percent = ball_pos / player_rect.width
            # calculate new x speed based on hit percentage
            self.speed_x = int(hit_percent * 10 - 5)
            self.speed_y *= -1
            self.hit_sound.play()

    def draw(self, surface):
        # draw ball image
        surface.blit(self.image, self.rect)


class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit_sound = pygame.mixer.Sound("assets/ball_blip.mp3")

    def ball_collision(self, ball):
        global player_score
        if self.rect.colliderect(ball.rect):
            ball.speed_y *= -1
            bricks.remove(self)
            player_score += 1
            self.hit_sound.play()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# brick variables, colors and spacing
brick_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
]
brick_width = (window_width - 80) // 10
brick_height = 25
brick_spacing = 5

# create bricks
bricks = []
for row in range(5):
    y = row * (brick_height + brick_spacing) + 100
    for col in range(10):
        x = 15 + col * (brick_width + brick_spacing) + 3
        color = random.choice(brick_colors)
        brick = Brick(x, y, brick_width, brick_height, color)
        bricks.append(brick)

# player info and other variables
player_paddle = pygame.image.load("assets/player_paddle.png")
player_width = 175
player_height = 25
player_rect = player_paddle.get_rect()
player_lives = 3
player_score = 0
font = pygame.font.Font(None, 36)
game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")

# player positioning
player_rect.x = (window_width - player_width) // 2
player_rect.y = window_height - player_height - 10

# player movement
move_left = False
move_right = False


def game_over():
    game_over_sound.play()


# balls
ball = Ball(random.randint(0, window_width), 400, "assets/ball.png")

if __name__ == "__main__":

    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # paddle movement positioning
        mouse_x, _ = pygame.mouse.get_pos()
        player_rect.centerx = mouse_x

        # keep paddle on screen
        if player_rect.left < 0:
            player_rect.left = 0
        elif player_rect.right > window_width:
            player_rect.right = window_width

        # ball stuff
        ball.update()

        # GAME STARTS HERE DRAWS EVERY FRAME
        # fill screen with a color to wipe away anything from last frame
        screen.fill("black")

        for rect in border_rects:
            pygame.draw.rect(screen, border_color, rect)

        for brick in bricks:
            brick.ball_collision(ball)

        for brick in bricks:
            brick.draw(screen)

        score_text = font.render(f"Score: {player_score}", True, (255, 0, 0))
        lives_text = font.render(f"Lives: {player_lives}", True, (255, 0, 0))

        # check lives
        if player_lives == 0:
            ball.speed_x = 0
            ball.speed_y = 0
            game_over_text = font.render(f"Game over!", True, (255, 0, 0))
            game_over()
            screen.blit(game_over_text, (window_width / 2, window_height / 2))
            running = False

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (window_width - 100, 10))
        screen.blit(player_paddle, player_rect)

        ball.draw(screen)

        # UPDATE THE SCREEN FROM THE GAME START TO HERE
        pygame.display.update()

        # flip() the display to put work on screen?
        pygame.display.flip()

        # sets FPS to 60 max
        clock.tick(60)


