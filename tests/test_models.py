from apple_health_parser.models.records import HealthData, HeartRateData
from apple_health_parser.utils.parser import Parser

BASE_ATTRIBS = {
    "type": "HKCategoryTypeIdentifierAppleStandHour",
    "sourceName": "fake_source",
    "creationDate": "2024-01-01 01:00:00 +0200",
    "startDate": "2024-01-01 01:00:00 +0200",
    "endDate": "2024-01-01 01:00:00 +0200",
    "value": "72",
}


def test_parsed_data(parser: Parser) -> None:
    flag = "HKQuantityTypeIdentifierHeartRate"
    parsed = parser.get_flag_records(flag)

    assert parsed.flag == flag
    assert len(parsed.dates) == 2
    assert len(parsed.sources) == 1
    assert len(parsed.records) == 2


def test_heart_rate_data_device_optional() -> None:
    record = HeartRateData.model_validate(BASE_ATTRIBS)
    assert record.device is None


def test_health_data_categorical_value_preserved() -> None:
    record = HealthData.model_validate(
        {**BASE_ATTRIBS, "value": "HKCategoryValueAppleStandHourStood"}
    )
    assert record.value == "HKCategoryValueAppleStandHourStood"
