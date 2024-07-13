# Tutorial

*Apple Health Parser* comes with a handy CLI (*command-line interface*). But if you'd rather write a short script to get parse your Apple Health data, that is also possible.

## Exporting Apple Health data

On iOS 17, as mentioned in the [official documentation](https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios), you can export all of your Apple Health data into one zipped file. This can be done by navigating to the *Health* app and then tapping on your profile picture, and then tapping on the *Export All Health Data* button.

## Basics

### Setting up the parser

First and foremost, you need to import the `Parser` and provide it with the path to your Apple Health `export.zip` file (see [Exporting Apple Health data](#exporting-apple-health-data)).

Notice that we set `overwrite=True` to automatically overwrite data if you previously exported data. If you don't provide the `overwrite` parameter, the parser will ask you whether you would like to delete previously exported data or not.

```python
from apple_health_parser.utils.parser import Parser


parser = Parser(export_file=<path_to_zip_file>, overwrite=True)
```

### Listing available flags

To list the available flags, simply get `flags` from the instance of `Parser`.

```python
print(parser.flags)

> ["HKCategoryTypeIdentifierAppleStandHour",
   "HKCategoryTypeIdentifierAudioExposureEvent",
   "HKCategoryTypeIdentifierSleepAnalysis",
   "HKDataTypeSleepDurationGoal",
   "HKQuantityTypeIdentifierActiveEnergyBurned"]
```

### Listing the sources

*Apple Health* data can originate from various sources, most commonly this will be your *iPhone* or *Apple Watch*. But they can also come from third-party providers (e.g. a GymKit-compatible threadmill).

#### For a single flag

In order to have the data relate to a single source, you first need to get the list of sources from your data. This can be easily done via the `get_sources` method from the `Parser` class. This method accepts an optional parameter `flag` (e.g. `"HKQuantityTypeIdentifierHeartRate"`), and returns a list of sources for that specific flag.

```python
sources = parser.get_sources(flag="HKQuantityTypeIdentifierHeartRate")
print(sources)

> ["Alexandre's iPhone", "Alexandre's Apple Watch", "GymKit"]
```

#### For everything

If no flag is provided, the method will return a dictionary with flags as keys and sources as values.

```python
sources = parser.get_sources()
print(sources)

> {"HKCategoryTypeIdentifierAppleStandHour": ["Alexandre's Apple Watch"],
   "HKCategoryTypeIdentifierSleepAnalysis": ["Alexandre's Apple Watch", "Alexandre's iPhone"],
   "HKDataTypeSleepDurationGoal": ["Health"]}
```

### Getting the records

This is a very simple step and can be done in one single line of code by calling the `get_flag_records` method from the parser:

```python
data = parser.get_flag_records(flag="HKQuantityTypeIdentifierHeartRate")
print(data)

> =================ParsedData==================
  Flag:       HKQuantityTypeIdentifierHeartRate
  Sources:    3 sources
  Dates:      117603 dates
  Records:    117603 records
```

In this particular case, the parser found a total of 117603 records, 117603 dates, all coming from 3 different sources.
