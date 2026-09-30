import pygame as pg




class Button:

    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen, font, hover_sound):
        hovering = self.rect.collidepoint(pg.mouse.get_pos())

        if hovering and not self.hovered:
            hover_sound.play()

        self.hovered = hovering

        if hovering:
            color = (255, 255, 100)
            draw_rect = self.rect.inflate(10, 10)
        else:
            color = (80, 80, 90)
            draw_rect = self.rect

        pg.draw.rect(screen, color, draw_rect, 4)

        text_surface = font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=draw_rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event is None:
            return False

        return (
            event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )