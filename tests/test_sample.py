"""
Test sample plugin
"""


def test_getsample(client):
    """  Test getcapabilites response
    """
    projectfile = "data/france_parts.qgs"

    # Make a request
    qs = "?SERVICE=WMS&REQUEST=GetSample&MAP=data/france_parts.qgs"
    rv = client.get(qs, projectfile)
    assert rv.status_code == 200
    assert rv.content.decode('utf-8') == 'Hello from sample'
