from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: tuple[int, int] | None = (CENTER_X, CENTER_Y),
        body_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Инициализация объекта с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self, screen: pygame.Surface) -> None:
        """Вирутальный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(
        self,
        position: tuple[int, int] | None = None,
        body_color: tuple[int, int, int] = APPLE_COLOR,
    ):
        """Инициализация объекта яблока."""
        super().__init__(position, body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод для случайного изменения позиции яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(
        self,
        position: tuple[int, int] = (CENTER_X, CENTER_Y),
        body_color: tuple[int, int, int] = SNAKE_COLOR,
        positions: list[tuple[int, int]] | None = None,
        direction: tuple[int, int] = RIGHT,
        next_direction: tuple[int, int] | None = None,
        last: tuple[int, int] | None = None,
    ):
        """Инициализация объекта змейки."""
        super().__init__(position=position, body_color=body_color)
        self.length: int = 1
        self.positions: list[tuple[int, int]] = (
            [position] if positions is None else positions
        )
        self.direction: tuple[int, int] = direction
        self.next_direction: tuple[int, int] | None = next_direction
        self.last: tuple[int, int] | None = last

    def get_head_position(self) -> tuple[int, int]:
        """Метод для получения позиции головы змейки."""
        return self.positions[0]

    def set_head_position(self, head_w: int, head_h: int) -> None:
        """Метод для установки позиции головы змейки."""
        self.positions[0] = (head_w, head_h)

    def move(self) -> None:
        """Метод для перемещения змейки."""
        head_position = self.get_head_position()
        self.positions.insert(
            0,
            (
                head_position[0] + self.direction[0] * GRID_SIZE,
                head_position[1] + self.direction[1] * GRID_SIZE,
            ),
        )
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Метод для сброса состояния змейки."""
        self.length = 1
        self.positions = [(CENTER_X, CENTER_Y)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def grow(self) -> None:
        """Метод для увеличения длины змейки."""
        self.length += 1

    def wrap_head_position(self) -> None:
        """Метод переноса головы змейки, при выходе за пределы экрана."""
        head_x, head_y = self.get_head_position()

        if head_x >= SCREEN_WIDTH:
            head_x = 0
        elif head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE

        if head_y >= SCREEN_HEIGHT:
            head_y = 0
        elif head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE

        self.set_head_position(head_x, head_y)

    def is_self_collision(self) -> bool:
        """Метод проверки столкновения змейки с самой собой."""
        if self.get_head_position() in self.positions[1:]:
            return True
        return False

    # Метод draw класса Snake
    def draw(self, screen: pygame.Surface) -> None:
        """Метод для отрисовки змейки на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self) -> None:
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake: Snake) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Главная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка событий
        handle_keys(snake)

        # Обновление направления
        snake.update_direction()

        # Движение змейки
        snake.move()
        snake.wrap_head_position()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()

            apple.randomize_position()

        # Проверка столкновения с собой
        collision_status = snake.is_self_collision()
        if collision_status:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
