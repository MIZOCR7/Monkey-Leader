import pygame 
import os, sys


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()

screen_width, screen_height = info.current_w, info.current_h 
icon = pygame.image.load('assets/icon.png')
window_width, window_height = screen_width - 800, screen_height - 150 


clock = pygame.time.Clock()
FPS = 60


pygame.display.set_caption("Monkey Defeater") 
pygame.display.set_icon(icon) 

screen = pygame.display.set_mode((window_width, window_height)) 
section_width = window_width // 32 
section_height = window_height // 32 
slope = section_height // 8


class Platform:
  def __init__(self, x, y, length): 
    self.x = x * section_width
    self.y = y * section_height 
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
      
      top_line = pygame.rect.Rect((self.x, self.y), (self.length*section_width, 2)) 
      
    pygame.draw.rect(screen, 'blue', top_line) 
    

def create_platform():
  platforms = [(5, 15, 5)]
  ladders = [] 
  bridge_objs = []
  
  for bridge in platforms:
    bridge_objs.append(Platform(*bridge)) 
    
  return bridge_objs  

def main():
  bridge_objs = create_platform()
  
  while True:
    screen.fill('black') 
    clock.tick(FPS)
    
    for bridge in bridge_objs:
      bridge.draw()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
        pygame.quit()
        
    pygame.display.update()
      

if __name__ == '__main__':
  main()
