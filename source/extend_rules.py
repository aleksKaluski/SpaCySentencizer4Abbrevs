import re
import xml.etree.ElementTree as ET


class Rule:
    """
    The class with the same structure as Segment's
    a rule looks like this:
    tag: rule, attrib: {'break': 'yes' or 'no'}
    """

    def __init__(self, breaking: bool, before_pattern_str: str = None, after_pattern_str: str = None):
        self.breaking = breaking  # True == stence breaks, otherwise False
        self.before_pattern_str = before_pattern_str  # strring before breaking point
        self.after_pattern_str = after_pattern_str

    def __str__(self):
        """
         Simple toString method
         """
        return f"breaking: {self.breaking} | before: {self.before_pattern_str} | after: {self.after_pattern_str}"


def get_rules_from_xml(path_to_file):
    """
    get_rules_from_xml takes the rules from the external file (srx)
    and rewrites them as the list of class objects.
    :param: path_to_file
    :return: list of the objects of the Rule class
    """
    # the file is analysed as a tree
    tree = ET.parse(path_to_file)
    root = tree.getroot()
    english_rules = root[1][0][2]

    rules = []
    for rule in english_rules:
        # checking whether the rule breaks the sentence and setting its attribute
        breaking = True if rule.attrib['break'] == 'yes' else False
        before_pattern_str = rule[0].text
        after_pattern_str = rule[1].text
        rules += [Rule(breaking, before_pattern_str, after_pattern_str)]
    return rules


def exceptions_generator(path_of_xml):
    """
    exceptions_generator takes segmentation rules from
    xml file and then finds the rules which do not break a string into
    a new sentence
    :param path_of_xml: XML file with rules
    :return: rule which do not break the sentence
    """
    rules = get_rules_from_xml(path_of_xml)
    exception_rules = []

    for rule in rules:
        # if rule.braking == False and there is no pattern in the rule
        if not rule.breaking and rule.after_pattern_str is None or rule.after_pattern_str == "":
            exception_rules += [rule]
    return exception_rules


def make_rules_compatible(xml_rules):
    """
    make_rules_compatible rewrites rules to make them compatible with Pythonic syntax of regex.
    Additionaly, this functions adds some custom exeptions to the logic of sentencizer.
    :param xml_rules: list of class objects (class = Rule)
    :return: set of re. expresions
    """

    eng_lowercase = u'abcdefghijklmnopqrstuvwxyz'
    eng_uppercase = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    compatible_rules = []
    for rule in xml_rules:
        # replace unicode properties with standard Python regex
        pattern = rule.before_pattern_str \
            .replace(r"\p{Lu}", "[" + eng_uppercase + "]") \
            .replace(r"\p{Ll}", "[" + eng_lowercase + "]") \
            .replace(r"(?iu)", "") \
            .replace(r"\p{L}", "[" + eng_uppercase + eng_lowercase + "]") \
            .replace(r"\p{N}", r"\d") \
            .replace(r"\u00A0", r"\s") \
            .replace(r"\p{Ps}", r"[\({\[]") \
            .replace(r"\p{Pe}", r"[\)\}\]]")
        raw_pattern = fr"{pattern}"  # using r-prefix to make it a raw string
        compatible_rules.append(raw_pattern)

    compatible_rules = add_missed_patterns(compatible_rules)

    # exclude rules which don't contain any letters from eng_lowercase and eng_uppercase
    compatible_rules = [fe for fe in compatible_rules
                        if re.search(f'.*[{eng_lowercase}{eng_uppercase}].*', fe)]

    return set(compatible_rules)


def load_and_process_rules(xml_path):
    """
    A vey simple function to speed up the process of using rules.
    :param xml_path: path  of XMl file with the rules
    :return: a set of compatible rules
    """
    rules = exceptions_generator(xml_path)
    compatible_rules = make_rules_compatible(rules)
    return compatible_rules


def add_missed_patterns(rules):
    """
    add_missed_patterns(rules) enables the user to add custom exceptions as python re.expressions.
    If expression is very long (has many tokens ex. "et. al" [3 tokens]) it might be better
    to break it into a few regular expressions ex. "et. al" -> r"[eE]t\.,?" (et.) and r"[aA]l\.,?" (al).

    :param rules: a set of re. exp. compatible with Python syntax
    :return: extended set of re. exp.
    """
    regex_patterns = [r"[eE]t\.? [aA]l[\.,]?", r"[fF]ig\.?|f+\.",
                      r"[iI]bid\.", r"[cC]it\.", r"[eE]sp\.,?",
                      r"[bB]tw\.,?", r"[eE]t\.,?", r"[aA]l\.,?"]

    for pattern in regex_patterns:
        try:
            rules.append(pattern)
        except Exception as e:
            print(f"Error {e} ")
    return set(rules)
