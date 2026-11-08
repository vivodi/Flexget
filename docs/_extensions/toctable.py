import os, fnmatch
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes

class TocTableDirective(Directive):
    """
        Directive to render a table of contents as a two-column summary table
        (Document Title and Description) while registering entries into Sphinx's toctree.

        Usage Examples:

        1. reStructuredText (Target Document with Description):
           Add the `:tocdesc:` field at the very top of the referenced document.

           .. code-block:: rst

               :tocdesc: A step-by-step tutorial to configure and launch your project.

               Getting Started
               ===============

               Welcome to the setup tutorial...

        2. reStructuredText (Navigation Page invoking `toctable`):
           Insert the directive where you want the table and toctree to appear.

           .. code-block:: rst

               User Guide
               ==========

               .. toctable::
                  :caption: Quick Navigation
                  :glob:
                  :maxdepth: 1

                  guide/*
                  reference/*


        3. (NOT WORKING!! As noted in the code comments below, tocdesc in Markdown is actually
           only read successfully during an incremental build where the invocation method is
           changed.)
           Markdown / MyST (Target Document with Description):
           Define `tocdesc` in the YAML front-matter at the beginning of the file.

           .. code-block:: markdown

               ---
               tocdesc: Complete API reference and configuration schema definitions.
               ---

               # Configuration Reference

               Here are the reference details...

        4. Markdown / MyST (Navigation Page invoking `toctable`):
           Call the directive using standard MyST syntax (` ```{toctable} `).

           .. code-block:: markdown

               # Overview

               ```{toctable}
               :caption: Directory Index
               :glob:
               :maxdepth: 1

               guide/*
               reference/*
               ```
        """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'maxdepth': directives.nonnegative_int,
        'glob': directives.flag,
        'caption': directives.unchanged,
        'hidden': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname
        srcdir = app.srcdir

        # ─────────────────────────────────────────────
        # 1. Collect document names (supports globbing)
        # ─────────────────────────────────────────────
        docnames = []
        for line in self.content:
            pattern = line.strip()
            if not pattern:
                continue

            if 'glob' in self.options:
                base_dir = os.path.dirname(env.doc2path(base_doc))
                abs_pattern = os.path.normpath(os.path.join(base_dir, pattern))

                for found_doc in sorted(env.found_docs):
                    abs_doc_path = os.path.normpath(env.doc2path(found_doc))
                    if fnmatch.fnmatch(abs_doc_path, abs_pattern):
                        docnames.append(found_doc)
            else:
                docname, _ = env.relfn2path(pattern, base_doc)
                docnames.append(docname)

        # Deduplicate while preserving order
        seen = set()
        docnames = [d for d in docnames if not (d in seen or seen.add(d))]

        # ─────────────────────────────────────────────
        # 2. Build the toctree node (registers in sidebar)
        # ─────────────────────────────────────────────
        toctree_node = addnodes.toctree()
        toctree_node['entries'] = [(None, d) for d in docnames]
        toctree_node['maxdepth'] = self.options.get('maxdepth', 1)
        toctree_node['glob'] = 'glob' in self.options
        toctree_node['caption'] = self.options.get('caption')
        toctree_node['hidden'] = True
        toctree_node['includefiles'] = docnames
        toctree_node['numbered'] = False
        toctree_node['titlesonly'] = False

        # ─────────────────────────────────────────────
        # 3. Construct the table node
        # ─────────────────────────────────────────────
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=25)
        tgroup += nodes.colspec(colwidth=75)
        thead = nodes.thead()
        tbody = nodes.tbody()
        tgroup += thead
        tgroup += tbody

        # Table header
        header = nodes.row()
        header += nodes.entry('', nodes.paragraph(text='Plugin'))
        header += nodes.entry('', nodes.paragraph(text='Description'))
        thead += header

        for docname in docnames:
            if docname not in env.found_docs:
                app.warn(f"[toctable] Document not found: {docname}")
                continue

            title_node = env.titles.get(docname)
            title = title_node.astext() if title_node else os.path.basename(docname)
            # TODO: BUG: When `tocdesc` is applied to Markdown files, `env.metadata.get(docname)`
            #  returns `None` during a clean build (no cache), and only contains values during
            #  cached incremental builds. However, re-running the build directly fails to
            #  re-trigger this code block. In fact, `tocdesc` appears correctly in the generated
            #  output only after alternating the execution: running it once with `:glob:` and
            #  `plugin.md`, followed by another run without `glob` using `plugin` (or the other
            #  way around).
            desc = env.metadata.get(docname, {}).get('tocdesc', '(No description available)')
            print(f'docname: {env.metadata.get(docname)}0000')
            link = app.builder.get_relative_uri(env.docname, docname)

            row = nodes.row()
            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=title, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

            entry2 = nodes.entry()
            para2 = nodes.paragraph(text=desc)
            entry2 += para2
            row += entry2

            tbody += row

        # ─────────────────────────────────────────────
        # 4. Output: Return toctree node and/or table
        # ─────────────────────────────────────────────
        if 'hidden' in self.options:
            # If hidden, only render the table in document body without toctree registration
            return [table]
        else:
            return [toctree_node, table]


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    return {'version': '0.1', 'parallel_read_safe': True}
