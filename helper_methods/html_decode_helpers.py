import bs4
import html


def decode_html(html_block):
    if not html_block:
        return ''
    if not isinstance(html_block, bs4.Tag):
        return html.unescape(html_block.string)

    return ''.join([decode_html(inner) for inner in html_block.children])