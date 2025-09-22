from datetime import datetime, timedelta
from loguru import logger
from src.folder import Folder

if __name__ == "__main__":
    
    #setup logging
    logger.add(f'./logs/log.log', rotation='1 week', retention='10 days', level='INFO')

    today = datetime.now()
    if today.weekday() == 0:
        date = today - timedelta(days=3)
    else:
        date = today - timedelta(days=1)
    
    folder = Folder(date)
    files_moved = folder.copy_files_to_destination()
    
    if files_moved == folder.df.shape[0]:
        folder.archive_folder()
        logger.info(f'All {files_moved} files moved and folder archived.')