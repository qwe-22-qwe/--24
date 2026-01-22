import pygame
import random
import sys

# Инициализация PyGame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.score = 0
        
    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx) % GRID_WIDTH
        new_y = (head_y + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
            
    def grow(self):
        self.length += 1
        self.score += 10
        
    def check_collision(self):
        return self.positions[0] in self.positions[1:]

class Food:
    def __init__(self):
        self.position = self.randomize_position()
        
    def randomize_position(self):
        return (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Змейка")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    font = pygame.font.SysFont(None, 36)
    
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    snake.reset()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            snake.move()
            
            # Проверка на еду
            if snake.positions[0] == food.position:
                snake.grow()
                food.position = food.randomize_position()
                while food.position in snake.positions:
                    food.position = food.randomize_position()
            
            # Проверка на столкновение
            if snake.check_collision():
                game_over = True
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Отрисовка змейки
        for i, (x, y) in enumerate(snake.positions):
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Отрисовка еды
        food_rect = pygame.Rect(food.position[0] * GRID_SIZE, 
                               food.position[1] * GRID_SIZE, 
                               GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        
        # Отрисовка счёта
        score_text = font.render(f"Очки: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Отрисовка Game Over
        if game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА! Нажми R для рестарта", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 
                                        HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
