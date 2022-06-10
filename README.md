# Python Chinese Pornounce
- 文字轉注音、漢語發音
- 注音、漢語發音轉文字
- 尋找相似發聲字
> 資料來源：[政府開放資料](https://data.gov.tw/dataset/5961)
## Install
### From PyPI
```sh
pip install py-chinese-pornounce
```
### From Repo
```sh
pip install -U git+https://github.com/p208p2002/py-chinese-pornounce.git
```
## Usage
```python
from py_chinese_pornounce import Word2Pornounce,Pornounce2Word

w2p = Word2Pornounce()
p2w = Pornounce2Word()
```
### Word2Pornounce
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
- Word2Pornounce._word2unicode(self, x)
- Word2Pornounce._uni2word(self,uni)
- Word2Pornounce._cns2word(self,cns)
- Word2Pornounce._uni2cns(self, uni)
> CNS: [中文標準交換碼](https://www.cns11643.gov.tw/index.jsp)

### Pornounce2Word
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