import glob
from rdflib import Graph, Namespace

def run_queries():
    g = Graph()
    
    # Load Ontology
    print("Loading Ontology (ens-sup.ttl)...")
    try:
        g.parse("ens-sup.ttl", format="turtle")
    except Exception as e:
        print(f"Error loading ontology: {e}")

    # Load Data (UGB and UASZ)
    data_files = ["UGB_ens-sup.ttl", "UASZ_ens-sup.ttl"]
    for df in data_files:
        print(f"Loading Data ({df})...")
        try:
            g.parse(df, format="turtle")
        except Exception as e:
            print(f"Error loading {df}: {e}")

    # Read Queries
    print("Reading Queries...")
    with open("requetesUtiliser.rq", "r") as f:
        query_text = f.read()

    # Split queries by some delimiter if possible, or just parse them manually.
    # The file has comments like "# REQUÊTE X : ..."
    # I will split by "SELECT" and reconstruct.
    # Actually, let's just parse the full file content manually into separate queries.
    
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
        elif line.strip().startswith("# REQUÊTE"):
             # Just a header, maybe store as description? for now ignore
             pass
        else:
            if query_id > 0: # Only add lines if we are inside a query
                current_query.append(line)
    
    if current_query:
        queries.append("\n".join(current_query))

    print(f"Found {len(queries)} queries.")

    # Execute Queries
    for i, q in enumerate(queries):
        print(f"\n--- Running Query {i+1} ---")
        # Add namespaces if missing in the split chunk (rdflib might need them)
        # Actually the file has prefixes at the top. I should prepend them to every query.
        prefixes = """
PREFIX ens: <http://www.ugb.sn/ressources/ens-sup.rdfs#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ugb: <http://www.ugb.sn/ressources/UGB#>
PREFIX uasz: <http://www.ugb.sn/ressources/UASZ#>
"""
        full_query = prefixes + q
        try:
            results = g.query(full_query)
            print(f"Results ({len(results)}):")
            for row in results:
                print(row)
        except Exception as e:
            print(f"Error executing query {i+1}: {e}")

if __name__ == "__main__":
    run_queries()
