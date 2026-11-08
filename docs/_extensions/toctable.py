import os
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.util import logging

logger = logging.getLogger(__name__)


class TocTableDirective(Directive):
    """
    Usage example:

        ```{toctable}
        :caption: Quick Navigation
        :maxdepth: 1

        guide/intro : Quickstart guide
        reference/api : Core API reference
        ```
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'maxdepth': directives.nonnegative_int,
        'caption': directives.unchanged,
        'hidden': directives.flag,
    }

    def _parse_line(self, line, line_lineno):
        """
        Parse a single line in the format: path/to/doc : Description text.
        Raises a directive error if the colon or description is missing.
        """
        if ':' not in line:
            raise self.error(
                f'[toctable] Missing description separator ":" in line: "{line}". '
                f'Expected format: "docname : description" (at line {line_lineno}).'
            )

        doc_path, desc = line.split(':', 1)
        doc_path = doc_path.strip()
        desc = desc.strip()

        if not doc_path:
            raise self.error(
                f'[toctable] Missing document path before ":" in line: "{line}" (at line {line_lineno}).'
            )

        if not desc:
            raise self.error(
                f'[toctable] Empty description for document "{doc_path}". '
                f'Please provide a non-empty description after ":" (at line {line_lineno}).'
            )

        return doc_path, desc

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname

        # ────────────────────────────────
        # 1. Collect document list and descriptions
        # ────────────────────────────────
        seen = set()
        unique_items = []  # Format: [(display_name, docname, desc), ...]

        for idx, line in enumerate(self.content):
            line_str = line.strip()
            if not line_str:
                continue

            # Calculate the exact line number in the source file for accurate error reporting
            line_lineno = self.content_offset + idx + 1
            doc_path, desc = self._parse_line(line_str, line_lineno)

            docname, _ = env.relfn2path(doc_path, base_doc)

            if docname not in env.found_docs:
                logger.warning(
                    f"[toctable] Document not found: {docname}",
                    location=(base_doc, line_lineno)
                )
                continue

            if docname not in seen:
                seen.add(docname)
                display_name = os.path.splitext(os.path.basename(docname))[0]
                unique_items.append((display_name, docname, desc))

        # Sort items within this single directive first
        unique_items.sort(key=lambda x: x[0].lower())
        docnames = [item[1] for item in unique_items]

        # ────────────────────────────────
        # 2. Build toctree node (for sidebar navigation)
        # ────────────────────────────────
        toctree_entries = [(item[0], item[1]) for item in unique_items]

        toctree_node = addnodes.toctree()
        toctree_node['entries'] = toctree_entries
        toctree_node['maxdepth'] = self.options.get('maxdepth', 1)
        toctree_node['glob'] = False
        toctree_node['caption'] = self.options.get('caption')
        toctree_node['hidden'] = True
        toctree_node['includefiles'] = docnames
        toctree_node['numbered'] = False
        toctree_node['titlesonly'] = False
        toctree_node['is_toctable'] = True

        # ────────────────────────────────
        # 3. Build table node
        # ────────────────────────────────
        table = nodes.table()
        table['is_toctable_table'] = True
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=25)
        tgroup += nodes.colspec(colwidth=75)
        thead = nodes.thead()
        tbody = nodes.tbody()
        tgroup += thead
        tgroup += tbody

        header = nodes.row()
        header += nodes.entry('', nodes.paragraph(text='Document'))
        header += nodes.entry('', nodes.paragraph(text='Description'))
        thead += header

        for display_name, docname, desc in unique_items:
            link = app.builder.get_relative_uri(base_doc, docname)

            row = nodes.row()
            row['sort_key'] = display_name.lower()
            row['docname'] = docname

            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=display_name, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

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


def merge_and_sort_toctables(app, doctree):
    """
    Runs at priority 100 (before Sphinx's TocTreeCollector at priority 500).
    Merges all `toctable` toctree nodes on the page into the first one and sorts alphabetically.
    """
    toctable_nodes = [
        node for node in doctree.findall(addnodes.toctree)
        if node.get('is_toctable')
    ]

    if len(toctable_nodes) > 1:
        primary_toc = toctable_nodes[0]
        seen_docs = set()
        merged_entries = []

        for node in toctable_nodes:
            for title, docname in node['entries']:
                if docname not in seen_docs:
                    seen_docs.add(docname)
                    merged_entries.append((title, docname))

        # Sort all entries across all toctables alphabetically
        merged_entries.sort(key=lambda x: (x[0] or '').lower())

        primary_toc['entries'] = merged_entries
        primary_toc['includefiles'] = [docname for _, docname in merged_entries]

        for node in toctable_nodes[1:]:
            node.parent.remove(node)


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    app.connect('doctree-read', merge_and_sort_toctables, priority=100)
    return {'version': '1.8', 'parallel_read_safe': True}