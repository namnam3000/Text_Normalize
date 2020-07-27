from flask import Flask, jsonify, request
import sys, os
import json
import configparser
import re
import norm.utils as norm_utils
import utils
import norm.normalize as normalize
import norm.read as read
import nltk
import VietnameseTextNormalizer as ViN
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def send_response(response_obj):
    response = jsonify(response_obj)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', 'accept,content-type,Origin,X-Requested-With,Content-Type,access_token,Accept,Authorization,source')
    response.headers.add('Access-Control-Allow-Credentials', True)
    return response




def normalize(sample):
    sample = utils.replace_multi_period(sample)

    # Tokenize
    sample_processed = utils.tokenize(sample)

    # Check abbre and foreign dict
    words = sample_processed.split()
    # print(words)
    words, idx_norm_by_dict = check_dict(words, abbre_dict)
    sample_processed = ' '.join(words)

    # print('SAMPLE PROCESSED: ', sample_processed)

    # Norm by rule
    sample_processed = norm_by_rule(sample_processed, ['code', 'verbatim', 'phone_single', 'norm_x', 'negative_number', 'number_plate', 'digit', 'phone', 'cardinal', 'measure', 'date', 'number_range', 'date_range', 'fraction', 'time', 'sport_score', 'roman', 'numletseq'])
    # print('NORM BY RULE: ', sample_processed)


    sample_processed = utils.replace_multi_period(sample_processed)

    # Lower case
    words = sample_processed.lower().strip().split()
    # Remove word not in vocab
    # print('BEFORE REMOVE BY TTS DICT'.upper(), words)
    words = check_punct(words)
    # words = check_tts_word(words, tts_words)
    # print('output: ', words)
    result = utils.replace_multi_space(' '.join(words).strip())
    result_list = nltk.sent_tokenize(result)
    result_list_out = []
    for sent in result_list:
        result_list_out.extend(split_sentence(sent))
    # print('INPUT: ', sample)
    # print('RESULT: ', result)

    # return send_response({'result':result})
    # return send_response({'result': result, 'result_list': result_list_out})
    return result
    

def fix_special_punct(ner_output):
    pattern = '[a-zA-Z]-[a-zA-Z]'
    match = re.findall(pattern, ner_output)
    for m in match:
        new_m = re.sub('-', ' , ', m)
        ner_output = re.sub(m, new_m, ner_output)
    return ner_output


def check_punct(words):
    punctuation = list(',:[]{}()\?\!\-\`\'\"\.')
    # punctuation = list('\?\!')
    special_punct = ['’']
    words_out = list()
    
    consecutive_punct = False
    for word in words:
        word = utils.norm_word(word)
        # print(word)
        for w in word.strip().split(' '):
            if w in special_punct:
                continue
            if w.strip() not in punctuation:
                # if is_valid_word(w):
                consecutive_punct = False
                words_out.append(w)
            elif w == '?' or w == '!' or w == '.' or w == ',' and not consecutive_punct:
                consecutive_punct = True
                words_out.append(w)
            else:
                if not consecutive_punct:
                    words_out.append(' ')
                consecutive_punct = True
            # print(words_out)
    return words_out


def is_valid_word(word):
    vi_char_lower = 'đàằầèềìòồờừỳùáắấéếíóốớứýúảẳẩẻểỉỏổởửỷủãẵẫẽễĩõỗỡữỹũạặậẹệịọộợựỵụăâêôơưk'
    vi_char_uppper = 'ĐÀẰẦÈỀÌÒỒỜỪỲÙÁẮẤÉẾÍÓỐỚỨÝÚẢẲẨẺỂỈỎỔỞỬỶỦÃẴẪẼỄĨÕỖỠỮỸŨẠẶẬẸỆỊỌỘỢỰỴỤĂÂÊÔƠƯK'
    pattern = '[^a-zA-Z' + vi_char_lower + vi_char_uppper + ']'
    if re.search(pattern, word):
        return False
    return True


def check_dict(words, abbre_dict):
    idx_norm_by_dict = list()
    deviation = 0
    for i in range(0, len(words)):
        if words[i] in abbre_dict:
            words[i] = abbre_dict[words[i]]
            idx_norm_by_dict.append(i)
            for j in range(1, deviation + 1):
                idx_norm_by_dict.append(i + j)
            deviation = len(words[i].split()) - 1
        # elif words[i].lower() in foreign_dict:
        #     words[i] = foreign_dict[words[i].lower()]
        #     idx_norm_by_dict.append(i)
        #     for j in range(1, deviation + 1):
        #         idx_norm_by_dict.append(i + j)
        #     deviation = len(words[i].split()) - 1

    return words, idx_norm_by_dict


def check_tts_word(words, tts_words):
    for i in range(len(words)):
        if words[i] not in tts_words:
            global oov_dict
            oov_dict = utils.add_oov(words[i], oov_dict)
            utils.write_oov_dict(oov_dict, config['resources']['oov_path'])
            words[i] = words[i]

    return words


def norm_by_rule(str, types):
    if 'norm_x' in types:
        str = norm_utils.remove_tag(normalize.norm_x(str, str)[1])
    if 'date_range' in types:
        str = norm_utils.remove_tag(normalize.normalize_date_range(str, str)[1])
    if 'date' in types:
        str = norm_utils.remove_tag(normalize.normalize_date(str, str)[1])
    if 'time' in types:
        str = norm_utils.remove_tag(normalize.normalize_time(str, str)[1])
    if 'fraction' in types:
        str = norm_utils.remove_tag(normalize.norm_tag_fraction(str, str)[1])
    if 'measure' in types:
        str = normalize.norm_measure(str, config['norm-pattern'])
    if 'number_range' in types:
        str = norm_utils.remove_tag(normalize.normalize_number_range(str, str)[1])
    if 'number_plate' in types:
        str = norm_utils.remove_tag(normalize.normalize_number_plate(str, str)[1])
    if 'phone' in types:
        str = norm_utils.remove_tag(normalize.normalize_phone_number(str, str)[1])
    if 'phone_single' in types:
        str = norm_utils.remove_tag(normalize.phone_single(str, str)[1])
    if 'digit' in types:
        str = norm_utils.remove_tag(normalize.norm_digit(str, str)[1])
    if 'sport_score' in types:
        str = norm_utils.remove_tag(normalize.normalize_sport_score(str, str)[1])
    if 'negative_number' in types:
        str = norm_utils.remove_tag(normalize.normalize_negative_number(str, str)[1])
    if 'numletseq' in types:
        tokens = str.split()
        str_norm = ''
        for token in tokens:
            str_norm = str_norm + ' ' + utils.norm_word(token)
        str = str_norm.strip()
    if 'code' in types:
        str = norm_utils.remove_tag(normalize.norm_code_type_1(str, str)[1])
        # print(str)
    if 'cardinal' in types:
        str = norm_utils.remove_tag(normalize.normalize_number(str, str)[1])
        # print(str)
    if 'verbatim' in types:
        str = norm_utils.remove_tag(normalize.norm_tag_verbatim(str, str)[1])
    if 'letter' in types:
        str = norm_utils.remove_tag(normalize.normalize_letters(str, str)[1])
        # print(str)
    if 'roman' in types:
        str = norm_utils.remove_tag(normalize.norm_tag_roman_num(str, str)[1])
        str = norm_utils.remove_tag(normalize.norm_tag_roman_num_v2(str, str)[1])

    return str



def split_sentence(sentence):
    list_sent = []
    start = 0
    if len(sentence.split()) > 100:
        match_all = list(re.finditer(',', sentence))
        if len(match_all) > 0:
            pre_match = match_all[0]

            for match in match_all:
                sent_check = ''.join(sentence[start:match.start()])
                tokens = sent_check.split()
                if len(tokens) > 100:
                    sub_sent_tokens = sentence[start:pre_match.start()].split()
                    # print('len sub: ', len(tokens))
                    if len(sub_sent_tokens) > 100:
                        idx_split = int(len(sub_sent_tokens) / 2)
                        sub_sent_1 = ' '.join(sub_sent_tokens[:idx_split])
                        sub_sent_2 = ' '.join(sub_sent_tokens[idx_split:])
                        list_sent.append(sub_sent_1)
                        list_sent.append(sub_sent_2)
                    else:
                        sub_sent = ''.join(sentence[start:pre_match.start()])
                        list_sent.append(sub_sent)
                    start = pre_match.end()
                pre_match = match
            # sub_sent = ''.join(sentence[start:pre_match.start()])
            # list_sent.append(sub_sent)
            # sub_sent = ''.join(sentence[pre_match.end():])
            # list_sent.append(sub_sent)
            sub_sent = ''.join(sentence[start:])
            list_sent.append(sub_sent)
        else:
            tokens = sentence.split()
            idx_split = int(len(tokens) / 2)
            list_sent.append(' '.join(tokens[:idx_split]))
            list_sent.append(' '.join(tokens[idx_split:]))
    else:
        list_sent.append(sentence)

    return list_sent

@app.route('/norm', methods=['GET', 'POST'])
def infer():
    message = request.json
    sample = message['sample']
    result = normalize(sample)
    print('INPUT: ', sample)
    print('RESULT: ', result)

    return send_response({'result':result})

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("conf/config.cfg")

    # dict
    abbre_dict = utils.read_txt_two_cols(config['resources']['abbre_path'])
    try:
        oov_dict = utils.read_oov(config['resources']['oov_path'])
    except:
        oov_dict = {}
    # init api
    # app.debug = True
    # host = os.environ.get('IP', '0.0.0.0')
    # port = int(os.environ.get('PORT', 11993))
    # app.run(host=host, port=port, threaded=True, use_reloader=False)
    # app.run()

    while True:
        inp = input('nhap input vao day: ')
        result = normalize(inp)
        print('result: ', result)