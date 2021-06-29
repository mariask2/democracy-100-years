import os
import json
from sklearn.feature_extraction import text
from nltk.corpus import stopwords

# An import that should function both locally and when running an a remote server
try:
    from environment_configuration import *
except:
    from topics2themes.environment_configuration import *

if RUN_LOCALLY:
    from topic_model_constants import *
    from word2vec_term_similarity import *

else:
    from topics2themes.topic_model_constants import *
    from topics2themes.word2vec_term_similarity import *
    

"""
Nr of topics to retrieve
"""
NUMBER_OF_TOPICS = 20

"""
The topic modelling algorithm is rerun with a decrease number of requested topics
until the number of found stable topics are similar to the ones requested
The amont of similarity is set here.
"""

PROPORTION_OF_LESS_TOPIC_TO_ALLOW = 0.9

"""
Nr of words to display for each topic
"""
NR_OF_TOP_WORDS = 15

"""
Nr of most typical document to retrieve for each topic
"""
#NR_OF_TOP_DOCUMENTS = 490
NR_OF_TOP_DOCUMENTS = 30

"""
Number of runs to check the stability of the retrieved topics.
Only topics that occur in all NUMBER_OF_RUNS runs will be
considered valid
"""
NUMBER_OF_RUNS = 100


"""
Mininimum overlap of retrieved terms to considered the retrieved topic as
the same topic of a another one
"""
OVERLAP_CUT_OFF = 0.8

"""
When counting overlap, outliers are removed. This sets percentage for what is to be retained
"""
PERCENTATE_NONE_OUTLIERS = 0.20

"""
Whether to use pre-processing (collocation detection and synonym clustering)
"""
PRE_PROCESS = True
VECTOR_LENGTH = 100
#SPACE_FOR_PATH = "/Users/marsk757/wordspaces/69/model.bin"
SPACE_FOR_PATH = "/Users/marsk757/corpora/SOU-corpus/SOUword2vec.model"
MAX_DIST_FOR_CLUSTERING = 0.62
WORDS_NOT_TO_INCLUDE_IN_CLUSTERING_FILE = "not_cluster.txt"
MANUAL_CLUSTER_FILE = "manual_clusters.txt"
GENSIM_FORMAT = True

"""
Mininimum occurrence in the corpus for a term to be included in the topic modelling
"""
MIN_DOCUMENT_FREQUENCY = 20

"""
Maximum occurrence in the corpus for a term to be included in the topic modelling
"""
MAX_DOCUMENT_FREQUENCY = 0.95

BINARY_TF = False


"""
Mininimum occurrence in the corpus for a term to be included in the clustering.
"""
MIN_DOCUMENT_FREQUENCY_TO_INCLUDE_IN_CLUSTERING = 5

"""
The stop word file of user-defined stopiwords to use (Scikit learn stop words are also used)
"""
STOP_WORD_FILE = "demokrati_stopwords.txt"

"""
The directories in which data is to be found. The data is to be in files with the ".txt" extension
in these directories. For each directory, there should also be a stance-label and a color associated with
the data
"""


DATA_LABEL_LIST = [{DATA_LABEL : "Focus", DIRECTORY_NAME : "fokus", LABEL_COLOR : GREEN },\
                   {DATA_LABEL : "No", DIRECTORY_NAME : "demokrati", LABEL_COLOR : "#ccad00"}]

TOPIC_MODEL_ALGORITHM = NMF_NAME
#TOPIC_MODEL_ALGORITHM = LDA_NAME

"""
    If an extracted term includes less than this among the documents that are extracted, this term is removed from the set of extracted terms
    Synonym clustering is performed before the counting is done, so a rare term with synonyms is retained
    """
MIN_FREQUENCY_IN_COLLECTION_TO_INCLUDE_AS_TERM = 1

MAX_NR_OF_FEATURES = 5000

STOP_WORD_SET = set(stopwords.words('swedish'))

SHOW_ARGUMENTATION = False
SHOW_SENTIMENT = False

REMOVE_DUPLICATES = True

MIN_NGRAM_LENGTH_FOR_DUPLICATE = 15

def get_title(doc_path):
    ls = []
    doc_id = os.path.split(doc_path)[-1]
    with open("title.json", "r") as title_data:
        title_dict = json.loads(title_data.read())
        if doc_id in title_dict:
            ls.append("SOU: " + title_dict[doc_id])
        else:
            print("NOT FOUND")
    with open("subtitle.json", "r") as subtitle_data:
        subtitle_dict = json.loads(subtitle_data.read())
        if doc_id in subtitle_dict:
            ls.append("Underrubrik: " + subtitle_dict[doc_id])
        else:
            print("NOT FOUND subtitle")

    return ls

ADDITIONAL_LABELS_METHOD = get_title


def corpus_specific_text_cleaning(text):

    text = text.replace("'", "")\
    .replace("’", "")\
    .replace("ˆ", "ö")\
    .replace("‰", "ä")\
    .replace("Â", "å")\
    
    #text.replace(" ,", ",")\
    #.replace("( ", " (")\
    #.replace(" )", ") ")\
    
    return text

CLEANING_METHOD = corpus_specific_text_cleaning

MANUAL_COLLOCATIONS = "manual_collocations.txt"

NUMBER_OF_SENTENCES_IN_SUMMARY = 2

