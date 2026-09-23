from dns import resolve_query


def test_a_record():
    response = resolve_query("example.com", "A")

    assert response["status"] == "success"
    assert response["record_type"] == "A"
    assert response["ip_address"] == "192.168.1.10"


def test_cname_record():
    response = resolve_query("www.example.com", "CNAME")

    assert response["status"] == "success"
    assert response["record_type"] == "CNAME"
    assert response["canonical_name"] == "example.com"
    assert response["ip_address"] == "192.168.1.10"


def test_unknown_a_record():
    response = resolve_query("unknown.com", "A")

    assert response["status"] == "error"
    assert response["message"] == "A record not found."


def test_unsupported_query():
    response = resolve_query("example.com", "MX")

    assert response["status"] == "error"
    assert response["message"] == "Only A and CNAME queries are supported."