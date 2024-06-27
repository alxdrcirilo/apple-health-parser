from apple_health_parser.config.definitions import get_flag_metadata

flags = get_flag_metadata()

md_table = "| **Flag** | Name | Unit | Color | Colormap |\n"
md_table += "| --- | --- | --- | --- | --- |\n"
for flag, metadata in flags.items():
    md_table += f"| `{flag}` | {metadata.name} | {metadata.unit} | {metadata.color} | {metadata.colormap} |\n"

print(md_table)
print(f"Found {len(flags)} flags")
