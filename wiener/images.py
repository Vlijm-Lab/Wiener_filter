import os
import numpy as np
import tifffile as tif
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable


def background_subtract(img, value):
    '''
    Subtract the background from the given image.

            Parameters:
                    img (np.ndarray): gray-scale image from which the background will be subtracted.
                    value (int): subtract the background value from input image, equal to 0 if no subtraction.

            Returns:
                    img_background_subtracted (np.ndarray): background subtracted gray-scale image.
    '''

    data_type = img.dtype
    img_background_subtracted = img.copy()
    img_background_subtracted = img_background_subtracted.astype(
        np.int16) - value
    img_background_subtracted *= (img_background_subtracted > 0)
    img_background_subtracted = img_background_subtracted.astype(data_type)

    return img_background_subtracted


def scalebar(ax, pixel_size, pixel_unit):
    '''
    Adds a scalebar to the image using the corresponding pixel size and pixel unit.

            Parameters:
                    ax (matplotlib.axes._axes.Axes): axis to place scalebar on.
                    pixel_size (float): pixel_size for one pixel (assuming square pixels).
                    pixel_unit (string): unit corresponding to the pixel_size (e.g. 'um' or 'nm').


            Returns:
                    ax (matplotlib.axes._axes.Axes): axis containing the placed scalebar.
    '''

    ax.add_artist(ScaleBar(pixel_size, pixel_unit, location='lower right', color='w', box_alpha=.0,
                  length_fraction=0.4, width_fraction=0.02, scale_loc='top', label_loc='top', font_properties={"size": 18}))

    return ax


def colorbar(ax, ax_img):
    '''
    Adds a colorbar on the right side of the image. Rescaling the axis object such that the colorbar fits in.

            Parameters:
                    ax (matplotlib.axes._axes.Axes): axis to use the colorbar on.
                    ax_img (matplotlib.image.AxesImage): image used to compute colorbar.

            Returns:
                    None.
    '''

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(ax_img, cax=cax)


def read_raw_tif(foldername, filename):
    '''
    Read image from tif file with corresponding directory and name.

            Parameters:
                    filename (string): filename of image, which is present in 'data/foldername' folder.

            Returns:
                    img (np.ndarray): gray-scale tif image.
    '''

    img = tif.imread(f'data/{foldername}/{filename}')

    bit16 = 2**15
    if np.min(img) >= bit16:
        img -= bit16

    return img


def choose_layer(img, layer):
    '''
    Select a layer within a z-stack to be used as 2D image for the filtering.

            Parameters:
                    img (np.ndarray): gray-scale image in 2d or 3d (zstack).
                    layer (int): if z-stack is used, select the layer to use the filter on.

            Returns:
                    img (np.ndarray): 2d gray-scale image (layer of zstack).
    '''

    if len(img.shape) == 3:
        img = img[layer, :, :]

    return img


def tif_save(img, foldername, filename, save):
    '''
    Save the image as tif file.

            Parameters:
                    img (np.ndarray): wiener-filtered image.
                    foldername (string): name of the folder in which the data is present.
                    filename (string): filename of raw image.
                    save (string): one of the saving options within the GUI, which selects if and how the image will be stored.

            Returns:
                    None.
    '''

    path = f'{foldername}/{filename.split(".")[0]}_wiener.tif'

    if save == "Save tif":
        tif.imwrite(path, img)


def unused_folder_name(path):
    '''
    Create folder name which does not exist yet (adding numbers behind names).

            Parameters:
                    path (string): string contains the directory for the folder to be created.                

            Returns:
                    path (string): the string which contains the directory of the created folder.
    '''

    current_path = path
    num = 1

    while os.path.isdir(current_path):
        current_path = f'{path}({num})'
        num += 1

    return current_path


def create_folder(path, force_new=False):
    '''
    Create folder with given path.

            Parameters:
                    path (string): string contains the directory for the folder to be created.
                    force_new (string): set to True if a new directory must be made.

            Returns:
                    path (string): the string which contains the directory of the created folder.
    '''

    if force_new:
        path = unused_folder_name(path)
        os.mkdir(path)
    else:
        if not os.path.isdir(path):
            os.mkdir(path)

    return path


def display_wiener(img, img_wiener, pixel_size, foldername, filename, save=False, cmap='gray', figsize=(12, 8), display=True):
    '''
    Display wiener-filtered image combined with raw.

            Parameters:
                    img (np.ndarray): raw image.
                    img_wiener (np.ndarray): wiener-filtered image.
                    pixel_size (float): pixel_size for one pixel (assuming square pixels).
                    foldername (string): name of the folder in which the data is present.                
                    filename (string): filename of raw image.
                    save (string): one of the saving options within the GUI, which selects if and how the image will be stored.
                    cmap (string): name of colormap used for displaying images.   
                    figsize (tuple): the size of displayed image.
                    display (bool): equal to 'True' if image needs to be displayed directly.

            Returns:
                    None.
    '''

    fig, ax = plt.subplots(1, 2, figsize=figsize)

    im0 = ax[0].imshow(img_wiener, cmap=cmap.lower())
    ax[0].set_title('Wiener Filtered', fontsize=20)
    ax[0].axis('off')
    ax[0] = scalebar(ax[0], pixel_size, 'nm')
    colorbar(ax[0], im0)

    im1 = ax[1].imshow(img, cmap=cmap.lower())
    ax[1].set_title('Raw', fontsize=20)
    ax[1].axis('off')
    ax[1] = scalebar(ax[1], pixel_size, 'nm')
    colorbar(ax[1], im1)

    plt.tight_layout()

    if save == "Save png":
        path = f'{foldername}/{filename.split(".")[0]}_wiener.png'
        plt.savefig(path)

    if display:
        plt.show()
    else:
        plt.close()


def settings_save(foldername, filename, pixel_size, background_subtraction, ratio, nsr, sigma_confocal, sigma_sted, save, batch):
    '''
    Display wiener-filtered image combined with raw.

            Parameters:
                    foldername (string): name of the folder in which the data is present.                
                    filename (string): filename of raw image.
                    pixel_size (float): pixel_size for one pixel (assuming square pixels).
                    background_subtraction (int): subtract background value from the input image, equal to 0 if no subtraction.
                    ratio (float): ratio of intensity caused by large PSF compared to small PSF.
                    nsr (float): Noise-to-Signal ratio.
                    sigma_confocal (float): sigma for the large Point-Spread-Function (Confocal).
                    sigma_sted (float): sigma for the small Point-Spread-Function (STED).
                    save (string): one of the saving options within the GUI, which selects if and how the image will be stored.                
                    batch (bool): equal to 'True' if batch is being processed instead of single image.

            Returns:
                    None.
    '''

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    bg = np.ones((100, 100))
    ax.imshow(bg, cmap='gray', vmin=0)
    ax.axis('off')

    text_size = 12
    line_size = text_size * 2 / 3
    caption_size = 14
    text_space1 = 5
    text_space2 = 70
    l = 3

    ax.text(text_space1, l*line_size, f'Settings Wiener Filter',
            fontsize=caption_size, fontweight='bold')
    l += 1

    ax.text(text_space1, l*line_size, f' Pixel size (nm):',  fontsize=text_size)
    ax.text(text_space2, l*line_size, f'{pixel_size}',  fontsize=text_size)
    l += 1

    ax.text(text_space1, l*line_size,
            f' Background Subtraction:',  fontsize=text_size)
    ax.text(text_space2, l*line_size,
            f'{background_subtraction}',  fontsize=text_size)
    l += 1

    ax.text(text_space1, l*line_size, f' Ratio conf/STED:',  fontsize=text_size)
    ax.text(text_space2, l*line_size, f'{ratio}',  fontsize=text_size)
    l += 1

    ax.text(text_space1, l*line_size,
            f' Noise-to-Signal ratio:',  fontsize=text_size)
    ax.text(text_space2, l*line_size, f'{nsr}',  fontsize=text_size)
    l += 1

    ax.text(text_space1, l*line_size, f' FWHM Confocal (nm):',  fontsize=text_size)
    ax.text(text_space2, l*line_size, f'{sigma_confocal}',  fontsize=text_size)
    l += 1

    ax.text(text_space1, l*line_size, f' FWHM STED (nm):',  fontsize=text_size)
    ax.text(text_space2, l*line_size, f'{sigma_sted}',  fontsize=text_size)
    l += 1

    plt.tight_layout()
    if save == "Save settings":
        path = f'{foldername}/{(filename.split(".")[0]+"_")*(1-batch)}settings{batch*"_batch"}.png'
        plt.savefig(path)
    plt.close()
