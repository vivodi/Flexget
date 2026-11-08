import os
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.util import logging

logger = logging.getLogger(__name__)


class TocTableDirective(Directive):
    """
    Usage example:

        .. toctable::
           :caption: Quick Navigation
           :maxdepth: 1

           guide/intro : Quickstart guide, including installation and basic configuration
           guide/advanced : Advanced features and custom extensions
           reference/api : Core API reference manual
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'maxdepth': directives.nonnegative_int,
        'caption': directives.unchanged,
        'hidden': directives.flag,
    }

    def _parse_line(self, line):
        """
        Parse a single line in the format: path/to/doc : Description text.
        Defaults to "No description available" if no colon/description is provided.
        """
        if ':' in line:
            doc_path, desc = line.split(':', 1)
            return doc_path.strip(), desc.strip()
        return line.strip(), 'No description available'

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname

        # ────────────────────────────────
        # 1. Collect document list and descriptions
        # ────────────────────────────────
        seen = set()
        unique_items = []  # Format: [(docname, desc), ...]

        for line in self.content:
            line_str = line.strip()
            if not line_str:
                continue

            doc_path, desc = self._parse_line(line_str)
            if not doc_path:
                continue

            # Convert relative path to Sphinx internal docname
            docname, _ = env.relfn2path(doc_path, base_doc)

            # Deduplicate while preserving order
            if docname not in seen:
                seen.add(docname)
                unique_items.append((docname, desc))

        docnames = [item[0] for item in unique_items]

        # ────────────────────────────────
        # 2. Build toctree node (for sidebar navigation)
        # ────────────────────────────────
        # To display filename without extension instead of doc title in toctree,
        # pass the filename as the explicit title: (display_name, docname).
        toctree_entries = [
            (os.path.splitext(os.path.basename(d))[0], d) for d in docnames
        ]

        toctree_node = addnodes.toctree()
        toctree_node['entries'] = toctree_entries
        toctree_node['maxdepth'] = self.options.get('maxdepth', 1)
        toctree_node['glob'] = False
        toctree_node['caption'] = self.options.get('caption')
        toctree_node['hidden'] = True
        toctree_node['includefiles'] = docnames
        toctree_node['numbered'] = False
        toctree_node['titlesonly'] = False

        # ────────────────────────────────
        # 3. Build table node
        # ────────────────────────────────
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
        header += nodes.entry('', nodes.paragraph(text='Keyword'))
        header += nodes.entry('', nodes.paragraph(text='Description'))
        thead += header

        for docname, desc in unique_items:
            if docname not in env.found_docs:
                logger.warning(
                    f"[toctable] Document not found: {docname}",
                    location=(base_doc, self.lineno)
                )
                continue

            # Display filename without extension instead of document title
            display_name = os.path.splitext(os.path.basename(docname))[0]
            link = app.builder.get_relative_uri(base_doc, docname)

            row = nodes.row()

            # Column 1: Document filename and link
            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=display_name, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

            # Column 2: Inline description
            entry2 = nodes.entry()
            para2 = nodes.paragraph(text=desc)
            entry2 += para2
            row += entry2

            tbody += row

        # ────────────────────────────────
        # 4. Output: return toctree and table nodes
        # ────────────────────────────────
        if 'hidden' in self.options:
            return [table]
        else:
            return [toctree_node, table]


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    return {'version': '1.1', 'parallel_read_safe': True}
