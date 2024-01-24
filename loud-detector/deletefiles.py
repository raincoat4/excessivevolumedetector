#run this to delete all the recordings in the folder
import os

def delete():
    save_directory = "/Users/liamrogers/Documents/recordings"

    for file_name in os.listdir(save_directory):
        file_path = os.path.join(save_directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    delete()
