# `plugins`
Print summaries for registered [plugins](/plugins/index).

## Optional arguments
| Argument | Description |
| --- | --- |
| `--group <group>` | Show plugins belonging to specify `<group>` |
| `--phase <phase>` | Show plugins that act on specified `<phase>` |
| `--builtins` | Show only [builtin](/guide/index) plugins |
| [`--table-type {plain,porcelain,github,single,double}`](/cli/misc/table-styles) | Select output table style |
| [`--porcelain`](/cli/misc/table-styles) | Make the output parseable. Similar to using `--table-type porcelain` |

## Examples
```console
#shows all builtin plugins
$ flexget plugins --builtins
```