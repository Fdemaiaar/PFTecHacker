from backend.app.detectors.heuristics import suspicious_pattern,in_blacklist
def test_pattern_digits():assert suspicious_pattern("http://111abc123.com")
def test_pattern_clean():assert not suspicious_pattern("https://insper.edu.br")
def test_blacklist_false():assert not in_blacklist("https://www.google.com")
