from wiener.functions import wiener_apply
from wiener.images import create_folder
import os
from ipywidgets import Layout, interact, Dropdown, BoundedIntText, BoundedFloatText, Textarea, ToggleButtons, fixed


def folder_selection():
    '''
    Interactive function to select folder which contains the raw data, placed in the 'data' folder.

            Parameters:
                    None.

            Returns:
                    folder (string): path to the raw data folder.
    '''

    style = {'description_width': '200px', 'width': '500px'}
    layout = Layout(width='500px', height='30px')

    folder = Dropdown(description='Select folder: ',
                      options=os.listdir(f'data'), style=style, layout=layout)
    display(folder)

    return folder


def wiener_filter(folder):
    '''
    Interactive function to set parameters for wiener filtering an image.

            Parameters:
                    None.

            Returns:
                    None.
    '''

    style = {'description_width': '200px', 'width': '500px'}
    layout = Layout(width='500px', height='30px')

    colormaps = ['Hot', 'Gray', 'Viridis', 'Plasma',
                 'Inferno', 'Magma', 'Cividis', 'HSV']

    saving_options = ["Don't save", "Save tif",
                      "Save png", "Save settings", "Run Batch"]

    store_folder = create_folder(f'data/{folder}_wiener', force_new=True)

    interact(wiener_apply,
             foldername=fixed(folder),
             store_folder=fixed(store_folder),
             filename=Dropdown(description='File name of raw image: ',
                               options=os.listdir(f'data/{folder}'), style=style, layout=layout),
             cmap=Dropdown(description='Colormap: ',
                           options=colormaps, style=style, layout=layout),
             pixel_size=BoundedIntText(description='Pixel size: ',
                                       min=1,
                                       max=50,
                                       step=1,
                                       value=20, style=style, layout=layout),
             background_subtraction=BoundedIntText(description='Background Subtraction: ',
                                                   min=0,
                                                   max=1000,
                                                   step=1,
                                                   value=0, style=style, layout=layout),
             ratio=BoundedFloatText(description='Ratio STED/Conf PSF influence: ',
                                    min=0.0,
                                    max=1.0,
                                    step=0.01,
                                    value=0.5, style=style, layout=layout),
             nsr=BoundedFloatText(description='Noise-to-Signal Ratio: ',
                                  min=0.01,
                                  max=.5,
                                  step=0.01,
                                  value=0.50,
                                  readout_format='.3f', style=style, layout=layout),
             sigma_confocal=BoundedFloatText(description='Sigma 1 (Confocal PSF): ',
                                             min=180,
                                             max=500,
                                             step=1,
                                             value=350, style=style, layout=layout),
             sigma_sted=BoundedFloatText(description='Sigma 1 (STED PSF): ',
                                         min=10,
                                         max=120,
                                         step=1,
                                         value=33, style=style, layout=layout),
             layer=BoundedIntText(description='Layer in stack: ',
                                  min=0,
                                  max=100,
                                  step=1,
                                  value=0, style=style, layout=layout),
             save_image=ToggleButtons(options=saving_options, description='Save tif - set to "Don\'t save" after saving.', button_style='info'))
