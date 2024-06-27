from apple_health_parser.utils.parser import Parser


def test_parsed_data(parser: Parser) -> None:
    flag = "HKQuantityTypeIdentifierHeartRate"
    parsed = parser.get_flag_records(flag)

    assert parsed.flag == flag
    assert len(parsed.dates) == 1
    assert len(parsed.sources) == 1
    assert len(parsed.records) == 1
