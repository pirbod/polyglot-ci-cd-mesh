from app import service_payload


def test_service_payload_contains_expected_metadata():
    payload = service_payload()
    assert payload["service"] == "python-service"
    assert payload["runtime"] == "python"
    assert payload["version"] == "1.0.0"
