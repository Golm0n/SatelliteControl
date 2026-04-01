class PilotAI:
    def __init__(self):
        self.name = "Default Pilot"

    def decide_thrust(self, velocity, lidar, fuel):
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
        ay = 0.4 # On pousse vers le haut
        
        # Logique d'esquive basique
        if lidar[0] < 100: # Si obstacle devant
            # On tourne vers le côté où il y a le plus d'espace
            ax = 0.8 if lidar[7] > lidar[1] else -0.8
            ay = -0.2 # On freine pour mieux tourner
            
        # Exemple d'utilisation du fuel : 
        # Si on est en galère de fuel, on arrête de pousser vers le haut
        if fuel < 10:
            ay = 0.0 
            
        return [ax, ay]