#ler o arquivo de texto original e salvar como CSV delimitado por vírgulas
input_file = 'concursos.txt'
output_file = 'concursos_formatado.csv'

with open(input_file, 'r') as file:
    lines = file.readlines()

#processar as linhas
with open(output_file, 'w') as file:
    #escrever cabeçalho no formato CSV
    file.write("Órgão,Edital,Código do Concurso,Lista de vagas\n")
    
    for line in lines:
        #separar os campos manualmente
        parts = line.split()
        orgao = parts[0]
        edital = parts[1]
        codigo = parts[2]
        vagas = ' '.join(parts[3:])  #combina o restante como "Lista de vagas"
        
        #ajustar a formatação das vagas para manter os colchetes
        vagas = vagas.strip()
        
        #escrever no arquivo CSV
        file.write(f'{orgao},{edital},{codigo},"{vagas}"\n')
