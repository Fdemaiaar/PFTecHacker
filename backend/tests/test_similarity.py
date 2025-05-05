from backend.app.detectors.similarity import run
def test_brand_similar():assert run("http://paypa1-login.com")["brand_similar"] is True
def test_brand_none():assert run("https://insper.edu.br")["brand_similar"] is False
