import random
import numpy

from pixel import Pixel

"""
Supposing a pixel is a tuple of (R,G,B) and each channel
is in the range of 0-255. The population will be conformed
by the neighborhood and random mutant pixels.
"""
POPULATION_SIZE = 25

R_INDEX = 0
G_INDEX = 1
B_INDEX = 2
IMAGE_CHANNELS = [R_INDEX, G_INDEX, B_INDEX]

MAX_CHANNEL_DEVIATION = 2

MIN_PIXEL_VALUE = 0
MAX_PIXEL_VALUE = 256
PIXEL_CHANNELS_NUM = 3

VALID_VALS_IN_CHANNELS = [i for i in range(MAX_PIXEL_VALUE)] # List of 1,2,3,...,255

MIN_DEVIATION_COEFFICIENT = 0
MAX_DEVIATION_COEFFICIENT = 0.5

LIST_OF_RESULTING_IMAGES = list()

class GAImageApplier:
    """
    This class will be in charged of applying the GA over all the image.
    Will iterate the image and determine if a pixel is noisy, if the
    pixel is noisy, then will apply the GA over it.

    Based on the neighborhood of the current pixel, this algorithm will
    iterate over a GA to stablish the best pixel that is going to fit in,
    to be replaced with the noisy pixel.
    """
    def __init__(self):
        self.image_obj = None # An instance of the ImageWrapper
        self.population = list() # List of instances of the class Pixel
        self.neighborhood_raw = None # Numpy array with the neighborhood of the Pixel
        self.resulting_images = list() # List of the resulting images of each pixel processed
        self.list_of_rows = list()

    # -- Setters & getters --
    def image_obj_set(self, image_obj):
        self.image_obj = image_obj
    def population_get(self):
        return self.population

    def resulting_images_get(self):
        return self.resulting_images

    def list_of_rows_get(self):
        return self.list_of_rows
    
    def population_set(self, population):
        """
        This function will set the new population, and the expected
        value is list of instances of the class Pixel.

        More than setting, this function converts the list of Pixel
        instances to a raw numpy array.

        :param population: list of Pixel instances to be set to the
        member population.
        """
        # Just setting the new population
        self.population = population

        self.neighborhood_raw = list()
        # Convert the population to raw neighborhood:
        for pixel in self.population:
            self.neighborhood_raw.append(numpy.array(pixel.get_chromosome()))
        
        self.neighborhood_raw = numpy.array(self.neighborhood_raw)
    # -- End of Setters & getters --

    def calculate_deviation_coeff(self, pixel, neighborhood):
        """
        The neighborhood is a list of pixels, accomodated in
        a numpy array as follows:

        [
            ...,
            [R0 G0 B0],
            [R1 G1 B1],
            [R2 G2 B2],
            ...
        ]

        To see if a pixel is noisy, a list of R's, G's and
        B's are going to be taken.
        
        The routine will compare how much the pixel is deviating
        from its neighborhood, and this is going to be calculated
        for each channel separately.

        To get the deviation coefficient, the following formula is
        needed:

        deviation_coeffiecient = (pixel_ch - mean_ch)/deviation_ch = Z (in statistics)

        If |Z| > 2 -> probable that is out of the average
        if |Z| > 3 -> highly probable that the value is a rare one.
        """
        # Since the neighborhood is numpy array, we can get columns at
        # once, with the following notation [:, col_index]. This means
        # that we want all the column in the certain x index.
        # Note: ngh stands for neighborhood, shorting it for readability
        nbh_r_channel = neighborhood[:, R_INDEX]
        nbh_g_channel = neighborhood[:, G_INDEX]
        nbh_b_channel = neighborhood[:, B_INDEX]

        # Getting the average per channel
        nbh_r_channel_mean = numpy.mean(nbh_r_channel)
        nbh_g_channel_mean = numpy.mean(nbh_g_channel)
        nbh_b_channel_mean = numpy.mean(nbh_b_channel)

        # Getting the standard deviation (std) per channel
        nbh_r_channel_std = numpy.std(nbh_r_channel)
        nbh_g_channel_std = numpy.std(nbh_g_channel)
        nbh_b_channel_std = numpy.std(nbh_b_channel)

        # Getting the deviation coeffiecient (dc) per channel
        nbh_r_channel_dc = (pixel[R_INDEX] - nbh_r_channel_mean)/nbh_r_channel_std
        nbh_g_channel_dc = (pixel[G_INDEX] - nbh_g_channel_mean)/nbh_g_channel_std
        nbh_b_channel_dc = (pixel[B_INDEX] - nbh_b_channel_mean)/nbh_b_channel_std

        return nbh_r_channel_dc, nbh_g_channel_dc, nbh_b_channel_dc


    def is_pixel_noisy(self, pixel, neighborhood):
        """
        This functions calculates the deviation coefficient based on
        a given neighborhood and the pixel to be analized.

        Based on this calculation, if the deviation of each channel
        is greater than MAX_CHANNEL_DEVIATIOn, then it will determine
        if the pixel being analized is noisy.

        :param pixel: the Pixel to be analized
        :param neighborhood: the beighborhood to compare the given pixel to.
        :return: True if the deviation of any of the 3 channels is greater
        than 2, false otherwise.
        :rtype: boolean
        """

        # Getting the deviation coefficient based on the pixel to be analized
        # and its given neighborhood
        nbh_r_channel_dc, nbh_g_channel_dc, nbh_b_channel_dc = self.calculate_deviation_coeff(pixel, neighborhood)
        
        # If one of all deviations is greater than 2, then the pixel is
        # considered as noisy. It means in further steps we need to appply
        # GA to clean the pixel.
        return abs(nbh_r_channel_dc) > MAX_CHANNEL_DEVIATION or\
            abs(nbh_g_channel_dc) > MAX_CHANNEL_DEVIATION or\
            abs(nbh_b_channel_dc) > MAX_CHANNEL_DEVIATION

    def create_population(self, neighborhood):
        """
        This function creates an initial population based on the
        neighborhood. The expected population size is contained
        in POPULATION_SIZE. If the neighborhood is lower than that
        constant, then adding mutant pixels.

        :param neighborhood: the neighborhood to start creating the
        population of the GA.
        """
        neighborhood_len = len(neighborhood)
        missing_individuals = POPULATION_SIZE - neighborhood_len

        if missing_individuals != 0:
            for mutant_index in range(missing_individuals):
                # Create a list of 3 vals in the range [0:256[
                mutant_pixel = random.sample(VALID_VALS_IN_CHANNELS, PIXEL_CHANNELS_NUM)
                numpy.append(neighborhood, numpy.array(mutant_pixel))
        self.neighborhood_raw = neighborhood

        pixel_objects = list()
        # Convert each pixel representing the RGB, to an object that
        # also stores the fitness score:
        for neighbor in neighborhood:
            pixel = Pixel()
            pixel.set_chromosome(neighbor)
            pixel_objects.append(pixel)
        
        self.population = pixel_objects

    def population_fitness_calculate(self):
        """
        This function iterates over the population (list of Pixel
        instances) and calculates the deviation coefficient per
        pixel. The sum of the deviations of each channel is the
        final fitness score.
        """
        for pixel in self.population:
            nbh_r_channel_dc, nbh_g_channel_dc, nbh_b_channel_dc = self.calculate_deviation_coeff(pixel.get_chromosome(), self.neighborhood_raw)
            pixel.set_fitness(nbh_r_channel_dc + nbh_g_channel_dc + nbh_b_channel_dc)


    def crossover_operation(self, pixel_parent_1, pixel_parent_2):
        """
        This function perform the crossover operation over a random choiced
        pixels from the first 50% of the pixels of the last generation.

        The idea is to iterate over the 3 channels of the new child pixel and
        decide based on a random choice if the child channel will be from the
        parent 1 or the parent 2.

        :param pixel_parent_1: pixel to do crossover to
        :param pixel_parent_2: pixel to do crossover to
        :return: child pixel after the crossover process between 2 parents
        :rtype: class Pixel
        """
        
        # Chromosome is a tuple of (R, G, B)
        temp_chromosome = list()
        list_parent_choice = [True, False]
        pixel = Pixel()
        for channel in IMAGE_CHANNELS:
            is_parent_1 = random.choice(list_parent_choice)
            if is_parent_1:
                temp_chromosome.append(pixel_parent_1.get_chromosome()[channel])
            else:
                temp_chromosome.append(pixel_parent_2.get_chromosome()[channel])
        pixel.set_chromosome(temp_chromosome)

        return pixel

    def start_ga_over_image(self):
        """
        This function iterates over the entire image, looking for noisy
        pixels and applying the GA over those.

        """
        # Getting the np formated image:
        image_to_process = self.image_obj.get_np_image_format()
        image_shape = self.image_obj.shape_get()
        image_height = image_shape[0]
        image_width = image_shape[1]
        image_channels = image_shape[2]
        
        print("------------------------------")
        print("Starting the Genetic Algorithm")


        image = 0
        # Accessing all pixels of the image:
        for j in range(image_height):
            for i in range(image_width):

                #if one_image >= image_width:
                #    return 0

                # Get the neighborhood of a given a pixel
                neighborhood = self.image_obj.neighborhood_get(j, i)

                # Check if the current pixel is noisy
                if (self.is_pixel_noisy(self.image_obj.pixel_get(j,i), neighborhood) == True):
                    
                    # Create an initial population, that consists on
                    # the neighborhood and some mutant pixels that will be added
                    # if the neighborhood is not 25 total:
                    self.create_population(neighborhood)


                    # Calculate the fitness of this population, we could already
                    # found the fittest pixel:
                    self.population_fitness_calculate()

                    # Sort the population based on the fitness score:
                    sorted_population = sorted(self.population_get(), key=lambda pixel:pixel.fitness)

                    # Setting the sorted population:
                    self.population_set(sorted_population)

                    # Start generations of the GA:

                    # Flag that is rised when a fittest pixel is found:
                    fittest_pixel_found = False

                    # Counter for generations:
                    generation = 1


                    while not fittest_pixel_found:

                        # Getting the first individual fitness, to see if it is
                        # on the required range of Z:
                        first_ind_fitness = self.population_get()[0].fitness

                        if MIN_DEVIATION_COEFFICIENT <= first_ind_fitness <= MAX_DEVIATION_COEFFICIENT:

                            # If we found the fittest pixel, then replace the noisy pixel
                            # with the fittest one:
                            self.image_obj.new_pixel_set(j, i, self.population_get()[0].get_chromosome())  

                            fittest_pixel_found = True


                            # Adding the image in numpy format to see the final result as an animated
                            # gif:
                            self.resulting_images.append(self.image_obj.get_np_image_format().copy())
                            
                            # Incrementing a counter that will tell in further stages, which is the last
                            # image for each row, that will be required to draw a green line indicating
                            # where the algorithm already passed
                            image += 1

                            # Break the loop for the current pixel, so we can continue with the
                            # following:
                            break
                        
                        # If the fittest pixel is not found yet, lets continue with the GA,
                        # creating a new generation:

                        # Bypass the first 20% of the last population to the new population
                        new_population = self.population_get()[0:int(POPULATION_SIZE*0.20)]

                        # Perform some crossover operation over the first 50% of the
                        # individuals of the last generation, to complete the 70%
                        # of the next generation:
                        for pixel_count in range(int(POPULATION_SIZE*0.75)):
                            pixel_parent_1 = random.choice(self.population_get()[0:int(POPULATION_SIZE*0.50)])
                            pixel_parent_2 = random.choice(self.population_get()[0:int(POPULATION_SIZE*0.50)])

                            # Crossover parent 1 with parent 2:
                            child_pixel = self.crossover_operation(pixel_parent_1, pixel_parent_2)
                            new_population.append(child_pixel)

                        # Complete the last 10% of the next generation by introducing some
                        # mutant pixels:
                        for pixel_count in range(int(POPULATION_SIZE*0.05)):
                            # Get random R G B values and converting this as the new
                            # mutant pixel:
                            mutant_chromosome = random.sample(VALID_VALS_IN_CHANNELS, PIXEL_CHANNELS_NUM)
                            mutant_pixel = Pixel()
                            mutant_pixel.set_chromosome(tuple(mutant_chromosome))
                            new_population.append(mutant_pixel)

                        # Now we have the Full next generation to work with:
                        self.population_set(new_population)
                        
                        # Calculate the fitness of each pixel of the recently created population:
                        self.population_fitness_calculate()

                        # Sort the population again based on the fitness
                        sorted_new_population = sorted(new_population, key=lambda pixel:pixel.fitness)
                        
                        # Finally, set the sorted population to be bypassed to the next generation:
                        self.population_set(sorted_new_population)

                        generation += 1
            # Once the row has been completed, store the index of the last
            # image of the last row:
            self.list_of_rows.append(image)     
        print("Finished the Genetic Algorithm")
        print("------------------------------")
        

