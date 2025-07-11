from  pathlib import Path
import os

SAMPLE_PATH = '../sample_files'

def upload_files(self, file_path=SAMPLE_PATH, object_key=None):
    try:
        file_path = Path(__file__).parent / file_path        

        if os.path.isfile(file_path):
            files = [file_path]
        else:
            files = [os.path.join(file_path, f) for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        
        # Upload each file
        for file in files:
            if object_key is None:
                key = file.split('/')[-1] #TODO - check
            else:
                key = f"{object_key}/{file.split('/')[-1]}"
                
            self.s3_client.upload_file(file, self.config['bucket_name'], key)
            print(f"Uploaded {file} to {self.config['bucket_name']}/{key}")
        
        return True
    
    except Exception as e:
        print(f"Error uploading files: {e}")
        raise e