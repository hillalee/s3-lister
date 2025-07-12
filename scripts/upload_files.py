from  pathlib import Path
import os
import boto3

SAMPLE_PATH = '../sample_files'

def upload_files(bucket_name, file_path=SAMPLE_PATH, object_key=None):
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
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
                
            s3_client.upload_file(file, bucket_name, key)
            print(f"Uploaded {file} to {bucket_name}/{key}")
        
        
        
        return True
    
    except Exception as e:
        print(f"Error uploading files: {e}")
        raise e
    

if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python upload_files.py <bucket_name> [file_path] [object_key]")
        exit(1)
        
    bucket_name = os.sys.argv[1]
    file_path = os.sys.argv[2] if len(os.sys.argv) > 2 else SAMPLE_PATH
    object_key = os.sys.argv[3] if len(os.sys.argv) > 3 else None
    upload_files(bucket_name, file_path=file_path, object_key=object_key)