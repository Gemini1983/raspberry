class Valve():
    # Elettrovalvole da gestire
    
    def __init__(self, id, nome,tasks,stato):
        # ogni elettrovalvola ha dei parametri  
        self.id = x
        self.nome = y
        self.tasks = tasks
        self.stato = stato
        
    def move_rocket(self, x_increment=0, y_increment=1):
        # Move the rocket according to the paremeters given.
        #  Default behavior is to move the rocket up one unit.
        self.x += x_increment
        self.y += y_increment
        
    def get_distance(self, other_rocket):
        # Calculates the distance from this rocket to another rocket,
        #  and returns that value.
        distance = sqrt((self.x-other_rocket.x)**2+(self.y-other_rocket.y)**2)
        return distance