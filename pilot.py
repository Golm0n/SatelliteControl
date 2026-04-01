class PilotAI:
    def __init__(self):
        self.name = "Default Pilot"

    def decide_thrust(self, velocity, lidar):
        """
        velocity: {'vx': float, 'vy': float}
        lidar: [N, NE, E, SE, S, SO, O, NO] (distances 0-150)
        Retourne: [poussée_x, poussée_y] entre -1.0 et 1.0
        """
        # Logique a Compléter : 
        # On va controler la poussée du satélite, on peut faire une poussée sur x -x y et -y
        # l'objectif est de coder une logique d'évitement d'obstacle, 
        # pour aller le plus haut possible, sans toucher aucun astéroides.
        # exemple : 

        ax = 0.0
        ay = 0.3 # On avance
        
        if lidar[0] < 80:
            ax = 1.0 if lidar[7] > lidar[1] else -1.0
            ay = -0.2
            
        return [ax, ay]