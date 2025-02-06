import os
from loguru import logger
from functions import delete_empty_folders, move_files, correct_folder_names
from orcca.status_handler import JSONStatus

global src_path
global dest_path

dest_path = '\\\\NASHCN01\\SHAREDATA\\NewRefCenter\\ANewReferralPHI\\NS\\'
src_path = f'{dest_path}\\BOT\\Medical Records'


def run():
    global src_path
    global dest_path
    
    logger.add(f'.\\logs\\log.log', rotation='1 week', retention='10 days', level='INFO')
    status = JSONStatus(
        master_file_path=r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\CBO Westbury Managers\LEADERSHIP\Bot Folder\Automated Scripts Status.json',
        process_name='Homecare File Move'
    )
    status.update_status('Running')
    try:
        correct_folder_names(src_path)
        folders = os.listdir(src_path)
        if len(folders) == 0 or folders is None:
            logger.warning('No folders found')
            status.update_status('Completed')
            return
        for folder in os.listdir(src_path):
            if (len(os.listdir(src_path))) > 0:
                path = os.path.join(src_path, folder)
                # get_files(path)

                files_moved = move_files(path)

        delete_empty_folders(src_path)
        logger.success(f'Moved {files_moved} files')
        status.update_status('Completed')
    except Exception as e:
        logger.error(e)
        status.update_status('Failed', errors=str(e))
    

if __name__ == '__main__':
    run()
