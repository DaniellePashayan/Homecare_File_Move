import os
from loguru import logger
from functions import delete_empty_folders, move_files, correct_folder_names

global src_path
global dest_path

dest_path = '\\\\NASHCN01\\SHAREDATA\\NewRefCenter\\ANewReferralPHI\\NS\\'
src_path = f'{dest_path}\\BOT\\Medical Records'


def run():
    global src_path
    global dest_path
    
    logger.add(f'.\\logs\\log.log', rotation='1 week', retention='10 days', level='INFO')
    correct_folder_names(src_path)
    for folder in os.listdir(src_path):
        if (len(os.listdir(src_path))) > 0:
            path = os.path.join(src_path, folder)
            # get_files(path)

            move_files(path)

    delete_empty_folders(src_path)
    logger.success('Process completed')

if __name__ == '__main__':
    run()
