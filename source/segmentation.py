from source import extend_rules as exr


def sgm_result_to_board(text_path, nlp, show_result=True):
    """
    Prints the result of segmentation in spacy.
    :param show_result:
    :param text_path: plain text (txt file)
    :param nlp: the nlp model
    :return: the result of segmentation and the number of sentences
    """
    try:
        with open(text_path, "r", encoding="utf-8") as file:
            txt = file.read()
    except FileNotFoundError:
        print(f"The file '{text_path}' does not exist.")

    doc = nlp(txt)
    sent_number = 0
    for sent in doc.sents:
        sent_number += 1
        if show_result:
            print(f"\nThat's sentence number: {sent_number} \n", sent)
    if show_result:
        print(f"The number of sentences is: {sent_number}")
    return sent_number


def sgm_result_to_file(text_path, nlp, output_file):

    try:
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"The file '{text_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

    doc = nlp(text)
    sent_number = 0

    try:
        with open(output_file, 'w', encoding='utf-16') as file:
            for sent in doc.sents:
                sent_number += 1
                file.write(f"\n{sent_number}: {sent}")

            final_result = f"\nThe number of sentences is: {sent_number}!!"
            file.write(final_result)

    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    return output_file


def load_and_process_rules(path_to_file):
    xml_rules = exr.exceptions_generator(path_to_file)
    compatible_rules = exr.make_rules_compatible(xml_rules)
    return compatible_rules
