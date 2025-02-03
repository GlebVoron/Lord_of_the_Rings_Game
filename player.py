from baze import *


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.y = y
        self.x = x
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows, scale_factor=0.15):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                scaled_frame = pygame.transform.scale(frame, (
                int(self.rect.w * scale_factor), int(self.rect.h * scale_factor)))
                self.frames.append(scaled_frame)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


    def move(self, movement):
        if movement == "up":
            self.y -= 5
        elif movement == "left":
            self.x -= 5
        elif movement == "right":
            self.x += 5

        self.rect.topleft = (self.x, self.y)

        # TODO код вставить в часть обработки событий
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             player.move("up")
        #         elif event.key == pygame.K_LEFT:
        #             player.move("left")
        #         elif event.key == pygame.K_RIGHT:
        #             player.move("right")

    def damage(self):
        # TODO сделать здесь алгоритм получения урона
        pass

    # TODO понять и сделать остальные фенкции
