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
        self.fuel_items = []
        self.fuel = 100.0     
        self.distance = 0
        self.is_alive = True
        self.thrust_power = 0.4
        self.friction = 0.98
        self.lidar_range = 150
        self.sat_radius = 10
        self._spawn_elements(0, -2000)

    def _spawn_elements(self, bottom_y, top_y):
        # Génération des astéroides et des items de fuel
        for _ in range(15):
            self.asteroids.append({
                "pos": pygame.Vector2(random.uniform(50, self.width-50), random.uniform(top_y, bottom_y)),
                "radius": random.uniform(15, 45)
            })
        for _ in range(2):
            self.fuel_items.append({
                "pos": pygame.Vector2(random.uniform(50, self.width-50), random.uniform(top_y, bottom_y)),
                "value": 30.0 
            })

    def get_fuel_radar(self):
        if not self.fuel_items: return None
        # Trouve le fuel le plus proche et renvoie la distance relative x et y
        closest = min(self.fuel_items, key=lambda x: self.pos.distance_to(x["pos"]))
        relative = closest["pos"] - self.pos
        return {"dx": round(relative.x, 2), "dy": round(relative.y, 2)}
    
    def get_lidar_data(self):
        distances = []
        # Angles pour N, NE, E, SE, S, SO, O, NO
        angles = [-90, -45, 0, 45, 90, 135, 180, 225]
        for angle in angles:
            rad = math.radians(angle)
            dir_vec = pygame.Vector2(math.cos(rad), math.sin(rad))
            closest = self.lidar_range

            # Gestion des murs
            if dir_vec.x > 0: 
                dist_wall = (self.width - self.pos.x) / dir_vec.x
                closest = min(closest, dist_wall)
            elif dir_vec.x < 0: 
                dist_wall = (0 - self.pos.x) / dir_vec.x
                closest = min(closest, dist_wall)
                
            # Gestion des astéroïdes
            for ast in self.asteroids:
                to_ast = ast["pos"] - self.pos
                projection = to_ast.dot(dir_vec)
                
                if projection > 0:
                    dist_to_line = math.sqrt(max(0, to_ast.length_squared() - projection**2))
                    
                    if dist_to_line < ast["radius"]:
                        collision_dist = projection - math.sqrt(ast["radius"]**2 - dist_to_line**2)
                        if 0 < collision_dist < closest:
                            closest = collision_dist
                            
            distances.append(round(closest, 2))
        return distances

    def update(self, thrust):
        if not self.is_alive: return

        thrust_intensity = math.sqrt(thrust[0]**2 + thrust[1]**2)
        fuel_cost = thrust_intensity * 0.15 
        
        if self.fuel > 0:
            self.fuel -= fuel_cost
            accel = pygame.Vector2(thrust[0], -thrust[1]) * self.thrust_power
            self.vel += accel
        else:
            self.fuel = 0 

        self.vel *= self.friction
        self.pos += self.vel
        
        dist_curr = int((self.height - 100) - self.pos.y)
        self.distance = max(self.distance, dist_curr)

        for ast in self.asteroids:
            if self.pos.distance_to(ast["pos"]) < ast["radius"] + self.sat_radius:
                self.is_alive = False

        for item in self.fuel_items[:]: 
            if self.pos.distance_to(item["pos"]) < 25:
                self.fuel = min(100.0, self.fuel + item["value"])
                self.fuel_items.remove(item)
        
        if self.pos.x < 0 or self.pos.x > self.width or self.pos.y > self.height + 200:
            self.is_alive = False

        highest_y = min(a["pos"].y for a in self.asteroids)
        if self.pos.y < highest_y + 800:
            self._spawn_elements(highest_y, highest_y - 1200)