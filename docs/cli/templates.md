# `templates`
View file templates to be used with [notifer](/plugins/index.md#notifier-services-output) plugins.

## Optional arguments
|  Argument | Description |
| --- | --- |
|`--name <template_name>`| Filter by `<template_name>`|
| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |

## Examples
```console
# Shows all templates
$ flexget templates

# Filters by name 'rss'
$ flexget templates --name rss
```