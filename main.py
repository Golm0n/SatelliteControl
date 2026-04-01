import pygame
from engine import SatelliteEngine
from display import Visualizer
from pilot import PilotAI

def run_challenge():
    # Configuration
    WIDTH, HEIGHT = 600, 800
    
    # Initialisation
    engine = SatelliteEngine(WIDTH, HEIGHT)
    view = Visualizer(WIDTH, HEIGHT)
    ai = PilotAI()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_l: # Toggle du LIDAR avec la touche 'L'
                    view.show_lidar_rays = not view.show_lidar_rays

                if event.key == pygame.K_r: # RESTART avec la touche 'R'
                    engine = SatelliteEngine(WIDTH, HEIGHT)

        # Logique de vol
        if engine.is_alive:
            lidar = engine.get_lidar_data()
            velocity = {"vx": engine.vel.x, "vy": -engine.vel.y}
            
            # Appel du pilote
            thrust = ai.decide_thrust(velocity, lidar)
            engine.update(thrust)

        view.draw(engine)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_challenge()