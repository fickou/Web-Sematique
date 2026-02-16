from docx import Document

doc = Document("Rapport_Projet_Web_Semantique.docx")
styles = [s.name for s in doc.styles]
print("Styles found:", styles)
