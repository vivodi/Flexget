import os, fnmatch
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes

class TocTableDirective(Directive):
    """
    用法示例：

        .. toc-table::
           :caption: 快速导航
           :glob:
           :maxdepth: 1

           guide/*
           reference/*
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

        # ────────────────────────────────
        # ① 收集文档列表（支持 glob）
        # ────────────────────────────────
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

        # 去重保持顺序
        seen = set()
        docnames = [d for d in docnames if not (d in seen or seen.add(d))]

        # ────────────────────────────────
        # ② 构造 toctree 节点（让它出现在侧边栏）
        # ────────────────────────────────
        toctree_node = addnodes.toctree()
        toctree_node['entries'] = [(None, d) for d in docnames]
        toctree_node['maxdepth'] = self.options.get('maxdepth', 1)
        toctree_node['glob'] = 'glob' in self.options
        toctree_node['caption'] = self.options.get('caption')
        toctree_node['hidden'] = True
        toctree_node['includefiles'] = docnames
        toctree_node['glob'] = 'glob' in self.options
        toctree_node['numbered'] = False
        toctree_node['titlesonly'] = False

        # ────────────────────────────────
        # ③ 构造表格节点
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

        # 表头
        header = nodes.row()
        header += nodes.entry('', nodes.paragraph(text='文档'))
        header += nodes.entry('', nodes.paragraph(text='描述'))
        thead += header

        for docname in docnames:
            if docname not in env.found_docs:
                app.warn(f"[toc-table] 文档未找到: {docname}")
                continue

            title_node = env.titles.get(docname)
            title = title_node.astext() if title_node else os.path.basename(docname)
            desc = env.metadata.get(docname, {}).get('tocdesc', '（暂无描述）')
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

        # ────────────────────────────────
        # ④ 输出：先插入 toctree，再插入表格
        # ────────────────────────────────
        if 'hidden' in self.options:
            # 如果隐藏，就只加到正文，不在侧边栏中显示
            return [table]
        else:
            return [toctree_node, table]


def setup(app):
    app.add_directive('toc-table', TocTableDirective)
    return {'version': '1.2', 'parallel_read_safe': True}
