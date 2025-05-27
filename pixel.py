class Pixel:
    """
    This class is intended to handle a single Pixel with its
    chromosome (R G B), and its fitness score
    """
    def __init__(self):
        self.chromosome = tuple() # Tuple storing the RGB channels
        self.fitness = int() # Fitness score
    
    # -- Setters & and getters --
    def set_chromosome(self, chromosome):
        self.chromosome = chromosome
    def get_chromosome(self):
        return self.chromosome
    def set_fitness(self, fitness):
        self.fitness = abs(fitness)
    def get_fitness(self):
        return self.fitness
    # -- End of Setters & getters --