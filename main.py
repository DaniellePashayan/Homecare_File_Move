import os
from functions import get_files, delete_empty_folders, move_files

global src_path
global dest_path

dest_path = 'S:/NewRefCenter/ANewReferralPHI/NS/'
src_path = f'{dest_path}/BOT/Medical Records'


def run():
    global src_path
    global dest_path
    for folder in os.listdir(src_path):
        if (len(os.listdir(src_path))) > 0:
            path = os.path.join(src_path, folder)
            get_files(path)
            move_files(path)

    delete_empty_folders(src_path)



if __name__ == '__main__':
    run()
