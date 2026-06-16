#!/bin/python3
import cv2
import random

class BouncingBox:
    def __init__(self, box_width, box_height, dx=5, dy=5):
        self.x = random.randint(2, 100)
        self.y = random.randint(2, 100)
        self.box_width = box_width
        self.box_height = box_height
        self.dx = dx
        self.dy = dy

    def update(self, frame_width, frame_height):
        # Move box
        self.x += self.dx
        self.y += self.dy

        # Bounce off left/right walls
        if self.x <= 0:
            self.x = 0
            self.dx = random.randint(4, 10)

        elif self.x + self.box_width >= frame_width:
            self.x = frame_width - self.box_width
            self.dx = -random.randint(4, 10)

        # Bounce off top/bottom walls
        if self.y <= 0:
            self.y = 0
            self.dy = random.randint(4, 10)

        elif self.y + self.box_height >= frame_height:
            self.y = frame_height - self.box_height
            self.dy = -random.randint(4, 20)

    def draw(self, frame):
        cv2.rectangle(
            frame,
            (int(self.x), int(self.y)),
            (int(self.x + self.box_width), int(self.y + self.box_height)),
            (0, 255, 255),
            -1
        )
        
    def __str__(self):
        return f"self.x = {self.x}; self.y = {self.y}; self.dy = {self.dy}; self.dx = {self.dx}"