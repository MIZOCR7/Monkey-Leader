# DONKEY KONG REBUILD IN PYTHON WITH THE PYGAME MODULE! (Est.720 Lines of Code)
import os
import sys

import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()

screen_width, screen_height = info.current_w, info.current_h
icon = pygame.image.load('assets/icon.png')
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60

# font = pygame.font.Font('freesansbold.ttf', 50)
# font2 = pygame.font.Font('freesansbold.ttf', 30)

pygame.display.set_caption("Monkey Defeater")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((window_width, window_height))
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8

start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height

row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope

active_level = 0
levels = [{'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                       (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                       (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                       (25, row2_y, 3), (22, row2_y - slope, 3),
                       (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                       (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                       (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                       (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                       (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                       (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                       (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                       (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                       (25, row4_y, 3), (22, row4_y - slope, 3),
                       (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                       (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                       (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                       (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                       (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                       (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                       (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                       (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                       (25, row6_y, 3), (22, row6_y - slope, 3),
                       (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                       (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                       (10, row6_y - 3 * section_height, 3)],
           'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                       (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                       (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                       (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                       (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                       (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                       (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                       (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                       (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                       (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
          'hammers': [(4, row6_top + section_height), (4, row4_top+section_height)],
           'target': (13, row6_y - 4 * section_height, 3)}]


class Bridge:
    def __init__(self, x, y, length):
        self.x = x * section_width
        self.y = y
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = (255, 51, 129)
        for i in range(self.length):
            bottom = self.y + section_height
            left = self.x + (section_width * i)
            center = left + (section_width * 0.5)
            right = left + section_width
            top = self.y
            pygame.draw.line(screen, platform_color, (left, top), (right, top), line_width)
            pygame.draw.line(screen, platform_color, (left, bottom), (right, bottom), line_width)
            pygame.draw.line(screen, platform_color, (left, bottom), (center, top), line_width)
            pygame.draw.line(screen, platform_color, (center, top), (right, bottom), line_width)

        top_line = pygame.rect.Rect((self.x, self.y), (self.length * section_width, 2))
        return top_line

class Ladder:
  def __init__(self, x, y, length):
    self.x = x * section_width
    self.y = y
    self.length = length 
    self.body = self.draw() 
  
  def draw(self):
    line_width = 3
    lad_color = 'light blue'
    lad_height = 0.6
    for i in range(self.length):
      top = self.y + lad_height * section_height * i 
      bottom = top + lad_height * section_height
      center = (bottom - top) / 2 + top 
      
      left = self.x 
      right = left + section_width 
      pygame.draw.line(screen, lad_color, (left, top), (left, bottom), line_width)
      pygame.draw.line(screen, lad_color, (right, top), (right, bottom), line_width)
      pygame.draw.line(screen, lad_color, (left, center), (right, center), line_width) 
    body = pygame.rect.Rect((self.x, self.y - section_height), (section_width, (lad_height * self.length + section_height)))
    return body 


def draw_screen():
    platforms = []
    climbers = []
    ladders_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for bridge in bridges:
      bridge_objs.append(Bridge(*bridge))
      platforms.append(bridge_objs[-1].top)
    for ladder in  ladders:
      ladders_objs.append(Ladder(*ladder))
      if ladder[2] >= 3:
        climbers.append(ladders_objs[-1].body) 
    
    
    return platforms, climbers 


def main():
    run = True
    while run:
        screen.fill('black')
        timer.tick(fps)

        plats, lads = draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
