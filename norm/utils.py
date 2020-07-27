import string
from nltk.util import ngrams
import collections
import pandas as pd
import glob
import re
import csv
import copy
from random import shuffle
import unidecode
import unicodedata


def filter_by_empty(file_name):
    # sed -i '/^$/d' main.txt
    # awk 'NF > 0' main.txt > out.txt
    fhand = open(file_name)
    fout = open('./filter_by_empty.txt', 'w')
    line_count = 0
    for line in fhand:
        if (line != '\n'):
            fout.write(line)
            line_count += 1
    print(line_count)
    fhand.close()
    fout.close()


def filter_by_dup(file_name):
    # awk '!seen[$0]++' data.txt > output.txt
    fhand = open(file_name)
    fout = open("./filter_by_dup.txt", "w")
    line_count = 0
    lines_seen = set()
    for line in fhand:
        if line not in lines_seen:
            fout.write(line)
            lines_seen.add(line)
            line_count += 1
    fhand.close()
    fout.close()


def filter_by_len(len_min, len_max, file_name):
    fhand = open(file_name)
    fout = open("./filter_by_len.txt", "w")
    line_count = 0
    for line in fhand:
        if len(line.split()) < len_max and len(line.split()) > len_min:
            fout.write(line)
            line_count += 1 
    print(line_count)
    fhand.close()
    fout.close()


def filter_by_emoji(file_name):
    # sed -i '/^$/d' main.txt
    # awk 'NF > 0' main.txt > out.txt
    vi_char_lower = 'đàằầèềìòồờừỳùáắấéếíóốớứýúảẳẩẻểỉỏổởửỷủãẵẫẽễĩõỗỡữỹũạặậẹệịọộợựỵụăâêôơư'

    vi_char_uppper = 'ĐÀẰẦÈỀÌÒỒỜỪỲÙÁẮẤÉẾÍÓỐỚỨÝÚẢẲẨẺỂỈỎỔỞỬỶỦÃẴẪẼỄĨÕỖỠỮỸŨẠẶẬẸỆỊỌỘỢỰỴỤĂÂÊÔƠƯ'
    not_emoji_char = string.printable + vi_char_lower + vi_char_uppper
    fhand = open(file_name)
    fout = open('./filter_by_emoji.txt', 'w')
    for line in fhand:
        line = line.replace('<3', ' ')
        for char in line:
            if char not in not_emoji_char:
                line = line.replace(char, ' ')
        fout.write(line)
    fhand.close()
    fout.close()


def shuffle_line(file_name):
    # shuf -n 1000 cong_nghe.txt -o 1k_cong_nghe.txt
    return None


def filter_by_url(file_name):
    fhand = open(file_name)
    fout = open('./filter_by_url.txt', 'w')
    line_count = 0
    for line in fhand:
        if (line.find('http') == -1 and line.find('www') == -1):
            fout.write(line)
            line_count += 1
    print(line_count)
    fhand.close()
    fout.close()


def pattern_by_cat(file_name):
    fhand = open("/home/tuyen/src/data/news_VQB/test_having_num.txt")
    fout = open("/home/tuyen/src/data/news_VQB/p_by_cat/xeco.txt", "w")

    f_cat = open(file_name)

    l = []
    for line in f_cat:
        l.append(line)

    for line in fhand:
        pattern = line.split('\t')[0]
        input_line = line.split('\t')[1] + '\n'
        norm_line = line.split('\t')[2]
        if input_line in l:
            fout.write(pattern + '\t' + input_line)
    
    fhand.close()
    fout.close()
    f_cat.close()


def ngrams_by_cat(file_name):
    
    fhand = open(file_name)
    s = ''
    
    for line in fhand:
        line = line.strip()
        s += line.split('\t')[1]
    
    tokens = [token for token in s.split(" ") if token != ""]
    
    ngrams_2 = list(ngrams(tokens, 2))
    ngrams_3 = list(ngrams(tokens, 3))
    counter_2 = collections.Counter(ngrams_2)
    print(counter_2.most_common(50))
    counter_3 = collections.Counter(ngrams_3)
    print(counter_3.most_common(10))

    fhand.close()


def check_tag(tag, tag2count):
    if 'PUNCT' in tag:
        tag2count['punct'] = tag2count['punct'] + 1
    if 'VERBATIM' in tag:
        tag2count['verbatim'] = tag2count['verbatim'] + 1
    if 'MEASURE' in tag:
        tag2count['measure'] = tag2count['measure'] + 1
    if 'DATE' in tag:
        tag2count['date'] = tag2count['date'] + 1
    if 'TIME' in tag:
        tag2count['time'] = tag2count['time'] + 1
    if 'CARDINAL' in tag:
        tag2count['cardinal'] = tag2count['cardinal'] + 1
    if 'DECIMAL' in tag:
        tag2count['decimal'] = tag2count['decimal'] + 1
    if 'DIGIT' in tag:
        tag2count['digit'] = tag2count['digit'] + 1
    if 'ROMAN' in tag:
        tag2count['roman'] = tag2count['roman'] + 1
    if 'LETTER' in tag:
        tag2count['letter'] = tag2count['letter'] + 1
    if 'FOREIGN' in tag:
        tag2count['foreign'] = tag2count['foreign'] + 1
    if 'ABBRE' in tag:
        tag2count['abbre'] = tag2count['abbre'] + 1
    if 'FRACTION' in tag:
        tag2count['fraction'] = tag2count['fraction'] + 1

    return tag2count


def save_conll(word_list, tag_list, conll_file):
    f_out = open(conll_file, 'w')
    for i in range(len(word_list)):
        for word, tag in zip(word_list[i], tag_list[i]):
            f_out.write(word + '\t' + tag + '\n')
        f_out.write('\n')


def get_data_by_class(csv_pattern, num_sample_per_class):

    sample_plain = list()
    sample_punct = list()
    sample_measure = list()
    sample_verba = list()
    sample_date = list()
    sample_time = list()
    sample_cardinal = list()
    sample_decimal = list()
    sample_digit = list()
    sample_roman = list()
    sample_letter = list()
    sample_foreign = list()
    sample_abbre = list()

    total_samples = list()

    for csv_file in glob.glob(csv_pattern):
        print(csv_file)

        df = pd.read_csv(csv_file, header=None, names=['origin', 'written', 'spoken'], delimiter='\t')
        origin = df['origin'].values.tolist()
        written = df['written'].values.tolist()
        spoken = df['spoken'].values.tolist()

        for o, w, s in zip(origin, written, spoken):
            if '<MEASURE>' in w and len(sample_measure) < num_sample_per_class:
                sample_measure.append((o, s, w))
            elif '<VERBATIM>' in w and len(sample_verba) < num_sample_per_class:
                sample_verba.append((o, s, w))
            elif '<DATE>' in w and len(sample_date) < num_sample_per_class:
                sample_date.append((o, s, w))
            elif '<TIME>' in w and len(sample_time) < num_sample_per_class:
                sample_time.append((o, s, w))
            elif '<CARDINAL>' in w and len(sample_cardinal) < num_sample_per_class:
                sample_cardinal.append((o, s, w))
            elif '<DECIMAL>' in w and len(sample_decimal) < num_sample_per_class:
                sample_decimal.append((o, s, w))
            elif '<DIGIT>' in w and len(sample_digit) < num_sample_per_class:
                sample_digit.append((o, s, w))
            elif '<ROMAN>' in w and len(sample_roman) < num_sample_per_class:
                sample_roman.append((o, s, w))
            elif '<LETTER>' in w and len(sample_letter) < num_sample_per_class:
                sample_letter.append((o, s, w))
            elif '<PUNCT>' in w and len(sample_punct) < num_sample_per_class:
                sample_punct.append((o, s, w))
            elif len(sample_plain) < num_sample_per_class:
                sample_plain.append((o, s, w))

        print('len measure: ', len(sample_measure))
        print('len verbe: ', len(sample_verba))
        print('len date: ', len(sample_date))
        print('len time: ', len(sample_time))
        print('len cardinal: ', len(sample_cardinal))
        print('len decimal: ', len(sample_decimal))
        print('len digit: ', len(sample_digit))
        print('len roman: ', len(sample_roman))
        print('len letter: ', len(sample_letter))
        print('len plain: ', len(sample_plain))
        print('len punct: ', len(sample_punct))

        if len(sample_measure) == num_sample_per_class and len(sample_verba) == num_sample_per_class and \
            len(sample_date) == num_sample_per_class and len(sample_time) == num_sample_per_class and \
            len(sample_cardinal) == num_sample_per_class  and len(sample_decimal) == num_sample_per_class and \
            len(sample_digit) == num_sample_per_class and len(sample_roman) == num_sample_per_class  and \
            len(sample_letter) == num_sample_per_class and len(sample_punct) == num_sample_per_class\
                and len(sample_plain) == num_sample_per_class: break

    total_samples.extend(sample_measure)
    total_samples.extend(sample_verba)
    total_samples.extend(sample_date)
    total_samples.extend(sample_time)
    total_samples.extend(sample_cardinal)
    total_samples.extend(sample_decimal)
    total_samples.extend(sample_digit)
    total_samples.extend(sample_roman)
    total_samples.extend(sample_letter)
    total_samples.extend(sample_plain)
    total_samples.extend(sample_punct)

    return total_samples


def convert_to_norm_format(csv_file_pattern):
    for csv_file in glob.glob(csv_file_pattern):
        print(csv_file)
        df = pd.read_csv(csv_file, delimiter='\t')
        origin = df['origin'].values.tolist()
        written = df['written'].values.tolist()
        spoken = df['spoken'].values.tolist()

        cls = {'<PUNCT>':'</PUNCT>', '<MEASURE>':'</MEASURE>', '<DATE>':'</DATE>', '<TIME>':'</TIME>',
               '<VERBATIM>':'</VERBATIM>', '<CARDINAL>':'</CARDINAL>', '<ROMAN>':'</ROMAN>',
               '<DIGIT>':'</DIGIT>', '<DECIMAL>':'</DECIMAL>', '<ADDRESS>':'</ADDRESS>',
               '<LETTER>':'</LETTER>'}

        csv_file_out = csv_file.replace('.csv', '_token.csv')
        fo = open(csv_file_out, 'w')
        csv_writer = csv.writer(fo, delimiter='\t')
        csv_writer.writerow(['class', 'written_form', 'spoken_form'])

        count = 0
        for i in range(0, len(origin)):
            count += 1
            origin_line = origin[i]
            written_line = written[i]
            spoken_line = spoken[i]

            written_partern_iter = re.finditer('<PUNCT>[^(<\/PUNCT>)]+<\/PUNCT>|<MEASURE>[^(</MEASURE>)]+<\/MEASURE>|'
                                         '<CARDINAL>[^(</CARDINAL>)]+<\/CARDINAL>|<DATE>[^(</DATE>)]+<\/DATE>|'
                                         '<TIME>[^(<\/TIME>)]+<\/TIME>|<VERBATIM>[^(</VERBATIM>)]+<\/VERBATIM>|'
                                         '<ROMAN>[^(<\/ROMAN>)]+<\/ROMAN>|<DECIMAL>[^(</DECIMAL>)]+<\/DECIMAL>|'
                                         '<ADDRESS>[^(<\/ADDRESS>)]+<\/ADDRESS>|<FRACTION>[^(</FRACTION>)]+<\/FRACTION>|'
                                         '<DIGIT>[^(<\/DIGIT>)]+<\/DIGIT>|<DATE>[^(<DATE>)]+<DATE>', written_line)


            spoken_partern_iter = re.finditer('<PUNCT>[^(<\/PUNCT>)]+<\/PUNCT>|<MEASURE>[^(</MEASURE>)]+<\/MEASURE>|'
                                               '<CARDINAL>[^(</CARDINAL>)]+<\/CARDINAL>|<DATE>[^(</DATE>)]+<\/DATE>|'
                                               '<TIME>[^(<\/TIME>)]+<\/TIME>|<VERBATIM>[^(</VERBATIM>)]+<\/VERBATIM>|'
                                               '<ROMAN>[^(<\/ROMAN>)]+<\/ROMAN>|<DECIMAL>[^(</DECIMAL>)]+<\/DECIMAL>|'
                                               '<ADDRESS>[^(<\/ADDRESS>)]+<\/ADDRESS>|<FRACTION>[^(</FRACTION>)]+<\/FRACTION>|'
                                               '<DIGIT>[^(<\/DIGIT>)]+<\/DIGIT>|<DATE>[^(<DATE>)]+<DATE>', spoken_line)

            written_line_part = list()
            start = 0
            for m in written_partern_iter:
                written_line_part.extend(written_line[start:m.start()].strip().split())
                written_line_part.append(m.group())
                start = m.end()
            written_line_part.append(written_line[start:].split())

            spoken_line_part = list()
            start = 0
            for m in spoken_partern_iter:
                spoken_line_part.extend(spoken_line[start:m.start()].strip().split())
                spoken_line_part.append(m.group())
                start = m.end()
            spoken_line_part.extend(spoken_line[start:].split())

            for written_term, spoken_term in zip(written_line_part, spoken_line_part):
                if written_term == spoken_term:
                    csv_writer.writerow(['PLAIN', written_term, '<self>'])
                else:
                    for k, v in cls.items():
                        if k in written_term:
                            try:
                                term_w = written_term.replace(k, '')
                                term_w = term_w.replace(v, '')
                                term_s = spoken_term.replace(k, '')
                                term_s = term_s.replace(v, '')
                                k = k[1:len(k) - 1]
                                csv_writer.writerow([k, str(term_w), term_s])
                                break
                            except:
                                print('written term: ', written_term)
                                print('spoken term: ', spoken_term)
                                pass
            csv_writer.writerow(['eos', 'eos', ''])


def convert_to_conll_format(csv_file):
    df = pd.read_csv(csv_file, delimiter='\t')
    origin = df['origin'].values.tolist()
    written = df['written'].values.tolist()
    spoken = df['spoken'].values.tolist()

    vnese_lower = 'aáàảãạăắằẳẵặâấầẩẫậeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵdđ'
    vnese_upper = 'AÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬEÉÈẺẼẸÊẾỀỂỄỆIÍÌỈĨỊOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢUÚÙỦŨỤƯỨỪỬỮỰYÝỲỶỸỴDĐ'
    character = 'a-zA-Z'
    number = '0-9'

    cls = {'<PUNCT>': '</PUNCT>',
           '<FOREIGN>': '</FOREIGN>',
           '<MEASURE>': '</MEASURE>',
           '<CARDINAL>': '</CARDINAL>',
           '<VERBATIM>': '</VERBATIM>',
           '<ROMAN>': '</ROMAN>',
           '<DATE>': '</DATE>',
           '<TIME>': '</TIME>',
           '<DIGIT>': '</DIGIT>',
           '<ABBRE>': '</ABBRE>',
           '<FRACTION>': '</FRACTION>',
           '<DECIMAL>': '</DECIMAL>',
           '<ADDRESS>': '</ADDRESS>',
           '<LETTER>': '</LETTER>'}

    csv_tts = csv_file.replace('.csv', '_tts.conll')
    csv_asr = csv_file.replace('.csv', '_asr.conll')
    csv_norm = csv_file.replace('.csv', '_seq2seq.csv')
    f_tts = open(csv_tts, 'w')
    f_asr = open(csv_asr, 'w')
    f_norm = open(csv_norm, 'w')
    csv_norm = csv.writer(f_norm, delimiter='\t')
    csv_norm.writerow(['tag', 'written', 'spoken'])

    count = 0
    for i in range(0, len(origin)):
        count += 1
        origin_line = origin[i]
        written_line = written[i]
        spoken_line = spoken[i]


        written_partern_iter = re.finditer('<PUNCT>((?!PUNCT).)*?<\/PUNCT>|'
                                           '<FOREIGN>((?!FOREIGN).)*?<\/FOREIGN>|'
                                           '<MEASURE>((?!MEASURE).)*?<\/MEASURE>|'
                                           '<CARDINAL>((?!CARDINAL).)*?<\/CARDINAL>|'
                                           '<VERBATIM>((?!VERBATIM).)*?<\/DATE>|'
                                           '<ROMAN>((?!ROMAN).)*?<\/ROMAN>|'
                                           '<DATE>((?!DATE).)*?<\/DATE>|'
                                           '<TIME>((?!TIME).)*?<\/TIME>|'
                                           '<LETTER>((?!LETTER).)*?<\/LETTER>|'
                                           '<DIGIT>((?!DIGIT).)*?<\/DIGIT>|'
                                           '<ABBRE>((?!ABBRE).)*?<\/ABBRE>|'
                                           '<FRACTION>((?!FRACTION).)*?<\/FRACTION>|'
                                           '<DECIMAL>((?!DECIMAL).)*?<\/DECIMAL>|'
                                           '<ADDRESS>((?!ADDRESS).)*?<\/ADDRESS>', written_line)

        spoken_partern_iter = re.finditer('<PUNCT>((?!PUNCT).)*?<\/PUNCT>|'
                                           '<FOREIGN>((?!FOREIGN).)*?<\/FOREIGN>|'
                                           '<MEASURE>((?!MEASURE).)*?<\/MEASURE>|'
                                           '<CARDINAL>((?!CARDINAL).)*?<\/CARDINAL>|'
                                           '<VERBATIM>((?!VERBATIM).)*?<\/DATE>|'
                                           '<ROMAN>((?!ROMAN).)*?<\/ROMAN>|'
                                           '<DATE>((?!DATE).)*?<\/DATE>|'
                                           '<TIME>((?!TIME).)*?<\/TIME>|'
                                           '<LETTER>((?!LETTER).)*?<\/LETTER>|'
                                           '<DIGIT>((?!DIGIT).)*?<\/DIGIT>|'
                                           '<ABBRE>((?!ABBRE).)*?<\/ABBRE>|'
                                           '<FRACTION>((?!FRACTION).)*?<\/FRACTION>|'
                                           '<DECIMAL>((?!DECIMAL).)*?<\/DECIMAL>|'
                                           '<ADDRESS>((?!ADDRESS).)*?<\/ADDRESS>', spoken_line)

        # match with written form
        written_line_part = list()
        start = 0
        for m in written_partern_iter:
            written_line_part.extend(written_line[start:m.start()].strip().split())
            written_line_part.append(m.group())
            start = m.end()
        written_line_part.append(written_line[start:].split())

        # match with spoken form
        spoken_line_part = list()
        start = 0
        for m in spoken_partern_iter:
            spoken_line_part.extend(spoken_line[start:m.start()].strip().split())
            spoken_line_part.append(m.group())
            start = m.end()
        spoken_line_part.extend(spoken_line[start:].split())

        for written_term, spoken_term in zip(written_line_part, spoken_line_part):
            if written_term == spoken_term:
                f_tts.write(written_term + '\tO\n')
                f_asr.write(written_term + '\tO\n')
            else:
                for start_tag, end_tag in cls.items():
                    if start_tag in written_term and start_tag in spoken_term:
                        try:
                            written_term_w = written_term.replace(start_tag, '') # remove start tag
                            written_term_w = written_term_w.replace(end_tag, '') # remove end tag
                            spoken_term_w = spoken_term.replace(start_tag, '')  # remove start tag
                            spoken_term_w = spoken_term_w.replace(end_tag, '')  # remove end tag

                            start_tag = start_tag[1:len(start_tag) - 1] # remove < and > token

                            if len(written_term_w) > 0:
                                words = written_term_w.split()
                                f_tts.write(words[0] + '\tB-' + start_tag + '\n')
                                for i in range(1, len(words)):
                                    f_tts.write(words[i] + '\tI-' + start_tag + '\n')

                            if len(spoken_term_w) > 0:
                                words = spoken_term_w.split()
                                f_asr.write(words[0] + '\tB-' + start_tag + '\n')
                                for i in range(1, len(words)):
                                    f_asr.write(words[i] + '\tI-' + start_tag + '\n')
                            if start_tag != 'PUNCT':
                                csv_norm.writerow([start_tag, written_term_w, spoken_term_w])

                            break
                        except:
                            print('Exception written: ')
                            print('written term: ', written_term)
                            print('spoken term: ', spoken_term)
                            print('-------------------------------------------------')
                            pass

        f_tts.write('\n')
        f_asr.write('\n')


def extract_ner_tag(ner_output):

    cls = {'<PUNCT>': '</PUNCT>',
           '<MEASURE>': '</MEASURE>',
           '<CARDINAL>': '</CARDINAL>',
           '<DATE>': '</DATE>',
           '<TIME>': '</TIME>',
           '<VERBATIM>': '</VERBATIM>',
           '<ROMAN>': '</ROMAN>',
           '<DECIMAL>': '</DECIMAL>',
           '<ADDRESS>': '</ADDRESS>',
           '<FRACTION>': '</FRACTION>',
           '<ABBRE>': '</ABBRE>',
           '<FOREIGN>': '</FOREIGN>',
           '<DIGIT>': '</DIGIT>',
           '<LETTER>': '</LETTER>'}

    # written_partern_iter = re.finditer('<PUNCT>[^<\/PUNCT>]+<\/PUNCT>|<MEASURE>[^</MEASURE>]+<\/MEASURE>|'
    #                                    '<CARDINAL>[^</CARDINAL>]+<\/CARDINAL>|<DATE>[^<DATE>]+<\/DATE>|'
    #                                    '<TIME>[^<\/TIME>]+<\/TIME>|<VERBATIM>[^</VERBATIM>]+<\/VERBATIM>|'
    #                                    '<ROMAN>[^<\/ROMAN>]+<\/ROMAN>|<DECIMAL>[^</DECIMAL>]+<\/DECIMAL>|'
    #                                    '<ADDRESS>[^<ADDRESS>]+<\/ADDRESS>|<FRACTION>[^<FRACTION>]+<\/FRACTION>|'
    #                                    '<DIGIT>[^<\/DIGIT>]+<\/DIGIT>', ner_output)


    written_partern_iter = re.finditer('<PUNCT>((?!PUNCT).)*?<\/PUNCT>|'
                                       '<MEASURE>((?!MEASURE).)*?<\/MEASURE>|'
                                       '<CARDINAL>((?!CARDINAL).)*?<\/CARDINAL>|'
                                       '<DATE>((?!DATE).)*?<\/DATE>|'
                                       '<TIME>((?!TIME).)*?<\/TIME>|'
                                       '<VERBATIM>((?!VERBATIM).)*?<\/VERBATIM>|'
                                       '<ROMAN>((?!ROMAN).)*?<\/ROMAN>|'
                                       '<DECIMAL>((?!DECIMAL).)*?<\/DECIMAL>|'
                                       '<ADDRESS>((?!ADDRESS).)*?<\/ADDRESS>|'
                                       '<FRACTION>((?!FRACTION).)*?<\/FRACTION>|'
                                       '<LETTER>((?!LETTER).)*?<\/LETTER>|'
                                       '<DIGIT>((?!DIGIT).)*?<\/DIGIT>', ner_output)


    written_line_part = list()
    start = 0
    for m in written_partern_iter:
        written_line_part.extend(ner_output[start:m.start()].strip().split()) # get tokens from left of Match
        written_line_part.append(m.group())
        start = m.end()
    written_line_part.append(ner_output[start:].split())

    written_term_list = list()

    for written_term in written_line_part:
        for k, v in cls.items():
            if k in written_term:
                written_term_list.append(written_term)
                break

    return written_term_list


def extract_term_from_ner_tag(ner_tag, start_tag, end_tag):
    ner_tag = ner_tag.replace(start_tag, '')
    ner_tag = ner_tag.replace(end_tag, '')

    return ner_tag.strip()


def process_foreign_words(f_foreign, f_news):
    df = pd.read_csv(f_foreign)
    words_foreign = df.word.values.tolist()
    trans_foreign= df.transcription.values.tolist()

    trans_dict = dict(zip(words_foreign, trans_foreign))

    origins = list()
    writtens = list()
    spokens = list()

    csv_writer = csv.writer(open('../data/ner_raw_foreign.csv', 'w'), delimiter='\t')
    csv_writer.writerow(['origin', 'written', 'spoken'])

    fo = open(f_news, 'r')
    count = 0
    count_sample = 0

    key2count = dict()

    lines = fo.readlines()
    shuffle(lines)

    for line in lines:

        count += 1
        print('\r count = %d' % count, end='\r')

        is_foreign = False

        words = line.split()
        written_words = copy.deepcopy(words)
        spoken_words = copy.deepcopy(written_words)

        for i in range(len(words)):
            if written_words[i] in trans_dict.keys():
                if written_words[i] not in key2count:
                    key2count[written_words[i]] = 1
                    is_foreign = True
                elif key2count[written_words[i]] < 100:
                    key2count[written_words[i]] = key2count[written_words[i]] + 1
                    is_foreign = True
                elif key2count[written_words[i]] >= 100:
                    is_foreign = False
                    break

                if is_foreign:
                    # print(' '.join(words))
                    # print('words: ', written_words[i], ' - values: ', trans_dict[written_words[i]])
                    count_sample += 1
                    print('\r count sample: %d' % count_sample)
                    spoken_words[i] = '<FOREIGN>' + str(trans_dict[written_words[i]]) + '</FOREIGN>'
                    written_words[i] = '<FOREIGN>' + written_words[i] + '</FOREIGN>'
                    # print('------------------------------------------------------------------------------------')

        origins.append(' '.join(words))
        writtens.append(' '.join(written_words))
        spokens.append(' '.join(spoken_words))

        if is_foreign:
            csv_writer.writerow([' '.join(words), ' '.join(written_words), ' '.join(spoken_words)])

        if count_sample == 600000: break


def read_vocab(f_vocab):
    fo = open(f_vocab, 'r')
    vocab = dict()
    for line in fo:
        words = line.split('\t')
        vocab[words[0]] = int(words[1])

    return vocab


def check_abbre(f_abbre):
    fo = open(f_abbre, 'r')
    f_2words = open('../resources/abbre_2words.txt', 'w')
    f_error_1 = open('../resources/abbre_error_1.txt', 'w')
    f_error_2 = open('../resources/abbre_error_2.txt', 'w')
    f_correct = open('../resources/abbre_correct.txt', 'w')
    for line in fo:
        abbre = line.split('\t')
        if len(abbre[0]) == 2:
            f_2words.write(line)
        else:
            words = abbre[1].split()
            orign_words = copy.deepcopy(words)
            for i in range(len(words)):
                words[i] = words[i][0]
            w = ''.join(words)
            if ''.join(c for c in unicodedata.normalize('NFD', w.upper()) if unicodedata.category(c) != 'Mn') != abbre[0]:
                f_error_2.write(' '.join(orign_words) + ' - ' + unidecode.unidecode(w.upper()) + ' - ' + abbre[0] + '\n')
                f_error_1.write(line)
            else:
                f_correct.write(line)


def check_abbre_v2(f_abbre, f_vocab):
    vocab = read_vocab(f_vocab)
    fo = open(f_abbre, 'r')
    f_correct_requence = open('../resources/abbre_correct_frequence.txt', 'w')
    f_wrong_requence = open('../resources/abbre_wrong_frequence.txt', 'w')
    for line in fo:
        abbre = line.split('\t')
        if abbre[0].lower() in vocab.keys() and vocab[abbre[0].lower()] > 1000:
            f_correct_requence.write(line.strip() + '\t' + str(vocab[abbre[0].lower()]) + '\n')
        elif abbre[0].lower() in vocab.keys():
            f_wrong_requence.write(line.strip() + '\t' + str(vocab[abbre[0].lower()]) + '\n')
        else:
            pass


def remove_tag(str):
    cls = {'<PUNCT>': '</PUNCT>',
           '<MEASURE>': '</MEASURE>',
           '<CARDINAL>': '</CARDINAL>',
           '<DATE>': '</DATE>',
           '<TIME>': '</TIME>',
           '<VERBATIM>': '</VERBATIM>',
           '<ROMAN>': '</ROMAN>',
           '<DECIMAL>': '</DECIMAL>',
           '<ADDRESS>': '</ADDRESS>',
           '<FRACTION>': '</FRACTION>',
           '<ABBRE>': '</ABBRE>',
           '<FOREIGN>': '</FOREIGN>',
           '<DIGIT>': '</DIGIT>',
           '<LETTER>': '</LETTER>'}
    for tag_start, tag_end in cls.items():
        str = str.replace(tag_start, '')
        str = str.replace(tag_end, '')

    return str


# check_abbre('../resources/Abbr_1100_13Aug.txt')
# check_abbre_v2('../resources/Abbr_1100_13Aug.txt', '../resources/vocab.txt.normalized')
# process_foreign_words('../resources/foreign.csv', '/media/nghidinh/DATA/data/text_corpus/News_corpus_VuQuocBinh/corpus-full-v2-normalized.txt')


# written_term_list = extract_ner_tag('Trung tá Nguyễn Bình Ngọc <PUNCT> , </PUNCT> phó trưởng Công an quận cho biết <PUNCT> , </PUNCT> khoảng <TIME> 10h06 </TIME> ngày <DATE> 2-8 </DATE> <PUNCT> , </PUNCT> Công an phường Cổ Nhuế <CARDINAL> 1 </CARDINAL> tiếp nhận đơn trình báo về việc một số nhân viên trường Pascal của bà Lê Thị Bích Dung <PUNCT> , </PUNCT> phó giám đốc Công ty CP Đầu tư phát triển giáo dục TDS Việt Nam <PUNCT> ( </PUNCT> Công ty TDS <PUNCT> ) </PUNCT> bị người của bà Trần Kim Phương <PUNCT> , </PUNCT> Chủ tịch HĐQT Công ty TDS bắt giữ tại lô TH1 <PUNCT> , </PUNCT> khu đô thị mới Cổ Nhuế <PUNCT> , </PUNCT> phường Cổ Nhuế <CARDINAL> 1 </CARDINAL> <PUNCT> . </PUNCT>')
# print(written_term_list)

# def gen_data(cls, written_term):
#     if cls == 'CARDINAL':
#         spoken_term = read.num2words_fixed(int(written_term))
#         print(num)


# convert_to_norm_format('../data/ner_raw_data.csv')
# gen_data('','')
