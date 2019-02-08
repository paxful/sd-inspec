# InSpec plugin for ServerDensity

## Overview

[InSpec](https://www.inspec.io/) plugin for [ServerDensity](http://serverdensity.io).
Tested with [sd-agent](https://github.com/serverdensity/sd-agent) v2.2.4.

## Installation

* Install InSpec from `https://www.inspec.io/downloads/`
* Copy the `inspec.py` script to `sd-agent` plugins folder `/usr/share/python/sd-agent/checks.d`
* Copy configuration file `inspec.yaml.example` to `/etc/sd-agent/conf.d/inspec.yaml`.
* Restart `sd-agent`

You can set custom path to InSpec using `inspec_path` option in `init_config` section.

## Metrics

* `total` is the number of total inspec tests.

* `failed` is the number of failed inspec tests.

* `passed` is the number of passed inspec tests.

You can check them with `sudo -iu sd-agent /usr/share/python/sd-agent/agent.py check inspec`

## Contributing

1. Fork the repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write your change
4. Write tests for your change (if applicable)
5. Run the tests, ensuring they all pass
6. Submit a Pull Request using Github

## License & Authors

* Author:: Andrei Skopenko [@scopenco](https://github.com/scopenco)

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
