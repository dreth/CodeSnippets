import os
import itertools

def convert(path, ffrom, fto, use='ffmpeg'):
    """
    Function to convert image files
    PARAMS:
    path = path to get files from
    ffrom = format to convert from
    fto = format to convert to
    use = engine to use, default is ffmpeg
    """
    # formats
    formats = [x for x in map(''.join, itertools.product(*zip(fto.upper(), fto.lower())))]

    # file list and filter files with such format
    file_list = os.listdir(path)
    file_list = [x for x in file_list if x[-4:] in formats]

    os.system('mkdir ./conversion')
    for f in file_list:
        if use == 'ffmpeg':
            os.system(f'{use} -i {f}{ffrom.lower()} ./conversion/{f}{fto.lower()}')
    
    print('\nDone!\n')