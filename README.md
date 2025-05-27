# Genetic-Algorithm-Image-Denoiser

The idea of this investigation is to apply a Genetic Algorithm (GA) to an image, in order to denoise it from digital noise.

This GA is agnostic to any mathematical operation such as __Convolution__ or Processing Images term such as __Kernel__. In anyway, this topic will be covered as a comparision in performance between Genetic Algorithms and the Processing Images approach.

This article will address the following topics:
- The problem of denoising an image.
- Specifics of Genetic Algorithms applied to Image Denoise.
- Implementation.
- Results.

## Image Denoising Problem

There are some theoretical approaches to manipulate images. One of them is related to apply mathematical operations over images, this is known as Image Processing. For sharpening, denoising, introducing noise and analize images, there are a concepts called __kernel__, __convolution__, and statistical concepts such as __mean__, __standard deviation__ and other terms that are required to be able to successfully analize images.

Since some of these operations are related to matrix operations, this always has to do with performance and resources usage.

Regarding the __denoise__ problem, for each sort of noise, there is an algorithm to address its denoise routine. So, the person interested in denoising images should study each problem to be able to apply the corresponding algorithm.

Some of the types of noise are the following:

- Chroma noise:

![image info](./images/lena_chroma_noised.png)

- Gaussian Noise:

![image info](./images/lena_gaussian_noised.png)

- Periodic Noise:

![image info](./images/lena_periodic_noise.png)

- Salt & Pepper Noise:

![image info](./images/lena_salt_pepper_noised.png)

The idea of denoising these images, is to get rid of the pixels that makes the image not fully clear.

## Genetic Algorithm concepts applied to Image Denoising Problem
## Implementation
## Results
![image info](./images/result.gif)
![image info](./images/lena.jpg)