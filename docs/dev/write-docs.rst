.. _Docstrings and documentation:

============================
Docstrings and documentation
============================

Contributing to docstrings
==========================

.. attention::
   All docstrings must be written in reStructuredText (reST) to ensure proper rendering
   in our documentation system.

When writing or updating docstrings, please use the Sphinx-style format. Here is a basic
example of a properly formatted Sphinx-style docstring::

    def example_function(param1: int, param2: str) -> bool:
        """
        Briefly describe what the function does.

        :param param1: Description of the first parameter.
        :param param2: Description of the second parameter.
        :return: Description of the return value.
        """
        pass

Make sure your docstrings are clear, concise, and follow the project's style guidelines.

Building and contributing to the documentation
==============================================

#. To build the HTML documentation, first :ref:`install the docs dependencies
   <Installing the docs dependencies>`.

#. Enter the virtual environment:

   .. tab-set::
      :sync-group: os

      .. tab-item:: Unix
         :sync: Unix

         .. code:: console

            $ source .venv/bin/activate

      .. tab-item:: Windows
         :sync: Windows

         .. code:: console

            $ Set-ExecutionPolicy Unrestricted -Scope CurrentUser
            $ .venv\Scripts\activate.ps1

#. Then navigate to the ``docs`` directory:

   .. code:: console

      $ cd docs

#. Finally, run:

   .. tab-set::
      :sync-group: os

      .. tab-item:: Unix
         :sync: Unix

         .. code:: console

            $ make html

      .. tab-item:: Windows
         :sync: Windows

         .. code:: console

            $ .\make html

Built docs are at ``docs/_build/html``.

If you want to make changes, feel free to submit a pull request.
