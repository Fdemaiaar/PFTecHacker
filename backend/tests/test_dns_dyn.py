from backend.app.detectors.dns_dyn_check import run
def test_dynamic_dns():assert run("http://mycam.no-ip.org")["dynamic_dns"] is True
def test_regular_domain():assert run("https://insper.edu.br")["dynamic_dns"] is False
