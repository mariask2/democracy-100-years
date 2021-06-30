# -*- coding: utf-8 -*-

import glob
import os
import json

TITLE = "<h1>"
SUBTITLE = "<h2>"
PARAGRAPH = "<p>"
WORD = "demokrati"
WORD_FIRST_IN_SENTENCE = "Demokrati"

def read_files():
    files = glob.glob('SOU-corpus-master/html/ft*')
    output_dict = {}
    statistics_dict = {}
    nr_of_paragraphs = [0]
    for i, file in enumerate(files):
        read_file(file, output_dict, statistics_dict, nr_of_paragraphs)
        
    dir_path = WORD
    title_dict = {}
    subtitle_dict = {}
    for nr, el in enumerate(output_dict.values()):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_name = os.path.join(dir_path, str(nr) + ".txt")
        f = open(file_name, "w")
        f.write(el[PARAGRAPH])
        title_dict[file_name.split("/")[1]] = el[TITLE]
        subtitle_dict[file_name.split("/")[1]] = el[SUBTITLE]
        f.close()
        
        
    with open('title.json', 'w') as f:
        json.dump(title_dict, f)
    with open('subtitle.json', 'w') as f:
        json.dump(subtitle_dict, f)
    
    with open('stat.txt', 'w') as stat_file:
        stat_list = sorted([(v, k) for (k, v) in  statistics_dict.items()], reverse=True)
        for v, k in stat_list:
            stat_file.write(k + " & " + str(v) + "\\\\ \n")
            stat_file.write("(``" + k + "'')" + "\\\\ \n")
    print("nr_of_paragraphs", nr_of_paragraphs)
    print("output_dict", len(output_dict.keys()))

def clean_line(line):
    line = line.replace("&ouml;", "ö")
    line = line.replace("&Ouml;", "Ö")
    line = line.replace("&auml;", "ä")
    line = line.replace("&Auml;", "ä")
    line = line.replace("&aring;", "å")
    line = line.replace("&Aring;", "Å")
    line = line.replace("&eacute;", "é")
    line = line.replace("&Eacute;", "É")
    line = line.replace("&permil;", "ä")
    line = line.replace("&circ;", "ö")
    line = line.replace("&Acirc;", "å")
    line = line.replace("&rdquo", "")
    return line

def read_file(file_name, output_dict, statistics_dict, nr_of_paragraphs):
    title = None
    subtitle = None
     
    url_base = "https://data.riksdagen.se/dokument/"
    file_name_leaf = os.path.split(file_name)[-1].replace("ft_", "")
    url = url_base + file_name_leaf
    title_env = False
    subtitle_env = False
    paragraph_env = False
    
    f = open(file_name)
    for line in f.readlines():

        line = clean_line(line)
        
        if title_env:
            if title == None or "örord" in title or "ill" in title or "SOU" in title:
                title = clean_line(line.strip())
            title_env = False
        if subtitle_env:
            subtitle = clean_line(line.strip())
            subtitle_env = False
        if paragraph_env:
            line_deleted = line.lower().replace("socialdemokrati", "").replace("sverigedemokrati", "").replace("istdemokrati", "").replace("nationaldemokrati","").replace("ny demokrati ","")
            if WORD in line_deleted:
                include_line = line.replace(WORD, " -<b>DEMOKRATI</b>- ").strip()
                include_line = include_line.replace(WORD_FIRST_IN_SENTENCE, " -<b>DEMOKRATI</b>- ").strip()

                include_line = include_line.replace("social -<b>DEMOKRATI</b>- ", "socialdemokrati")
                include_line = include_line.replace("Social -<b>DEMOKRATI</b>- ", "Socialdemokrati")
                include_line = include_line.replace("ist -<b>DEMOKRATI</b>- ", "istdemokrati")
                include_line = include_line.replace("sverige -<b>DEMOKRATI</b>- ", "sverigedemokrati")
                include_line = include_line.replace("Sverige -<b>DEMOKRATI</b>- ", "Sverigedemokrati")
                include_line = include_line.replace("National -<b>DEMOKRATI</b>- ", "Nationaldemokrati")
                include_line = include_line.replace("national -<b>DEMOKRATI</b>- ", "nationaldemokrati")
                include_line = include_line.replace("ny  -<b>DEMOKRATI</b>-  ", "ny demokrati ")
                include_line = include_line.replace("Ny  -<b>DEMOKRATI</b>-  ", "Ny demokrati ")
                
                include_line = '<a href="' + url + '" target="_blank"><u>pdf</u></a> ' + include_line
                include_line = include_line.replace("Stockholm:", "stockholmpublishinginfo")
                
                if include_line not in output_dict:
                    line_for_statistics = line.replace(",", " ").replace("?", " ").replace("!", " ").replace(":", " ").replace(";", " ").replace(".", " ")
                    token_for_statistics = line_for_statistics.lower().strip().split(" ")
                    for token in token_for_statistics:
                        if WORD in token:
                            if token not in statistics_dict:
                                statistics_dict[token] = 0
                            statistics_dict[token] = statistics_dict[token] + 1
                        
                output_dict[include_line]={PARAGRAPH: include_line, TITLE: title, SUBTITLE: subtitle}
                        
            paragraph_env = False
        if line.strip() == TITLE:
            title_env = True
        if line.strip() == SUBTITLE:
            subtitle_env = True
        if line.strip() == PARAGRAPH:
            paragraph_env = True
            nr_of_paragraphs[0] = nr_of_paragraphs[0] + 1
    f.close()

if __name__ == "__main__":
    read_files()
