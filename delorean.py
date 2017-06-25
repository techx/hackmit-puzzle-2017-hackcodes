import re

class NotWellFormedException(Exception):
    pass

class DeLorean:
    # n = log2(bucket_size)
    def __init__(self, corpus, bucket_size=16, n=4):
        self.bucket_size = bucket_size
        self.n = n

        words = DeLorean.words_from_corpus(corpus)
        sorted_words = DeLorean.unique_words_sorted_by_first_occurence(words)
        self.buckets = self.truncate_extra_words(sorted_words)
        self.bucket_idxs = { self.buckets[i]: i for i in range(len(self.buckets)) }
        self.word_set = set(self.buckets)

        self.n_words = len(self.buckets) // self.bucket_size
        self.max_bits = self.n * self.n_words


    @staticmethod
    def words_from_corpus(corpus):
        corpus = corpus.lower().replace('\n', ' ')
        corpus = re.sub('[^a-zA-Z ]+', '', corpus)
        corpus = corpus.split(' ')
        output = []
        for word in corpus:
            word = word.strip()
            if len(word) > 0:
                output.append(word)
        #return output
        return list(filter(lambda w: len(w) > 0, map(lambda w: w.strip(), corpus)))

    @staticmethod
    def unique_words_sorted_by_first_occurence(words):
        done = set([])
        o = []
        for word in words:
            if word not in done:
                done.add(word)
                o.append(word)
        return o

    def truncate_extra_words(self, ordered_words):
        floord_n_words = self.bucket_size * (len(ordered_words) // self.bucket_size)
        return ordered_words[:floord_n_words]

    def encode_without_permutation(self, message_bitstring):
        while len(message_bitstring) % self.n != 0:
            message_bitstring += '0'
        assert len(message_bitstring) <= self.max_bits
        current_bucket = 0
        out = []
        for i in range(len(message_bitstring)//self.n):
            out.append(self.encode_N_bs(message_bitstring[i*self.n:(i+1)*self.n], current_bucket))
            current_bucket += 1
        return out

    def encode_N_bs(self, N_bs, current_bucket_idx):
        idx = int(N_bs, 2)
        return self.buckets[(current_bucket_idx*self.bucket_size) + idx]

    def decode_sorted(self, word_list):
        if len(word_list) > self.n_words:
            raise NotWellFormedException()
            # too many words
        message = []
        current_bucket = 0
        for word in word_list:
            idx = self.buckets.index(word) - (current_bucket * self.bucket_size)
            if idx < 0 or idx >= self.bucket_size:
                raise NotWellFormedException()
                # these words aren't in the buckets lmao
                # it's bad
            bits = "{0:b}".format(idx)
            bits = ("0" * (self.n - len(bits))) + bits
            message.append(bits)
            current_bucket += 1

        return ''.join(message)

    def sort_words_inplace(self, word_list):
        for word in word_list:
            if word not in self.word_set:
                raise NotWellFormedException()
        word_list.sort(key=self.buckets.index)

    def decode(self, word_list):
        self.sort_words_inplace(word_list)
        return self.decode_sorted(word_list)

