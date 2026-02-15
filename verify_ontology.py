from rdflib import Graph
import sys

def compare_files(file1, format1, file2, format2):
    print(f"Comparaison de {file1} ({format1}) et {file2} ({format2})...")
    g1 = Graph()
    g2 = Graph()
    
    try:
        g1.parse(file1, format=format1)
    except Exception as e:
        print(f"Erreur lors du parsing de {file1}: {e}")
        return False

    try:
        g2.parse(file2, format=format2)
    except Exception as e:
        print(f"Erreur lors du parsing de {file2}: {e}")
        return False

    iso = g1.isomorphic(g2)
    print(f"Graphes isomorphes ? {'OUI' if iso else 'NON'}")
    print(f"Triplets dans {file1}: {len(g1)}")
    print(f"Triplets dans {file2}: {len(g2)}")
    
    if not iso:
        in_g1_not_g2 = g1 - g2
        in_g2_not_g1 = g2 - g1
        print(f"Triplets uniques à {file1}: {len(in_g1_not_g2)}")
        print(f"Triplets uniques à {file2}: {len(in_g2_not_g1)}")
    
    return iso

print("--- Vérification RDFS ---")
compare_files("ens-sup.rdfs", "xml", "ens-sup.ttl", "turtle")

print("\n--- Vérification OWL ---")
compare_files("ens-sup.owl", "xml", "ens-sup-owl.ttl", "turtle")
