import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Matches "Custom Title <doc_path>" syntax directly without relying on Sphinx internal imports
EXPLICIT_TITLE_RE = re.compile(r'^(.+?)\s*(?<!\x00)<([^<]*?)>$')


class TocTableDirective(Directive):
    """
    Usage example:

        ```{toctable}
        :caption: Quick Navigation
        :maxdepth: 1

        guide/intro : **Quickstart** guide with [official link](https://example.com) <br> Second line
        Intro Alias <guide/intro> : Alias entry pointing to the same intro document
        Custom API Name <reference/api> : Core `API` reference
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
        Parse a single line in one of the following formats:
        1. path/to/doc : Description text
        2. Custom Display Name <path/to/doc> : Description text

        Returns:
            (custom_title, doc_path, desc)
            where custom_title is None if angle brackets are not used.
        """
        if ':' not in line:
            raise self.error(
                f'[toctable] Missing description separator ":" in line: "{line}". '
                f'Expected format: "docname : description" or "title <docname> : description" '
                f'(at line {line_lineno}).'
            )

        # Safely split by the first ':' after '>' if '<...>' is present,
        # allowing colons inside custom titles if needed.
        if '>' in line and '<' in line and line.find('<') < line.find('>') < line.find(':', line.find('>')):
            sep_idx = line.find(':', line.find('>'))
            left_part, desc = line[:sep_idx].strip(), line[sep_idx + 1:].strip()
        else:
            left_part, desc = line.split(':', 1)
            left_part = left_part.strip()
            desc = desc.strip()

        if not left_part:
            raise self.error(
                f'[toctable] Missing document target before ":" in line: "{line}" (at line {line_lineno}).'
            )

        if not desc:
            raise self.error(
                f'[toctable] Empty description for target "{left_part}". '
                f'Please provide a non-empty description after ":" (at line {line_lineno}).'
            )

        # Match "Custom Title <doc_path>"
        match = EXPLICIT_TITLE_RE.match(left_part)
        if match:
            custom_title = match.group(1).strip()
            doc_path = match.group(2).strip()
            if not doc_path:
                raise self.error(
                    f'[toctable] Empty document path inside angle brackets "<>" in line: "{line}" '
                    f'(at line {line_lineno}).'
                )
            return custom_title, doc_path, desc

        return None, left_part, desc

    def _parse_desc_into_entry(self, entry_node, desc, line_lineno, source_path):
        """
        Parse Markdown/rST inline syntax ([link](), **bold**, `code`) and <br> tags
        into docutils nodes inside the table cell.
        """
        parts = re.split(r'<br\s*/?>', desc, flags=re.IGNORECASE)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            temp_container = nodes.Element()
            rst_lines = StringList([part], items=[(source_path, line_lineno)])
            self.state.nested_parse(rst_lines, self.content_offset, temp_container)

            for child in temp_container.children:
                entry_node += child

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname
        source_path = env.doc2path(base_doc)

        # ────────────────────────────────
        # 1. Collect document list and descriptions (without deduplicating by docname)
        # ────────────────────────────────
        items = []  # Format: [(display_name, docname, desc, line_lineno), ...]

        for idx, line in enumerate(self.content):
            line_str = line.strip()
            if not line_str:
                continue

            line_lineno = self.content_offset + idx + 1
            custom_title, doc_path, desc = self._parse_line(line_str, line_lineno)

            docname, _ = env.relfn2path(doc_path, base_doc)

            if docname not in env.found_docs:
                logger.warning(
                    f"[toctable] Document not found: {docname}",
                    location=(base_doc, line_lineno)
                )
                continue

            # Use custom title from <...> if provided, otherwise fallback to filename without extension
            display_name = (
                custom_title
                if custom_title
                else os.path.splitext(os.path.basename(docname))[0]
            )
            items.append((display_name, docname, desc, line_lineno))

        # Sort items within this single directive by display_name (case-insensitive)
        items.sort(key=lambda x: x[0].lower())

        # Keep includefiles unique for Sphinx's internal file tracker, while entries keep all aliases
        includefiles = list(dict.fromkeys(item[1] for item in items))

        # ────────────────────────────────
        # 2. Build toctree node (for sidebar navigation)
        # ────────────────────────────────
        toctree_entries = [(item[0], item[1]) for item in items]

        toctree_node = addnodes.toctree()
        toctree_node['entries'] = toctree_entries
        toctree_node['maxdepth'] = self.options.get('maxdepth', 1)
        toctree_node['glob'] = False
        toctree_node['caption'] = self.options.get('caption')
        toctree_node['hidden'] = True
        toctree_node['includefiles'] = includefiles
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

        for display_name, docname, desc, line_lineno in items:
            link = app.builder.get_relative_uri(base_doc, docname)

            row = nodes.row()
            row['sort_key'] = display_name.lower()
            row['docname'] = docname

            # Column 1: Display name (custom title or filename) and link
            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=display_name, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

            # Column 2: Rich-text parsed description
            entry2 = nodes.entry()
            self._parse_desc_into_entry(entry2, desc, line_lineno, source_path)
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
    Merges all `toctable` toctree nodes on the page into the first one and sorts alphabetically,
    preserving multiple aliases pointing to the same document.
    """
    toctable_nodes = [
        node for node in doctree.findall(addnodes.toctree)
        if node.get('is_toctable')
    ]

    if len(toctable_nodes) > 1:
        primary_toc = toctable_nodes[0]
        merged_entries = []

        for node in toctable_nodes:
            for title, docname in node['entries']:
                merged_entries.append((title, docname))

        # Sort all entries across all toctables alphabetically by display title
        merged_entries.sort(key=lambda x: (x[0] or '').lower())

        primary_toc['entries'] = merged_entries
        primary_toc['includefiles'] = list(
            dict.fromkeys(docname for _, docname in merged_entries)
        )

        for node in toctable_nodes[1:]:
            node.parent.remove(node)


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    app.connect('doctree-read', merge_and_sort_toctables, priority=100)
    return {'version': '2.2', 'parallel_read_safe': True}
