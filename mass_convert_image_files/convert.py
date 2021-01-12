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
    formats = [x for x in map(''.join, itertools.product(*zip(ffrom.upper(), ffrom.lower())))]

    # file list and filter files with such format
    lstdr = os.listdir(path)
    file_list = []
    for f in lstdr:
        try:
            if f.split('.')[1] in formats:
                file_list.append(f)
        except:
            continue

    os.system('mkdir ./conversion')
    for f in file_list:
        f = f.split('.')[0]
        if use == 'ffmpeg': 
            os.system(f'{use} -i "./{f}.{ffrom.lower()}" "./conversion/{f}.{fto.lower()}"')
    
    print('\nDone!\n')

convert('./','webp', 'png')