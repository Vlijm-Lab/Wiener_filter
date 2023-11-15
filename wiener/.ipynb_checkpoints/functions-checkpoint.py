from wiener.images import display_wiener, read_raw_tif, choose_layer, background_subtract, tif_save, create_folder, settings_save
import os
import scipy
import numpy as np
from numpy.fft import fftshift, fft2, ifft2


def gaussian_2d(x, y, sigma):
    '''
    Calculates a 2D Gaussian value.

        Parameters:
            x (float): value for x-dimension.
            y (float): value for y-dimension.
            sigma (float): sigma value corresponding the desired Gaussian.

        Returns:
            gaussian (float): 2D Gaussian value corresponding to given parameters.
    '''

    gaussian = np.exp(-(x**2/(2*sigma**2) + y**2/(2*sigma**2)))

    return gaussian


def gaussian_psf(shape, sigma, normalized=True):
    '''
    Creates a Guassian Point-Spread-Function.

        Parameters:
            shape (tuple): x,y dimension of the desired kernel.
            sigma (float): sigma value corresponding to the desired Gaussian.
            normalize (bool): normalized the kernel if equal to 'True'.

        Returns:
            gaussian (float): Gaussian Point-Spread-Function created with input parameters.
    '''

    x_half = shape[0]/2
    y_half = shape[1]/2

    x, y = np.mgrid[-x_half:x_half, -y_half:y_half]

    gaussian = gaussian_2d(x, y, sigma)
    if normalized:
        gaussian /= gaussian.sum()

    return gaussian


def wiener_deconvolution(img, pixel_size, sigma_confocal, sigma_sted, nsr, ratio):
    '''
    Wiener deconvolution applied to input image using two Point-Spread-Functions.

        Parameters:
            img (np.ndarray): gray-scale image to be deconvolved.
            pixel_size (float): the pixel size in the image, assuiming square pixels.
            sigma_confocal (float): sigma for the large Point-Spread-Function (Confocal).
            sigma_sted (float): sigma for the small Point-Spread-Function (STED).
            nsr (float): Noise-to-Signal ratio.
            ratio (float): ratio of intensity caused by large PSF compared to small PSF.

        Returns:
            deconv_img (np.ndarray): gray-scale wiener deconvolved image.
    '''

    FWHM = 2.35482 * pixel_size
    shape = img.shape

    sigma_confocal_pixels = sigma_confocal / FWHM
    sigma_sted_pixels = sigma_sted / FWHM

    psf_confocal = gaussian_psf(shape, sigma_confocal_pixels)
    psf_sted = gaussian_psf(shape, sigma_sted_pixels)

    psf = ratio * psf_sted + (1-ratio) * psf_confocal

    deconv_img = np.copy(img)

    kernel = fftshift(psf)

    deconv_img = fft2(deconv_img)
    kernel = fft2(kernel)

    kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + nsr)

    deconv_img = deconv_img * kernel
    deconv_img = np.abs(ifft2(deconv_img))
    deconv_img = np.float32(deconv_img)

    return deconv_img


def wiener_apply(foldername, store_folder, filename, cmap, pixel_size, background_subtraction, ratio, nsr, sigma_confocal, sigma_sted, layer, save_image):
    '''
    Applies wiener filter to given .tif file with corresponding parameters.

            Parameters:
                    folder name (string): folder consisting the raw data, which is within the 'data' folder.
                    store_name (string): folder to store the filtered data, which is within the 'data' folder.
                    filename (string): filename of the image, which is present in the folder with the name 'foldername'.
                    cmap (string): name of colormap used for displaying images.
                    pixel_size (float): the pixel size in the image, assuming square pixels.
                    background_subtraction (int): subtract background value from the input image, equal to 0 if no subtraction.
                    ratio (float): ratio of intensity caused by large PSF compared to small PSF.
                    nsr (float): Noise-to-Signal ratio.
                    sigma_confocal (float): sigma for the large Point-Spread-Function (Confocal).
                    sigma_sted (float): sigma for the small Point-Spread-Function (STED).
                    layer (int): if z-stack is used, select the layer to use the filter on.
                    save_image (string): select if and how to save the image.

            Returns:
                    None.
    '''

    if save_image == 'Run Batch':
        filenames = os.listdir(f'data/{foldername}')
        store_png = create_folder(f'{store_folder}/batch_png')
        store_tif = create_folder(f'{store_folder}/batch_tif')
        settings_save(store_folder, filename, pixel_size, background_subtraction,
                      ratio, nsr, sigma_confocal, sigma_sted, "Save settings", True)
        for filename in filenames:
            img = read_raw_tif(foldername, filename)
            img = choose_layer(img, layer)
            img_bg = background_subtract(img, background_subtraction)
            img_wiener = wiener_deconvolution(
                img_bg, pixel_size, sigma_confocal, sigma_sted, nsr, ratio)
            display_wiener(img, img_wiener, pixel_size, store_png,
                           filename, "Save png",  cmap, display=False)
            tif_save(
                img_wiener, f'{store_folder}/batch_tif', filename, "Save tif")

    else:
        img = read_raw_tif(foldername, filename)
        img = choose_layer(img, layer)
        img_bg = background_subtract(img, background_subtraction)
        img_wiener = wiener_deconvolution(
            img_bg, pixel_size, sigma_confocal, sigma_sted, nsr, ratio)
        display_wiener(img, img_wiener, pixel_size, store_folder,
                       filename, save_image,  cmap)
        settings_save(store_folder, filename, pixel_size, background_subtraction,
                      ratio, nsr, sigma_confocal, sigma_sted, save_image, False)
        tif_save(img_wiener, store_folder, filename, save_image)
