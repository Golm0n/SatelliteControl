import pygame
import math
import os

class Visualizer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Consolas", 20)
        self.width = width
        self.height = height
        
        # Configuration
        self.show_lidar_rays = True
        
        # Chargement des images
        img_dir = os.path.join(os.path.dirname(__file__), 'img')
        
        self.bg_img = pygame.image.load(os.path.join(img_dir, 'background.jpg')).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))
        
        self.sat_img = pygame.image.load(os.path.join(img_dir, 'satellite.png')).convert_alpha()
        self.sat_img = pygame.transform.scale(self.sat_img, (40, 40)) # Ajuste la taille ici
        
        self.ast_img = pygame.image.load(os.path.join(img_dir, 'asteroid.png')).convert_alpha()

        self.fuel_img = pygame.image.load(os.path.join(img_dir, 'fuel.jpg')).convert_alpha()
        self.fuel_img = pygame.transform.scale(self.fuel_img, (30, 30))


    def draw(self, engine):
        self.screen.blit(self.bg_img, (0, 0))
        offset_y = -engine.pos.y + self.height * 0.75

        for ast in engine.asteroids:
            draw_pos = (int(ast["pos"].x), int(ast["pos"].y + offset_y))
            if -200 < draw_pos[1] < self.height + 200:
                # On redimensionne l'image selon son rayon réel dans le moteur
                scaled_ast = pygame.transform.scale(self.ast_img, (int(ast["radius"]*2), int(ast["radius"]*2)))
                rect = scaled_ast.get_rect(center=draw_pos) # On centre l'image redimensionné
                self.screen.blit(scaled_ast, rect)

        for item in engine.fuel_items:
            draw_pos = (int(item["pos"].x), int(item["pos"].y + offset_y))
            if -50 < draw_pos[1] < self.height + 50:
                rect = self.fuel_img.get_rect(center=draw_pos)
                self.screen.blit(self.fuel_img, rect)
                
        if self.show_lidar_rays and engine.is_alive:
            lidar_data = engine.get_lidar_data()
            angles = [-90, -45, 0, 45, 90, 135, 180, 225]
            for i, dist in enumerate(lidar_data):
                rad = math.radians(angles[i])
                end_x = engine.pos.x + math.cos(rad) * dist
                end_y = engine.pos.y + math.sin(rad) * dist + offset_y
                pygame.draw.line(self.screen, (0, 255, 0), (engine.pos.x, engine.pos.y + offset_y), (end_x, end_y), 1)

        sat_rect = self.sat_img.get_rect(center=(int(engine.pos.x), int(engine.pos.y + offset_y)))
        tilt_angle = -engine.vel.x * 2 # inclinaison lors des virages
        rotated_sat = pygame.transform.rotate(self.sat_img, tilt_angle)
        new_rect = rotated_sat.get_rect(center=sat_rect.center)
        

        pygame.draw.rect(self.screen, (50, 50, 50), (self.width - 120, 20, 100, 20)) # Fond gris
        fuel_color = (0, 255, 0) if engine.fuel > 30 else (255, 0, 0)
        pygame.draw.rect(self.screen, fuel_color, (self.width - 120, 20, int(engine.fuel), 20)) # Jauge
        fuel_txt = self.font.render(f"FUEL", True, (255, 255, 255))
        self.screen.blit(fuel_txt, (self.width - 170, 20))


        if not engine.is_alive:
            pygame.draw.circle(self.screen, (255, 0, 0), sat_rect.center, 20, 2)
            
        self.screen.blit(rotated_sat, new_rect)

        dist_txt = self.font.render(f"DISTANCE: {engine.distance}m", True, (255, 255, 255))
        self.screen.blit(dist_txt, (20, 20))
        
        pygame.display.flip()