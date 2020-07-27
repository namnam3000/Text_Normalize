from nltk import word_tokenize
from string import punctuation
import pandas as pd
import re


def read_tts_dict(path):
    words = list()
    fo = open(path, 'r')
    for line in fo:
        words.append(line.split()[0].strip())

    return words


def read_vnmese_words(path):
    words = list()
    fo = open(path, 'r')
    for line in fo:
        words.append(line.strip())

    return words


def read_oov(path):
    oov_dict = dict()
    fo = open(path, 'r')
    for line in fo:
        words = line.split('\t')
        oov_dict[words[0]] = int(words[1])

    return oov_dict


def add_oov(oov_word, oov_dict):
    if oov_word not in oov_dict:
        oov_dict[oov_word] = 1
    else: oov_dict[oov_word] = oov_dict[oov_word] + 1

    return oov_dict


def write_oov_dict(oov_dict, path):
    fo = open(path, 'w')
    for key, value in oov_dict.items():
        fo.write(str(key) + '\t' + str(value) + '\n')


def read_txt_two_cols(path):
    trans_dict = dict()
    fo = open(path, 'r')
    for line in fo:
        try:
            pairs = line.split('\t')
            words = pairs[0]
            transcription = pairs[1].replace('_', ' ')
            trans_dict[words.strip()] = transcription.strip().lower()
        except:
            print(line.strip())
            print(pairs)

    return trans_dict

def read_txt_two_cols_1(path):
    trans_dict = dict()
    fo = open(path, 'r')
    for line in fo:
        try:
            pairs = line.split('\t')
            words = pairs[0]
            transcription = pairs[1].replace('_', ' ')
            trans_dict[words.strip().lower()] = transcription.strip().lower()
        except:
            print(line.strip())
            print(pairs)

    return trans_dict


def read_foreign_2words(path):
    trans_dict = dict()
    fo = open(path, 'r')
    f_error = open('resources/error.txt', 'w')
    for line in fo:
        pairs = line.split('\t')
        words = pairs[0].split()
        transcription = pairs[1].split()
        if len(words) != len(transcription):
            f_error.write(line)
            continue
        for i in range(len(words)):
            trans_dict[words[i].strip().lower()] = transcription[i].strip().lower()

    return trans_dict


# manually tokenize
def norm_word(word):
    char = list(word)
    pre_is_word = False
    pre_is_punct = False
    punct = '! " “ \' ( ) - / : ; ? + [ ] _ ` { | } ~ ” – `` '' – ” ...'.split()
    for i in range(len(char)):
        # if char[i] in punctuation:
        if char[i] in punct:
            if pre_is_word:
                char[i] = ' ' + char[i]
                # print(char)
            else:
                char[i] = char[i] + ' '
            pre_is_word = False
            pre_is_punct = True
        else:
            if pre_is_punct:
                char[i] = ' ' + char[i]
            pre_is_word = True
            pre_is_punct = False

    return ''.join(char)


def replace_multi_period(str):
    str = re.sub('(\.+\s+)+\.*', ' . ', str)
    str = re.sub('\.{2, 100}', ' . ', str)
    return str


def replace_multi_space(str):
    str = re.sub(' +', ' ', str)
    return str

# print(replace_multi_period("Mức giá này giảm 600.000 đồng/lượng theo cả 2 chiều mua vào và bán ra so với phiên giao dịch gần nhất . Tại thị trường thế giới, giá vàng đang được giao dịch tại ngưỡng 1.459,2 USD/ounce (Theo Kitco News)."))

def tokenize(input_str):
    tokens = word_tokenize(input_str)
    # for i in range(len(tokens)):
    #     tokens[i] = norm_word(tokens[i])

    input_str = " ".join(tokens)

    return replace_multi_space(input_str)


def convert_csv_to_txt(f_csv, delimiter):
    df = pd.read_csv(f_csv, delimiter=delimiter)
    words = df.word.values.tolist()
    transcription = df.transcription.values.tolist()
    txt_name = f_csv.replace('.csv', '.txt')
    fo = open(txt_name, 'w')
    assert len(words) == len(transcription), 'len(words) != len(transcription)'
    for i in range(len(words)):
        fo.write(str(words[i]).strip() + '\t' + str(transcription[i]).strip() + '\n')

# print(read_txt_two_cols('resources/abbre_correct.txt'))
# print(read_txt_two_cols('resources/foreign.txt'))
# convert_csv_to_txt('resources/foreign.csv', delimiter=',')
# check_foreign('resources/foreign.txt')
# read_foreign_2words('resources/foreign_2words.txt')


def check_foreign(f_foreign):
    fout = open('resources/foreign_2words.txt', 'w')
    count = 0
    fo = open(f_foreign, 'r')
    for line in fo:
        pairs = line.split('\t')
        words = pairs[0]
        if len(words.split()) > 2:
            count += 1
            print(words)
            fout.write(line)
    print(count)

 