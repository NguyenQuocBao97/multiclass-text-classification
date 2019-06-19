import underthesea as uts

if __name__ == "__main__":

    """Load sentences and labels"""
    folder_name = './vn_sino_words'
    file_name = folder_name + '/sino_words.txt'
    write_file = folder_name + '/processed_sino_words.txt'

    f = open(file_name, 'r')
    w_f = open(write_file, 'w')
    lines = f.read().split('\n')
    tokenized_words = []

    for sen in lines:
        word = sen.split(':')[0]
        tokenized_words += [word.lower()]
    w_f.writelines('\n'.join(tokenized_words))
    print(tokenized_words)


