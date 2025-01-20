import spacy

import functions as fun
import extend_rules as exr
import segmentation as sgr
import sentencizer as sts

from spacy.lang.en import English
from sentencizer import CustomSentencizer
import cProfile
import pstats
import io


def main():

    text_path = r'C:\Sentencizer_rewrited_Vol5\files\input.txt'

    output_path = r'C:\Sentencizer_rewrited_Vol5\files\output.txt'

    # SpaCySentencizer4Abbrevs
    NLP = English()
    NLP.add_pipe("sentencizer")
    sts.add_custom_sentencizer(NLP)
    print(f"Pipeline components: {NLP.pipe_names}")
    sgr.sgm_result_to_board(text_path, NLP)
    # sgr.sgm_result_to_file(text_path, NLP, output_path)


    # basic spaCy sentencizer
    nlp = English()
    nlp.add_pipe("sentencizer")
    sgr.sgm_result_to_board(text_path, nlp)


if __name__ == "__main__":
    main()

    # uncomment for perfomance results
    # pr = cProfile.Profile()
    # pr.enable()
    #
    # main()
    #
    # pr.disable()
    #
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())