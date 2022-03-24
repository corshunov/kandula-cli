# Kandula CLI

Welcome to Kandula CLI!

The tool provides command line interface to operate Kandula application servers.

Kandula servers must be tagged with key <main_tag_key> and value <main_tag_value> which can be adjusted in 'settings.json' file.

Default values are:  
- `main_tag_key`:   Project  
- `main_tag_value`: kandula

The tool provides 4 methods:
- get-instances
  Allows to get Kandula instances (either just names, or full info by using flag `-f`).
  The output by default is text styled depending on instance state:
  | State         | Style              |
  |:--------------|:-------------------|
  | pending       | green underlined   |
  | running       | green              |
  | stopping      | default underlined |
  | stopped       | default            |
  | shutting-down | red underlined     |
  | terminated    | red                |

- start-instances
- stop-instances
- terminate-instances

CLI does logging to `kandula.log` file as well as to stream when launched with flag `-v`.
