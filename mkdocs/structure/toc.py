"""
Deals with generating the per-page table of contents.

For the sake of simplicity we use the Python-Markdown `toc` extension to
generate a list of dicts for each toc item, and then store it as AnchorLinks to
maintain compatibility with older versions of MkDocs.
"""


def get_toc(toc_tokens):
    toc = [_parse_toc_token(i) for i in toc_tokens]
    # For the table of contents, always mark the first element as active
    if len(toc):
        toc[0].active = True
    return TableOfContents(toc)


class TableOfContents:
    """
    Represents the table of contents for a given page.
    """

    def __init__(self, items):
        # 这里的每个元素是 AnchorLink，总共存储一篇markdown中的所有前2级标题
        # 这个前2级标题是指：
        #     如果markdown中有一级标题和二级标题，那么把一级标题和二级标题取出来；
        #     如果markdown中有一级标题和三级标题，没有二级标题，那么把一级标题和三级标题取出来；
        # 这个实现很有意思，之后看下如何实现的
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return ''.join([str(item) for item in self])


class AnchorLink:
    """
    A single entry in the table of contents.
    """

    def __init__(self, title, id, level):
        """
        :param title: 标题的内容
        :param id:
        :param level: 标题的等级，比如是1级标题，还是2级标题
        :return:
        """
        self.title, self.id, self.level = title, id, level
        self.children = []

    @property
    def url(self):
        return '#' + self.id

    def __str__(self):
        return self.indent_print()

    def indent_print(self, depth=0):
        indent = '    ' * depth
        ret = f'{indent}{self.title} - {self.url}\n'
        for item in self.children:
            ret += item.indent_print(depth + 1)
        return ret


def _parse_toc_token(token):
    anchor = AnchorLink(token['name'], token['id'], token['level'])
    for i in token['children']:
        anchor.children.append(_parse_toc_token(i))
    return anchor
