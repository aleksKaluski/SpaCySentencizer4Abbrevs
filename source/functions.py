from pathlib import Path


def path_to(file_name, folder='C:\dane'):
    """
    The aim of this function is to make path-finding process easier :)
    Note that you don't have to change the dashes from '\' to '/'!
    :param file_name: name of the file
    :param folder: path of the folder in which the file is kept
    :return: the proper path of the file
    """
    try:
        data_folder = Path(folder)  # \ -> / resolved automatically
        file_path = data_folder / file_name
        print("path: ", file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")
        return file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def remove_newlines(input_file_path, output_file_path):
    """
    remove_newlines(...) was created for tests. It rewrites
    formatted article into text without line break characters.

    :param input_file_path: txt file
    :param output_file_path: empty txt file
    :return: txt file without line break characters
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
                open(output_file_path, 'w', encoding='utf-8') as outfile:

            text = infile.read()
            text_without_newlines = text.replace('\n', ' ')
            outfile.write(text_without_newlines)

        print(f"Processed text written to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def rules_to_file(rules, path_to_file):
    try:
        with open(path_to_file, 'w', encoding='utf-16') as file:
            for rule in rules:
                file.write(f"{rule}\n")
        print(f"Rules have been saved to '{path_to_file}'.")
    except Exception as e:
        print(f"An error occurred while saving the rules: {e}")


def file_to_rules(path_to_file):
    rules = []
    try:
        with open(path_to_file, 'r', encoding='utf-16') as file:
            rules = [line.strip() for line in file]
        # print(f"Rules have been read from '{path_to_file}'.")
    except FileNotFoundError:
        print(f"The file '{path_to_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the rules: {e}")
    return rules