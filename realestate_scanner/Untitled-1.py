zip_file_path = '/mnt/data/realestate-scanner.zip'
extracted_folder_path = '/mnt/data/realestate_scanner_extracted'

# Extracting the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# Listing the contents of the extracted folder
extracted_files = os.listdir(extracted_folder_path)
extracted_files