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
僅支援*單一文字*轉換
#### 文字轉注音
```python
w2p.to_chewin("我") # ㄨㄛˇ
```
#### 文字轉漢語發音
```python
w2p.to_han("我") # wo3
```

#### 其他轉換
- Word2Pronounce._word2unicode(self, x)
- Word2Pronounce._uni2word(self,uni)
- Word2Pronounce._cns2word(self,cns)
- Word2Pronounce._uni2cns(self, uni)
> CNS: [中文標準交換碼](https://www.cns11643.gov.tw/index.jsp)

### Pronounce2Word
僅支援*單一文字*查詢

#### 注音找文字 
```python
p2w.chewin2word('ㄨㄛˇ') 
# ['䰀', '婑', '捰', '㦱', '我', '䂺']
```

#### 漢語發音找文字
```python
p2w.han2word('wo3')
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
p2w.find_similar_vocab("汽車")
# ['七尺', '棋車', '棋车', '气车', '氣車', '汽车', '騎車', '骑车']
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