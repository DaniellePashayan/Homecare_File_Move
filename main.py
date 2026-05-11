from datetime import datetime
import time
import pandas as pd
import os
import shutil
import re
from loguru import logger


#setup logging
logger.add(f'./logs/log.log', rotation='1 week', retention='10 days', level='INFO')


class Folder:
    def __init__(self):
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
        else:
            logger.warning(f'Folder {folder_name} is not empty, skipping deletion')


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
                    else:
                        logger.warning(f'File {file} already exists in {self.destination_path}')

                self.delete_empty_folders(folder_name)
        except Exception as e:
            logger.error(f'Error moving {file}: {e}')

            
    def write_csv(self):
        today = datetime.today().strftime('%Y-%m-%d')
        # check if all rows in the file tracker have been moved
        if self.file_tracker['moved'].all():
            logger.success('All files moved successfully')
        else:
            logger.error('Not all files were moved successfully')
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
            break