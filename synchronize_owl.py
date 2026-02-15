from rdflib import Graph

def sync_owl():
    ttl_file = "ens-sup-owl.ttl"
    xml_file = "ens-sup.owl"
    
    print(f"Loading {ttl_file}...")
    g = Graph()
    g.parse(ttl_file, format="turtle")
    
    print(f"Writing {xml_file} in RDF/XML...")
    g.serialize(destination=xml_file, format="xml")
    
    print("Synchronization complete.")

if __name__ == "__main__":
    sync_owl()
