# Python Chinese Pornounce
## Install
```sh
pip install -U git+https://github.com/p208p2002/py-chinese-pornounce.git
```
## Usage
```python
from py_chinese_pornounce import Word2Pornounce,WordPornounceFinder

w2p = Word2Pornounce()
wpf = WordPornounceFinder()
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
### WordPornounceFinder
僅支援*單一文字*查詢

#### 注音找文字 
```python
wpf.chewin2word('ㄨㄛˇ') 
# ['䰀', '婑', '捰', '㦱', '我', '䂺']
```

#### 漢語發音找文字
```python
wpf.han2word('wo3')
# ['䰀', '婑', '捰', '㦱', '我', '䂺']
```

#### 文字找同發音
```python
wpf.find_same("我")
# ['䰀', '婑', '捰', '㦱', '䂺']
```

#### 文字找近似發音
```python
wpf.find_similar("我")
# ['蠖', '臥', '䇶', '䂺', '䪝', '捾', '偓', '握', '捰', '卧', '雘', '㦱', '濣', '䠎', '楃', '沃', '渥', '䁊', '涴', '幄', '龌', '㓇', '矱', '斡', '㠛', '肟', '齷', '仴', '䰀', '婑', '喔', '腛', '䀑']
```