# Debugging with IPython

To use IPython as your default interactive debugger, configure your environment in two steps:

1. Install IPython:
   ```console
   $ pip install ipython
   ```
2. Point the default breakpoint hook to IPython:
   ```console
   $ export PYTHONBREAKPOINT=IPython.terminal.debugger.set_trace
   ```

Once configured, simply place `breakpoint()` anywhere in your code to drop directly into an IPython session.
