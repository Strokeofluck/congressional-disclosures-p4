"""Small offline renderer for this report's headings, prose, lists and tables."""
import html,re
def inline(s):
    s=html.escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s)
def render(text):
    out=[];table=False
    for line in text.splitlines():
        if line.startswith('|'):
            if re.match(r'^\|[ :|\-]+\|$',line):continue
            if not table:out.append('<table>');table=True
            out.append('<tr>'+''.join('<td>'+inline(v.strip())+'</td>' for v in line.strip('|').split('|'))+'</tr>');continue
        if table:out.append('</table>');table=False
        h=re.match(r'^(#{1,6}) (.*)',line)
        if h:out.append('<h'+str(len(h[1]))+'>'+inline(h[2])+'</h'+str(len(h[1]))+'>')
        elif line.strip():out.append('<p>'+inline(line)+'</p>')
    if table:out.append('</table>')
    return '\n'.join(out)
