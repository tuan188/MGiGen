import hashlib


class Encoder:

    def encode(self, alg, string):
        if alg == 'md5':
            return self.encode_md5(string)
        return string

    def encode_md5(self, string):
        return hashlib.md5(string.encode()).hexdigest()
