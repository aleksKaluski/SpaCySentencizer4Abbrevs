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
    # ścieżka do pliku, który chcesz podzielić na zdania
    text_path = fun.path_to("papers_10pack_clean.txt", folder=r'C:\dane')

    # ścieżka do pliku, w którym chcesz otrzymać ostateczny wynik analizy
    output_path = fun.path_to("wynik.txt", folder=r'C:\dane\test')

    # działanie sentencizera
    NLP = English()
    NLP.add_pipe("sentencizer")
    sts.add_custom_sentencizer(NLP)
    print(f"Pipeline components: {NLP.pipe_names}")

    # działanie sentencizera spacy
    nlp = English()
    nlp.add_pipe("sentencizer")

    # wynik działania!
    # sgr.sgm_result_to_board(text_path, nlp)
    sgr.sgm_result_to_board(text_path, NLP)
    # sgr.sgm_result_to_file(text_path, NLP, output_path)


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

    main()

    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())