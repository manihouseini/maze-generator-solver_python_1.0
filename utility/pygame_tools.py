import pygame

pygame.init()
FONT = pygame.font.Font(None, 30)


def debug(text, y):
    txt = FONT.render(str(text), True, (255, 255, 255), (0, 0, 0))
    win = pygame.display.get_surface()
    win.blit(txt, (10, y))
