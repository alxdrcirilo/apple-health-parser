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

### Listing the devices

In addition to sources, you also get information regarding the devices your Apple Health data originates from. In a nutshell, sources is the shorthand name for a given device. For example, you may have `"Alexandre's Apple Watch"` as the sole source, but `['Apple Watch (Watch6,7; 10.2)', 'Apple Watch (Watch6,7; 10.3)', 'Apple Watch (Watch6,7; 10.3.1)', 'Apple Watch (Watch6,7; 10.4)', 'Apple Watch (Watch6,7; 10.5)', 'Apple Watch (Watch6,7; 10.6)', 'Apple Watch (Watch6,7; 10.6.1)'` as devices. That's because device information includes the following:

- Device name
- Hardware version
- Software version (if provided)

The `get_devices` method from the `Parser` class works in the same fashion as the `get_sources` method, i.e. on a single flag or on the entirety of the data. Here's an example for a single flag:

```python
devices = parser.get_devices(flag="HKQuantityTypeIdentifierHeartRate")
print(devices)

> ['Apple Watch (Watch6,7; 10.2)', 'Apple Watch (Watch6,7; 10.3)', 'Apple Watch (Watch6,7; 10.3.1)', 'Apple Watch (Watch6,7; 10.4)', 'Apple Watch (Watch6,7; 10.5)', 'Apple Watch (Watch6,7; 10.6)', 'Apple Watch (Watch6,7; 10.6.1)']
```

### Getting the records

This is a very simple step and can be done in one single line of code by calling the `get_flag_records` method from the parser:

```python
data = parser.get_flag_records(flag="HKQuantityTypeIdentifierHeartRate")
print(data)

> =================ParsedData==================
  Flag:       HKQuantityTypeIdentifierHeartRate
  Sources:    3 sources
  Devices:    8 devices
  Dates:      117603 dates
  Records:    117603 records
```

In this particular case, the parser found a total of 117603 records, 117603 dates, all coming from 3 different sources.

### Exporting data to CSV files

Once you have parsed your data, you can export all parsed data to CSV files using the `export` method. This method will create a directory and export each health data flag to its own CSV file.

```python
# Export all parsed data to CSV files in a directory called 'health_data_export'
parser.export(dir_name="health_data_export")
```

The export method will:

1. Create the specified directory if it doesn't exist
2. Generate a separate CSV file for each health data flag (e.g., `HKQuantityTypeIdentifierHeartRate.csv`, `HKQuantityTypeIdentifierStepCount.csv`, etc.)
3. Export all records for each flag, including data from all sources and devices

For example, if your Apple Health data contains heart rate, step count, and oxygen saturation, the export will create:

- `health_data_export/HKQuantityTypeIdentifierHeartRate.csv`
- `health_data_export/HKQuantityTypeIdentifierStepCount.csv`
- `health_data_export/HKQuantityTypeIdentifierOxygenSaturation.csv`

Each CSV file contains all the parsed records with their timestamps, values, sources, and other metadata, making it easy to analyze your health data in spreadsheet software or other data analysis tools.
