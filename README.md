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

This section will talk about the concepts of Genetic Algorithms and how they are interpreted in this specific implementation.

1. Individual

For this case, and individual is a pixel already identified as noisy. The way it is determined is by calculating the __Deviation Coefficient__ (__Z__ in statistics terms). How much the pixel is away from the mean? That is the question the algorithm wants to answer before applying the GA over it. Basically, if __|Z| > 2__, then the pixel is considered as noisy.

Refreshing on how the __Deviation Coefficient__ is calculated, and how it is calculated for a RGB pixel:


Assuming we have a Population of pixels __x__:

$$
population = \{x_1, x_2, x_3, ..., x_n\}
$$

First step is to get the mean from the population:
$$
mean = \mu = \frac{\sum_{i=0}^n x_i}{n}
$$

Then, the __Standard Deviation__:

$$
\sigma = \sqrt{\frac{\sum_{i=0}^n \left(x_i - \mu\right)^2}{n}}
$$

Finally, to calculate the __Deviation Coefficient__ of the pixel $x_i$:

$$
Z = \frac{x_i - mean}{\sigma} 
$$

Then, a pixel is noisy if $|Z\left(x_i\right)| > 2$.

2. Gene
3. Selection
4. Crossover operator
5. Mutation operator
6. 

## Implementation
```

```
## Results
![image info](./images/result.gif)
![image info](./images/lena.jpg)