from collections import defaultdict
import re
import random

def find_one_use_words(corpus):
    corpus = corpus.lower().replace('\n', ' ')
    corpus = re.sub('[^a-zA-Z ]+', '', corpus)
    freq_dict = defaultdict(lambda: 0)
    for word in corpus.split(' '):
        word = word.strip()
        if len(word) > 0:
            freq_dict[word] += 1
    uniqs = set([])
    for word, count in freq_dict.items():
        uniqs.add(word)
    return list(uniqs)

def uniq_words_sort_by_occ(corpus):
    corpus = corpus.lower().replace('\n', ' ')
    corpus = re.sub('[^a-zA-Z ]+', '', corpus)
    freq_dict = defaultdict(lambda: 0)
    already = set([])
    c = []
    for word in corpus.split(' '):
        word = word.strip()
        if len(word) > 0:
            if word not in already:
                already.add(word)
                c.append(word)
    return c

def to_buckets(words, bs=16):
    buckets = []
    while len(words) >= bs:
        buckets.append(words[:bs])
        words = words[bs:]
    return buckets

def encode(m, buckets):
    n = 4# log2 16
    while len(m) % n != 0:
        m += '0'
    cur_b = 0
    code = []
    while len(m) > 0:
        cur_m = m[:n]
        idx = int(cur_m, 2)
        code.append(buckets[cur_b][idx])
        cur_b += 1
        m = m[n:]
    return code

def decode(encoded, buckets):
    n = 4
    cur_b = 0
    m = ''
    while len(encoded) > 0:
        word = encoded.pop(0)
        idx = buckets[cur_b].index(word)
        c = "{0:b}".format(idx)
        while len(c) < n:
            c = "0" + c
        m += c
        cur_b += 1
    return m

c = open('script.txt', 'r').read()
#find_one_use_words(c)
#print(c)
uniqs = uniq_words_sort_by_occ(c)
#uniqs.sort()
#print('[' + ', '.join(map(lambda x: '\'' + x + '\'', uniqs)) + ']')
bucks = to_buckets(uniqs)

print(encode("11110111100010100110110011011011010100101000000001000010011001111110110101110011011011111101101000010101110111101011001010111000000001010111000010100000011011001011011001011000010000110111111110010110011111010011100011111101001100010110110110001110001010100010101000111101011001111101100010101010111010001010111001010100111000100011011011011111101111010100000101100010111001111010", bucks))

print(decode('eric of anywhere pacific fact marty jesus me assistance he good damn yknow around real sir even microphone middle cut take someday stars look since dad killed into happen sleep having uncle embarrassment calls chased little felt pick complete eightyeight intact sent behind circuits invented entire duty electricity must mankind journey wings intense cast bug sundays start ah port fiddling honey oughta read expires united practical weve studio answer ran interfered nurses instead visitors break vulcan nothings live pole confidence cute punch forties everything eighteenyearsold certain peckerwood marvins lookin matter connecting proof greg sleepyhead ride'.split(' '), bucks))

'''
while True:
    inp = '0101011101'
    c =encode(inp, bucks)
    random.shuffle(c)
    c = sorted(c, key=uniqs.index)
    res = decode(c, bucks)
    #print(res)
    assert res.startswith(inp)

#print('\n'.join(sorted(find_one_use_words(c))))

'''
