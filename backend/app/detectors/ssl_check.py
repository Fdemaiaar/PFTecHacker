import ssl, socket, datetime as dt
def run(url):
    host = url.split("://")[-1].split("/")[0]
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
        s.settimeout(3)
        s.connect((host, 443))
        cert = s.getpeercert()
    exp = dt.datetime.strptime(cert['notAfter'],'%b %d %H:%M:%S %Y GMT')
    issuer = dict(x[0] for x in cert['issuer'])['commonName']
    valid_cn = host in cert['subjectAltName'][0][1]
    return {"ssl_expired": exp < dt.datetime.utcnow(),
            "ssl_issuer": issuer,
            "ssl_cn_mismatch": not valid_cn}
