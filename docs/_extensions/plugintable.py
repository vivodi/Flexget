import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.environment.adapters.toctree import TocTree
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)

REF_PREFIX = 'plugin:'


def _get_default_display_name(docname):
    """
    Return the default display name for a given Sphinx `docname`.
    If the document is `*/index`, return the parent directory name `*`.
    Otherwise, return the filename without extension.
    """
    norm_docname = docname.replace('\\', '/')
    base_name = os.path.splitext(os.path.basename(norm_docname))[0]
    if base_name == 'index':
        parent_dir = os.path.basename(os.path.dirname(norm_docname))
        if parent_dir:
            return parent_dir
    return base_name


class PluginTableDirective(Directive):
    """
    Usage example:

        ```{plugintable}
        :caption: Quick Navigation
        :maxdepth: 1

        list/imdb_list : Use movies in your IMDb list...
        daemon/index : Daemon mode documentation (displays as "daemon")
        rss : Parse RSS-feed.
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
                f'[plugintable] Missing description separator ":" in line: "{line}". '
                f'Expected format: "docname : description" (at line {line_lineno}).'
            )

        doc_path, desc = line.split(':', 1)
        doc_path = doc_path.strip()
        desc = desc.strip()

        if not doc_path:
            raise self.error(
                f'[plugintable] Empty document path before ":" in line: "{line}" (at line {line_lineno}).'
            )

        if not desc:
            raise self.error(
                f'[plugintable] Empty description for target "{doc_path}". '
                f'Please provide a non-empty description after ":" (at line {line_lineno}).'
            )

        return doc_path, desc

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
        Register `display_name` in `env.plugintable_plugin_refs` for `plugin:<name>` links.
        """
        if not hasattr(env, 'plugintable_plugin_refs'):
            env.plugintable_plugin_refs = {}

        key_lower = display_name.lower()
        existing = env.plugintable_plugin_refs.get(key_lower)
        if existing and existing[0] != target_docname and existing[2] != env.docname:
            logger.warning(
                f'[plugintable] Duplicate plugin reference "{REF_PREFIX}{display_name}": '
                f'previously pointed to "{existing[0]}", now overwritten by "{target_docname}".',
                location=(env.docname, line_lineno)
            )

        for key in (display_name, key_lower, nodes.fully_normalize_name(display_name)):
            env.plugintable_plugin_refs[key] = (target_docname, display_name, env.docname)

    def run(self):
        env = self.state.document.settings.env
        app = env.app
        base_doc = env.docname
        source_path = env.doc2path(base_doc)

        seen = set()
        unique_items = []  # Format: [(display_name, docname, desc, line_lineno), ...]

        for idx, line in enumerate(self.content):
            line_str = line.strip()
            if not line_str:
                continue

            line_lineno = self.content_offset + idx + 1
            doc_path, desc = self._parse_line(line_str, line_lineno)

            docname, _ = env.relfn2path(doc_path, base_doc)

            if docname not in env.found_docs:
                logger.warning(
                    f"[plugintable] Document not found: {docname}",
                    location=(base_doc, line_lineno)
                )
                continue

            # Deduplicate by docname within the directive
            if docname not in seen:
                seen.add(docname)
                display_name = _get_default_display_name(docname)
                unique_items.append((display_name, docname, desc, line_lineno))
                self._register_plugin_ref(env, display_name, docname, line_lineno)

        unique_items.sort(key=lambda x: x[0].lower())
        docnames = [item[1] for item in unique_items]

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
        toctree_node['is_plugintable'] = True

        table = nodes.table()
        table['is_plugintable_table'] = True
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=25)
        tgroup += nodes.colspec(colwidth=75)
        thead = nodes.thead()
        tbody = nodes.tbody()
        tgroup += thead
        tgroup += tbody

        header = nodes.row()
        header += nodes.entry('', nodes.paragraph(text='Keyword'))
        header += nodes.entry('', nodes.paragraph(text='Description'))
        thead += header

        for display_name, docname, desc, line_lineno in unique_items:
            link = app.builder.get_relative_uri(base_doc, docname)

            row = nodes.row()
            row['sort_key'] = display_name.lower()
            row['docname'] = docname

            # Column 1: Render display_name as inline code inside the link
            entry1 = nodes.entry()
            para1 = nodes.paragraph()
            ref = nodes.reference(refuri=link, internal=True)
            ref += nodes.literal(display_name, display_name)
            para1 += ref
            entry1 += para1
            row += entry1

            # Column 2: Rich-text parsed description
            entry2 = nodes.entry()
            self._parse_desc_into_entry(entry2, desc, line_lineno, source_path)
            row += entry2

            tbody += row

        if 'hidden' in self.options:
            return [table]
        else:
            return [toctree_node, table]


def merge_and_sort_plugintables(app, doctree):
    """
    Runs at priority 100 (before Sphinx's TocTreeCollector at priority 500).
    Merges all `plugintable` toctree nodes on the page into the first one and sorts alphabetically.
    """
    plugintable_nodes = [
        node for node in doctree.findall(addnodes.toctree)
        if node.get('is_plugintable')
    ]

    if len(plugintable_nodes) > 1:
        primary_toc = plugintable_nodes[0]
        seen_docs = set()
        merged_entries = []

        for node in plugintable_nodes:
            for title, docname in node['entries']:
                # Deduplicate by docname across multiple plugintables on the same page
                if docname not in seen_docs:
                    seen_docs.add(docname)
                    merged_entries.append((title, docname))

        merged_entries.sort(key=lambda x: (x[0] or '').lower())

        primary_toc['entries'] = merged_entries
        primary_toc['includefiles'] = [docname for _, docname in merged_entries]

        for node in plugintable_nodes[1:]:
            node.parent.remove(node)


def merge_plugintable_plugin_refs(app, env, docnames, other):
    if hasattr(other, 'plugintable_plugin_refs'):
        if not hasattr(env, 'plugintable_plugin_refs'):
            env.plugintable_plugin_refs = {}
        env.plugintable_plugin_refs.update(other.plugintable_plugin_refs)


class PluginReferenceTransform(SphinxPostTransform):
    """
    Runs at priority 3 — strictly BEFORE MyST-Parser's `ResolveMystReferences` (priority 4).
    Resolves `[](plugin:xxx)`, `<plugin:xxx>`, `[](plugin:xxx/subpage)`, and
    `[](plugin:xxx#anchor)` into inline-code links (or custom-text links when explicit).
    """
    default_priority = 3

    def _lookup_base_plugin(self, plugin_name):
        """
        Look up a single registered plugin name (without subpage or `#anchor`).
        Returns `(target_docname, default_title)` or `None`.
        """
        labels = getattr(self.env, 'plugintable_plugin_refs', {})
        match = (
            labels.get(plugin_name)
            or labels.get(plugin_name.lower())
            or labels.get(nodes.fully_normalize_name(plugin_name))
        )
        if match:
            return match[0], match[1]

        # Fallback for incremental builds when plugintable pages were not re-parsed
        target_lower = plugin_name.lower()
        for doc in self.env.found_docs:
            default_name = _get_default_display_name(doc)
            if default_name.lower() == target_lower:
                return doc, default_name
        return None

    def _resolve_plugin_spec(self, raw_spec):
        """
        Parse `<plugin_name>[/<subpage>][#<anchor>]` and resolve to:
        `(target_docname, default_title, anchor)` or `None` if not found.
        """
        if '#' in raw_spec:
            path_part, anchor = raw_spec.split('#', 1)
            path_part = path_part.strip()
            anchor = anchor.strip()
        else:
            path_part = raw_spec.strip()
            anchor = ''

        if not path_part:
            return None

        # Case 1: Simple plugin name without subpage (e.g., `imdb_list` or `imdb_list#example`)
        if '/' not in path_part:
            base_match = self._lookup_base_plugin(path_part)
            if not base_match:
                return None
            target_docname, default_title = base_match
            return target_docname, default_title, anchor

        # Case 2: Plugin with subpage (e.g., `daemon/subpage` or `imdb_list/subpage#example`)
        base_plugin, subpage = path_part.split('/', 1)
        base_plugin = base_plugin.strip()
        subpage = subpage.strip().strip('/')

        base_match = self._lookup_base_plugin(base_plugin)
        candidates = []

        if base_match:
            base_docname, _ = base_match
            norm_base = base_docname.replace('\\', '/')
            base_dir = os.path.dirname(norm_base)

            if os.path.basename(norm_base) == 'index':
                # e.g., base is `plugins/daemon/index` -> subpage is `plugins/daemon/<subpage>`
                candidates.append(f'{base_dir}/{subpage}' if base_dir else subpage)
                candidates.append(f'{base_dir}/{subpage}/index' if base_dir else f'{subpage}/index')
            else:
                # e.g., base is `plugins/list/imdb_list` -> check `plugins/list/imdb_list/<subpage>`
                # and sibling `plugins/list/<subpage>`
                candidates.append(f'{norm_base}/{subpage}')
                candidates.append(f'{norm_base}/{subpage}/index')
                if base_dir:
                    candidates.append(f'{base_dir}/{subpage}')

        # Also check if any document in `found_docs` ends with `/<path_part>` directly
        candidates.append(path_part)

        found_docs_lower = {doc.lower(): doc for doc in self.env.found_docs}
        for cand in candidates:
            cand_norm = cand.strip('/').lower()
            if cand_norm in found_docs_lower:
                resolved_doc = found_docs_lower[cand_norm]
                return resolved_doc, path_part, anchor

        for doc_lower, doc_real in found_docs_lower.items():
            if doc_lower.endswith('/' + path_part.lower()):
                return doc_real, path_part, anchor

        return None

    def run(self, **kwargs):
        fromdocname = self.env.docname

        # 1. Intercept `pending_xref` nodes generated by MyST `[](plugin:xxx)`
        for node in list(self.document.findall(addnodes.pending_xref)):
            target = node.get('reftarget', '')
            if not target.lower().startswith(REF_PREFIX):
                continue

            raw_spec = target[len(REF_PREFIX):].strip()
            resolved = self._resolve_plugin_spec(raw_spec)
            if not resolved:
                logger.warning(
                    f'[plugintable] Unknown plugin reference "{target}".',
                    location=node
                )
                node.replace_self(nodes.literal(raw_spec, raw_spec))
                continue

            target_docname, default_title, anchor = resolved

            if node.get('refexplicit') and node.children:
                inner_node = node.children[0].deepcopy()
            else:
                # Render implicit `[](plugin:xxx)` as inline code: `<code>xxx</code>`
                inner_node = nodes.literal(default_title, default_title)

            refnode = make_refnode(
                self.app.builder,
                fromdocname,
                target_docname,
                anchor,
                inner_node,
                default_title,
            )
            node.replace_self(refnode)

        # 2. Intercept direct `nodes.reference` generated by `<plugin:xxx>` autolinks or URL schemes
        for node in list(self.document.findall(nodes.reference)):
            refuri = node.get('refuri', '')
            if not refuri.lower().startswith(REF_PREFIX):
                continue

            raw_spec = refuri[len(REF_PREFIX):].strip()
            resolved = self._resolve_plugin_spec(raw_spec)
            if not resolved:
                logger.warning(
                    f'[plugintable] Unknown plugin reference "{refuri}".',
                    location=node
                )
                continue

            target_docname, default_title, anchor = resolved
            new_uri = self.app.builder.get_relative_uri(fromdocname, target_docname)
            if anchor:
                new_uri = f'{new_uri}#{anchor}'

            node['refuri'] = new_uri
            node['internal'] = True

            current_text = node.astext().strip()
            if not current_text or current_text.lower() == refuri.lower():
                node.clear()
                node += nodes.literal(default_title, default_title)


# Patch Sphinx's `TocTree.resolve` so that any TOC entry generated from a `plugintable`
# renders its link text wrapped in `nodes.literal` (inline code) in the sidebar.
_orig_toctree_resolve = TocTree.resolve


def _patched_toctree_resolve(self, docname, builder, toctree, *args, **kwargs):
    result = _orig_toctree_resolve(self, docname, builder, toctree, *args, **kwargs)
    if result is not None and toctree.get('is_plugintable'):
        plugintable_titles = {title for title, _ in toctree.get('entries', []) if title}
        for ref in result.findall(nodes.reference):
            if (
                len(ref.children) == 1
                and isinstance(ref.children[0], nodes.Text)
                and ref.astext() in plugintable_titles
            ):
                text = ref.astext()
                ref.clear()
                ref += nodes.literal(text, text)
    return result


TocTree.resolve = _patched_toctree_resolve


def setup(app):
    app.add_directive('plugintable', PluginTableDirective)
    app.connect('doctree-read', merge_and_sort_plugintables, priority=100)
    app.connect('env-merge-info', merge_plugintable_plugin_refs)
    app.add_post_transform(PluginReferenceTransform)
    return {'version': '3.7', 'parallel_read_safe': True}
