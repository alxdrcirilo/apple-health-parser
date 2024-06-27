# Plots

## Configuration

There are 3 types of plots that can be generated:

1. **Standard**: The most generic type of plot *Apple Health Parser* can generate. With the exception of *heart rate* data that includes *motion context* metadata, all remaining flags are plotted the same way.
2. **Heatmap**: Heatmaps are useful when trying to visualize 2-dimensional data such as yearly views (i.e. record at a given day and month).
3. **Overview**: Overview plots include multiple flags (e.g. the activity overview includes the active energy burned, exercise time, and stand time).

!!! note
    Heatmaps require an `operation` argument, providing an invalid operation or not providing one at all will cause [`InvalidHeatmapOperation`](../usage/exceptions.md#apple_health_parser.exceptions.InvalidHeatmapOperation) to be raised.

### Arguments

The `Plot` class is derived from the `PlotInterface` [ABC](https://docs.python.org/3/library/abc.html) class.

When instantianting `Plot`, only one argument is required: the `data` argument - refers to the `ParsedData` object (i.e. object you get after using the `get_flag_records` method from the `Parser` class). The `year` argument is technically also required, but if not provided, will default to the current year. The `source` and `operation` arguments are optional. Lastly, the `heatmap` and `title` arguments are boolean flags which are set to `False` by default. Setting `heatmap` to `True` will generate a heatmap instead (be sure to provide an `operation` as heatmaps require one). Setting `title` to `True` will show the title in the plot.

!!! tip
    You can get the list of available sources using the [`get_sources`](../usage/utils/parser.md#apple_health_parser.utils.parser.Parser.get_sources) method from the `Parser` class.

::: apple_health_parser.interfaces.plot_interface.PlotInterface.__init__
    options:
      show_root_heading: false
      show_root_full_path: false
      show_root_toc_entry: false
      show_docstring_description: false
      show_docstring_raises: false
      show_docstring_returns: false
      show_source: false

#### Operations

The allowed `operation` attributes are listed in the table below.

| Operation   |       Description       |
|:-----------:|:-----------------------:|
| `count`     | Total count of records  |
| `max`       | Max value of records    |
| `mean`      | Mean value of records   |
| `median`    | Median value of records |
| `min`       | Min value of records    |
| `sum`       | Sum of records          |

### Showing/Saving

Plots can be `shown` and/or `saved`. Showing a plot will trigger a new tab to show up in your default browser with an interactive plot thanks to the [`plotly`](https://plotly.com/) dependency. If you wish to save your plot, you can do so in several formats: `png`, `jpeg`, `webp`, `svg`, and `pdf`.

::: apple_health_parser.interfaces.plot_interface.PlotInterface.plot
    options:
      show_root_heading: false
      show_root_full_path: false
      show_root_toc_entry: false
      show_docstring_description: false
      show_docstring_raises: false
      show_docstring_returns: false
      show_source: false

## Examples

```python
from apple_health_parser.plot import Plot


plt = Plot(data=data, source=source, operation="sum")
plt.plot(save=True)
```

Once we have obtained the parsed data and picked the data source as we've seen in the [Getting the records](basics.md#getting-the-records) and [Listing the sources](basics.md#listing-the-sources) sections, all that remains is to instantiate the `Plot` class and provide it with the parsed data (i.e. `data`), the source (i.e. `source`), and the operation we want to apply if any (in this case, `sum`). Lastly, we simply call the `plot` method with the appropriate arguments.

This will open a tab in your default web browser by default (add `show=False` to the function call otherwise) and in this case we also explicitely defined that we want the generated plot to be saved (i.e. using `save=True`).

Now say we would rather visualize this in a heatmap. Fortunately that's pretty easy to do as well!

```python
heatmap = Plot(data=data, source=source, operation="sum", heatmap=True)
heatmap.plot(save=True)
```

As you have probably noticed, all that is required is to provide an additional argument when instantiating the `Plot` class - `heatmap`. This argument is set to `False` by default.

Below you can find some examples for both the standard and heatmap plots.

### Distance walking/running

=== "Standard"
    ![distance_walking_running_plot_light](../assets/plots/plot_distance_walking_running_2024_sum_light.svg#only-light)
    ![distance_walking_running_plot_dark](../assets/plots/plot_distance_walking_running_2024_sum_dark.svg#only-dark)

=== "Heatmap"
    ![distance_walking_running_heatmap_light](../assets/plots/heatmap_distance_walking_running_2024_sum_light.svg#only-light)
    ![distance_walking_running_heatmap_dark](../assets/plots/heatmap_distance_walking_running_2024_sum_dark.svg#only-dark)

### Activity overview

*Apple Health Parser* also comes with a handy way of plotting the *activity overview* which includes the following:

- **Active energy burned (kcal)**: total amount of energy burned through physical activity, including both exercise and daily activities. It is measured in kilocalories (kcal) and provides an estimate of the calories expended by the body.
- **Apple exercise time (min)**: duration of exercise activities recorded by your Apple device. It measures the amount of time spent actively engaged in physical exercise, such as running, walking, or cycling.
- **Apple stand time (min)**: duration of time spent standing or moving around during the day. It encourages users to take breaks from sitting and promotes a more active lifestyle.

![activity_overview_light](../assets/plots/activity_overview_light.svg#only-light)
![activity_overview_dark](../assets/plots/activity_overview_dark.svg#only-dark)
