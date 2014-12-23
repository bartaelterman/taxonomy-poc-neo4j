from py2neo import Graph, Node, Relationship
import re
import csv
import sys

def check_arguments():
    if len(sys.argv) != 3:
        print 'usage: ./load_taxonomy_data.py <nodes csv> <dotfile>'
        sys.exit(-1)
    else:
        return sys.argv[1:]

def clear_database(graph):
    graph.cypher.execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")

def open_graphdb():
    g = Graph()
    return g

def parse_nodes_from_line(line):
    match = re.search('--|->|<-', line)
    if match:
        i = match.start()
        node1 = line[:i].strip().replace(';', '')
        node2 = line[i+2:].strip().replace(';', '')
        if match.group() == '--':
            direction = None
        if match.group() == '->':
            direction = 'right'
        if match.group() == '<-':
            direction = 'left'
        return [[node1, node2], direction]
    return [None, None]

def create_nodes(nodes_file, graph):
    reader = csv.reader(open(nodes_file), delimiter=',')
    header = reader.next()
    nodes = {}
    for row in reader:
        sci_name, tax_rank = row
        n = Node('Taxon', scientific_name=sci_name, taxon_rank=tax_rank)
        nodes[sci_name] = n
        graph.create(n)
    return nodes

def create_edges(dotfile, nodes, graph, edge_type='is_child_of'):
    f = open(dotfile)
    edges = []
    for line in f:
        lnodes, edge_direction = parse_nodes_from_line(line)
        if lnodes:
            n1 = nodes[lnodes[0]]
            n2 = nodes[lnodes[1]]
            if edge_direction == 'right':
                r = Relationship(n1, edge_type, n2)
            elif edge_direction == 'left':
                r = Relationship(n2, edge_type, n1)
            else:
                r = Relationship(n1, edge_type, n2)
            graph.create(r)
            edges.append(lnodes)
    return [nodes, edges]


def main():
    nodes_file, dotfile = check_arguments()
    g = open_graphdb()
    clear_database(g)
    nodes = create_nodes(nodes_file, g)
    create_edges(dotfile, nodes, g)

main()
