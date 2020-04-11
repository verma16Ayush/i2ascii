import numpy as np
from PIL import Image
import argparse
from datetime import datetime as dt

seventy_shades_of_gray = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`\'. "
ten_shades_of_gray = "@%#*+=-:. "


def get_mean_brightness(tile):
    '''
    this function calculates the mean brightness of the tile passed as parameter
    :param tile: a cropped image
    :return: average value of brightness of that tile. float value ranging between [0, 255]
    '''
    tile_array = np.array(tile)
    w, h = np.shape(tile)
    avg_brightness = np.mean(np.reshape(tile_array, w * h))
    return avg_brightness


def convert_image_to_ascii(path, cols=200, scale=0.43, more_shades=True):
    """
    this function does all the work and i'm too tired to describe it for you.
    :param path: path of the input image file
    :param cols: columns of text in the output file desired
    :param scale: aspect ratio of the font type. the default font type is monospace font courier. a default ratio of
    0.43 is already set for that
    :param more_shades: specify if you want a more detailed output based on a 70 level shade ramp or 10 levels. this
    :param is inversely related to the number of columns you supply
    :return: a list of strings for the output file
    """
    img = Image
    try:
        img = Image.open(fp=path).convert('L')

    except Exception as e:
        print(e)
        print('cannot open the file specified')
        exit(0)

    w, h = np.asarray(img).shape
    tile_width = w / cols
    tile_height = tile_width / scale
    print('original image dimensions: {} x {}'.format(w, h))
    print('tile dimensions: {} x {}'.format(tile_width, tile_height))
    rows = int(h / tile_height)
    ascii_img = list()
    for i in range(0, rows):
        y1 = int(i * tile_height)
        y2 = int((i + 1) * tile_height)
        ascii_img.append('')
        if i == rows - 1:
            y2 = h - 1

        for j in range(0, cols):
            x1 = int(j * tile_width)
            x2 = int((j + 1) * tile_width)
            if j == cols - 1:
                x2 = w - 1

            tile = img.crop((x1, y1, x2, y2))
            avg_b = get_mean_brightness(tile)
            if more_shades:
                lookup_val = int((avg_b / 255) * 69)
                x = seventy_shades_of_gray[lookup_val]
            else:
                lookup_val = int((avg_b / 255) * 9)
                x = ten_shades_of_gray[lookup_val]
            ascii_img[i] += x

    return ascii_img


def main():
    # create parser
    cols = 200
    scale = 0.43
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--file', dest='img_file', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='out_file', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--more_levels', dest='more_levels', action='store_true')

    # parse arguments
    args = parser.parse_args()
    img_file = args.img_file

    # set output file
    out_file = img_file[:-4] + '_ascii_art.txt'
    # store the type of shade
    more_levels = True
    if args.more_levels:
        more_levels = args.more_levels
    if args.out_file:
        out_file = args.out_file
    # set scale default as 0.43, which suits a Courier font
    if args.scale:
        scale = float(args.scale)
    # set cols
    if args.cols:
        cols = int(args.cols)
    print('generating ASCII art...')
    # convert image to ASCII text

    ascii_img = convert_image_to_ascii(img_file, cols, scale, more_levels)
    # open a new text file

    f = open(out_file, 'w')
    # write each string in the list to the new file
    for row in ascii_img:
        f.write(row + '\n')
    # clean up
    f.close()
    print("ASCII art written to %s" % out_file)


# call main
if __name__ == '__main__':
    main()
