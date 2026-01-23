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
FPS_EASY = 8
FPS_MEDIUM = 12
FPS_HARD = 16

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
DARK_GRAY = (40, 40, 40)

class Snake:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.score = 0
        self.is_paused = False
        
        # Настройки в зависимости от сложности
        if self.difficulty == "easy":
            self.speed = FPS_EASY
            self.food_value = 10
        elif self.difficulty == "medium":
            self.speed = FPS_MEDIUM
            self.food_value = 15
        else:  # hard
            self.speed = FPS_HARD
            self.food_value = 20
        
    def move(self):
        if self.is_paused:
            return
            
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
        self.score += self.food_value
        
    def check_collision(self):
        # На сложном уровне проигрыш при столкновении со стеной
        if self.difficulty == "hard":
            head_x, head_y = self.positions[0]
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                return True
        
        # Проверка на столкновение с собой (для всех уровней)
        return self.positions[0] in self.positions[1:]
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

class Food:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.position = self.randomize_position()
        self.timer = 0
        self.max_timer = self.get_max_timer()
        
    def get_max_timer(self):
        # Еда исчезает быстрее на сложных уровнях
        if self.difficulty == "easy":
            return 300  # 10 секунд при 30 FPS
        elif self.difficulty == "medium":
            return 200  # ~6.7 секунд
        else:
            return 150  # 5 секунд
            
    def randomize_position(self):
        return (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
    
    def update(self, is_paused=False):
        if not is_paused:
            self.timer += 1
        if self.timer >= self.max_timer:
            return True  # Еда исчезла
        return False
    
    def get_color(self):
        # Цвет еды показывает, сколько времени осталось
        if self.timer < self.max_timer * 0.3:
            return RED  # Полная свежесть
        elif self.timer < self.max_timer * 0.6:
            return (255, 150, 0)  # Оранжевый
        else:
            return (255, 100, 100)  # Бледно-красный

def draw_button(screen, text, rect, color, hover_color, font, is_hovered):
    """Рисует кнопку с эффектом наведения"""
    current_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, current_color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def difficulty_menu():
    """Меню выбора сложности"""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка - Выбор сложности")
    
    # Используем системный шрифт, который поддерживает русские символы
    try:
        font_large = pygame.font.SysFont("arial", 48)
        font_medium = pygame.font.SysFont("arial", 36)
        font_small = pygame.font.SysFont("arial", 24)
    except:
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
    
    # Кнопки
    button_width, button_height = 200, 60
    button_y_start = HEIGHT // 2 - 100
    
    easy_btn = pygame.Rect(WIDTH//2 - button_width//2, button_y_start, button_width, button_height)
    medium_btn = pygame.Rect(WIDTH//2 - button_width//2, button_y_start + 80, button_width, button_height)
    hard_btn = pygame.Rect(WIDTH//2 - button_width//2, button_y_start + 160, button_width, button_height)
    
    # Описания сложностей
    difficulties = {
        "easy": {
            "color": GREEN,
            "desc": ["• Медленная скорость", "• Еда не исчезает", "• Сквозные стены", "• +10 очков за еду"]
        },
        "medium": {
            "color": YELLOW,
            "desc": ["• Средняя скорость", "• Еда исчезает через 7 сек", "• Сквозные стены", "• +15 очков за еду"]
        },
        "hard": {
            "color": RED,
            "desc": ["• Высокая скорость", "• Еда исчезает через 5 сек", "• Стены убивают", "• +20 очков за еду"]
        }
    }
    
    selected_difficulty = None
    
    while selected_difficulty is None:
        mouse_pos = pygame.mouse.get_pos()
        
        # Проверка наведения на кнопки
        easy_hover = easy_btn.collidepoint(mouse_pos)
        medium_hover = medium_btn.collidepoint(mouse_pos)
        hard_hover = hard_btn.collidepoint(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(mouse_pos):
                    selected_difficulty = "easy"
                elif medium_btn.collidepoint(mouse_pos):
                    selected_difficulty = "medium"
                elif hard_btn.collidepoint(mouse_pos):
                    selected_difficulty = "hard"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    selected_difficulty = "easy"
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    selected_difficulty = "medium"
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    selected_difficulty = "hard"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Отрисовка
        screen.fill((30, 30, 50))  # Темно-синий фон
        
        # Заголовок
        title = font_large.render("ВЫБЕРИТЕ СЛОЖНОСТЬ", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Кнопки
        draw_button(screen, "ЛЕГКО (1)", easy_btn, GREEN, (100, 255, 100), font_medium, easy_hover)
        draw_button(screen, "СРЕДНЯЯ (2)", medium_btn, YELLOW, (255, 255, 100), font_medium, medium_hover)
        draw_button(screen, "СЛОЖНО (3)", hard_btn, RED, (255, 100, 100), font_medium, hard_hover)
        
        # Подсказки
        hint = font_small.render("Используйте мышь или клавиши 1, 2, 3", True, WHITE)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 80))
        
        hint2 = font_small.render("ESC - Выход", True, WHITE)
        screen.blit(hint2, (WIDTH//2 - hint2.get_width()//2, HEIGHT - 40))
        
        # Показ описания при наведении
        desc_y = 350
        desc_font = pygame.font.SysFont("arial", 20) if pygame.font.get_default_font() else pygame.font.Font(None, 20)
        
        if easy_hover:
            for i, line in enumerate(difficulties["easy"]["desc"]):
                text = desc_font.render(line, True, GREEN)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, desc_y + i*25))
        elif medium_hover:
            for i, line in enumerate(difficulties["medium"]["desc"]):
                text = desc_font.render(line, True, YELLOW)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, desc_y + i*25))
        elif hard_hover:
            for i, line in enumerate(difficulties["hard"]["desc"]):
                text = desc_font.render(line, True, RED)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, desc_y + i*25))
        
        pygame.display.flip()
    
    return selected_difficulty

def main_game(difficulty):
    """Основная игра с выбранной сложностью"""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Змейка - {difficulty.upper()}")
    clock = pygame.time.Clock()
    
    snake = Snake(difficulty)
    food = Food(difficulty)
    
    # Шрифты с поддержкой русского
    try:
        font = pygame.font.SysFont("arial", 36)
        small_font = pygame.font.SysFont("arial", 24)
        tiny_font = pygame.font.SysFont("arial", 18)
    except:
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        tiny_font = pygame.font.Font(None, 18)
    
    running = True
    game_over = False
    food_blink = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                # Выход
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                
                # Рестарт
                elif game_over and event.key == pygame.K_r:
                    snake.reset()
                    food = Food(difficulty)
                    game_over = False
                
                # Возврат в меню
                elif game_over and event.key == pygame.K_m:
                    return "menu"
                
                # Пауза
                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    paused = snake.toggle_pause()
                    
                    # Если пауза включена, показываем сообщение
                    if paused and not game_over:
                        pause_start_time = pygame.time.get_ticks()
                        while snake.is_paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.QUIT:
                                    return "quit"
                                elif pause_event.type == pygame.KEYDOWN:
                                    if pause_event.key == pygame.K_p or pause_event.key == pygame.K_SPACE:
                                        snake.toggle_pause()
                                    elif pause_event.key == pygame.K_ESCAPE:
                                        return "menu"
                            
                            # Отрисовка паузы
                            screen.fill(BLACK)
                            
                            # Змейка
                            for i, (x, y) in enumerate(snake.positions):
                                color = GREEN if i == 0 else BLUE
                                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                                pygame.draw.rect(screen, color, rect)
                                pygame.draw.rect(screen, BLACK, rect, 1)
                            
                            # Еда
                            food_rect = pygame.Rect(food.position[0] * GRID_SIZE, 
                                                   food.position[1] * GRID_SIZE, 
                                                   GRID_SIZE, GRID_SIZE)
                            pygame.draw.rect(screen, food.get_color(), food_rect)
                            
                            # Сообщение о паузе
                            pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                            pause_surface.fill((0, 0, 0, 180))
                            screen.blit(pause_surface, (0, 0))
                            
                            pause_text = font.render("ПАУЗА", True, YELLOW)
                            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, 
                                                    HEIGHT//2 - 50))
                            
                            continue_text = small_font.render("P или ПРОБЕЛ - продолжить", True, WHITE)
                            screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, 
                                                       HEIGHT//2 + 10))
                            
                            menu_text = small_font.render("ESC - выйти в меню", True, WHITE)
                            screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, 
                                                   HEIGHT//2 + 40))
                            
                            pygame.display.flip()
                
                # Управление змейкой (только если не game over и не пауза)
                elif not game_over and not snake.is_paused:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over and not snake.is_paused:
            snake.move()
            
            # Проверка на еду
            if snake.positions[0] == food.position:
                snake.grow()
                food.position = food.randomize_position()
                while food.position in snake.positions:
                    food.position = food.randomize_position()
                food.timer = 0  # Сброс таймера
            
            # Обновление еды (исчезновение)
            if food.update(snake.is_paused):
                food.position = food.randomize_position()
                while food.position in snake.positions:
                    food.position = food.randomize_position()
                food.timer = 0
            
            # Проверка на столкновение
            if snake.check_collision():
                game_over = True
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Отрисовка сетки (только на сложном уровне)
        if difficulty == "hard":
            for x in range(0, WIDTH, GRID_SIZE):
                pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))
        
        # Отрисовка змейки
        for i, (x, y) in enumerate(snake.positions):
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Отрисовка еды с миганием перед исчезновением
        food_blink += 1
        if food.timer > food.max_timer * 0.8 and food_blink % 10 < 5:
            pass  # Пропускаем отрисовку (мигание)
        else:
            food_rect = pygame.Rect(food.position[0] * GRID_SIZE, 
                                   food.position[1] * GRID_SIZE, 
                                   GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, food.get_color(), food_rect)
        
        # Отрисовка счёта и информации
        score_text = font.render(f"Очки: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Индикатор сложности
        diff_color = GREEN if difficulty == "easy" else YELLOW if difficulty == "medium" else RED
        diff_text = small_font.render(f"Сложность: {difficulty}", True, diff_color)
        screen.blit(diff_text, (WIDTH - diff_text.get_width() - 10, 10))
        
        # Индикатор паузы
        if snake.is_paused and not game_over:
            pause_indicator = small_font.render("ПАУЗА", True, YELLOW)
            screen.blit(pause_indicator, (WIDTH//2 - pause_indicator.get_width()//2, 10))
        
        # Таймер еды (прогресс-бар)
        if difficulty != "easy":
            timer_width = 200
            timer_height = 10
            timer_x = WIDTH // 2 - timer_width // 2
            timer_y = HEIGHT - 30
            
            # Фон прогресс-бара
            pygame.draw.rect(screen, (50, 50, 50), 
                           (timer_x, timer_y, timer_width, timer_height))
            
            # Заполнение
            fill_width = int(timer_width * (1 - food.timer / food.max_timer))
            timer_color = food.get_color()
            pygame.draw.rect(screen, timer_color, 
                           (timer_x, timer_y, fill_width, timer_height))
            
            # Текст
            timer_text = small_font.render("Время еды:", True, WHITE)
            screen.blit(timer_text, (timer_x, timer_y - 20))
        
        # Отрисовка Game Over
        if game_over:
            # Затемнение
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 
                                        HEIGHT // 2 - 50))
            
            # Финальный счёт
            final_score = small_font.render(f"Финальный счёт: {snake.score}", True, WHITE)
            screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 
                                     HEIGHT // 2))
            
            # Подсказки
            restart_text = tiny_font.render("R - начать заново", True, WHITE)
            menu_text = tiny_font.render("M - выйти в меню", True, WHITE)
            esc_text = tiny_font.render("ESC - выход", True, WHITE)
            
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 
                                      HEIGHT // 2 + 40))
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 
                                   HEIGHT // 2 + 70))
            screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, 
                                  HEIGHT // 2 + 100))
        
        # Подсказки управления (используем символы ASCII вместо стрелок)
        if not game_over:
            controls = [
                "Управление: Стрелки ВВЕРХ/ВНИЗ/ВЛЕВО/ВПРАВО",
                "Пауза: P или ПРОБЕЛ",
                "Меню: ESC"
            ]
            for i, text in enumerate(controls):
                control_text = tiny_font.render(text, True, (150, 150, 150))
                screen.blit(control_text, (10, HEIGHT - 90 + i * 25))
        
        pygame.display.flip()
        clock.tick(snake.speed)
    
    return "quit"

def main():
    """Главная функция"""
    pygame.display.set_caption("Змейка с выбором сложности")
    
    current_screen = "menu"
    difficulty = "medium"
    
    while True:
        if current_screen == "menu":
            difficulty = difficulty_menu()
            current_screen = "game"
        elif current_screen == "game":
            result = main_game(difficulty)
            if result == "menu":
                current_screen = "menu"
            elif result == "quit":
                break
        else:
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
