import underthesea as uts

if __name__ == "__main__":

    """Load sentences and labels"""
    folder_name = './vn_frequent_words'
    file_name = folder_name + '/frequent_words.txt'
    write_file = folder_name + '/processed_frequent_words.txt'

    f = open(file_name, 'r')
    w_f = open(write_file, 'w')
    lines = f.read().split('\n')
    tokenized_words = []

    for sen in lines:
        word = uts.word_tokenize(sen, format='text')
        words = []
        # print(word, type(word))
        if ' ' in word:
            words = word.split(' ')
            tokenized_words.extend(words)
        else:
            tokenized_words.append(word)

    w_f.writelines('\n'.join(tokenized_words))
    print(tokenized_words)


