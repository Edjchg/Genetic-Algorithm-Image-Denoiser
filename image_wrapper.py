from PIL import Image, ImageDraw, ImageFont
import numpy

NEIGHBORHOOD_START_POSITION_SUBSTRACTOR = 2
NEIGHBORHOOD_HEIGHT_WIDTH = 5

R_INDEX = 0
G_INDEX = 1
B_INDEX = 2

class ImageWrapper:
    """
    This Image Wrapper covers some operations over an Image,
    such as open it, save it, get the neighborhood of
    a pixel, convert the PIL image to Numpy array,
    insert salt and peper noise to an Image if required.

    :param image_path: the string to the path of the image to
    work with
    """
    def __init__(self, image_path):
        if image_path is None or\
            not isinstance(image_path, str):
            print("Error creating the ImageWrapper")
            return -1

        self.image_path = image_path
        self.format = None
        self.shape = None # (shape tuple: height, width, channels)
        self.pil_image_format = None
        self.np_image_format = None
        self.neighborhood_start_position_substractor = 2
        self.neighborhood_height_width = 5
        self.result_image_name = str()

    # -- Setters & getters --
    def get_np_image_format(self): 
        return self.np_image_format
    def shape_get(self):
        return self.shape
    def new_pixel_set(self, pixel_y, pixel_x, rgb_value):
        self.np_image_format[pixel_y][pixel_x] = rgb_value
    def pixel_get(self, pixel_y, pixel_x):
        return self.np_image_format[pixel_y][pixel_x]
    def set_result_image_name(self, name):
        self.result_image_name = name
    # -- End of Setters & getters --

    def image_opener(self):
        """
        Loading the image in RAM and extract some details, like
        the format, shape, and convert the PIL image to Numpy
        array.
        """

        # Opening the image from the given path
        self.pil_image_format = Image.open(self.image_path)

        # Converting the image to numpy format
        self.np_image_format = numpy.array(self.pil_image_format)

        self.format = self.pil_image_format.format
        
        self.shape = self.np_image_format.shape

    
    def introduce_salt_peper_noise(self):
        """
        If the image has no noise, then introduce it
        """

        # Introduce 10% of noise:
        noise_pixels_num = int(self.shape[0] * self.shape[1] * 0.10)

        for noise_pixel in range(noise_pixels_num):
            new_noise_pixel_x = random.randint(0, self.shape[1] - 1)
            new_noise_pixel_y = random.randint(0, self.shape[0] - 1)

            new_pixel_color = random.randint(0, 1)

            self.np_image_format[new_noise_pixel_y][new_noise_pixel_x] = numpy.array([new_pixel_color*255, new_pixel_color*255, new_pixel_color*255])

    def introduce_chroma_noise(self):

        # Introduce 10% of noise:
        noise_pixels_num = int(self.shape[0] * self.shape[1] * 0.10)

        for noise_pixel in range(noise_pixels_num):
            new_noise_pixel_x = random.randint(0, self.shape[1] - 1)
            new_noise_pixel_y = random.randint(0, self.shape[0] - 1)

            noisy_pixel = random.sample(VALID_VALS_IN_CHANNELS, PIXEL_CHANNELS_NUM)

            self.np_image_format[new_noise_pixel_y][new_noise_pixel_x] = numpy.array(noisy_pixel)


    def introduce_periodic_noise(self):
        # Introduce 10% of noise:
        image_height = self.shape[0]
        image_width = self.shape[1]

        # Accessing all pixels of the image:
        for j in range(image_height):
            for i in range(image_width):
                current_pixel = self.pixel_get(j, i)
                noise_to_introduce = int(20*numpy.sin(10*j))

                if current_pixel[0] + noise_to_introduce > 255:
                   current_pixel[0] = 255
                else:
                    current_pixel[0] = current_pixel[0] + noise_to_introduce

                if current_pixel[1] + noise_to_introduce > 255:
                   current_pixel[1] = 255
                else:
                    current_pixel[1] = current_pixel[1] + noise_to_introduce

                if current_pixel[2] + noise_to_introduce > 255:
                   current_pixel[2] = 255
                else:
                    current_pixel[2] = current_pixel[2] + noise_to_introduce

    def introduce_gaussian_noise(self):
        """
        mean is set to 127.5, the midpoint of the 0-255 range, to center the distribution.
        std_dev is set to 50, a value that ensures most values will fall within the 0-255 range, but you can adjust it as needed.
        np.clip ensures that no values are less than 0 or greater than 255.
        .astype(np.uint8) converts the array to unsigned 8-bit integers, a common format for image data.
        """
        mean = 0
        std_dev = 50
        gaussian = numpy.random.normal(mean, std_dev, (self.shape[0], self.shape[1], self.shape[2]))
        clipped_values = numpy.clip(gaussian, 0, 255)
        uint8_values = clipped_values.astype(numpy.uint8)
        self.np_image_format = self.np_image_format + uint8_values

    def neighborhood_get(self, pixel_y, pixel_x):
        """
        The neighborhood of the pixel is a matrix represented
        as follows:

            0 0 0 0 0
            0 0 0 0 0
            0 0 x 0 0
            0 0 0 0 0
            0 0 0 0 0
        
        The x represents the pixel being processed.
        The 0 represents a neighbor of that pixel

        This function will take care of the edge pixels, and
        get the proper neighborhood.

        :param pixel_y: y position of the pixel being processed
        :param pixel_x: x position of the pixel being processed

        :return: a list corresponding to the pixel's neighborhood
        :rtype: list
        """
        
        # Calculating the start positions of the pixel neighborhood
        temp_start_x_pos = pixel_x - self.neighborhood_start_position_substractor
        temp_start_y_pos = pixel_y - self.neighborhood_start_position_substractor

        # If the process is accesing edge pixels, the start positions
        # might be negative, so those pixels are out of range (in python
        # there is the posibility to access negative indexes, but here
        # is something we want to avoid)
        start_x_pos = temp_start_x_pos if temp_start_x_pos >= 0 else 0 
        start_y_pos = temp_start_y_pos if temp_start_y_pos >= 0 else 0

        # Calculating the end positions of the neighborhood. We are not
        # taking into consideration if the ending indexes are out of the
        # of the range, because there is a try/except catching if the
        # process is in that scenary
        finish_x_pos = temp_start_x_pos + self.neighborhood_height_width
        finish_y_pos = temp_start_y_pos + self.neighborhood_height_width

        neighborhood_list = list()

        for j in range(start_y_pos, finish_y_pos):
            for i in range(start_x_pos, finish_x_pos):
                
                # Catch the case where the routine is accesing pixels
                # out of the range
                try:
                    neighborhood_list.append(self.np_image_format[j][i])
                except IndexError:
                    # If out of index, then continue with the next position
                    continue
                
        return numpy.array(neighborhood_list)

    def create_gif_from_images(self, list_of_np_images, list_of_rows):

        list_np_images_to_pil_form = [Image.fromarray(image) for image in list_of_np_images]

        len_of_np_images = len(list_np_images_to_pil_form)

        index = 0
        move_y_line = 0

        for image in list_np_images_to_pil_form:
            draw = ImageDraw.Draw(image)

            # Iterating over the stored images, in list_of_rows are all the
            # indexes of each last images per row. Once this routine reachs
            # the index stored in list_of_rows, means the line should mive
            # one step above:
            if index == list_of_rows[0]:
                list_of_rows = list_of_rows[1:]
                move_y_line += 1
            
            # Drawing the image over the Image:
            draw.line([(0, move_y_line), (int(self.shape[1]), move_y_line)], fill="green")
            index += 1

        list_np_images_to_pil_form[0].save("./result.gif",
                                           save_all=True,
                                           append_images=list_np_images_to_pil_form[1:],
                                           duration=15,
                                           loop=0)

    def denoise_salt_pepper_deterministically(self):
        image_height = self.shape[0]
        image_width = self.shape[1]

        self.neighborhood_height_width = 3
        self.neighborhood_start_position_substractor = 1

        # Accessing all pixels of the image:
        for j in range(image_height):
            for i in range(image_width):
                neighborhood = self.neighborhood_get(j, i)
                nbh_r_channel = neighborhood[:, R_INDEX]
                nbh_g_channel = neighborhood[:, G_INDEX]
                nbh_b_channel = neighborhood[:, B_INDEX]

                # Getting the average per channel
                nbh_r_channel_mean = numpy.mean(nbh_r_channel)
                nbh_g_channel_mean = numpy.mean(nbh_g_channel)
                nbh_b_channel_mean = numpy.mean(nbh_b_channel)

                
                self.new_pixel_set(j, i, numpy.array([nbh_r_channel_mean, nbh_g_channel_mean, nbh_b_channel_mean]))


    def show(self):
        # Convert image from Numpy to PIL image:
        self.pil_image_format = Image.fromarray(self.np_image_format)
        self.pil_image_format.show()

    def save(self):
        self.pil_image_format = Image.fromarray(self.np_image_format)
        self.pil_image_format.save(self.result_image_name)