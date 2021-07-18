# -*- coding: utf-8 -*-

import glob
import os
import json
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim import utils

TITLE = "<h1>"
SUBTITLE = "<h2>"
PARAGRAPH = "<p>"
WORD = "demokrati"

def read_files(files):
    
    output_list = []
    
    #dir_path = "word2vecformat"
    #if not os.path.exists(dir_path):
    #    os.makedirs(dir_path)
    #file_name = str(os.path.join(dir_path, "soulines.txt"))
    #f = open(file_name, "w")
    print("processing " + str(len(files)))
    for nr, file in enumerate(files):
        read_file(file, output_list)
        if nr%100 == 0:
            print(nr)
            #break
        #f.flush()
    #f.close()
    return output_list
        
    
def read_file(file_name, output_list):
    title = None
    subtitle = None
    title_env = False
    subtitle_env = False
    paragraph_env = False
    
    read_from = open(file_name)
    for line in read_from.readlines():
        line = line.replace("&ouml;", "ö")
        line = line.replace("&Ouml;", "Ö")
        line = line.replace("&auml;", "ä")
        line = line.replace("&Auml;", "ä")
        line = line.replace("&aring;", "å")
        line = line.replace("&Aring;", "Å")
        line = line.replace("&eacute;", "é")
        line = line.replace("&Eacute;", "É")
        line = line.replace(", ", " ")
        line = line.replace("? ", " ")
        line = line.replace("! ", " ")
        line = line.replace(": ", " ")
        line = line.replace("; ", " ")
        
        if title_env:
            title = line.strip()
            #f.write(title + "\n")
            output_list.append(utils.simple_preprocess(title))
            title_env = False
        if subtitle_env:
            subtitle = line.strip()
            #f.write(subtitle + "\n")
            output_list.append(utils.simple_preprocess(subtitle))
            subtitle_env = False
        if paragraph_env:
            for el in line.strip().split(". "):
                output_list.append(utils.simple_preprocess(el))
                #f.write(el + "\n")
            paragraph_env = False
        if line.strip() == TITLE:
            title_env = True
        if line.strip() == SUBTITLE:
            subtitle_env = True
        if line.strip() == PARAGRAPH:
            paragraph_env = True
    read_from.close()


        
if __name__ == "__main__":
    PARTS = 10
    files = glob.glob('SOU-corpus-master/html/ft*')
    files_1 = files[0:3*int(len(files)/PARTS)]
    
    output_list = read_files(files_1)
    print("Start training")
    model = Word2Vec(sentences=output_list, window=3, min_count=20, workers=4)
    print("Nr of words " + str(len(model.wv.vocab)))
    vec_ca = model.wv['ca']
    print(len(vec_ca))
    
    """
    for nr in range(4, PARTS):
        print(str((nr-1) * int(len(files)/PARTS)) + " to " + str(nr*int(len(files)/PARTS)))
        files_2 = files[(nr-1) * int(len(files)/PARTS):nr*int(len(files)/PARTS)]
        output_list_2 = read_files(files_2)
        model.train(output_list_2, total_examples=len(output_list_2), epochs=model.epochs)
    """
    print("Nr of words " + str(len(model.wv.vocab)))
    model.save("SOUword2vec-created.model")
    
    #print(output_list)
