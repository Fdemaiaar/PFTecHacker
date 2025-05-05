from backend.app.detectors.heuristics import suspicious_pattern

def test_digits():
    assert suspicious_pattern("http://1111abc.com")

def test_clean():
    assert not suspicious_pattern("https://insper.edu.br")
