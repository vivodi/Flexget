# No Entries Ok
FlexGet normally expects a task to produce entries on every run, and outputs a warning log entry if no entries were produced:
```text
Task didn't produce any entries. This is likely due to a mis-configured or non-functional input.
```
If you have a task where this is not indicative of a problem, you can change this to a verbose log entry (which is not normally output or logged), by including this plugin in the task.

## Configuration
```yaml
no_entries_ok: yes
```