import glob
from rdflib import Graph, Namespace
import owlrl

def run_queries_owl():
    g = Graph()
    
    # Load OWL Ontology
    print("Loading Ontology (ens-sup-owl.ttl)...")
    try:
        g.parse("ens-sup-owl.ttl", format="turtle")
    except Exception as e:
        print(f"Error loading ontology: {e}")

    # Load Data (UGB only as requested)
    data_file = "UGB_ens-sup.ttl"
    print(f"Loading Data ({data_file})...")
    try:
        g.parse(data_file, format="turtle")
    except Exception as e:
        print(f"Error loading {data_file}: {e}")

    # Apply OWL Reasoning
    print("Applying OWL Inference (OWLRL)...")
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    
    # Read Queries
    print("Reading Queries...")
    with open("requetesUtiliser.rq", "r") as f:
        query_text = f.read()

    queries = []
    current_query = []
    lines = query_text.splitlines()
    query_id = 0
    
    for line in lines:
        if line.strip().startswith("SELECT"):
            if current_query:
                queries.append("\n".join(current_query))
                current_query = []
            query_id += 1
            current_query.append(line)
        else:
            if query_id > 0: 
                current_query.append(line)
    
    if current_query:
        queries.append("\n".join(current_query))

    print(f"Found {len(queries)} queries.")

    # Execute Queries
    prefixes = """
PREFIX ens: <http://www.ugb.sn/ressources/ens-sup.rdfs#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ugb: <http://www.ugb.sn/ressources/UGB#>
PREFIX uasz: <http://www.ugb.sn/ressources/UASZ#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
"""

    for i, q in enumerate(queries):
        print(f"\n--- Running Query {i+1} ---")
        full_query = prefixes + q
        try:
            results = g.query(full_query)
            print(f"Results ({len(results)}):")
            for row in results:
                print(row)
        except Exception as e:
            print(f"Error executing query {i+1}: {e}")

if __name__ == "__main__":
    run_queries_owl()
