from py_chinese_pronounce import Word2Pronounce,Pronounce2Word

w2p = Word2Pronounce()
p2w = Pronounce2Word()

def test_to_chewin():
    assert w2p.to_chewin("我") == "ㄨㄛˇ" 

def test_to_han():
    assert w2p.to_han("我") == "wo3" 

def test_chewin2word():
    assert "我" in p2w.chewin2word('ㄨㄛˇ') 

def test_han2word():
    assert "我" in p2w.han2word('wo3') 

def test_find_same():
    assert "我" in p2w.find_same("婑")

def test_find_similar():
    assert "喔" in p2w.find_similar("我")
