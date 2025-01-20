import zipfile
import os
import time
import shutil
import os

def extract_diag_from_bpm(bpm_file, output_folder="output"):
    # Extract the BPM file contents
    with zipfile.ZipFile(bpm_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

    # Locate the .diag file
    diag_file = None
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".diag"):
                diag_file = os.path.join(root, file)
                break

    if not diag_file:
        raise FileNotFoundError("No .diag file found in the BPM archive.")


    diag_folder = "xml"
    os.makedirs(diag_folder, exist_ok=True)
    with zipfile.ZipFile(diag_file, 'r') as diag_zip:
        diag_zip.extractall(diag_folder)

    print(f".diag content extracted to {diag_folder}")
    time.sleep(0.2)
    clean_folders()
    return diag_folder


def clean_folders():
    # Delete the 'output' folder if it exists
    if os.path.exists("output"):
        shutil.rmtree("output")
        print("Deleted 'output' folder.")
    if os.path.exists("xml/ImageArtifactImages"):
        shutil.rmtree("xml/ImageArtifactImages")
        print("Deleted 'ImageArtifactImages' folder.")

    # Delete all files in 'xml' folder except 'Diagram.xml'
    xml_folder = "xml"
    if os.path.exists(xml_folder):
        for file in os.listdir(xml_folder):
            if file != "Diagram.xml":
                file_path = os.path.join(xml_folder, file)
                os.remove(file_path)
                print(f"Deleted {file_path}")



# Example usage
extract_diag_from_bpm("file.bpm")
