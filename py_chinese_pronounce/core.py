import re
import os
from collections import defaultdict
import Levenshtein
from functools import lru_cache
import itertools
import pandas
import  ahocorasick    
from typing import List

class Word2Pronounce():
    """
    文字轉換發音
    """
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
        with open(os.path.join(os.path.dirname(__file__), 'CNS_pinyin_1.txt'), encoding='utf-8') as f:
            lines = f.read().strip().split("\n")

        self._data = [line.split("\t") for line in lines]

        # chewin2han_map
        self.chewin2han_map = {}
        for chewin, *pinyin in self._data:
            self.chewin2han_map[chewin] = pinyin[0]

        
        # 詞彙注音字典
        self.vocab_pronounce_df = pandas.read_excel(os.path.join(os.path.dirname(__file__), 'dict_concised_2014_20230112.xlsx'))
        self.vocab_pronounce_df = self.vocab_pronounce_df.set_index('字詞名')
        vocabs = self.vocab_pronounce_df.index.to_list()
        self.ac_tree = ahocorasick.AhoCorasick(*vocabs) # AC自動機
    
    
    def sent_to_chewin(self,x)->List[str]:
        results = list(self.ac_tree.search(x,True))
        results.sort(key=lambda x:x[-1][1]+(x[-1][1]-x[-1][0])/10)
        out = [None] * len(x)
        
        for r in results:
            words = r[0]
            w_range = r[-1]

            chewin = self.vocab_pronounce_df.loc[words]['注音一式']
            
            if type(chewin) == str:
                chewin = chewin.strip().split()                
            else:
                chewin = chewin.to_list()
            
            # 當輸入是多音詞時
            if (len(words) > 1 and len(chewin) > 1 and '\u3000' in chewin[0]) :
                chewin_pp = self.vocab_pronounce_df.loc[words]['多音排序']
                if type(chewin_pp) == str:
                    chewin_pp = chewin_pp.strip().split()
                else:
                    chewin_pp = chewin_pp.to_list()
                idx = chewin_pp.index(min(chewin_pp))
                chewin = chewin[idx].split("\u3000")
                
            chewin_idx = 0
            for i in range(w_range[0],w_range[1]):
                out[i] = chewin[chewin_idx]
                chewin_idx += 1
        
        for i,(o,char) in enumerate(zip(out,x)):
            if o == None:
                try:
                    out[i] = self.to_chewin(char)
                except:
                    pass
        
        return out

    def sent_to_han(self,x)->List[str]:
        results = list(self.ac_tree.search(x,True))
        results.sort(key=lambda x:x[-1][1]+(x[-1][1]-x[-1][0])/10)

        chewin_list = [None] * len(x)
        out = [None] * len(x)

        polyphone_check = False

        for r in results:
            words = r[0]
            w_range = r[-1]
            chewin = self.vocab_pronounce_df.loc[words]['注音一式']

            if type(chewin) == str:
                chewin = chewin.strip().split()
            else:
                chewin = chewin.to_list()

            # 當輸入是多音詞時
            if (len(words) > 1 and len(chewin) > 1 and '\u3000' in chewin[0]) :
                chewin_pp = self.vocab_pronounce_df.loc[words]['多音排序']
                if type(chewin_pp) == str:
                    chewin_pp = chewin_pp.strip().split()
                else:
                    chewin_pp = chewin_pp.to_list()
                idx = chewin_pp.index(min(chewin_pp))
                chewin = chewin[idx].split("\u3000")

            chewin_idx = 0
            for i in range(w_range[0],w_range[1]):
                chewin_list[i] = chewin[chewin_idx]
                chewin_idx += 1

        for i in range(len(chewin_list)) :
            out[i] = self._chewin2han(chewin_list[i])

        for i,(o,char) in enumerate(zip(out,x)):
            if o == None:
                try:
                    out[i] = self.to_han(char)
                except:
                    pass
        return out
            
    def _word2unicode(self, x):
        uni = hex(ord(x))
        uni = re.sub("^0x", "", uni).upper()
        return uni

    def _uni2word(self, uni):
        word = bytes(f"\\u{uni}", 'utf-8').decode(encoding='unicode_escape')
        return word

    def _cns2word(self, cns):
        return self._uni2word(self._cns2uni(cns))

    def _uni2cns(self, uni):
        return self.uni2cns_map[uni]

    def _cns2uni(self, cns):
        return self.cns2uni_map[cns]

    def _cns2chewin(self, uni):
        return self.cns2chewin_map[uni]

    def _chewin2han(self, chewin):
        return self.chewin2han_map[chewin]

    def to_chewin(self, x):
        """
        字轉注音

        :parm str x: 單一字元(長度:1)
        :retrun: 注音
        :rtype: str
        """
        cns_code = self._uni2cns(self._word2unicode(x))
        chewin = self._cns2chewin(cns_code)
        return chewin

    def to_han(self, x):
        """
        字轉漢語發音

        :parm x: 單一字元(長度:1)
        :retrun: 漢語拼音
        :rtype: str
        """
        return self._chewin2han(self.to_chewin(x))
    
    def char_pronounce_similar(self, a, b):
        """
        字元發音相似(0~1)

        :parm a: 單一字元(長度:1)
        :parm b: 單一字元(長度:1)
        :retrun: 發音相似度 (0~1)
        :rtype: float
        """
        try:
            ap = self.to_han(a)
            bp = self.to_han(b)
        except:
            return 0.0
        edit_dis = Levenshtein.distance(ap, bp)
        length = max(len(ap), len(bp))
        return 1.0 - edit_dis/length

    def sent_pronounce_similar(self, sentence_a, sentence_b):
        """
        句發音相似(0~1)

        :parm sentence_a: 句字
        :parm sentence_b: 句子
        :retrun: 發音相似度 (0~1)
        :rtype: float
        """
        score = 0.0
        for a, b in zip(sentence_a, sentence_b):
            score += self.char_pronounce_similar(a, b)
        return score/max(len(sentence_a), len(sentence_b))


class Pronounce2Word(Word2Pronounce):
    """
    發音轉/找文字
    """
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
                vocab_pronounces, vocab_no_tune_pronounces = [], []
                for word in vocab:
                    han_word = self.to_han(word)
                    vocab_pronounces.append(han_word)
                    vocab_no_tune_pronounces.append(
                        re.sub('[2-5]', "", han_word))
            except:
                continue

            vp_key = '-'.join(vocab_pronounces)
            vp_no_tune_key = '-'.join(vocab_no_tune_pronounces)

            self.sc_dict_han_map[vp_key].append(vocab)
            self.sc_dict_han_no_tune_map[vp_no_tune_key].append(vocab)

    def _setup_chewin2word_map(self):
        self.chewin2word_map = defaultdict(set)
        for cns, chewin in self.cns2chewin_map.items():
            try:
                self.chewin2word_map[chewin].update(self._cns2word(cns))
            except:
                pass

    def _setup_han2word_map(self):
        self.han2word_map = defaultdict(set)
        for cns, chewin in self.cns2chewin_map.items():
            try:
                self.han2word_map[self._chewin2han(
                    chewin)].update(self._cns2word(cns))
            except:
                pass

    def chewin2word(self, x):
        """
        注音找文字

        :parm x: 注音拼音（單一文字長度）
        :retrun: 相同發音文字
        :rtype: list[str]
        """
        return list(self.chewin2word_map[x])

    def han2word(self, x):
        """
        漢語拼音找文字

        :parm x: 漢語拼音（單一文字長度）
        :retrun: 相同發音文字
        :rtype: list[str]
        """
        return list(self.han2word_map[x])

    def find_same(self, x):
        """
        文字找相同發音文字

        :parm x: 單一文字
        :retrun: 相同發音文字
        :rtype: list[str]
        """
        han = self.to_han(x)
        same = self.han2word(han)
        try:
            same.remove(x)
        except:
            pass
        return same

    def find_similar(self, x):
        """
        文字找相似發音文字（去除聲調）

        :parm x: 單一文字
        :retrun: 相似音文字
        :rtype: list[str]
        """
        han = self.to_han(x)
        base_tune = re.sub('[2-5]', "", han)
        out = []
        for tune in ['', '2', '3', '4', '5']:
            new_han = f"{base_tune}{tune}"
            similar_results = self.han2word(new_han)
            out += similar_results
        out = list(set(out))
        try:
            out.remove(x)
        except:
            pass
        return out

    def find_similar_vocab(self, vocab):
        """
        詞彙找相似發音詞彙；去除聲調
        例如：汽車->騎車。

        :parm vocab: 詞彙
        :retrun: 相似音詞彙
        :rtype: list[str]
        """
        vocab_pronounces = [re.sub('[2-5]', "", self.to_han(word))
                            for word in vocab]
        vp_key = '-'.join(vocab_pronounces)
        similar = self.sc_dict_han_no_tune_map[vp_key]
        try:
            similar.remove(vocab)
        except:
            pass
        return similar

    def find_same_vocab(self, vocab):
        """
        詞彙找相同發音詞彙；去除聲調
        例如：堵住->賭注。

        :parm vocab: 詞彙
        :retrun: 相同音詞彙
        :rtype: list[str]
        """
        vocab_pronounces = [self.to_han(word) for word in vocab]
        vp_key = '-'.join(vocab_pronounces)
        same = self.sc_dict_han_map[vp_key]
        try:
            same.remove(vocab)
        except:
            pass
        return same
    
    def find_similar_vocab_level(self, vocab, level=1,_limit_search_keys=1000000):
        """
        詞彙找相似發音詞彙；編輯距離
        例如：清晨->傾城。

        :parm vocab: 詞彙
        :parm level: 允許每一個字最大的發音編輯距離
        :parm _limit_search_keys: 搜尋的發音組合上限
        :retrun: 相似音詞彙
        :rtype: list[str]
        """
        vocab_no_tune_pronounces = [re.sub('[2-5]', "", self.to_han(word)) for word in vocab]
        similar_han_pronounces = []
        for char_han_pronounce in vocab_no_tune_pronounces:
            similar_hans = self._find_similar_han_pronounces(char_han_pronounce,level=level)
            similar_hans = list(set([re.sub('[2-5]', "", x) for x in similar_hans])) # clear tune
            similar_han_pronounces.append(similar_hans)

        vp_keys = itertools.islice(itertools.product(*similar_han_pronounces),_limit_search_keys)
        vp_keys = ['-'.join(x) for x in vp_keys]

        similar = []
        for vp_key in vp_keys:
            _find_similar = self.sc_dict_han_no_tune_map[vp_key]
            similar += _find_similar
        
        try:
            similar.remove(vocab)
        except:
            pass

        similar.sort(key=lambda x:self.sent_pronounce_similar(x,vocab),reverse=True)
    
        return similar


    @lru_cache(maxsize=500)
    def _find_similar_han_pronounces(self, han, level=1):
        """
        漢語發音找相似漢語發音

        :parm han: 漢語發音
        :parm level: 最大編輯距離
        :retrun: 相似漢語發音
        :rtype: list[str]
        """
        out = []
        for compare_han in self.han2word_map.keys():
            ed_step = Levenshtein.distance(han, compare_han)
            if ed_step <= level:
                out.append(compare_han)
        return out
