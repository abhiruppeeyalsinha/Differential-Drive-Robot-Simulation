import pygame
import math


class Enviornmnet():
    def __init__(self, dimensions):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

        self.height = dimensions[0]
        self.width = dimensions[1]

        pygame.display.set_caption("Differential Drive Robot")
        self.map = pygame.display.set_mode((self.width, self.height))

        # self.text = 'default text'
        self.font = pygame.font.Font(r"E:\robotics\freesansbold.ttf", 50)
        self.text = self.font.render('default', True, self.white, self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center = (dimensions[1]-600, dimensions[0]-100)

    def write_info(self, vl, vr, theta):
        text = f"Vl = {vl} Vr = {vr} theta = {int(math.degrees(theta))}"
        self.text = self.font.render(text, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)


class Robot():
    def __init__(self, start_pos, roboImg, width):
        self.meter_to_pix = 3779.52
        self.w = width
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.theta = 0
        self.vl = 0.01*self.meter_to_pix
        self.vr = 0.01*self.meter_to_pix
        self.max_speed = 0.02*self.meter_to_pix
        self.min_speed = 0.02*self.meter_to_pix

        self.img = pygame.image.load(roboImg)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def move(self, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    self.vl += 0.01*self.meter_to_pix
                elif event.key == pygame.K_SPACE:
                    self.vl -= 0.01*self.meter_to_pix
                elif event.key == pygame.K_BACKSPACE:
                    self.vr += 0.01*self.meter_to_pix
                elif event.key == pygame.K_LSHIFT:
                    self.vr -= 0.01*self.meter_to_pix

        self.x += ((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        self.y += ((self.vl+self.vr)/2)*math.sin(self.theta)*dt
        self.theta += (self.vr-self.vl)/self.w*dt

        self.rotated = pygame.transform.rotozoom(
            self.img, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))


pygame.init()

start = (200, 200)
dim = (600, 1200)
running = True
dt = 0
last_time = pygame.time.get_ticks()


enviornmnet = Enviornmnet(dim)
robot = Robot(start, r"E:\robotics\robot.png", 0.01*3779.52)

while running:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            running = False
        robot.move(event)
    dt = (pygame.time.get_ticks()-last_time)/1000
    last_time = pygame.time.get_ticks()
    print(dt)
    pygame.display.update()
    enviornmnet.map.fill(enviornmnet.white)
    robot.move()
    robot.draw(enviornmnet.map)
    enviornmnet.write_info(int(robot.vl), int(robot.vr), robot.theta)
