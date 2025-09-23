import datetime
from loguru import logger
import os
import shutil
import pandas as pd
import re
from src.notify import send_error_notification

class Folder:
    def __init__(self, date: datetime.datetime):
        self.destination_path = r'//NASHCN01/SHAREDATA/NewRefCenter/ANewReferralPHI/NS'
        self.source_path = r'//NASHCN01/SHAREDATA/NewRefCenter/ANewReferralPHI/NS/BOT/Medical Records'
        self.date = date
        self.df = pd.DataFrame()
        self.dated_folder = None
        
    def get_dated_folder(self) -> str:
        folders = os.listdir(self.source_path)
        folders = [re.sub(r'\s\(\d+\)', '', subfolder) for subfolder in folders]
        dated_folder = [folder for folder in folders if self.date.strftime('%m_%d_%y') in folder]
        if len(dated_folder) == 0:
            logger.error(f'No folder found for date {self.date.strftime("%m_%d_%y")}')
            send_error_notification(f'HomeCare - No folder found for date {self.date.strftime("%m_%d_%y")}')
            raise FileNotFoundError(f'No folder found for date {self.date.strftime("%m_%d_%y")}')
        else:
            self.dated_folder = os.path.join(self.source_path, dated_folder[0])
            return self.dated_folder
    
    def list_files(self):
        self.get_dated_folder()
        return [file for file in os.listdir(self.dated_folder) if '.pdf' in file]
    
    def convert_files_to_df(self, date:datetime.datetime, file_list:list):
        dict_list = {date.strftime('%m_%d_%y'): file_list}
        
        df = [(key, value) for key, values in dict_list.items() for value in values]
        df = pd.DataFrame(df, columns=["date", "file"])
        df['moved'] = False
        self.df = df
        csv_path = f'./logs/trackers/{self.date.strftime("%Y")}/{self.date.strftime("%m %Y")}'
        os.makedirs(csv_path, exist_ok=True)
        df.to_csv(f'{csv_path}/{self.date.strftime("%m-%d-%y")}.csv', index=False)
    
    def copy_files_to_destination(self):
        file_list = self.list_files()
        self.convert_files_to_df(self.date, file_list)
        files_moved = 0
        
        for file in file_list:
            source_file = os.path.join(self.dated_folder, file)
            destination_file = os.path.join(self.destination_path, file)
            try:
                shutil.copy(source_file, destination_file)
                # check if file exists in destination
                if os.path.exists(destination_file):
                    self.df.loc[self.df['file'] == file, 'moved'] = True
                    files_moved += 1
                    logger.debug(f'Copied {file} to {self.destination_path}')
            except Exception as e:
                logger.error(f'Error copying {file}: {e}')
                send_error_notification(f'HomeCare - Error copying {file}: {e}')
        return files_moved
    
    def archive_folder(self):
        logger.info(f'Archiving folder {self.dated_folder}')
        archive_folder = os.path.join(self.source_path, 'ARCHIVE')
        # once the files are copied, zip the folder and move to archive
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
        shutil.make_archive(self.dated_folder, 'zip', self.dated_folder)
        logger.info(f'Created zip file {self.dated_folder}.zip')
        shutil.move(f'{self.dated_folder}.zip', os.path.join(archive_folder, f'{os.path.basename(self.dated_folder)}.zip'))
        # remove the original folder and files
        shutil.rmtree(self.dated_folder)
        logger.success(f'Archived and removed folder {self.dated_folder}')