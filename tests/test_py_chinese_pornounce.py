from py_chinese_pornounce import Word2Pornounce,WordPornounceFinder

w2p = Word2Pornounce()
wpf = WordPornounceFinder()

def test_to_chewin():
    assert w2p.to_chewin("我") == "ㄨㄛˇ" 

def test_to_han():
    assert w2p.to_han("我") == "wo3" 

def test_chewin2word():
    assert "我" in wpf.chewin2word('ㄨㄛˇ') 

def test_han2word():
    assert "我" in wpf.han2word('wo3') 

def test_find_same():
    assert "我" in wpf.find_same("婑")

def test_find_similar():
    assert "喔" in wpf.find_similar("我")
