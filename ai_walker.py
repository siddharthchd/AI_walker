import pygame
import pymunk
import pymunk.pygame_util
import os
import math
import sys
import random

screen_width = 900
screen_height = 650
space = pymunk.Space()
space.gravity = (0.0, -100.0)
generation = 0

class Human:

    def __init__(self):

        moment = 5
        friction = 0.5
        self.shape = pymunk.Poly.create_box(None, (50, 100))
        body_moment = pymunk.moment_for_poly(moment, self.shape.get_vertices())
        self.body = pymunk.Body(moment, body_moment)
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)

        self.body.position = (screen_width / 2, 500)
        self.shape.body = self.body
        self.shape.color = (150, 150, 150, 0)

        # head
        head_moment = pymunk.moment_for_circle(moment, 0, 30)
        self.head_body = pymunk.Body(moment, head_moment)
        self.head_body.position = (self.body.position.x, self.body.position.y + 80)
        self.head_shape = pymunk.Circle(self.head_body, 30)
        self.head_joint1 = pymunk.PivotJoint(self.head_body, self.body, (-5, -30), (-5, 50))
        self.head_joint2 = pymunk.PivotJoint(self.head_body, self.body, (5, -30), (5, 50))

        # arms
        arm_size = (100, 20)

        self.left_arm_upper_shape = pymunk.Poly.create_box(None, arm_size)
        left_arm_upper_moment = pymunk.moment_for_poly(moment, self.left_arm_upper_shape.get_vertices())
        self.left_arm_upper_body = pymunk.Body(moment, left_arm_upper_moment)
        self.left_arm_upper_body.position = (self.body.position.x - 30, self.body.position.y)
        self.left_arm_upper_shape.body = self.left_arm_upper_body
        self.left_arm_upper_joint = pymunk.PivotJoint(self.left_arm_upper_body, self.body, (arm_size[0] / 2, 0), (-25, 30))
        self.left_arm_motor = pymunk.SimpleMotor(self.body, self.left_arm_upper_body, 0)

        self.right_arm_upper_shape = pymunk.Poly.create_box(None, arm_size)
        right_arm_upper_moment = pymunk.moment_for_poly(moment, self.right_arm_upper_shape.get_vertices())
        self.right_arm_upper_body = pymunk.Body(moment, right_arm_upper_moment)
        self.right_arm_upper_body.position = (self.body.position.x + 30, self.body.position.y)
        self.right_arm_upper_shape.body = self.right_arm_upper_body
        self.right_arm_upper_joint = pymunk.PivotJoint(self.right_arm_upper_body, self.body, (arm_size[0] / 2, 0), (25, 30))
        self.right_arm_motor = pymunk.SimpleMotor(self.body, self.right_arm_upper_body, 0)

        # thighs
        thigh_size = (30, 60)

        self.left_thigh_shape = pymunk.Poly.create_box(None, thigh_size)
        left_thigh_moment = pymunk.moment_for_poly(moment, self.left_thigh_shape.get_vertices())
        self.left_thigh_body = pymunk.Body(moment, left_thigh_moment)
        self.left_thigh_body.position = (self.body.position.x - 20, self.body.position.y - 50)
        self.left_thigh_shape.body = self.left_thigh_body
        self.left_thigh_shape.friction = friction
        self.left_thigh_joint = pymunk.PivotJoint(self.left_thigh_body, self.body, (0, thigh_size[1] / 2), (-20, -50))
        self.left_thigh_motor = pymunk.SimpleMotor(self.body, self.left_thigh_body, 0)

        self.right_thigh_shape = pymunk.Poly.create_box(None, thigh_size)
        right_thigh_moment = pymunk.moment_for_poly(moment, self.right_thigh_shape.get_vertices())
        self.right_thigh_body = pymunk.Body(moment, right_thigh_moment)
        self.right_thigh_body.position = (self.body.position.x - 20, self.body.position.y - 50)
        self.right_thigh_shape.body = self.right_thigh_body
        self.right_thigh_shape.friction = friction
        self.right_thigh_joint = pymunk.PivotJoint(self.right_thigh_body, self.body, (0, thigh_size[1] / 2), (-20, -50))
        self.right_thigh_motor = pymunk.SimpleMotor(self.body, self.right_thigh_body, 0)

        # shin
        shin_size = (20, 70)

        self.left_shin_shape = pymunk.Poly.create_box(None, shin_size)
        left_shin_moment = pymunk.moment_for_poly(moment, self.left_shin_shape.get_vertices())
        self.left_shin_body = pymunk.Body(moment, left_shin_moment)
        self.left_shin_body.position = (self.left_thigh_body.position.x, self.left_thigh_body.position.y - 100)
        self.left_shin_shape.body = self.left_shin_body
        self.left_shin_shape.friction = friction
        self.left_shin_joint = pymunk.PivotJoint(self.left_shin_body, self.left_thigh_body, (0, shin_size[1] / 2), (0, -thigh_size[1] / 2))
        self.left_shin_motor = pymunk.SimpleMotor(self.left_thigh_body, self.left_shin_body, 0)

        self.right_shin_shape = pymunk.Poly.create_box(None, shin_size)
        right_shin_moment = pymunk.moment_for_poly(moment, self.right_shin_shape.get_vertices())
        self.right_shin_body = pymunk.Body(moment, right_shin_moment)
        self.right_shin_body.position = (self.right_thigh_body.position.x, self.right_thigh_body.position.y - 100)
        self.right_shin_shape.body = self.right_shin_body
        self.right_shin_shape.friction = friction
        self.right_shin_joint = pymunk.PivotJoint(self.right_shin_body, self.right_thigh_body, (0, shin_size[1] / 2), (0, -thigh_size[1] / 2))
        self.right_shin_motor = pymunk.SimpleMotor(self.right_thigh_body, self.right_shin_body, 0)


        space.add(self.body, self.shape, self.head_body, self.head_shape, self.head_joint1, self.head_joint2)
        space.add(self.left_thigh_body, self.left_thigh_shape, self.left_thigh_joint, self.left_thigh_motor)
        space.add(self.right_thigh_body, self.right_thigh_shape, self.right_thigh_joint, self.right_thigh_motor)
        space.add(self.left_shin_body, self.left_shin_shape, self.left_shin_joint, self.left_shin_motor)
        space.add(self.right_shin_body, self.right_shin_shape, self.right_shin_joint, self.right_shin_motor)

        shape_filter = pymunk.ShapeFilter(group = 1)
        self.shape.filter = shape_filter
        self.head_shape.filter = shape_filter
        self.left_arm_upper_shape.filter = shape_filter
        self.right_arm_upper_shape.filter = shape_filter
        self.left_thigh_shape.filter = shape_filter
        self.right_thigh_shape.filter = shape_filter
        self.left_shin_shape.filter = shape_filter
        self.right_shin_shape.filter = shape_filter

        self.face = pygame.image.load('angry_pepe_frog.png')
        self.face = pygame.transform.scale(self.face, (100,100))

        self.is_done = False
        self.distance = 0
        self.left_arm_flag = False
        self.right_arm_flag = False
        self.left_thigh_flag = False
        self.right_thigh_flag = False
        self.left_shin_flag = False
        self.right_shin_flag = False


    def get_shape(self):

        body = self.body, self.shape
        head = self.head_body, self.head_shape, self.head_joint1, self.head_joint2
        left_leg_thigh = self.left_thigh_body, self.left_thigh_shape, self.left_thigh_joint, self.left_thigh_motor
        right_leg_thigh = self.right_thigh_body, self.right_thigh_shape, self.right_thigh_joint, self.right_thigh_motor
        left_leg_shin = self.left_shin_body, self.left_shin_shape, self.left_shin_joint, self.left_shin_motor
        right_leg_shin = self.right_shin_body, self.right_shin_shape, self.right_shin_joint, self.right_shin_motor

        return body, head, left_leg_thigh, left_leg_shin, right_thigh, right_shin

    def get_data(self):

        left_thigh = ((360 - math.degrees(self.left_thigh_body.angle)) - (360 - math.degrees(self.body.angle))) / 360.0
        left_shin = ((360 - math.degrees(self.left_shin_body.angle)) - (360 - math.degrees(self.body.angle))) / 360.0
        right_thigh = ((360 - math.degrees(self.right_thigh_body.angle)) - (360 - math.degrees(self.body.angle))) / 360.0
        right_shin = ((360 - math.degrees(self.right_shin_body.angle)) - (360 - math.degrees(self.body.angle))) / 360.0

        return self.body.angle, left_thigh, left_shin, right_thigh, right_shin

    def draw_face(self, screen):

        rotated_face = rot_center(self.face, math.degrees(self.head_body.angle))
        screen.blit(rotated_face, (self.head_body.position[0] - 50, screen_height - self.head_body.position[1] - 50))

    def set_color(self, color, rest_color = (0, 0, 255)):

        self.shape.color = color
        self.head_shape.color = color
        self.left_thigh_shape.color = rest_color
        self.left_shin_shape.color = rest_color
        self.right_thigh_shape.color = rest_color
        self.right_shin_shape.color = rest_color

    def add_space(self, space):

        space.add(self.body, self.shape, self.head_body, self.head_shape, self.head_joint1, self.head_joint2)
        space.add(self.left_thigh_body, self.left_thigh_shape, self.left_thigh_joint, self.left_thigh_motor)
        space.add(self.left_shin_body, self.left_shin_shape, self.left_shin_joint, self.left_shin_motor)
        space.add(self.right_thigh_body, self.right_thigh_shape, self.right_thigh_joint, self.right_thigh_motor)
        space.add(self.right_shin_body, self.right_shin_shape, self.right_shin_joint, self.right_shin_motor)

def add_land(space):

    land_size = (screen_width -300, 20)
    shape = pymunk.Poly.create_box(None, land_size)
    shape.friction = 0.5
    shape.elasticity = 1.0
    moment = pymunk.moment_for_poly(1, shape.get_vertices())
    body = pymunk.Body(9999, moment, body_type = pymunk.Body.KINEMATIC)
    body.position = (screen_width / 2 + 300, 300)
    shape.body = body
    space.add(body, shape)

    return shape

def rot_center(image, angle):

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()

    return rot_image

def main():

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill([255, 255, 255])
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    land = add_land(space)
    ruler = 0
    nets = []
    humans = []
    ticks_to_next = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        ticks_to_next -= 1
        if ticks_to_next <= 0:
            ticks_to_next = 25
            human = Human()
            humans.append(human)

        space.step(1/50.0)
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(50)

main()
