from pixel import Pixel
from ga_image_applier import GAImageApplier
from image_wrapper import ImageWrapper
import time

def denoise_image():
    
    print("Welcome to Genetic Algorithm Denoiser")
    print("Please Choose Among the following noised Lenas:")
    user_input = input("1 - Chroma Noise, 2 - Gaussian Noise, 3 - Periodic Noise, 4 - Salt & Pepper Noise\n")

    try:
        user_input = int(user_input)
    except ValueError:
        print("Please provide an integer between the range showed before.")
        return -1
    
    if not (1 <= user_input <= 4):
        print("Please provide an integer between the range showed before.")
        return -1

    switcher = {
        1: "./lena_chroma_noised.png",
        2: "./lena_gaussian_noised.png",
        3: "./lena_periodic_noise.png",
        4: "./lena_salt_pepper_noised.png"
    }

    TARGET_IMAGE_PATH = switcher.get(user_input)

    # Create the image wrapper to apply operations
    # over the image that will be processed:
    image = ImageWrapper(TARGET_IMAGE_PATH)

    # Loading the image in RAM, and also converting the
    # image to Numpy Array:
    image.image_opener()

    image.set_result_image_name("./test.png")

    # Create the instance of the object in charged of
    # applying the Genetic Algorithm over the image:
    ga_applier = GAImageApplier()

    # Passing the image that will be processed to the
    # Genetic Algorithm applier:
    ga_applier.image_obj_set(image)
    
    start_time = time.time()
    ga_applier.start_ga_over_image()
    end_time = time.time()
    print("The GA took: ", end_time - start_time)

    list_of_resulting_images = ga_applier.resulting_images_get()
    list_of_rows = ga_applier.list_of_rows_get()

    image.create_gif_from_images(list_of_resulting_images, list_of_rows)

    image.save()

    image2 = ImageWrapper(TARGET_IMAGE_PATH)
    image2.image_opener()
    image2.set_result_image_name("./test2.png")
    start_time = time.time()
    image2.denoise_salt_pepper_deterministically()
    end_time = time.time()
    print("The math algorithm took: ", end_time - start_time)
    image2.save()
denoise_image()
