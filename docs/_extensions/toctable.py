import os, fnmatch
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes


# Define a custom placeholder node
class toctable_node(nodes.General, nodes.Element):
    pass


class TocTableDirective(Directive):
    """
    Directive to render a table of contents as a two-column summary table
    (Document Title and Description) while registering entries into Sphinx's toctree.
    Collects target docnames and defers table rendering until all documents
    are fully read and metadata is populated.

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


        3. Markdown / MyST (Target Document with Description):
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
        base_doc = env.docname

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
        # 2. Build standard toctree node
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
        # 3. Create a placeholder node for deferred rendering
        # ─────────────────────────────────────────────
        placeholder = toctable_node()
        placeholder['docnames'] = docnames
        placeholder['base_doc'] = base_doc

        if 'hidden' in self.options:
            return [placeholder]
        else:
            return [toctree_node, placeholder]


def resolve_toctables(app, doctree, fromdocname):
    """
    Hooked to 'doctree-resolved' event.
    Executes after ALL documents have been read, guaranteeing env.metadata
    and env.titles are fully populated even on clean builds.
    """
    env = app.env

    for node in doctree.traverse(toctable_node):
        docnames = node.get('docnames', [])

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
        header += nodes.entry('', nodes.paragraph(text='Document'))
        header += nodes.entry('', nodes.paragraph(text='Description'))
        thead += header

        for docname in docnames:
            if docname not in env.found_docs:
                app.warn(f"[toctable] Document not found: {docname}")
                continue

            title_node = env.titles.get(docname)
            title = title_node.astext() if title_node else os.path.basename(docname)

            # Now env.metadata is 100% guaranteed to be populated
            raw_desc = env.metadata.get(docname, {}).get('tocdesc', '(No description available)')
            desc = str(raw_desc)  # Ensure conversion in case YAML parses dates/numbers
            link = app.builder.get_relative_uri(fromdocname, docname)

            row = nodes.row()

            # Title column with link
            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=title, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

            # Description column
            entry2 = nodes.entry()
            para2 = nodes.paragraph(text=desc)
            entry2 += para2
            row += entry2

            tbody += row

        # Replace placeholder node with the rendered table
        node.replace_self(table)


def setup(app):
    app.add_node(toctable_node)
    app.add_directive('toctable', TocTableDirective)
    # Register the hook so tables resolve after all docs are loaded
    app.connect('doctree-resolved', resolve_toctables)
    return {'version': '0.2', 'parallel_read_safe': True}
