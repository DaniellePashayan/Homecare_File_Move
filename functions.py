import datetime as dt
import pandas as pd
import os
import shutil
import tqdm
import re
from glob import glob

global dest_path
dest_path = 'S:/NewRefCenter/ANewReferralPHI/NS/'


def get_files(folder):
    date_frmt = folder.split('\\')[-1]
    date = dt.datetime.strptime(date_frmt, "%m_%d_%y")

    # get all the files in the folder and add to dataframe
    files = glob(f'{folder}/*.pdf')
    df = pd.DataFrame({'file_date': date, 'file_name': files})

    # check if output file exists
    year = dt.datetime.strftime(date, format = '%Y')
    month = dt.datetime.strftime(date, format = '%m')
    output_path = f'M:/CPP-Data/CBO Westbury Managers/LEADERSHIP/Bot Folder/Part A/Home Care/Outputs/{year} {month}.xlsx'

    # if output exists, add it to existing, if not create a new file
    if os.path.exists(output_path):
        existing_df = pd.read_excel(output_path)
        dates = pd.to_datetime(existing_df['file_date'].unique())
        if not date in dates:
            existing_df = pd.concat([existing_df, df])
            existing_df = existing_df.drop_duplicates()
            with pd.ExcelWriter(output_path) as writer:
                existing_df.to_excel(writer, index = None)
    else:
        df.to_excel(output_path, index = None)


def correct_folder_names(folder):
    for subfolder in os.listdir(folder):
        path = os.path.join(folder, subfolder)
        new_foldername = re.sub(r'\s\(\d+\)', '', subfolder)
        new_path = os.path.join(folder, new_foldername)
        if not os.path.exists(new_path):
            os.rename(path, new_path)
        else:
            if len(os.listdir(path)) == 0:
                os.rmdir(path)


def move_files(folder):
    global dest_path
    for file in tqdm.tqdm(os.listdir(folder)):
        src = f'{folder}/{file}'
        dest = f'{dest_path}/{file}'
        shutil.move(src, dest)


def delete_empty_folders(path):
    for folder in os.listdir(path):
        folder = os.path.join(path, folder)
        if len(os.listdir(folder)) == 0:
            shutil.rmtree(folder)
