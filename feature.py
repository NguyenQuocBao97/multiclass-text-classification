import math

import pandas as pd
import numpy as np
import re
import glob
import pandas.core.series
import underthesea
import pyexcelerate as pye
from pandas import DataFrame
from pyexcelerate import Workbook


def get_file_names_in_path(path):
    files = [f for f in glob.glob(path + "/*.ws", recursive=True)]

    return files


def clean_str(s):
    """Clean sentence"""
    s = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", s)
    s = re.sub(r"\'s", " \'s", s)
    s = re.sub(r"\'ve", " \'ve", s)
    s = re.sub(r"n\'t", " n\'t", s)
    s = re.sub(r"\'re", " \'re", s)
    s = re.sub(r"\'d", " \'d", s)
    s = re.sub(r"\'ll", " \'ll", s)
    s = re.sub(r",", " , ", s)
    s = re.sub(r"!", " ! ", s)
    s = re.sub(r"\(", " \( ", s)
    s = re.sub(r"\)", " \) ", s)
    s = re.sub(r"\?", " \? ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r'\S*(x{2,}|X{2,})\S*', "xxx", s)
    s = re.sub(r'[^\x00-\x7F]+', "", s)
    return s.strip().lower()


def load_common_words(type='frequent'):
    """

    :return dict:
    """
    result = {}
    folder_name = './vn_{}_words'.format(type)
    file_name = folder_name + '/processed_{}_words.txt'.format(type)

    file = open(file_name, 'r')
    for row in file.read().split('\n'):
        result[row] = 1

    # print(result)
    return result


def load_data_and_labels():
    """Load sentences and labels"""
    folder_list = ['Difficult', 'Easy', 'Normal']
    folder_name = './1000_documents_3_levels/{}'
    features = {
        'aslw': None,
        'asls': None,
        'aslc': None,
        'awls': None,
        'awlc': None,
        'pdw': None,
        'pddw': None,
        'ddwdw': None,
        'pds': None,
        'pdds': None,
        'ddsds': None,
        'psvw': None,
        'pdsvw': None,
        'dsvwdw': None,
        'fres': None,
        'fkgl': None,
        'cli': None,
        'fog': None,
        'bgl': None,
        'smog': None,
        'ari': None,
        'dca': None
    }
    csv_cols = ['file'] + list(features.keys()) + ['result']
    csv_data = [csv_cols]

    for sub_di in folder_list:
        filenames = get_file_names_in_path(folder_name.format(sub_di))
        common_words_list = load_common_words()
        sino_words_list = load_common_words(type='sino')

        for name in filenames:
            try:
                data = pd.read_csv(name, sep="\n", header=None, engine='python')
            except Exception as e:
                with open(name, 'r+') as f:
                    file_data = f.read()
                    f.seek(0)
                    f.write(file_data.replace('"', ''))
                    f.close()
                data = pd.read_csv(name, sep="\n", header=None, engine='python')
            document = ''.join(data[0].array)

            syllables = document.split(' ')  # type: list[str]
            words = []
            for sy in syllables:
                for word in sy.split('_'):
                    words += [word]
            # words = np.array([syllable.split('_') for syllable in syllables]).flatten()  # ????????????

            mono_syllables = [sy for sy in syllables if '_' not in sy]
            poly_syllables = [sy for sy in syllables if '_' in sy]
            long_syllables = [sy for sy in poly_syllables if len(sy.split('_')) > 2]

            distict_syllables = list(set(document.split(' ')))
            distict_words = list(set(words))

            total_syllables = len(syllables)
            total_words = len(words)
            total_mono_syllables = len(mono_syllables)
            total_long_syllables = len(long_syllables)
            total_distict_syllables = len(distict_syllables)
            total_distict_words = len(distict_words)
            total_characters = sum(len(word) for word in words)
            total_sentences = len(data[0].array)

            # Average sentence length
            aslw = total_words / total_sentences
            asls = total_syllables / total_sentences
            aslc = total_characters / total_sentences

            # Average word length
            awls = total_characters / total_syllables
            awlc = total_characters / total_words

            # Percentage of difficult words
            common_syllables = [sy for sy in syllables if common_words_list.get(sy)]
            difficult_syllables = [sy for sy in syllables if common_words_list.get(sy, 0) == 0]
            common_unique_syllables = list(set(common_syllables))
            difficult_unique_syllables = list(set(difficult_syllables))

            common_words = [word for word in words if common_words_list.get(word)]
            difficult_words = [word for word in words if common_words_list.get(word, 0) == 0]
            common_unique_words = list(set(common_syllables))
            difficult_unique_words = list(set(difficult_syllables))

            total_common_syllables = len(common_syllables)
            total_difficult_syllables = len(difficult_syllables)
            total_common_unique_syllables = len(common_unique_syllables)
            total_difficult_unique_syllables = len(difficult_unique_syllables)
            total_common_words = len(common_words)
            total_difficult_words = len(difficult_words)
            total_common_unique_words = len(common_unique_words)
            total_difficult_unique_words = len(difficult_unique_words)

            pdw = total_difficult_words / total_words
            pddw = total_difficult_unique_words / total_words
            ddwdw = total_difficult_unique_words / total_distict_words
            pds = total_difficult_syllables / total_syllables
            pdds = total_difficult_unique_syllables / total_syllables
            ddsds = total_difficult_unique_syllables / total_distict_syllables

            # Percentage of Sino-Vietnamese Words

            sino_words = [w for w in words if sino_words_list.get(w)]
            sino_unique_words = list(set(sino_words))

            total_sino_words = len(sino_words)
            total_sino_unique_words = len(sino_unique_words)

            psvw = total_sino_words / total_words
            pdsvw = total_sino_unique_words / total_words
            dsvwdw = total_sino_unique_words / total_distict_words

            # Using difficult words to calculate

            # FRES: Flesch Readability Ease score
            fres = 206.835 - (84.6 * (float(total_syllables) / float(total_words))) - (
                    1.015 * (float(total_words) / float(total_sentences)))

            # Flesch-Kincaid Grade Level
            fkgl = 0.39 * (float(total_words) / float(total_sentences)) + (
                    11.8 * (float(total_syllables) / float(total_words))) - 15.59

            # ColemanLiauIndex (still testing)
            # THis one is too low # cli = ((character_count/w_count) * 4.71) - ((100.0 * sent_count)/w_count) * .30 - 15.8
            # cli = 0.0588 * ((float(mod_char_count) / float(w_count))) - (0.30 * ((float(sent_count) / (float(w_count))) - 15.8))
            cli = 5.888 * (float(total_characters) / float(total_words)) - (
                    29.5 * (float(total_sentences) / float(total_words))) - 15.800
            # standard_cli = -27.4004 * (ecp/100) + 23.06395
            # cli = -15.8 + 5.88 * (float(character_count/w_count)) - 29.59 * (float(w_count/sent_count))

            # Gunning Fog
            fog = (0.4 * (float(total_words) / float(total_sentences) + 10.0 * (
                    float(total_difficult_words) / float(total_words))))

            # Bormuth Grade Level Score (unreliable)
            awl = (float(total_characters) / float(total_words))
            afw = float(total_common_words / total_words)
            asl = float(total_words / total_sentences)

            bgl = .886593 - (awl * 0.03640) + (afw * 0.161911) - (asl * 0.21401) - (asl * 0.000577) - (asl * 0.000005)

            # SMOG
            smog = 1.0430 * math.sqrt((total_difficult_words) * (30.0 / total_sentences)) + (3.1291)

            # ari
            # ari = 4.71 * (character_count/w_count) + 0.5 * (w_count/sent_count) - 21.43
            ari = 4.71 * (total_characters / total_words) + 0.5 * (total_words / total_sentences) - 21.43
            # Powers-Sumner-Kearl (unreliable; for 100 word passages
            # psk = (0.0778 * asl) + .0455 * (100 * (sy_count/w_count)) - 2.2029

            # Dale-Chall Readability Formula
            dcr = 0.1579 * (pdw) + (0.0496 * asl)
            dca = dcr + 3.6365

            features = {
                'aslw': aslw if aslw > 0 else 0,
                'asls': asls if asls > 0 else 0,
                'aslc': aslc if aslc > 0 else 0,
                'awls': awls if awls > 0 else 0,
                'awlc': awlc if awlc > 0 else 0,
                'pdw': pdw if pdw > 0 else 0,
                'pddw': pddw if pddw > 0 else 0,
                'ddwdw': ddwdw if ddwdw > 0 else 0,
                'pds': pds if pds > 0 else 0,
                'pdds': pdds if pdds > 0 else 0,
                'ddsds': ddsds if ddsds > 0 else 0,
                'psvw': psvw if psvw > 0 else 0,
                'pdsvw': pdsvw if pdsvw > 0 else 0,
                'dsvwdw': dsvwdw if dsvwdw > 0 else 0,
                'fres': fres if fres > 0 else 0,
                'fkgl': fkgl if fkgl > 0 else 0,
                'cli': cli if cli > 0 else 0,
                'fog': fog if fog > 0 else 0,
                'bgl': bgl if bgl > 0 else 0,
                'smog': smog if smog > 0 else 0,
                'ari': ari if ari > 0 else 0,
                'dca': dca if dca > 0 else 0,
                'result': sub_di
            }

            csv_data.append([name] + list(features.values()))

    # print(csv_data)
    wb = Workbook()
    wb.new_sheet("sheet name", data=csv_data)
    wb.save("output.xlsx")

    # selected = ['product', 'consumer_complaint_narrative']
    # non_selected = list(set(df.columns) - set(selected))

    # return x_raw, y_raw, df, labels


def load_file_trained():
    df = pd.read_excel('output.xlsx')
    selected = ['file', 'result']
    non_selected = list(set(df.columns) - set(selected))

    df = df.drop(non_selected, axis=1)  # Drop non selected columns
    df = df.dropna(axis=0, how='any', subset=selected)  # Drop null rows
    df = df.reindex(np.random.permutation(df.index))  # Shuffle the dataframe

    # Map the actual labels to one hot labels
    labels = sorted(list(set(df[selected[0]].tolist())))
    one_hot = np.zeros((len(labels), len(labels)), int)
    np.fill_diagonal(one_hot, 1)
    label_dict = dict(zip(labels, one_hot))

    x_raw = df[selected[1]].apply(lambda x: clean_str(x)).tolist()
    y_raw = df[selected[0]].apply(lambda y: label_dict[y]).tolist()
    return x_raw, y_raw, df, labels


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """Iterate the data batch by batch"""
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(data_size / batch_size) + 1

    for epoch in range(num_epochs):
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data

        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


def extract_feature(document):
    """
        A formula for extracting the features of document
    :param str document:
    :return dict:
    """

    return {
        'surface_features': [],
        'pos_features': [],
        'pt_features': [],
        'mb_features': [],
        'it_features': []
    }


if __name__ == '__main__':
    load_data_and_labels()
