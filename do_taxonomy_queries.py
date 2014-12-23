from py2neo import Graph, Node, Relationship
g = Graph()

# Find all species and subspecies under taxon `taxon3` (genus)
i = g.cypher.execute("""match (n:Taxon {scientific_name: "taxon3", taxon_rank: "genus"})
                     <-[:is_child_of*1..2]-(m)
                     return m.scientific_name, m.taxon_rank""")
print i

# Find all parents from `taxon10`
i = g.cypher.execute("""match (n:Taxon {scientific_name: 'taxon10'})-[:is_child_of*1..5]->(m)
                     return m.scientific_name, m.taxon_rank""")
print i
