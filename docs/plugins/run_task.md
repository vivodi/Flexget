# Run Task

| Option | Default | Description |
| --- | --- | --- |
| when | always | Specify when other task(s) is/are executed. Possible values are `accepted`, `rejected`, `failed`, `aborted`, `always`.|
| task | -- | Name of task(s) to be executed

> Note that `aborted` is not included in `always`. Tasks will only run on `aborted` if specified.
{.is-warning}

#### Example

```yaml
run_task:
  when: accepted
  task: another-task-to-be-executed
```

```yaml
run_task:
  when: 
    - accepted
    - rejected
  task:
    - another-task-to-be-executed
    - third-task-to-be-executed
```
