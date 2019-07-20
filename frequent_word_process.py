import underthesea as uts
import pandas as pd
from feature import get_file_names_in_path
__FREQUENT_THRESHOLD = 10

if __name__ == "__main__":

    # """Load sentences and labels"""
    # folder_name = './vn_frequent_words'
    # file_name = folder_name + '/frequent_words.txt'
    # write_file = folder_name + '/processed_frequent_words.txt'
    #
    # f = open(file_name, 'r')
    # w_f = open(write_file, 'w')
    # lines = f.read().split('\n')
    # tokenized_words = []
    #
    # for sen in lines:
    #     word = uts.word_tokenize(sen, format='text')
    #     words = []
    #     # print(word, type(word))
    #     if ' ' in word:
    #         words = word.split(' ')
    #         tokenized_words.extend(words)
    #     else:
    #         tokenized_words.append(word)
    #
    # w_f.writelines('\n'.join(tokenized_words))
    # print(tokenized_words)
    folder_list = ['Difficult', 'Easy', 'Normal']
    folder_name = './1000_documents_3_levels/{}'

    sys_count = {}
    total_sys = 0
    for sub_di in folder_list[:10]:
        filenames = get_file_names_in_path(folder_name.format(sub_di))
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

            syllables = map(lambda x: x.lower(), document.split(' ')) # type: [str]

            for sys in syllables:
                total_sys += 1
                if not sys_count.get(sys):
                    sys_count[sys] = 1
                else:
                    sys_count[sys] += 1

    COUNT_THRESHOLD = total_sys / __FREQUENT_THRESHOLD
    diff_sys = [k for k, v in sys_count.items() if v < COUNT_THRESHOLD]

    folder_name = './vn_frequent_words'
    # file_name = folder_name + '/frequent_words.txt'
    write_file = folder_name + '/processed_frequent_words.txt'
    w_f = open(write_file, 'w')
    w_f.writelines('\n'.join(diff_sys))
    w_f.close()


