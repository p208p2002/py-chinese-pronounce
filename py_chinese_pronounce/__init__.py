import re
import os
from collections import defaultdict
import editdistance
from functools import lru_cache

class Word2Pronounce():
    def __init__(self) -> None:

        # uni2cns map
        self.uni2cns_dict_path = os.path.join(
            os.path.dirname(__file__),
            'CNS2UNICODE_Unicode BMP.txt'
        )

        with open(self.uni2cns_dict_path, encoding='utf-8') as f:
            lines = f.read().strip().split("\n")

        self._uni2cns_data = [line.split("\t") for line in lines]
        self.uni2cns_map = {}

        for cns, uni in self._uni2cns_data:
            self.uni2cns_map[uni] = cns
        
        # cns2uni map
        self.cns2uni_map = {v: k for k, v in self.uni2cns_map.items()}

        # chewin
        self.cns2chewin_dict = os.path.join(
            os.path.dirname(__file__),
            'CNS_phonetic.txt'
        )

        with open(self.cns2chewin_dict, encoding='utf-8') as f:
            lines = f.read().strip().split("\n")

        self._cns2chewin_data = [line.split("\t") for line in lines]
        self.cns2chewin_map = {}

        for cns, chewin in self._cns2chewin_data:
            self.cns2chewin_map[cns] = chewin
        

        # chewin to others
        with open(os.path.join(os.path.dirname(__file__),'CNS_pinyin_1.txt'), encoding='utf-8') as f:
            lines = f.read().strip().split("\n")

        self._data = [line.split("\t") for line in lines]
        
        ## chewin2han_map
        self.chewin2han_map = {}
        for chewin, *pinyin in self._data:
            self.chewin2han_map[chewin] = pinyin[0]

    def _word2unicode(self, x):
        uni = hex(ord(x))
        uni = re.sub("^0x", "", uni).upper()
        return uni
    
    def _uni2word(self,uni):
        word = bytes(f"\\u{uni}",'utf-8').decode(encoding='unicode_escape')
        return word
    
    def _cns2word(self,cns):
        return self._uni2word(self._cns2uni(cns))

    def _uni2cns(self, uni):
        return self.uni2cns_map[uni]
    
    def _cns2uni(self,cns):
        return self.cns2uni_map[cns]

    def _cns2chewin(self,uni):
        return self.cns2chewin_map[uni]
    
    def _chewin2han(self,chewin):
        return self.chewin2han_map[chewin]
    
    def to_chewin(self, x):
        cns_code = self._uni2cns(self._word2unicode(x))
        chewin = self._cns2chewin(cns_code)
        return chewin
    
    def to_han(self, x):
        return self._chewin2han(self.to_chewin(x))

class Pronounce2Word(Word2Pronounce):
    def __init__(self) -> None:
        super().__init__()
        self._setup_chewin2word_map()
        self._setup_han2word_map()
        self._setup_sc_dict_han_map()
        

    def _setup_sc_dict_han_map(self):
        _path = os.path.join(
            os.path.dirname(__file__),
            'sc-dict.txt'
        )

        with open(_path, encoding='utf-8') as f:
            vocabs = f.read().strip().split("\n")

        self.sc_dict_han_map = defaultdict(list)
        self.sc_dict_han_no_tune_map = defaultdict(list)

        for vocab in vocabs:
            try:
                vocab_pronounces = [self.to_han(word) for word in vocab]
                vocab_no_tune_pronounces = [re.sub('[2-5]',"",self.to_han(word)) for word in vocab]
            except:
                continue
            
            vp_key = '-'.join(vocab_pronounces)
            vp_no_tune_key = '-'.join(vocab_no_tune_pronounces)

            self.sc_dict_han_map[vp_key].append(vocab)
            self.sc_dict_han_no_tune_map[vp_no_tune_key].append(vocab)          

    def _setup_chewin2word_map(self):
        self.chewin2word_map = defaultdict(set)
        for cns,chewin in self.cns2chewin_map.items():
            try:
                self.chewin2word_map[chewin].update(self._cns2word(cns))
            except:
                pass
        
    def _setup_han2word_map(self):
        self.han2word_map = defaultdict(set)
        for cns,chewin in self.cns2chewin_map.items():
            try:
                self.han2word_map[self._chewin2han(chewin)].update(self._cns2word(cns))
            except:
                pass
    
    def chewin2word(self,x):
        return list(self.chewin2word_map[x])
    
    def han2word(self,x):
        return list(self.han2word_map[x])

    def find_same(self,x):
        han = self.to_han(x)
        same = self.han2word(han)
        try:
            same.remove(x)
        except:
            pass
        return same
    
    def find_similar(self,x):
        han = self.to_han(x)
        base_tune = re.sub('[2-5]',"",han)
        out = []
        for tune in ['','2','3','4','5']:
            new_han = f"{base_tune}{tune}"
            similar_results = self.han2word(new_han)
            out += similar_results
        out = list(set(out))
        try:
            out.remove(x)
        except:
            pass
        return out
    
    def find_similar_vocab(self,vocab):
        vocab_pronounces = [re.sub('[2-5]',"",self.to_han(word)) for word in vocab]
        vp_key = '-'.join(vocab_pronounces)
        similar = self.sc_dict_han_no_tune_map[vp_key]
        try:
            similar.remove(x)
        except:
            pass
        return similar
    
    def find_same_vocab(self,vocab):
        vocab_pronounces = [self.to_han(word) for word in vocab]
        vp_key = '-'.join(vocab_pronounces)
        same = self.sc_dict_han_map[vp_key]
        try:
            same.remove(x)
        except:
            pass
        return same

    @lru_cache(maxsize=200)
    def _find_similar_han_pronounces(self,han,level=1):
        out = []
        for compare_han in self.han2word_map.keys():
            ed_step = editdistance.eval(han,compare_han)
            if ed_step <= level:
                out.append(compare_han)
        return out
    

# For compatibility
Word2pronounce = Word2Pronounce