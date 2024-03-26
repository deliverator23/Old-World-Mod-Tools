from unityparser import UnityDocument
import os
import shutil
import yaml


def patch_controller(filename, working_folder_path, source_controller_file_map, index):
    extracted_controller_file = working_folder_path + "\\" + filename
    print("{}: Loading extracted file {}".format(index, extracted_controller_file))
    try:
        extracted_controller = UnityDocument.load_yaml(extracted_controller_file)
    except yaml.reader.ReaderError as e:
        print("Exception: {} - {}".format(e.__class__.__name__,  e.reason))
        return

    motion_map = {}

    for entry in extracted_controller.entries:
        if entry.__class__.__name__ == 'AnimatorState':
            motion_map[entry.m_Name] = entry.m_Motion

    original_controller_file = source_controller_file_map[filename] + "\\" + filename
    print("{}: Loading original file {}".format(index, original_controller_file))
    try:
        working_controller = UnityDocument.load_yaml(original_controller_file)
    except yaml.reader.ReaderError as e:
        print("Exception: {} - {}".format(e.__class__.__name__, e.reason))
        return

    for entry in working_controller.entries:
        if entry.__class__.__name__ == 'AnimatorState':
            entry.m_Motion = motion_map[entry.m_Name]

    patched_path = temp_path + "\\AnimatorController_patched"
    if not os.path.exists(patched_path):
        os.makedirs(patched_path)
    patched_full_path = patched_path + "\\" + filename
    print("{}: Writing patched file {}".format(index, patched_full_path))
    working_controller.dump_yaml(patched_full_path)
    return


ow_asset_library_path = input("Please enter your Old World extracted asset library path: ")
ow_game_path = input("Please enter your Old World game path: ")
temp_path = input("Please enter a path for temporary files: ")

#ow_asset_library_path = "C:\\Users\\<username>\\OldWorld_AssetLibrary_2021.3.24"
#temp_path = "C:\\Game Mods\\Modding Work\\OldWorld\\Temp"
#ow_game_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Old World"

animator_controller_path = ow_asset_library_path + "\\Assets\\AnimatorController"
reference_graphics_path = ow_game_path + "\\Reference\\Graphics"


source_controller_file_map = {}
for path, subdirs, files in os.walk(reference_graphics_path):
    for filename in files:
        if filename.endswith(".controller"):
            source_controller_file_map[filename] = path

index = 1
for path, subdirs, files in os.walk(animator_controller_path):
    for filename in files:
        if filename.endswith(".controller") and filename in source_controller_file_map:
            extracted_path = temp_path + "\\AnimatorController_extracted"
            if not os.path.exists(extracted_path):
                os.makedirs(extracted_path)
            shutil.copy(animator_controller_path + "\\" + filename, extracted_path + "\\" + filename)
            patch_controller(filename, extracted_path, source_controller_file_map, index)
            index = index + 1
