# SpaCySentencizer4Abbrevs: Rule-Based Sentence Segmentation with spaCy

## Overview
**SpaCySentencizer4Abbrevs** extends spaCy's sentence segmentation capabilities by introducing a robust, rule-based approach to handle abbreviations and special cases. This project is designed to address challenges with text segmentation when dealing with scientific documents, abbreviations (e.g., "et al."), and other non-standard sentence-ending patterns. Users can easily customize the segmentation rules to meet their specific needs.

## Key Features
- Handles exceptions like abbreviations and scientific terms.
- Rule-based approach with customizable regular expressions.
- Seamless integration with spaCy's NLP pipeline.
- Outputs accurate sentence segmentation even in challenging text structures.

## File Structure

### 1. **`extend_rules.py`**
   - Processes segmentation rules stored in SRX (Segmentation Rules eXchange) format.
   - Converts rules into Python-compatible regular expressions.
   - Key functions:
     - `get_rules_from_xml(path_to_file)`: Extracts rules from an SRX file.
     - `exceptions_generator(path_of_xml)`: Generates non-breaking rules.
     - `make_rules_compatible(xml_rules)`: Converts SRX rules into Python-compatible regex patterns.
     - `add_missed_patterns(rules)`: Adds custom rules for abbreviations (e.g., "et al.").

### 2. **`segmentation.py`**
   - Contains utility functions for applying sentence segmentation to text.
   - Handles input and output for text segmentation tasks.
   - Key functions:
     - `sgm_result_to_board(text_path, nlp, show_result=True)`: Outputs segmented sentences and their count.
     - `sgm_result_to_file(text_path, nlp, output_file)`: Writes segmented sentences and their count to a file.

### 3. **`sentencizer.py`**
   - Implements a custom spaCy pipeline component for sentence segmentation.
   - Handles token-level checks for punctuation and exceptions.
   - Key classes and functions:
     - `CustomSentencizer`: Custom spaCy pipeline for sentence segmentation.
     - `is_in_exceptions(token, doc, i, show_result=False)`: Checks if a token is part of an exception.
     - `is_new_paragraph(token, doc, i, show_result=True)`: Identifies new paragraphs based on text patterns.
     - `add_custom_sentencizer(nlp)`: Integrates the custom sentencizer into a spaCy pipeline.

## Usage
## Example Usage
```python
  import spacy
  from sentencizer import CustomSentencizer
  from spacy.lang.en import English
  import sentencizer as sts

  text_path = r'your_absolute_path_to_txt_file'
  output_path = r'your_absolute_path_to_txt_file'

  # SpaCySentencizer4Abbrevs
  NLP = English()
  NLP.add_pipe("sentencizer")
  sts.add_custom_sentencizer(NLP)
  print(f"Pipeline components: {NLP.pipe_names}")

  # prints the result
  sgr.sgm_result_to_board(text_path, NLP)
  # saves the result to file
  sgr.sgm_result_to_file(text_path, NLP, output_path)

```

## Customization
You can add or modify rules by updating the `add_missed_patterns` function in `extend_rules.py`. For example:
```python
regex_patterns = [
    r"[eE]t\.? [aA]l[\.,]",  # et al.
    r"[fF]ig\.?"]           # fig.
]
```

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request if you have improvements or bug fixes.

## Sources: 
SpaCySentencizer4Abbrevs leverages the SRX file from LanguageTool to enhance sentence segmentation for text containing abbreviations. The SRX rules used in this project are sourced from LanguageTool's repository, specifically: <br>
https://github.com/languagetool-org/languagetool/blob/master/languagetool-core/src/main/resources/org/languagetool/resource/segment.srx

Key functionalities of the program, including:
- The structure of the Rule class
- SRX rule parsing
- Compatibility adjustments for rules
are either directly adapted from or heavily inspired by the work in the spaCy-PL utilities repository. <br>
link: https://github.com/spacy-pl/utils

Additionally, thanks to spaCy's publicly available codebase, I was able to customize the Sentencizer class to further improve functionality. See spaCy’s implementation: <br>
https://github.com/explosion/spaCy/blob/master/spacy/pipeline/sentencizer.pyx

## License
This project is licensed under the CC0-1.0 license.

