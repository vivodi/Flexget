# Creating a Plugin

FlexGet's functionality is built entirely around plugins. Every plugin is a Python class that defines a configuration schema, hooks into specific task execution phases, and registers itself with the core event system.

## Minimal Example

Create a new Python module in `flexget/plugins/` (for example, `flexget/plugins/filter/my_plugin.py`):

```python
from loguru import logger

from flexget import plugin
from flexget.event import event

logger = logger.bind(name='my_plugin')


class MyPlugin:
    """A brief description of what this plugin does."""

    schema = {
        'type': 'boolean',
    }

    @plugin.priority(plugin.PRIORITY_DEFAULT)
    def on_task_filter(self, task, config):
        if not config:
            return
        for entry in task.entries:
            if 'unwanted' in entry['title'].lower():
                entry.reject('Title contains an unwanted keyword')


@event('plugin.register')
def register_plugin():
    plugin.register(MyPlugin, 'my_plugin', api_ver=2)
```

---

## Core Components

### 1. Configuration Schema

The `schema` attribute uses [JSON Schema](https://json-schema.org/) to validate user configurations in `config.yml` before the task runs.

```python
schema = {
    'type': 'object',
    'properties': {
        'keyword': {'type': 'string'},
        'case_sensitive': {'type': 'boolean', 'default': False},
    },
    'required': ['keyword'],
    'additionalProperties': False,
}
```

### 2. Task Phase Methods

Plugins interact with tasks by implementing `on_task_<phase>(self, task, config)` methods. Every phase method receives the current `task` instance and the validated user `config`.

| Phase Method | Purpose |
| :--- | :--- |
| `on_task_start` | Initialize resources or validate prerequisites before processing begins. |
| `on_task_input` | Generate and return a list of `Entry` objects. |
| `on_task_metainfo` | Enrich existing entries with additional fields or metadata. |
| `on_task_filter` | Call `entry.accept()` or `entry.reject()` to filter entries. |
| `on_task_modify` | Alter entry fields prior to output execution. |
| `on_task_download` | Fetch files associated with accepted entries. |
| `on_task_output` | Perform actions on `task.accepted` entries (e.g., send to a client). |
| `on_task_exit` | Clean up resources after the task finishes effortlessly. |

```{tip}
Use the `@plugin.priority(value)` decorator on any phase method to control execution order when multiple plugins run in the same phase (higher numbers run first; default is `128`).
```

### 3. Plugin Registration

Register the plugin at the bottom of your module using the `@event('plugin.register')` decorator:

```python
@event('plugin.register')
def register_plugin():
    plugin.register(MyPlugin, 'my_plugin', api_ver=2, interfaces=['task'])
```

```{note}
Always specify `api_ver=2`. By default, `interfaces=['task']` is assumed, allowing the plugin to be used directly at the task level in `config.yml`.
```

---

## Error Handling

When handling runtime errors inside a plugin, use FlexGet's built-in exception classes from `flexget.plugin` instead of raising generic Python exceptions:

* **`PluginError`**: Exception class that should be raised when an expected error occurs in a plugin which should terminate task/feed execution (such as unreachable endpoints, invalid credentials, or missing required files). Raising `PluginError` cleanly aborts the current task and logs the failure without printing a raw stack trace.
* **`PluginWarning`**: For non-abort situations, raise `PluginWarning` to log a warning message without halting task execution.

```python
from flexget.plugin import PluginError, PluginWarning


class MyOutputPlugin:
    schema = {'type': 'string'}

    def on_task_output(self, task, config):
        if not self.service_available(config):
            # Expected error that should terminate task/feed execution
            raise PluginError(f'Cannot connect to service at {config}')

        if not task.accepted:
            # Non-abort situation
            raise PluginWarning('No accepted entries to process')
```
