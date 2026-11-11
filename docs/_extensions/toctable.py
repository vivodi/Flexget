import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)

# Matches either:
# 1. "Custom Title <doc_path> : Description" -> groups: (custom_title, doc_path, None, desc)
# 2. "doc_path : Description"                -> groups: (None, None, doc_path, desc)
LINE_RE = re.compile(r'^(?:(.+?)\s*<([^<>]+)>|([^:<>]+?))\s*:\s*(.+)$')


class TocTableDirective(Directive):
    """
    Usage example:

        ```{toctable}
        :caption: Quick Navigation
        :maxdepth: 1

        guide/intro : **Quickstart** guide with [official link](https://example.com) <br> **Note:** Second line
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

        match = LINE_RE.match(line)
        if not match:
            raise self.error(
                f'[toctable] Invalid syntax or empty description in line: "{line}". '
                f'Expected format: "docname : description" or "title <docname> : description" '
                f'(at line {line_lineno}).'
            )

        custom_title_grp, bracket_path_grp, plain_path_grp, desc = match.groups()
        desc = desc.strip()

        if bracket_path_grp is not None:
            custom_title = custom_title_grp.strip()
            doc_path = bracket_path_grp.strip()
        else:
            custom_title = None
            doc_path = plain_path_grp.strip()

        if not doc_path:
            raise self.error(
                f'[toctable] Empty document path in line: "{line}" (at line {line_lineno}).'
            )

        if not desc:
            raise self.error(
                f'[toctable] Empty description for target "{doc_path}" (at line {line_lineno}).'
            )

        return custom_title, doc_path, desc

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

    def _register_ref_label(self, env, display_name, target_docname):
        """
        Store `display_name` in a fallback dictionary on `env` rather than polluting `std` domain labels directly.
        This ensures relative file links in the current directory take priority over `toctable` global names.
        """
        if not hasattr(env, 'toctable_ref_labels'):
            env.toctable_ref_labels = {}

        for key in (display_name, display_name.lower()):
            env.toctable_ref_labels[key] = (target_docname, display_name)

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

            # Register display_name in our fallback lookup table
            self._register_ref_label(env, display_name, docname)

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


def merge_toctable_ref_labels(app, env, docnames, other):
    """
    Support Sphinx parallel builds (-j auto) by merging registered ref labels across workers.
    """
    if not hasattr(other, 'toctable_ref_labels'):
        return
    if not hasattr(env, 'toctable_ref_labels'):
        env.toctable_ref_labels = {}

    env.toctable_ref_labels.update(other.toctable_ref_labels)


def resolve_toctable_missing_reference(app, env, node, contnode):
    """
    Fallback resolver for unresolved references (`[text](name)`, `[](name)`, `{ref}`name``, `{doc}`name``).
    Only triggered AFTER local relative file paths and explicit std labels failed to match.
    """
    target = node.get('reftarget')
    if not target:
        return None

    fromdocname = node.get('refdoc', env.docname)

    # 1. Always check if `target` exists as a relative document in the current directory FIRST
    rel_docname, _ = env.relfn2path(target, fromdocname)
    if rel_docname in env.found_docs:
        target_docname = rel_docname
        default_title = os.path.splitext(os.path.basename(rel_docname))[0]
    else:
        # 2. Otherwise, fallback to `toctable` registered labels
        labels = getattr(env, 'toctable_ref_labels', {})
        match = labels.get(target) or labels.get(target.lower())
        if not match:
            return None
        target_docname, default_title = match

    # Determine link text: if user wrote `[](imdb_list)` (no explicit text), use `default_title`
    if node.get('refexplicit'):
        inner_node = contnode
    else:
        inner_node = nodes.inline(default_title, default_title)

    return make_refnode(
        app.builder,
        fromdocname,
        target_docname,
        '',
        inner_node,
        default_title,
    )


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    app.connect('doctree-read', merge_and_sort_toctables, priority=100)
    app.connect('env-merge-info', merge_toctable_ref_labels)
    app.connect('missing-reference', resolve_toctable_missing_reference)
    return {'version': '2.5', 'parallel_read_safe': True}
