from datetime import datetime
import time
import pandas as pd
import os
import shutil
import re
from loguru import logger
from pushbullet import Pushbullet
from orcca.status_handler import JSONStatus


#setup logging
logger.add(f'./logs/log.log', rotation='1 week', retention='10 days', level='INFO')
status = JSONStatus(
        master_file_path=r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\CBO Westbury Managers\LEADERSHIP\Bot Folder\Automated Scripts Status.json',
        process_name='Homecare File Move'
    )

class Notifier:
    def __init__(self, api_key):
        self.pb = Pushbullet(api_key)
    
    def notify(self, title, message):
        self.pb.push_note(title, message)

class Folder:
    def __init__(self):
        status.update_status('Running')
        self.destination_path = r'//NASHCN01/SHAREDATA/NewRefCenter/ANewReferralPHI/NS'
        self.source_path = r'//NASHCN01/SHAREDATA/NewRefCenter/ANewReferralPHI/NS/BOT/Medical Records'
        
        
    def _get_files(self, folder_name):
        full_path = os.path.join(self.source_path, folder_name)
        return [file for file in os.listdir(full_path) if '.pdf' in file]
    
    
    def _get_folders(self):
        folders = os.listdir(self.source_path)
        # removes " (1)" from folder names in case of duplicates
        return [re.sub(r'\s\(\d+\)', '', subfolder) for subfolder in folders]
    
    
    def _get_folders_and_files(self):
        self.file_list = {date: folder._get_files(date) for date in self._get_folders()}


    def _convert_file_list_to_csv(self):
        df = [(key, value) for key, values in self.file_list.items() for value in values]
        df = pd.DataFrame(df, columns=["date", "file"])
        df['moved'] = False
        self.file_tracker = df

    def delete_empty_folders(self, folder_name):
        if len(os.listdir(os.path.join(self.source_path, folder_name))) == 0:
            logger.debug(f'Deleting empty folder {folder_name}')
            os.rmdir(os.path.join(self.source_path, folder_name))
            status.update_status('Completed')
        else:
            logger.warning(f'Folder {folder_name} is not empty, skipping deletion')
            notifier.notify('Homecare File Move', f'Folder {folder_name} is not empty, skipping deletion')
            status.update_status('Error', f'Folder {folder_name} is not empty, skipping deletion')


    def move_files(self):
        self._get_folders_and_files()
        self._convert_file_list_to_csv()
        
        try:
            for folder_name, files in self.file_list.items():
                for file in files:
                    source = os.path.join(self.source_path, folder_name, file)
                    destination = os.path.join(self.destination_path, file)
                    if not os.path.exists(destination):
                        print(f'Moving {file} from {folder_name} to {self.destination_path}')
                        shutil.move(source, destination)
                        if os.path.exists(destination):
                            logger.debug(f'Moved {file} from {folder_name} to {self.destination_path}')
                            self.file_tracker.loc[self.file_tracker['file'] == file, 'moved'] = True
                        else:
                            logger.error(f'{file} from {folder_name} said it was moved to {self.destination_path}, but was not.')
                            notifier.notify('Homecare File Move', f'{file} from {folder_name} said it was moved to {self.destination_path}, but was not.')
                    else:
                        logger.warning(f'File {file} already exists in {self.destination_path}')

                self.delete_empty_folders(folder_name)
        except Exception as e:
            logger.error(f'Error moving {file}: {e}')
            status.update_status('Error', e)
            notifier.notify('Homecare File Move', f'Error moving {file}: {e}')

            
    def write_csv(self):
        today = datetime.today().strftime('%Y-%m-%d')
        # check if all rows in the file tracker have been moved
        if self.file_tracker['moved'].all():
            logger.success('All files moved successfully')
        else:
            logger.error('Not all files were moved successfully')
            status.update_status('Error', 'Not all files were moved successfully')
            notifier.notify('Homecare File Move', 'Not all files were moved successfully')
        os.makedirs('./logs/trackers', exist_ok=True)
        self.file_tracker.to_csv(f'./logs/trackers/{today}.csv', index=False)

if __name__ == '__main__':
    folder = Folder()
    while True:
        if not os.path.exists(folder.source_path):
            time.sleep(900) # 15 minutes
        else:
            folder.move_files()
            folder.write_csv()
            status.update_status('Completed')
            break