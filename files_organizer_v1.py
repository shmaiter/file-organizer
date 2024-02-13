import os
import shutil
import sys

# PENDIENTES
# Investigar como dar permisos al script para que pueda ser ejecutado sin que el antivirus lo bloquee.


# path example: r'C:\Users\shmai\Downloads'

def selection_menu() -> str:
    print(f"\n+ {42 * '-'} +")
    print(f"| {42 * ' '} |")
    print(
        f"|{'Welcome to File Organizer App'.center(44)}|"
    )
    print(f"| {42 * ' '} |")
    print(f"+ {42 * '-'} +")

    validated_path = validate_path()

    return validated_path


def validate_path() -> str:
    # path = "C:\\Users\\John\\Documents\\Data.txt"  # Replace with your path

    while True:
        path = input('Enter the directory full path you would like to organize: \n> ')
        path = modify_path(path)
        if os.path.exists(path):
            print("\nThe path exists.")
            return path
        else:
            user_input = user_input_sanitation("\nThe path does not exist. Would you like to try again? (y/n): ")
            if user_input == 'n':
                print("\nClosing the program. . .")
                sys.exit(0)


def modify_path(path: str) -> str:
    mod_path = repr(path).replace("'", "")
    mod_path = mod_path.replace('"', "")
    print(mod_path)
    return mod_path


def scan_directory(dir_path) -> list:
    files_list = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    files_details = {}

    for file in files_list:
        ext = os.path.splitext(file)[1][1:]

        if ext in files_details:
            files_details[ext] += 1
        else:
            if len(ext) == 0:
                files_details['unknown'] = 1
            else:
                files_details[ext] = 1

    print(f"\n************* Files extensions found in the directory: {dir_path}")
    print(files_details)
    print(f"Amount of files in the directory: {len(files_list)}")

    if len(files_list) == 0:
        print(">>> No files to organize <<<")
        return []
    else:
        user_confirmation(files_list)
        return [files_list, files_details]


def user_confirmation(files_list: list) -> None:
    print("\nThe following files will be moved into their respective directories according to their extensions:")
    for index, file in enumerate(files_list):
        print(f"{index+1}: {file}")

    input_str = user_input_sanitation("\nDo you want to continue? (y/n): ")

    if input_str == 'n':
        print("\nClosing the program. . .")
        sys.exit(0)


def make_directories(unorganized_files, extensions, dir_path) -> None:
    for ext in extensions:
        fullpath_new_dir = os.path.join(dir_path, ext)

        if not os.path.isdir(fullpath_new_dir):  # if the directory doesn't exist
            os.mkdir(fullpath_new_dir)
            print(f"\n************* Finished making directory: {ext}")

        unorganized_files = move_files(ext, fullpath_new_dir, unorganized_files, dir_path)
        print(f'|\n|\nPending files to move: {unorganized_files}')


# think about updating the files_list after every move of files
def move_files(ext, fullpath_new_dir, unorganized_files, dir_path) -> list:
    remove_list = []
    for file in unorganized_files:
        fullpath_to_file = os.path.join(dir_path, file)

        if os.path.isfile(fullpath_to_file):  # if it's a file
            if file.endswith(ext) or ext == 'unknown' and os.path.splitext(file)[1] == '':
                print(f"Moving file: {file}")
                shutil.move(os.path.join(fullpath_to_file), os.path.join(fullpath_new_dir, file))
                remove_list.append(file)

    print(f"************* Finished moving files with extension: {ext}")
    return [file for file in unorganized_files if file not in remove_list]

def user_input_sanitation(output_str: str) -> str:
    while True:
        input_str = input(output_str).lower().strip()
        if input_str == '' or input_str != 'n' and input_str != 'y':
            print("(Please enter a letter 'y' or 'n' to continue.)")
        else:
            return input_str


if __name__ == "__main__":

    while True:
        repr_dir_path = selection_menu()
        file_details = scan_directory(repr_dir_path)

        if len(file_details) > 0:
            make_directories(file_details[0], file_details[1], repr_dir_path)

        user_input = user_input_sanitation("\nWould you like to organize another directory? (y/n): ")
        if user_input == 'n':
            print("\nClosing the program. . .")
            sys.exit(0)
