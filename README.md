# PyHelpers
Collection of helpers for python developers (configuration structure, read-write utils, api utils)

## Important

In the `src/config_helpers.py` you need to change the `CONFIG_PATH` to the path of your configuration file.

## Helpers

**Read-write helpers** in `src/read_write.py`

- `read_json`, `write_json`, `append_json` - read, write, append json file
- `read_csv`, `write_csv`, `append_csv` - read, write, append csv file

**Configuration structure** in `conf/` \
**Configuration utils** in `src/config_helpers.py`

- `read_config` - read configuration from file (supports overrides like in hydras)
- `pprint_config` - pretty print configuration

**API utils** in `src/api/`

- `api.py` - simple api client based on OpenAPI 
- `prompter.py` - an util to create prompts based on the template
- `handler/` - handlers (post- and pre- processing) for the api requests

**Logging utils** in `src/loggers.py`

- `get_colorful_logger` - get colorful logger
- `get_file_logger` - get file logger

## Examples

In the `examples` folder