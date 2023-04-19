## Sonic Switch Automation POC
This repository provides an implementation example of automating SONiC Switch configuration. With this repository it is possible to manage (create and delete) multiple VLANs on a SONiC switch based on a YAML based configuration file. The logic for the switch configuration is based on a python script that implements a REST client against the Broadcom based SONiC OS distribution.

### Local development based on ASDF
To start local development run ```make install```. Afterwards activate the project's virtual Python environment with ```pipshell env```.

### Local development without ASDF
To start local development run ```make install-dep``` to install Python dependencies.

### Running the script
The following provides a description on running the script.
The script relies on four positional arguments:
1. switch_address: IP address of the switch to configure.
2. username: Username to use to authenticate against the switch.
3. password: Password to use to authenticate against the switch.
4. config: Config YAML to use to configure the switch.

#### Execution example
```python main.py "192.168.2.190" "admin" "***" "config.yml"```

### Configuration
The configuration file is based on YAML and expects the following schema:
```
switch:
  address: string
config:
  vlans:
    - name: string
      state: string [ present | absent ]
```

For an example see [config.yml](config.yml).
