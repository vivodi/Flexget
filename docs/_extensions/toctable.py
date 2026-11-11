import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)

# Matches either:
# 1. "Custom Title <doc_path> : Description" -> groups: (custom_title, doc_path, None, desc)
# 2. "doc_path : Description"                -> groups: (None, None, doc_path, desc)
LINE_RE = re.compile(r'^(?:(.+?)\s*<([^<>]+)>|([^:<>]+?))\s*:\s*(.+)$')

REF_PREFIX = 'plugin:'


class TocTableDirective(Directive):
    """
    Usage example:

        ```{toctable}
        :caption: Quick Navigation
        :maxdepth: 1

        list/imdb_list : Use movies in your IMDb list...
        Custom Name <rss> : Parse RSS-feed.
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

    def _register_plugin_ref(self, env, display_name, target_docname, line_lineno):
        """
        Register `display_name` in `env.toctable_plugin_refs` for `[](plugin:<name>)` links.
        """
        if not hasattr(env, 'toctable_plugin_refs'):
            env.toctable_plugin_refs = {}

        key_lower = display_name.lower()
        existing = env.toctable_plugin_refs.get(key_lower)
        if existing and existing[0] != target_docname and existing[2] != env.docname:
            logger.warning(
                f'[toctable] Duplicate plugin reference "{REF_PREFIX}{display_name}": '
                f'previously pointed to "{existing[0]}", now overwritten by "{target_docname}".',
                location=(env.docname, line_lineno)
            )

        for key in (display_name, key_lower, nodes.fully_normalize_name(display_name)):
            env.toctable_plugin_refs[key] = (target_docname, display_name, env.docname)

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname
        source_path = env.doc2path(base_doc)

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

            display_name = (
                custom_title
                if custom_title
                else os.path.splitext(os.path.basename(docname))[0]
            )
            items.append((display_name, docname, desc, line_lineno))

            self._register_plugin_ref(env, display_name, docname, line_lineno)

        items.sort(key=lambda x: x[0].lower())
        includefiles = list(dict.fromkeys(item[1] for item in items))

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

            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(text=display_name, refuri=link)
            para1 += ref
            entry1 += para1
            row += entry1

            entry2 = nodes.entry()
            self._parse_desc_into_entry(entry2, desc, line_lineno, source_path)
            row += entry2

            tbody += row

        if 'hidden' in self.options:
            return [table]
        else:
            return [toctree_node, table]


def merge_and_sort_toctables(app, doctree):
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

        merged_entries.sort(key=lambda x: (x[0] or '').lower())

        primary_toc['entries'] = merged_entries
        primary_toc['includefiles'] = list(
            dict.fromkeys(docname for _, docname in merged_entries)
        )

        for node in toctable_nodes[1:]:
            node.parent.remove(node)


def merge_toctable_plugin_refs(app, env, docnames, other):
    if not hasattr(other, 'toctable_plugin_refs'):
        return
    if not hasattr(env, 'toctable_plugin_refs'):
        env.toctable_plugin_refs = {}

    env.toctable_plugin_refs.update(other.toctable_plugin_refs)


class PluginReferenceTransform(SphinxPostTransform):
    """
    Runs at priority 3 — strictly BEFORE MyST-Parser's `ResolveMystReferences` (priority 4).
    Resolves `[](plugin:xxx)` and `[Custom Text](plugin:xxx)` into internal document links.
    """
    default_priority = 3

    def _lookup_plugin(self, plugin_name):
        labels = getattr(self.env, 'toctable_plugin_refs', {})
        match = (
            labels.get(plugin_name)
            or labels.get(plugin_name.lower())
            or labels.get(nodes.fully_normalize_name(plugin_name))
        )
        if match:
            return match[0], match[1]

        # Fallback for incremental builds when toctable pages were not re-parsed
        target_lower = plugin_name.lower()
        for doc in self.env.found_docs:
            if os.path.splitext(os.path.basename(doc))[0].lower() == target_lower:
                return doc, os.path.splitext(os.path.basename(doc))[0]
        return None

    def run(self, **kwargs):
        fromdocname = self.env.docname

        # 1. Intercept `pending_xref` nodes generated by MyST `[](plugin:xxx)`
        for node in list(self.document.findall(addnodes.pending_xref)):
            target = node.get('reftarget', '')
            if not target.lower().startswith(REF_PREFIX):
                continue

            plugin_name = target[len(REF_PREFIX):].strip()
            match = self._lookup_plugin(plugin_name)
            if not match:
                logger.warning(
                    f'[toctable] Unknown plugin reference "{target}".',
                    location=node
                )
                node.replace_self(nodes.inline(plugin_name, plugin_name))
                continue

            target_docname, default_title = match

            if node.get('refexplicit'):
                inner_node = node.children[0].deepcopy() if node.children else nodes.inline(default_title, default_title)
            else:
                inner_node = nodes.inline(default_title, default_title)

            refnode = make_refnode(
                self.app.builder,
                fromdocname,
                target_docname,
                '',
                inner_node,
                default_title,
            )
            node.replace_self(refnode)

        # 2. Intercept direct `nodes.reference` in case `plugin:` is parsed as a raw URL scheme
        for node in list(self.document.findall(nodes.reference)):
            refuri = node.get('refuri', '')
            if not refuri.lower().startswith(REF_PREFIX):
                continue

            plugin_name = refuri[len(REF_PREFIX):].strip()
            match = self._lookup_plugin(plugin_name)
            if not match:
                logger.warning(
                    f'[toctable] Unknown plugin reference "{refuri}".',
                    location=node
                )
                continue

            target_docname, default_title = match
            new_uri = self.app.builder.get_relative_uri(fromdocname, target_docname)
            node['refuri'] = new_uri
            node['internal'] = True

            current_text = node.astext().strip()
            if not current_text or current_text.lower() == refuri.lower():
                node.clear()
                node += nodes.Text(default_title)


def setup(app):
    app.add_directive('toctable', TocTableDirective)
    app.connect('doctree-read', merge_and_sort_toctables, priority=100)
    app.connect('env-merge-info', merge_toctable_plugin_refs)
    app.add_post_transform(PluginReferenceTransform)
    return {'version': '3.0', 'parallel_read_safe': True}