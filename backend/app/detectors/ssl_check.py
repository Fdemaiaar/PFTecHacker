import ssl, socket, datetime as dt

def run(url: str) -> dict:
    host = url.split("://")[-1].split("/")[0]
    out = {"ssl_expired": None, "ssl_issuer": None, "ssl_cn_mismatch": None}
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(4)
            s.connect((host, 443))
            cert = s.getpeercert()

        exp = dt.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y GMT")
        issuer = dict(x[0] for x in cert["issuer"]).get("commonName", "")
        valid_cn = host in cert.get("subjectAltName", [(None, "")])[0][1]

        out.update(
            {
                "ssl_expired": exp < dt.datetime.utcnow(),
                "ssl_issuer": issuer,
                "ssl_cn_mismatch": not valid_cn,
            }
        )
    except Exception:
        # host não resolve ou não suporta TLS
        out.update({"ssl_expired": True, "ssl_cn_mismatch": True})
    return out
