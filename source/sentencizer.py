import spacy
import re
import functions as fun
import extend_rules as exr
from spacy.pipeline import Pipe

exceptions = exr.load_and_process_rules(xml_path=fun.path_to("segment.srx"))


def compile_pattern(rules):
    patterns = []
    for rule in rules:
        pattern = re.compile(rule)
        patterns.append(pattern)
    return set(patterns)


exceptions = compile_pattern(exceptions)

punct_chars = [
    '!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '߹',
    '।', '॥', '၊', '။', '።', '፧', '፨', '᙮', '᜵', '᜶', '᠃', '᠉', '᥄',
    '᥅', '᪨', '᪩', '᪪', '᪫', '᭚', '᭛', '᭞', '᭟', '᰻', '᰼', '᱾', '᱿',
    '‼', '‽', '⁇', '⁈', '⁉', '⸮', '⸼', '꓿', '꘎', '꘏', '꛳', '꛷', '꡶',
    '꡷', '꣎', '꣏', '꤯', '꧈', '꧉', '꩝', '꩞', '꩟', '꫰', '꫱', '꯫', '﹒',
    '﹖', '﹗', '！', '．', '？', '𐩖', '𐩗', '𑁇', '𑁈', '𑂾', '𑂿', '𑃀',
    '𑃁', '𑅁', '𑅂', '𑅃', '𑇅', '𑇆', '𑇍', '𑇞', '𑇟', '𑈸', '𑈹', '𑈻', '𑈼',
    '𑊩', '𑑋', '𑑌', '𑗂', '𑗃', '𑗉', '𑗊', '𑗋', '𑗌', '𑗍', '𑗎', '𑗏', '𑗐',
    '𑗑', '𑗒', '𑗓', '𑗔', '𑗕', '𑗖', '𑗗', '𑙁', '𑙂', '𑜼', '𑜽', '𑜾', '𑩂',
    '𑩃', '𑪛', '𑪜', '𑱁', '𑱂', '𖩮', '𖩯', '𖫵', '𖬷', '𖬸', '𖭄', '𛲟', '𝪈',
    '｡', '。'
]

punct_chars = set(punct_chars)


class CustomSentencizer(Pipe):
    """
    CustomSentencizer(...) is an alternative to classic spacy Sentencizer.
    The logic of new sentences prediction was changed to give you more
    precise and robust tool to segmentation.
    """

    def __init__(self, punct_chars=None, overwrite=False):
        self.punct_chars = set(punct_chars) if punct_chars else {".", "!", "?"}
        self.overwrite = overwrite

    def __call__(self, doc):
        print("CustomSentencizer called")
        tags = self.predict([doc])
        self.set_annotations([doc], tags)
        return doc

    def predict(self, docs):
        """
        New Logic for Sentence Prediction

        This new approach to sentence prediction relies on identifying exceptions using regular expressions.
        The `predict(...)` method iterates through each token in a `Doc` object. When it encounters a punctuation
        mark (e.g., "."), it checks for exceptions (e.g., "btw.") using the `is_in_exceptions(...)` method.
        If an exception is detected, `predict(...)` marks the index of the next token. This ensures that
        the beginning of a new sentence is not incorrectly set.

        :param docs: A collection of `Doc` objects (or a single `Doc` object).
        :return: A list of predictions indicating sentence boundaries.
        """
        guesses = []
        for doc in docs:
            doc_guesses = [False] * len(doc)
            if len(doc) > 0:
                start = 0
                seen_period = False  # the previous character was in punct_characters
                doc_guesses[0] = True # first word is always the beggining of new sentence
                marked_token = None

                for i, token in enumerate(doc):
                    is_in_punct_chars = token.text in self.punct_chars
                    in_exceptions = False

                    if is_in_punct_chars and 0 < i < len(doc) - 3:
                        in_exceptions = is_in_exceptions(token, doc, i, show_result=False)
                        if in_exceptions:
                            marked_token = i + 1

                    if (seen_period and not is_in_punct_chars and not in_exceptions and i != marked_token) or \
                            (is_new_paragraph(token, doc, i) == True):
                        r"""
                        seen_period - the previous token was a punctuation mark
                        not is_in_punct_chars - this token is not a punctuation mark
                        not is_in_exceptions - this token in not a part of an exception 
                        i != marked_token - this token is not marked
                        is_new_paragraph(...) - check whether token is a beginning of a 
                        new paragraph ex. "...brain. \n\nBackground\n\..."
                        """
                        doc_guesses[start] = True  # set the beginning of a new sentence
                        start = token.i
                        seen_period = False
                    elif is_in_punct_chars:
                        seen_period = True
                    elif not is_in_punct_chars:
                        seen_period = False
                if start < len(doc):
                    doc_guesses[start] = True
            guesses.append(doc_guesses)
        return guesses

    def set_annotations(self, docs, batch_tag_ids):
        for i, doc in enumerate(docs):
            doc_tag_ids = batch_tag_ids[i]
            for j, tag_id in enumerate(doc_tag_ids):
                doc[j].is_sent_start = tag_id


@spacy.language.Language.factory("custom_sentencizer")
def create_custom_sentencizer(nlp, name):
    return CustomSentencizer(punct_chars=punct_chars)


def is_in_exceptions(token, doc, i, show_result=False):
    """
    `is_in_exceptions(...)` checks whether a token is part of an exception.

    :param token: The token being checked.
    :param doc: The `Doc` object over which iteration occurs.
    :param i: The index of the token within the `Doc`.
    :param show_result: Optional flag to enable printing debug information.
    :return: A boolean value indicating whether the token is part of an exception.
    """
    start = i - 1
    end = i + 3
    span = doc[start:end]

    def is_regular_exp(rules, string, token_index):
        for rule in rules:
            try:
                result = rule.search(string)
                if result:
                    # Determine token position
                    result_index = start + result.start()

                    if token_index > result_index:
                        # print("-------------------------------")
                        # print(f"token: {token}")
                        # print(f"pattern: {rule}")
                        # print(f"exception: {result.group()}")
                        # print(f"Span causing exception: {span.text}")
                        return True
            except re.error as e:
                print(f"Error compiling rule: {rule}\nReason: {e}")
        return False

    if is_regular_exp(exceptions, span.text, i):
        if show_result:
            print(f'''
                  doc[i] = {doc[i]}
                  doc[s] = {doc[start]}
                  doc[end] = {doc[end - 1]}
                  doc[s:end] = {doc[start:end]}
                  span = {span}
                  ''')
            print(f"full span text: {span.text}")
        return True
    return False


def is_new_paragraph(token, doc, i, show_result=True):
    new_paragraph_1 = [r"\n", r"\n\n", r"\n\n\n"]
    if any(paragraph in token.text for paragraph in new_paragraph_1) and doc[i - 1].text == ".":
        if show_result:
            print(f"""
                    token = {token.text}
                    doc[{i}-1] = {doc[i - 1]}
                    doc[{i}] = {doc[i]}
                """)
        return True
    return False


def add_custom_sentencizer(nlp):
    if "sentencizer" in nlp.pipe_names:
        nlp.remove_pipe("sentencizer")

    nlp.add_pipe("custom_sentencizer")
    return nlp
