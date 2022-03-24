# Kandula CLI

Welcome to Kandula CLI!

The tool provides command line interface to operate Kandula application servers.


## Installation

In order to use the tool:  
- download the tool with `git clone git@github.com:corshunov/kandula-cli.git`
- make sure you have AWS profile for using `awscli`  
- make sure you have Python3 installed
- install Python libs with `python3 -m pip install -r /script_dir/requirements.txt`
- make the script executable with `chmod +x /script_dir/kancli`  
- adjust settings (if needed)  
  Kandula servers must be tagged with key `main_tag_key` and value `main_tag_value` which can be adjusted in `settings.json` file.

  Default values are:  
  | Setting        | Default value |
  |:---------------|:--------------|
  | main_tag_key   | Project       |
  | main_tag_value | kandula       |


## Usage

The tool provides 4 methods:
- get-instances  
  Allows to get Kandula instances (either just names, or full info by using flag `-f`).  

  The output format can be set with option `-o` (`--output`) to `text` (default) or `json`.  
  Text output is styled depending on instance state:
  | State         | Style              |
  |:--------------|:-------------------|
  | pending       | green underlined   |
  | running       | green              |
  | stopping      | default underlined |
  | stopped       | default            |
  | shutting-down | red underlined     |
  | terminated    | red                |

  Instances can be filtered by state with option `-s` (`--state`). In order to specify several states, use the option several times (e.g. `kancli get-instances -s running -s stopped`).

- start-instances  
  Allows to start Kandula instances that are in stopped state. Instances in other states are ignored.  

- stop-instances  
  Allows to stop Kandula instances that are in running or pending state. Instances in other states are ignored.

- terminate-instances  
  Allows to terminate Kandula instances that are not already in shutting-down or terminated states.

Methods to start, stop, and terminate instances support flag `--dry-run` allowing to show the result of operations without actually running them.

The tool logs to `script_dir/kandula.log` file and allows to print logs to terminal by specifying flag `-v` (WARNING level) or `-vv` (INFO level) for all 4 methods.
