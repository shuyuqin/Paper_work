"""

"""

import os
from os.path import join as pjoin
import matplotlib.pyplot as plt
import glob
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import random
import tensorflow as tf
import numpy as np
import string
from matplotlib import (pyplot as plt, animation, colors,
                        ticker, path, patches, patheffects)

def set_seeds(seed=42):
    """
    :param seed: random value to set the sequence of the shuffle and random normalization

    """
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    tf.random.set_seed(seed)
    np.random.seed(seed)


def make_folder(folder, **kwargs):
    """
    Function that makes new folders

    :param folder: folder where to save
    :type folder: string
    :return: folder where to save
    :rtype: string
    """


    # Makes folder
    os.makedirs(folder, exist_ok=True)

    return (folder)


def labelfigs(axes, number, style='wb', loc='br',
              string_add='', size=20, text_pos='center'):
    """
    Adds labels to figures

    Parameters
    ----------
    axes : matplotlib axes
        axes which to add the plot to
    number : int
        letter number
    style : str, optional
        sets the color of the letters
    loc : str, optional
        sets the location of the label
    string_add : str, optional
        custom string as the label
    size : int, optional
        sets the font size for the label
    text_pos : str, optional
        set the justification of the label
    """

    # Sets up various color options
    formatting_key = {'wb': dict(color='w',
                                 linewidth=1.5),
                      'b': dict(color='k',
                                linewidth=0.5),
                      'w': dict(color='w',
                                linewidth=0.5)}

    # Stores the selected option
    formatting = formatting_key[style]

    # finds the position for the label
    x_min, x_max = axes.get_xlim()
    y_min, y_max = axes.get_ylim()
    x_value = .08 * (x_max - x_min) + x_min

    # Sets the location of the label on the figure
    if loc == 'br':
        y_value = y_max - .1 * (y_max - y_min)
        x_value = .08 * (x_max - x_min) + x_min
    elif loc == 'tr':
        y_value = y_max - .9 * (y_max - y_min)
        x_value = .08 * (x_max - x_min) + x_min
    elif loc == 'bl':
        y_value = y_max - .1 * (y_max - y_min)
        x_value = x_max - .08 * (x_max - x_min)
    elif loc == 'tl':
        y_value = y_max - .9 * (y_max - y_min)
        x_value = x_max - .08 * (x_max - x_min)
    elif loc == 'tm':
        y_value = y_max - .9 * (y_max - y_min)
        x_value = x_min + (x_max - x_min) / 2
    elif loc == 'bm':
        y_value = y_max - .1 * (y_max - y_min)
        x_value = x_min + (x_max - x_min) / 2
    else:
        raise ValueError(
            'Unknown string format imported please look at code for acceptable positions')

    # adds a custom string
    if string_add == '':

        # Turns to image number into a label
        if number < 26:

            axes.text(x_value, y_value, string.ascii_lowercase[number],
                      size=size, weight='bold', ha=text_pos,
                      va='center', color=formatting['color'],
                      path_effects=[patheffects.withStroke(linewidth=formatting['linewidth'],
                                                           foreground="k")])

        # allows for double letter index
        else:
            axes.text(x_value, y_value, string.ascii_lowercase[0] + string.ascii_lowercase[number - 26],
                      size=size, weight='bold', ha=text_pos,
                      va='center', color=formatting['color'],
                      path_effects=[patheffects.withStroke(linewidth=formatting['linewidth'],
                                                           foreground="k")])
    else:
        # writes the text to the figure
        axes.text(x_value, y_value, string_add,
                  size=size, weight='bold', ha=text_pos,
                  va='center', color=formatting['color'],
                  path_effects=[patheffects.withStroke(linewidth=formatting['linewidth'],
                                                       foreground="k")])

def savefig(filename, printing):

    """
    function that saves the figure

    :param filename: path to save file
    :type filename: string
    :param printing: contains information for printing
                     'dpi': int
                            resolution of exported image
                      print_EPS : bool
                            selects if export the EPS
                      print_PNG : bool
                            selects if print the PNG
    :type printing: dictionary

    """


    # Saves figures at EPS
    if printing['EPS']:
        plt.savefig(filename + '.eps', format='eps',
                    dpi=printing['dpi'], bbox_inches='tight')

    # Saves figures as PNG
    if printing['PNG']:
        plt.savefig(filename + '.png', format='png',
                    dpi=printing['dpi'], bbox_inches='tight')


def make_movie(movie_name, input_folder, output_folder, file_format,
                            fps, output_format = 'mp4', reverse = False):
    """
    function that makes the movie of the images data

    :param movie_name: name of the movie
    :type movie_name: string
    :param input_folder: folder where the image series is located
    :type input_folder: string
    :param output_folder: folder where the movie will be saved
    :type output_folder: string
    :param file_format: sets the format of the files to import
    :type file_format: string
    :param fps: frames per second
    :type fps: numpy, int
    :param output_format: sets the format for the output file
                          supported types .mp4 and gif
                          animated gif create large files
    :type output_format: string (, optional)
    :param reverse: sets if the movie will be one way of there and back
    :type reverse: bool  (, optional)

    """


    # searches the folder and finds the files
    file_list = glob.glob('./' + input_folder + '/*.' + file_format)

    # Sorts the files by number makes 2 lists to go forward and back
    list.sort(file_list)
    file_list_rev = glob.glob('./' + input_folder + '/*.' + file_format)
    list.sort(file_list_rev,reverse=True)

    # combines the file list if including the reverse
    if reverse:
        new_list = file_list + file_list_rev
    else:
        new_list = file_list


    if output_format == 'gif':
        # makes an animated gif from the images
        clip = ImageSequenceClip(new_list, fps=fps)
        clip.write_gif(output_folder + '/{}.gif'.format(movie_name), fps=fps)
    else:
        # makes and mp4 from the images
        clip = ImageSequenceClip(new_list, fps=fps)
        clip.write_videofile(output_folder + '/{}.mp4'.format(movie_name), fps=fps)