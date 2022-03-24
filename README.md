# Kandula CLI

Welcome to Kandula CLI!

The tool provides command line interface to operate Kandula application servers.

Kandula servers must be tagged with key `main_tag_key` and value `main_tag_value` which can be adjusted in `settings.json` file.

Default values are:  
| Setting        | Default value |
|:---------------|:--------------|
| main_tag_key   | Project       |
| main_tag_value | kandula       |

The tool provides 4 methods:
- get-instances  
  Allows to get Kandula instances (either just names, or full info by using flag `-f`).  
  The output by default is text styled depending on instance state:
  | State         | Style                                                    |
  |:--------------|:---------------------------------------------------------|
  | pending       | <u><span style="color:green">green underlined</span></u> |
  | running       | <span style="color:green">green</span>                   |
  | stopping      | <u>default underlined</u>                                |
  | stopped       | default                                                  |
  | shutting-down | <u><span style="color:red">red underlined</span></u>     |
  | terminated    | <span style="color:red">green</span>                     |

- start-instances  
  Only instances in stopped state can be started. Instances in other states are ignored.  

- stop-instances  
  Only instances in running or pending state can be stopped. Instances in other states are ignored.

- terminate-instances  
  Instances already in shutting-down or terminated states are ignored.

Methods to start, stop, and terminate instances support flag `--dry-run` allowing to show the result of operations without actually running them.

The tool logs to `script_dir/kandula.log` file and allows to print logs to terminal (`-v` for WARNING level and `-vv` for INFO level).
