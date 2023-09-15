from py2neo import Graph, Path, Node, Relationship, walk
from pyvis.network import Network
from IPython.display import display, HTML, Image
from typing import Union
from textwrap import shorten
import subprocess
import json

def strip_property_prefix(input_dict, prefix):
    output_dict = {}
    for key, value in input_dict.items():
        if key.startswith(prefix):
            new_key = key[len(prefix):]
        else:
            new_key = key
        output_dict[new_key] = value
    return output_dict

def py2neo_to_pyvis(net: Network,
                    obj: Union[Path, Node, Relationship],
                    auto_rel_label=False,
                    edge_default_width=3,
                    font_default_size=20):
    if type(obj) is Path:
        for o in walk(obj):
            py2neo_to_pyvis(net, o)
    elif type(obj) is Node:
        p = strip_property_prefix(dict(obj), "vis_")
        label = p['label'] or p['display_name'] or p['title'] or p['name'] or p['id'] or ''
        p['label'] = shorten(label, width=50, placeholder="...").replace(':', ':\n')
        if 'group' not in p or p['group'] is None:
            p['group'] = str(obj.labels)
        if 'font' not in p or p['font'] is None:
            p['font'] = {'size': font_default_size}
        net.add_node(obj.identity, **p)
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
        p = strip_property_prefix(dict(obj), "vis_")
        if 'title' not in p or p['title'] is None:
            p['title'] = neo4j_label
        if 'label' not in p or p['label'] is None:
            p['label'] = (neo4j_label if auto_rel_label else None)
        if 'group' not in p or p['group'] is None:
            p['group'] = neo4j_label
        if 'width' not in p or p['width'] is None:
            p['width'] = edge_default_width
        net.add_edge(start_node.identity, end_node.identity, **p)


def create_or_update_network(graph: Graph,
                             query: str,
                             height: str = "300px",
                             auto_rel_label=False,
                             net: Network = None,
                             seed: int = None,
                             **kwargs) -> Network:
    data = graph.run(query, **kwargs).data()
    if net is None:
        net = Network(height, notebook=True, cdn_resources='in_line', directed=True)
        net.force_atlas_2based(overlap=0.7, damping=1)
        if seed is not None:
            options = json.loads(net.options.to_json())
            options['layout'] = {"randomSeed": seed, "improvedLayout": True}
            options = json.dumps(options)
            net.set_options(options)
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

def cleanup(graph: Graph):
    # remove styling properties from nodes and relationships
    graph.run("""
        MATCH (n) WHERE any(key IN keys(n) WHERE key STARTS WITH 'vis_')
        WITH n, [key IN keys(n) WHERE key STARTS WITH 'vis_'] AS keys
        CALL apoc.create.removeProperties(n, keys) YIELD node RETURN node;
    """)
    graph.run("""
        MATCH ()-[r]-() WHERE any(key IN keys(r) WHERE key STARTS WITH 'vis_')
        WITH r, [key IN keys(r) WHERE key STARTS WITH 'vis_'] AS keys
        CALL apoc.create.removeRelProperties(r, keys) YIELD rel RETURN rel;
    """)