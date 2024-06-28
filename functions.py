import datetime as dt
import pandas as pd
import os
import shutil
import tqdm
import re
from glob import glob
import zipfile
import csv


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
    
    records_transferred = 0
    
    all_file_names = get_list_of_worked_accounts()
    
    for file in tqdm(os.listdir(folder)):
        if file.endswith('.pdf'):
            if not was_worked(file, all_file_names):
            # Extract the filename without extension (assuming account number is part of the filename)

                # Check if the filename (or a part of it) is present in the account number set
                src = os.path.join(folder, file)
                dest = os.path.join(dest_path, file)
                shutil.move(src, dest)  # Use move fnction from shutil
                records_transferred +=1
    print(f'{records_transferred=}')


def delete_empty_folders(path):
    for folder in os.listdir(path):
        folder = os.path.join(path, folder)
        if len(os.listdir(folder)) == 0:
            shutil.rmtree(folder)

def get_list_of_worked_accounts():
    folder_path = "M:/CPP-Data/Sutherland RPA/Northwell Process Automation ETM Files/GOA/Inputs/moved"
    months = ['2024 05', '2024 06']
    folders_to_ignore = os.listdir('S:/NewRefCenter/ANewReferralPHI/NS/BOT/Medical Records')
    
    for month in months:
        path = f'{folder_path}/{month}'

        # Open the CSV file for writing
        with open("file_names.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Name", "Folder"])

            # Loop through zip files in the folder
        
            for filename in glob(f'{path}/Homecare*.zip'):
                for folder in folders_to_ignore:
                    if folder not in filename:
                        # Open the zip file
                        with zipfile.ZipFile(filename, 'r') as zip_ref:
                            # Get a list of file names inside the zip
                            file_names = [name for name in zip_ref.namelist()]

                            # Write zip filename and list of files to CSV
                            for file in file_names:
                                writer.writerow([file,filename])
    all_file_names = set()
    with open("file_names.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        
        for row in reader:
            # Extract file names from the second column (index 1)
            all_file_names.add(row[0])
    return all_file_names

def was_worked(file_name, all_file_names):
    if file_name in all_file_names:
        return True
    else:
        return False