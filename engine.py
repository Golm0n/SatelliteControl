import pygame
import math
import random

class SatelliteEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = pygame.Vector2(width // 2, height - 100)
        self.vel = pygame.Vector2(0, 0)
        self.asteroids = []
        self.distance = 0
        self.is_alive = True
        self.thrust_power = 0.4
        self.friction = 0.98
        self.lidar_range = 150
        self.sat_radius = 10
        self._spawn_asteroids(0, -2000)

    def _spawn_asteroids(self, bottom_y, top_y):
        for _ in range(15):
            self.asteroids.append({
                "pos": pygame.Vector2(random.uniform(50, self.width-50), random.uniform(top_y, bottom_y)),
                "radius": random.uniform(15, 45)
            })

    def get_lidar_data(self):
        distances = []
        angles = [-90, -45, 0, 45, 90, 135, 180, 225]
        for angle in angles:
            rad = math.radians(angle)
            dir_vec = pygame.Vector2(math.cos(rad), math.sin(rad))
            closest = self.lidar_range
            for ast in self.asteroids:
                to_ast = ast["pos"] - self.pos
                if to_ast.dot(dir_vec) > 0:
                    d = max(0, to_ast.length() - ast["radius"])
                    if d < closest: closest = d
            distances.append(round(closest, 2))
        return distances

    def update(self, thrust):
        if not self.is_alive: return
        accel = pygame.Vector2(thrust[0], -thrust[1]) * self.thrust_power
        self.vel += accel
        self.vel *= self.friction
        self.pos += self.vel
        self.distance = max(self.distance, int((self.height - 100) - self.pos.y))

        for ast in self.asteroids:
            if self.pos.distance_to(ast["pos"]) < ast["radius"] + self.sat_radius:
                self.is_alive = False
        
        if self.pos.x < 0 or self.pos.x > self.width or self.pos.y > self.height:
            self.is_alive = False

        highest_y = min(a["pos"].y for a in self.asteroids)
        if self.pos.y < highest_y + 600:
            self._spawn_asteroids(highest_y, highest_y - 1000)