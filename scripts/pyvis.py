from py2neo import Graph, Path, Node, Relationship, walk
from pyvis.network import Network
from IPython.display import display, HTML, Image
from typing import Union
from textwrap import shorten
import subprocess


def py2neo_to_pyvis(net: Network, obj: Union[Path, Node, Relationship], auto_rel_label=False, edge_default_width=3):
    if type(obj) is Path:
        for o in walk(obj):
            py2neo_to_pyvis(net, o)
    elif type(obj) is Node:
        label = obj['display_name'] or obj['title'] or obj['name'] or obj['id'] or ''
        obj['label'] = shorten(label, width=50, placeholder="...").replace(':', ':\n')
        obj['group'] = obj['group'] or str(obj.labels)
        obj['font'] = obj['font'] or {'size': 20}
        net.add_node(obj.identity, **obj)
    elif issubclass(type(obj), Relationship):
        start_node = obj.start_node
        end_node = obj.end_node
        # check that no relations already exists (doesn't allow multiple relationships)
        for e in net.edges:
            if e['from'] == start_node.identity and e['to'] == end_node.identity:
                return
        py2neo_to_pyvis(net, start_node)
        py2neo_to_pyvis(net, end_node)
        neo4j_label = type(obj).__name__
        if obj['title'] is None:
            obj['title'] = neo4j_label
        if obj['label'] is None:
            obj['label'] = (neo4j_label if auto_rel_label else None)
        if obj['group'] is None:
            obj['group'] = neo4j_label
        if obj['width'] is None:
            obj['width'] = edge_default_width
        net.add_edge(start_node.identity, end_node.identity, **obj)


def create_or_update_network(graph: Graph,
                             query: str,
                             height: str = "600px",
                             width: str = "100%",
                             auto_rel_label=False,
                             net: Network = None,
                             **kwargs) -> Network:
    data = graph.run(query, **kwargs).data()
    if net is None:
        net = Network(height=height, width=width, notebook=True, cdn_resources='in_line', directed=True)
        net.force_atlas_2based(overlap=0.7)
    for row in data:
        for obj in row.values():
            py2neo_to_pyvis(net, obj, auto_rel_label=auto_rel_label)
    return net


def draw_network(net: Network,
                 file: str = None,
                 link_only=False,
                 screenshot=False):
    html = net.generate_html()
    if file:
        if file.endswith(".html"):
            with open(file, mode="w", encoding="utf-8") as f:
                f.write(html)
            if screenshot:
                result = subprocess.run(['python', 'scripts/save-screenshot.py', file], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                error = result.stderr.decode('utf-8')
                if error != "":
                    raise RuntimeError(error)

        else:
            raise RuntimeError("Unsupported file extension")

    if file:
        if link_only:
            display(HTML(f'<a href="{file}" target="_blank">Click here to open the graph.</a>'))
        if screenshot:
            display(Image(filename=file.replace('.html', '.png')))
    else:
        display(HTML(html))


def draw(graph: Graph,
         query: str,
         height: str = "300px",
         file=None,
         do_display=True,
         auto_rel_label=False,
         **kwargs):
    net = create_or_update_network(graph, query, height=height, auto_rel_label=auto_rel_label, **kwargs)
    return draw_network(net, file=file, link_only=not do_display)
