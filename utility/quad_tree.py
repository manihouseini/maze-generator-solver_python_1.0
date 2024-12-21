import pygame
import math, random


class Moving_point:
    def __init__(self, x, y, content, width=0, height=0) -> None:
        self.x = x
        self.y = y
        self.speedX = random.random() * 4 - 2
        self.speedY = random.random() * 4 - 2
        self.content = content
        self.width = width
        self.height = height

    def show(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), 3)

    def distance_to(self, point):
        return math.sqrt(((point.x - self.x) ** 2) + ((point.y - self.y) ** 2))

    def update(self):
        self.x += self.speedX
        self.y += self.speedY
        if self.x < 0:
            self.x = self.width
        if self.x > self.width:
            self.x = 0

        if self.y < 0:
            self.y = self.height
        if self.y > self.height:
            self.y = 0


class Point:
    def __init__(self, x, y, content) -> None:
        self.x = x
        self.y = y
        self.content = content

    def show(self, win, color):
        pygame.draw.circle(win, color, (self.x, self.y), 3)

    def distance_to(self, point):
        return math.sqrt(((point.x - self.x) ** 2) + ((point.y - self.y) ** 2))


class Rect:
    def __init__(self, x, y, w, h) -> None:
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.north_wall = y
        self.west_wall = x
        self.east_wall = x + w
        self.south_wall = y + h

    def show(self, win):
        pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.w, self.h), 1)

    def intersects(self, rec):
        return not (
            rec.west_wall >= self.east_wall
            or rec.east_wall <= self.west_wall
            or rec.north_wall >= self.south_wall
            or rec.south_wall <= self.north_wall
        )

    def contains(self, point):
        return (
            point.x >= self.west_wall
            and point.x <= self.east_wall
            and point.y >= self.north_wall
            and point.y <= self.south_wall
        )


class Quad_tree:
    def __init__(self, x, y, w, h, copacity) -> None:
        self.boundry = Rect(x, y, w, h)
        self.copacity = copacity
        self.points = []
        self.devided = False

    def show(self, win):
        top = (self.boundry.x + self.boundry.w // 2, self.boundry.y)
        bottom = (self.boundry.x + self.boundry.w // 2, self.boundry.y + self.boundry.h)
        left = (self.boundry.x, self.boundry.y + self.boundry.h // 2)
        right = (self.boundry.x + self.boundry.w, self.boundry.y + self.boundry.h // 2)
        pygame.draw.line(win, (255, 255, 255), top, bottom, 1)
        pygame.draw.line(win, (255, 255, 255), left, right, 1)
        if self.devided:
            self.north_west.show(win)
            self.north_east.show(win)
            self.south_west.show(win)
            self.south_east.show(win)

    def devide(self):
        x = self.boundry.x
        y = self.boundry.y
        w = self.boundry.w / 2
        h = self.boundry.h / 2

        self.north_west = Quad_tree(x, y, w, h, self.copacity)
        self.north_east = Quad_tree(x + w, y, w, h, self.copacity)
        self.south_west = Quad_tree(x, y + h, w, h, self.copacity)
        self.south_east = Quad_tree(x + w, y + h, w, h, self.copacity)

    def insert(self, point):
        if not self.boundry.contains(point):
            return False
        if len(self.points) <= self.copacity:
            self.points.append(point)
            return True
        if not self.devided:
            self.devide()
            self.devided = True

        return (
            self.north_west.insert(point)
            or self.north_east.insert(point)
            or self.south_west.insert(point)
            or self.south_east.insert(point)
        )

    def circle_query_setup(self, x, y, r):
        ls = []
        rec = Rect(x - r, y - r, r * 2, r * 2)
        point = Point(x, y, 10)
        return self.circle_query(point, r, rec, ls)

    def circle_query(self, point, r, rec, ls=[]):
        if not self.boundry.intersects(rec):
            return ls

        for p in self.points:
            if p.distance_to(point) <= r:
                ls.append(p)

        if not self.devided:
            return ls

        self.north_west.circle_query(point, r, rec, ls)
        self.north_east.circle_query(point, r, rec, ls)
        self.south_west.circle_query(point, r, rec, ls)
        self.south_east.circle_query(point, r, rec, ls)

        return ls

    def rect_query_setup(self, x, y, w, h):
        rec = Rect(x, y, w, h)
        return self.rect_query(rec, [])

    def rect_query(self, rec, ls):
        # found = ls
        if not self.boundry.intersects(rec):
            return ls

        for p in self.points:
            if rec.contains(p):
                ls.append(p)

        if not self.devided:
            return ls

        self.north_west.rect_query(rec, ls)
        self.north_east.rect_query(rec, ls)
        self.south_west.rect_query(rec, ls)
        self.south_east.rect_query(rec, ls)

        return ls

    def clear(self):
        self.points.clear()

        if self.devided:
            self.north_west = 0
            self.north_east = 0
            self.south_west = 0
            self.south_east = 0

        self.devided = False
