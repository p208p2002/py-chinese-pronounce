# Python Chinese Pronounce
- 文字轉注音、漢語發音
- 注音、漢語發音轉文字
- 尋找相似、相同發聲字/單詞

> 資料來源：[政府開放資料](https://data.gov.tw/dataset/5961), [超齊百萬字典檔](https://github.com/samejack/sc-dictionary)

## Install
### From PyPI
```sh
pip install py-chinese-pronounce
```
### From Repo
```sh
pip install -U git+https://github.com/p208p2002/py-chinese-pronounce.git
```
## Usage
```python
from py_chinese_pronounce import Word2Pronounce,Pronounce2Word

w2p = Word2Pronounce()
p2w = Pronounce2Word()
```
### Word2Pronounce
僅支援*單一字元*轉換
#### 文字轉注音
```python
w2p.to_chewin("我") # ㄨㄛˇ
```
#### 文字轉漢語發音
```python
w2p.to_han("我") # wo3
```

#### 發音相似度比較
```python
w2p.char_pronounce_similar(a,b)
w2p.sent_pronounce_similar(sent_a, sent_b)
# 數值區間落在[0-1]
```

#### 其他轉換
- Word2Pronounce._word2unicode(self, x)
- Word2Pronounce._uni2word(self,uni)
- Word2Pronounce._cns2word(self,cns)
- Word2Pronounce._uni2cns(self, uni)
> CNS: [中文標準交換碼](https://www.cns11643.gov.tw/index.jsp)

### Pronounce2Word
詞彙尋功能支援多字元，其餘僅支援*單一字元*查詢

#### 注音找文字 
```python
p2w.chewin2word("ㄨㄛˇ") 
# ['䰀', '婑', '捰', '㦱', '我', '䂺']
```

#### 漢語發音找文字
```python
p2w.han2word("wo3")
# ['䰀', '婑', '捰', '㦱', '我', '䂺']
```

#### 文字找同發音
```python
p2w.find_same("我")
# ['䰀', '婑', '捰', '㦱', '䂺']
```

#### 文字找近似發音
```python
p2w.find_similar("我")
# ['蠖', '臥', '䇶', '䂺', '䪝', '捾', '偓', '握', '捰', '卧', '雘', '㦱', '濣', '䠎', '楃', '沃', '渥', '䁊', '涴', '幄', '龌', '㓇', '矱', '斡', '㠛', '肟', '齷', '仴', '䰀', '婑', '喔', '腛', '䀑']
```

#### 相似發聲單詞
```python
p2w.find_similar_vocab("汽車") # 去除聲調找相似
# ['七尺', '棋車', '棋车', '气车', '氣車', '汽车', '騎車', '骑车']
```
```python
p2w.find_similar_vocab_level("清晨",level=1) # 發音編輯距離找相似
# ['傾城', '清城', '清澄', '青城', '清淳', '清純', '清纯', '清醇', '清神', '青神', '星塵', ...
```

#### 相同發聲單詞
```python
p2w.find_same_vocab("汽車")
# ['气车', '氣車', '汽车']
```

#### 其他轉換
- Pronounce2Word._find_similar_han_pronounces(self,han,level=1)

    尋找相似發音
    - han: 漢語發音
    - level: 編輯距離（越大越寬鬆）