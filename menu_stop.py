import pygame
import pygame.mixer
import pygame.camera
from pygame.locals import *
import progress_board
import start
import sys
import bd_win
from PyQt6.QtWidgets import QApplication

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для звука

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Главное меню")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Шрифт
font = pygame.font.Font(None, 36)


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


# Класс ползунка
class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.thumb_width = 10  # Ширина "ползунка"
        self.thumb_rect = pygame.Rect(x + int(width * initial_value) - self.thumb_width // 2, y, self.thumb_width,
                                      height)
        self.value = initial_value
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)  # Фон ползунка
        pygame.draw.rect(screen, RED, self.thumb_rect)  # Ползунок

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                x = event.pos[0] - self.thumb_width // 2
                x = max(self.rect.left, min(x, self.rect.right - self.thumb_width))
                self.thumb_rect.x = x
                self.value = (x - self.rect.left) / (self.rect.width - self.thumb_width)
                self.value = max(0.0, min(self.value, 1.0))

    def get_value(self):
        return self.value


def logbook():
    app = QApplication(sys.argv)
    log_window = bd_win.LogWindow()
    log_window.show()
    app.exec()


def open_settings():
    global settings_open
    settings_open = True
    settings_menu()


# Основной цикл настроек
def settings_menu():
    global settings_open
    settings_open = True
    settings_screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Настройки")
    volume_slider = Slider(50, 100, 300, 20, initial_value=0.5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                settings_open = False
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.set_caption("Главное меню")
                return
            volume_slider.handle_event(event)

        volume = volume_slider.get_value()
        pygame.mixer.music.set_volume(volume)  # Устанавливаем громкость музыки

        settings_screen.fill(BLACK)
        volume_slider.draw(settings_screen)
        volume_text = font.render(f"Громкость: {int(volume * 100)}%", True, WHITE)
        settings_screen.blit(volume_text, (50, 50))

        pygame.display.flip()

    settings_open = False
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Главное меню")


# Создание кнопок
button_width = 200
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y_start = 150
button_spacing = 100

logbook_button = Button(button_x, button_y_start + button_spacing, button_width, button_height, "Логи игроков", GRAY,
                        WHITE,
                        logbook)
settings_button = Button(button_x, button_y_start + 2 * button_spacing, button_width, button_height, "Настройки", GRAY,
                         WHITE, open_settings)

buttons = [logbook_button, settings_button]

# Флаг, указывающий, открыты ли настройки
settings_open = False


# Основной цикл меню
def main_menu():
    progress_board.create_table()
    progress_board.record_level_session()
    background_image = pygame.image.load("fon/горы.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Загрузка фоновой музыки
    pygame.mixer.music.load("music/2.mp3")
    pygame.mixer.music.set_volume(0.5)  # установите громкость
    pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        # Обработка наведения мыши
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            if button.is_hovered(mouse_pos):
                button.color = button.hover_color
            else:
                button.color = GRAY

        # Отрисовка
        screen.blit(background_image, (0, 0))  # Отображаем фоновое изображение
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Запуск меню
if __name__ == "__main__":
    main_menu()
