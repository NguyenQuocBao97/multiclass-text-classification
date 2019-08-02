import math
import pickle
import underthesea as uts
from feature import load_common_words
import numpy as np

common_words_list = load_common_words()
sino_words_list = load_common_words(type='sino')


def get_features(tokenized_text):
    global common_words_list, sino_words_list

    sentences = []
    for each_text in tokenized_text:
        sentences.extend(each_text.split('\n'))

    document = ' '.join(sentences)
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
    total_sentences = len(sentences)

    # Average sentence length
    aslw = total_words / total_sentences
    asls = total_syllables / total_sentences
    aslc = total_characters / total_sentences

    # Average word length
    awls = total_syllables / total_words
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

    # bgl = .886593 - (awl * 0.03640) + (afw * 0.161911) - (asl * 0.21401) - (asl * 0.000577) - (asl * 0.000005)

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
        'aslw': aslw,
        'asls': asls,
        'aslc': aslc,
        'awls': awls,
        'awlc': awlc,
        'pdw': pdw,
        'pddw': pddw,
        'ddwdw': ddwdw,
        'pds': pds,
        'pdds': pdds,
        'ddsds': ddsds,
        'psvw': psvw,
        'pdsvw': pdsvw,
        'dsvwdw': dsvwdw,
        'fres': fres,
        'fkgl': fkgl,
        'cli': cli,
        'fog': fog,
        'smog': smog,
        'ari': ari,
        'dca': dca
    }
    return features

if __name__ == "__main__":
    input_text = """Tiếng Việt được chính thức ghi nhận trong Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam 2013, tại Chương I Điều 5 Mục 3, là ngôn ngữ quốc gia của Việt Nam [6]. Tiếng Việt bao gồm cách phát âm tiếng Việt và chữ Quốc ngữ để viết. Tuy nhiên, hiện chưa có bất kỳ văn bản nào ở cấp nhà nước quy định giọng chuẩn và quốc tự của tiếng Việt [7]. Hiện nay phần lớn các văn bản trong nước được viết theo những "Quy định về chính tả tiếng Việt và về thuật ngữ tiếng Việt" áp dụng cho các sách giáo khoa, báo và văn bản của ngành giáo dục nêu tại Quyết định của Bộ Giáo dục số 240/QĐ ngày 5 tháng 3 năm 1984 [8] do những người thụ hưởng giáo dục đó sau này ra làm việc trong mọi lĩnh vực xã hội."""

    dt_file = [open('./saved_model/dt_model_group-12.pkl', 'rb'), 'Decision Tree']
    nb_file = [open('./saved_model/nb_model_group-12.pkl', 'rb'), 'Naive Bayes']
    rf_file = [open('./saved_model/rf_model_group-12.pkl', 'rb'), 'Random Forest']
    svm_file = [open('./saved_model/svm_model_group-12.pkl', 'rb'), 'Support Vector Machine']
    knn_file = [open('./saved_model/knn_model_group-12.pkl', 'rb'), 'K Nearest Neighbor']

    for file in [svm_file, dt_file, rf_file, nb_file, knn_file]:
        name = file[1]
        model = pickle.load(file[0])
        tokenized_input_text = uts.word_tokenize(input_text, format="text")
        features = get_features(tokenized_input_text) # type: dict


        feature_values = np.array(list(features.values()))
        feature_values = feature_values.reshape(1, -1)

        print(name, ':       ', model.predict(feature_values))
    # Get input feature

    # print(dt_model.predict(input_text))