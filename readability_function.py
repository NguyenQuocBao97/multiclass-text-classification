# !/usr/bin/python
# coding=UTF-8
import math


def count_characters(text):
    count = 0
    for char in text:
        count += 1
    return count


def to_cv(word):
    """ Convert word to a cv-list.
    Each vowel of word is replaced by a "v" in the cv-list, and each
    non-vowel is replaced by a 'c'.
    """
    cv_list = []
    for ch in word:
        if ch in 'aeiou':
            #       if ch in 'aeiouy':
            cv_list.append('v')
        else:
            cv_list.append('c')
    return cv_list


def count_cv(cv):
    """ Count the # of times "c", "v" occur consecutively in cv.
    """
    count = 0
    i = 0
    while i < len(cv) - 1:  # the -1 is important!
        if cv[i] == 'c' and cv[i + 1] == 'v':
            count += 1
        i += 1
    return count


def count_vowel_groups(word):
    """ Return the # of vowel-groups in word.
    """
    cv = to_cv(word)
    count = count_cv(cv)
    if cv[0] == 'v':
        count += 1
    return count


def count_syllables_in_word(word):
    vgc = count_vowel_groups(word)
    count_hard_words = 0
    if vgc == 0:
        return 1
    else:
        return vgc


def count_syllables(text):
    """ Returns total # of syllables in all words of text.
    """
    words = text.split()
    total_syllables = 0
    for w in words:
        total_syllables += count_syllables_in_word(w)
    return total_syllables


def count_hard_words(text):
    hardwords = 0
    words = text.split()
    for w in words:
        if count_syllables_in_word(w) >= 3:
            hardwords += 1
    return hardwords


def count_sentences(s):
    return s.count('.') + s.count('!') + s.count('?')


def count_words(s):
    return len(s.split())


def familiar_words(text):
    f_words = 0
    words = text.split()
    for w in words:
        if w in open('dale_chall_word_list.txt').read():
            f_words += 1
    return f_words


def modcharcount(text):
    characters = count_characters(text)
    spaces = count_words(text)
    mod_char_count = characters - spaces
    return mod_char_count


def summarize():
    s = "ielts_band_6.txt"
    # s = "ielts_band_6.txt"

    try:
        text = open(s, 'r').read().lower()
        print('Successfully opened ' + s)
    except IOError:
        text = s

    # get text stats
    sy_count = count_syllables(text)
    w_count = count_words(text)
    sent_count = count_sentences(text)
    character_count = count_characters(text)
    hardwords = count_hard_words(text)
    f_words = float(familiar_words(text))
    mod_char_count = modcharcount(text)
    asl = float(w_count / sent_count)
    # awl modified to mod_char_count from char_count
    afw = float(f_words / w_count)
    pdw = ((float(hardwords) / float(w_count)) * 100)
    pfw = (f_words / w_count) * 100
    mod_char_count = modcharcount(text)
    awl = (float(mod_char_count) / float(w_count))
    # Average Syllables per Word
    spw = (float(sy_count) / float(w_count))
    # used for coleman liau standard
    # ecp = 141.8401 - (0.214590 * mod_char_count) + (1.079812 * sent_count)
    # FRES: Flesch Readability Ease score
    fres = 206.835 - (84.6 * (float(sy_count) / float(w_count))) - (1.015 * (float(w_count) / float(sent_count)))

    # Flesch-Kincaid Grade Level
    fkgl = 0.39 * (float(w_count) / float(sent_count)) + (11.8 * (float(sy_count) / float(w_count))) - 15.59

    # ColemanLiauIndex (still testing)
    # THis one is too low # cli = ((character_count/w_count) * 4.71) - ((100.0 * sent_count)/w_count) * .30 - 15.8
    # cli = 0.0588 * ((float(mod_char_count) / float(w_count))) - (0.30 * ((float(sent_count) / (float(w_count))) - 15.8))
    cli = 5.888 * (float(mod_char_count) / float(w_count)) - (29.5 * (float(sent_count) / float(w_count))) - 15.800
    # standard_cli = -27.4004 * (ecp/100) + 23.06395
    # cli = -15.8 + 5.88 * (float(character_count/w_count)) - 29.59 * (float(w_count/sent_count))

    # Gunning Fog
    fog = (0.4 * (float(w_count) / float(sent_count) + 10.0 * (float(hardwords) / float(w_count))))

    # Bormuth Grade Level Score (unreliable)
    bgl = .886593 - (awl * 0.03640) + (afw * 0.161911) - (asl * 0.21401) - (asl * 0.000577) - (asl * 0.000005)

    # SMOG
    smog = 1.0430 * math.sqrt((hardwords) * (30.0 / sent_count)) + (3.1291)

    # ari
    # ari = 4.71 * (character_count/w_count) + 0.5 * (w_count/sent_count) - 21.43
    ari = 4.71 * (character_count / w_count) + 0.5 * (w_count / sent_count) - 21.43
    # Powers-Sumner-Kearl (unreliable; for 100 word passages
    # psk = (0.0778 * asl) + .0455 * (100 * (sy_count/w_count)) - 2.2029

    # Dale-Chall Readability Formula
    dcr = 0.1579 * (pdw) + (0.0496 * asl)
    dca = dcr + 3.6365

    def inrange(x, min, max):
        return (min is None or min <= x) and (max is None or max >= x)

    if inrange(dca, 0, 4.9):
        dcgl = 4.0
    elif inrange(dca, 5.0, 5.9):
        dcgl = 6.0
    elif inrange(dca, 6.0, 6.9):
        dcgl = 8.0
    elif inrange(dca, 7.0, 7.9):
        dcgl = 10.0
    elif inrange(dca, 8.0, 8.9):
        dcgl = 12.0
    elif inrange(dca, 9.0, 9.9):
        dcgl = 15.0
    else:
        dcgl = 16.0

    print("\n--------------------------------\nInput:\n" + text + "\n--------------------------------\n")
    # Grade Level Average
    grade = (cli + ari + smog + fkgl + fog + dcgl) / 6.0
    # printreadability report
    print('Readability report for ' + s)
    print('Total character count: ' + str(character_count))
    print('Character count without spaces: ' + str(mod_char_count))
    print('Total syllable count: ' + str(sy_count))
    print('Average Syllables Per Word: ' + str(spw))
    print('Total word count: ' + str(w_count))
    print('Total sentence count: ' + str(sent_count))
    print('Polysyllable words (3+ syllables): ' + str(hardwords))
    print('Total Familiar Words: ' + str(f_words))
    #    print('ECP: ' +str(ecp)
    print('Average Sentence Length: ' + str(asl))
    print('Average Word Length: ' + str(awl))
    print('Average Familiar Words: ' + str(afw))
    print('Percent Difficult Words: ' + str(pdw))
    print('Percent Familiar Words: ' + str(pfw))
    print('----------------')
    print('Flesch reading ease score (FRES): ' + str(fres))
    print('Dale Chall Adjusted Score: ' + str(dca))
    print('----------------')
    print('Flesch-Kincaid grade level: ' + str(fkgl))
    print('Simplified Coleman Liau Index score: ' + str(cli))
    #    print('*Standard Coleman Liau Index score: ' +str(standard_cli)
    print('(Gunning) Fog: ' + str(fog))
    print('SMOG index: ' + str(smog))
    print('Automated Readability Index: ' + str(ari))
    print('*Bormuth Grade Level Score: ' + str(bgl))
    print('New Dale Chall Adjusted Grade Level (max of range): ' + str(dcgl))
    #    print('*Powers-Sumner-Kearl Grade Level: ' +str (psk)
    print('----------------')
    print('Average Grade Score: ' + str(grade))


if __name__ == "__main__":
    summarize()
