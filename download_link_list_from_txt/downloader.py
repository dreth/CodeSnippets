import os


def download(filename='', subfolder_name='folder_name', path='~/Downloads', txt_name='txt', use="curl", mkdirs=False, original=True):
    """
    Bulk download files from a list of links
    filename: name of the file to be used in in case the files will be renamed
              optional if original=True
    subfolder_name: name of the subfolder to create and download things to
    path: download path
    txt_name: name of the text file containing the links, default txt
    use: command to use, default curl
    mkdirs: if text includes name above groups of links, create dir to include links below it
    original: rename the files or not
    """
    # path_prev = f'{path}'
    path = f'{path}/{subfolder_name}'

    with open(txt_name) as f:
        links = f.read().splitlines()
    
    os.system(f'mkdir {path}')

    if mkdirs == True:

        file_tree = {}
        curr_subfolder = ''

        for n,line in enumerate(links):
            if line[:4] != "http":
                curr_subfolder = line
                file_tree[curr_subfolder] = []
                os.system(f'mkdir {path}/{curr_subfolder}')
            else:
                file_tree[curr_subfolder].append(line)

        for subfolder, links_list in file_tree.items():
            command = f"cd {path}/{subfolder} && {use}"
            for n,link in enumerate(links_list):
                if original == True:
                    command = command + f" -O '{link}'"
                else:
                    command = command + f" -o '{filename}_{n}' {link}"
            os.system(f"{command} && cd ..")
    
    else:
        command = use
        for n,link in enumerate(links):
            if original == True:
                command = command + f" -O '{link}'"
            else:
                command = command + f" -o '{filename}_{n}' {link}"
        os.system(f"cd {path} && {command}")


params = {
    'filename':''
    ,'subfolder_name':'lezen_lingua'
    ,'path':'~/Downloads'
    ,'txt_name':'txt'
    ,'use':"curl"
    ,'mkdirs':True
    ,'original':True
}

download(**params)