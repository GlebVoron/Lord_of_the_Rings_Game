# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *
from monsters import *
import sys
import pygame.mixer
import pygame.camera
from pygame.locals import *

# Объявляем переменные
WIN_WIDTH = 1000  # Ширина создаваемого окна
WIN_HEIGHT = 840  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = '#0aafd0'
pygame.mixer.init()

FILE_DIR = os.path.dirname(__file__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.mixer.music.load("music/1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

F = False

F1 = open('%s/levels/level.txt' % FILE_DIR)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel(levelFile):
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                if commands[0] == "portal":  # если первая команда portal, то создаем портал
                    tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)
                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]), int(commands[7]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


def main(Level):
    progress_board.create_table()
    global level
    global entities
    global animatedEntities
    global monsters
    global platforms
    level = []
    entities = pygame.sprite.Group()  # Все объекты
    animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
    monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    time_start = datetime.datetime.now()
    progress_board.take_start_time(time_start)
    pygame.mixer.music.load("music/1.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    loadLevel(Level)
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Властелин колец")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    left = right = False  # по умолчанию - стоим
    up = False
    running = False
    px = playerX
    py = playerY
    hero = Player(px, py)  # создаем героя по (x,y) координатам
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "_":
                pf1 = Platform1(x, y)
                entities.add(pf1)
                platforms.append(pf1)
            if col == "^":
                pf2 = Platform2(x, y)
                entities.add(pf2)
                platforms.append(pf2)
            if col == "$":
                pf3 = Platform3(x, y)
                entities.add(pf3)
                platforms.append(pf3)
            if col == "!":
                f = Forest(x, y)
                entities.add(f)
                platforms.append(f)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            if col == "K":
                pr1 = Princess1(x, y)
                entities.add(pr1)
                platforms.append(pr1)
                animatedEntities.add(pr1)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                SCREEN_WIDTH = 800
                SCREEN_HEIGHT = 600
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                time_stop = datetime.datetime.now()
                progress_board.take_end_time(time_stop)
                progress_board.take_level_passed("Не пройден")
                menu_stop.main_menu()
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        animatedEntities.update()  # показываеaм анимацию
        monsters.update(platforms)  # передвигаем всех монстров
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms)  # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран
    else:
        pygame.display.update()


level = []
entities = pygame.sprite.Group()  # Все объекты
animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
platforms = []  # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main(F1)
