import os
import sys, random 

import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()

screen_width, screen_height = info.current_w, info.current_h
icon = pygame.image.load('assets/icon.png')
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60

font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30) 

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


barrel_img = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel.png'), (section_width * 1.5, section_height * 2))  

flames_img = pygame.transform.scale(pygame.image.load('assets/images/fire.png'),(section_width * 2, section_height))
barrel_side = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel2.png'), (section_width * 2, section_height * 2.5))

dk1 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk1.png'), (section_width * 5, section_height * 5))

dk2 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk2.png'), (section_width * 5, section_height * 5))

dk3 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk3.png'), (section_width * 5, section_height * 5))


barrel_spawn_time = 360
barrel_count = barrel_spawn_time / 2 
barrel_time = 360 
fireball_trigger = False 

counter = 0

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


class Barrel(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((50,50)) 
    self.rect = self.image.get_rect() 
    self.rect.center = (x, y) 
    self.y_change = 0
    self.dir = 1
    self.x_change = 1
    self.pos = 0
    self.count = 0
    self.oil_collision = False 
    self.falling = False
    self.check_lad = False 
    self.was_falling = False 
    self.bottom = self.rect 
  
  
  def update(self, fire_trig):
        if self.y_change < 8 and not self.falling:
            self.y_change += 5
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.y_change = 0
                self.falling = False
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    fire_trig = True
        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 3
            else:
                self.x_change = -3
        else:
            self.x_change = 0
        
        
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height:
            self.kill()
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 3))
        return fire_trig

    
    
  def check_fall(self):
    already_collided = False 
    below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height)) 
    for lad in lads:
      if below.colliderect(lad) and not self.falling and not self.check_lad:
        self.check_lad = True
        already_collided = True
        if random.randint(0, 60) == 60:
          self.falling = True 
          self.y_change = 4 
    
    if not already_collided:
      self.check_lad = False 
  
  def draw(self):
    screen.blit(pygame.transform.rotate(barrel_img, 90*self.pos), self.rect.topleft)
  

class Bridge:
    def __init__(self, x, y, length):
        self.x = x * section_width
        self.y = y
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = (225, 51, 129)
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
      center = (lad_height/2) * section_height + top 
      
      left = self.x 
      right = left + section_width 
      pygame.draw.line(screen, lad_color, (left, top), (left, bottom), line_width)
      pygame.draw.line(screen, lad_color, (right, top), (right, bottom), line_width)
      pygame.draw.line(screen, lad_color, (left, center), (right, center), line_width) 
    body = pygame.rect.Rect((self.x, self.y - section_height), (section_width, (lad_height * self.length * section_height + section_height))) 
    return body 


def draw_extras():
    oil = draw_oil()
    return oil

def draw_oil():
    x_coord, y_coord = 4 * section_width, window_height - 4.5 * section_height 
    oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2*section_width, 2.5*section_height]) 
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 *section_width, y_coord, 2.2*section_width, .2*section_height])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 *section_width, y_coord + 2.3 * section_height, 2.2 * section_width, .2*section_height]) 
    pygame.draw.rect(screen, 'light blue', [x_coord + 0.1 * section_width, y_coord + .2*section_height, .2*section_width, .2*section_height])
    
    pygame.draw.rect(screen, 'light blue', [x_coord, y_coord + 0.5 * section_height, 2 * section_width, .2 * section_height])
    pygame.draw.rect(screen, 'light blue', [x_coord, y_coord + 1.7 * section_height, 2 * section_width, .2 * section_height]) 
    
    screen.blit(font2.render('OIL', True, 'light blue'), (x_coord + .4 * section_width - 10, y_coord + 0.7 * section_height - 2))  
    
    for i in range(4):
        pygame.draw.circle(screen, 'red', (x_coord + 0.5*section_width + i*0.4*section_width, y_coord + 2.1 * section_height), 3) 
    
    if counter < 15 or 30 < counter < 45:
        screen.blit(flames_img, (x_coord, y_coord - section_height)) 
    else:
        screen.blit(pygame.transform.flip(flames_img, True, False), (x_coord, y_coord - section_height)) 
    
    return oil 

def draw_barrels():
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 5.4 * section_height)) 
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 5.4 * section_height)) 
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 7.7 * section_height)) 
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 7.7 * section_height)) 
    
    
    
def draw_kong():
    phase_time = barrel_time // 4
    if barrel_spawn_time - barrel_count > 3 * phase_time:
        monkey_img = dk2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        monkey_img = dk1
    elif barrel_spawn_time - barrel_count > phase_time:
        monkey_img = dk3
    else:
        monkey_img = pygame.transform.flip(dk1, True, False) 
        screen.blit(barrel_img, (270, 270)) 
    
    screen.blit(monkey_img, (3.5 * section_width, row6_y - 5.5 * section_height))
    

def draw_screen():
    platforms = []
    climbers = []
    ladders_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']
    
    
    for ladder in  ladders:
      ladders_objs.append(Ladder(*ladder))
      if ladder[2] >= 3:
        climbers.append(ladders_objs[-1].body) 
    for bridge in bridges:
      bridge_objs.append(Bridge(*bridge))
      platforms.append(bridge_objs[-1].top)
    
    
    
    return platforms, climbers 



barrels = pygame.sprite.Group()  

def main():
    global barrel_count, barrel_time, plats, lads, fireball_trigger, oil_drum, counter
    while True:
        screen.fill('black')
        timer.tick(fps)
        if counter < 60:
            counter += 1
        else:
            counter = 0 
        
        plats, lads = draw_screen() 
        oil_drum = draw_extras() 
        draw_barrels()
        draw_kong()
        if barrel_count < barrel_spawn_time:
          barrel_count += 1
        else:
          barrel_count = random.randint(0, 120) 
          barrel_time = barrel_spawn_time - barrel_count
          barrel = Barrel(random.randint(100,600), 270) 
          barrels.add(barrel) 
          
        
        for barrel in barrels:
          barrel.draw() 
          barrel.check_fall() 
          fireball_trigger = barrel.update(fireball_trigger)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
