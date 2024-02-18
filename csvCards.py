import csv

# Lista de flashcards com o tema PMBOK
flashcards_pmbok = [
    {"termo": "Projeto", "definicao": "Um esforço temporário empreendido para criar um produto, serviço ou resultado exclusivo."},
    {"termo": "Gerenciamento de Projetos", "definicao": "A aplicação de conhecimentos, habilidades, ferramentas e técnicas às atividades do projeto para atender aos requisitos do projeto."},
    {"termo": "Áreas de Conhecimento", "definicao": "Um conjunto de práticas relacionadas a uma área específica de gerenciamento de projetos."},
    {"termo": "Processos", "definicao": "Um conjunto de atividades inter-relacionadas e coordenadas que transformam insumos em saídas."},
    {"termo": "Grupo de Processos", "definicao": "Um conjunto lógico de atividades relacionadas, reunidas para alcançar um objetivo específico do projeto."}
]

# Nome do arquivo CSV
csv_file = "flashcards_pmbok.csv"

# Escrevendo os flashcards no arquivo CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Escrevendo o cabeçalho
    writer.writerow(['termo', 'definicao'])
    
    # Escrevendo os flashcards
    for flashcard in flashcards_pmbok:
        writer.writerow([flashcard['termo'], flashcard['definicao']])
        
print(f"Flashcards gerados com sucesso e salvos em '{csv_file}'.")
