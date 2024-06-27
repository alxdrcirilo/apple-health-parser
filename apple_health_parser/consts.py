from apple_health_parser.config.definitions import (
    AllowedImageFormats,
    Operations,
    OverviewType,
    PlotType,
    get_flag_metadata,
)

FLAG_METADATA = get_flag_metadata()
ALLOWED_IMAGE_FORMATS = [fmt.value for fmt in AllowedImageFormats]
OPERATIONS = [op.value for op in Operations]
PLOT_TYPES = [ptype.value for ptype in PlotType]
OVERVIEW_TYPES = [overview.name.lower() for overview in OverviewType]
