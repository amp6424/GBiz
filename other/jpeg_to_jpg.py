import os

# Function to rename a .jpeg file to .jpg
def convert_jpeg_to_jpg(file_path):
    # Check if the file has a .jpeg extension
    if file_path.lower().endswith('.jpeg'):
        # Get the base name without extension
        base_name = os.path.splitext(file_path)[0]
        # Create new file name with .jpg extension
        new_file_path = base_name + '.jpg'
        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"File renamed to: {new_file_path}")
    else:
        print("The file is not a .jpeg format.")

# Example usage
file_path = "generated_3358037507.jpeg"
convert_jpeg_to_jpg(file_path)

