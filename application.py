from flask import Flask, jsonify
from waitress import serve
import csv 

app = Flask(__name__)

#vamos carregar os arquivos
def carregar_candidatos():
    with open('data/candidatos_formatado.csv', 'r') as file: #abrindo arquivo
        reader = csv.DictReader(file, delimiter=',') # vamos ler os dados separado por TAB
        return list(reader)

def carregar_concursos():
    with open('data/concursos_formatado.csv', 'r') as file: #abrindo arquivo
        reader = csv.DictReader(file, delimiter=',') # vamos ler os dados separado por ,
        return list(reader)

candidatos = carregar_candidatos()
#print(candidatos)
concursos = carregar_concursos()
#print(concursos)

@app.route('/concursos/<cpf>', methods=['GET'])
def get_concursos(cpf):
    #filtragem por cpf
    candidato = next((c for c in candidatos if c['CPF'] == cpf), None)
    if not candidato:
        return jsonify({'error': 'Candidato nao encontrado'}), 404
    
    #extrai funçoes do candidato
    profissoes = candidato['Profissões'].strip('[]').split(', ')

    #filtra os concursos nas quais vagas incluem pelo menos uma das profissões do candidato
    concursos_filtrados = []
    for conc in concursos:
        vagas = conc['Lista de vagas'].strip('[]').split(',')
        vagas = [v.strip() for v in vagas]  # remove espaços em cada vaga
        if any(prof in vagas for prof in profissoes):
            concursos_filtrados.append({
                'Órgão': conc['Órgão'],
                'Edital': conc['Edital'],
                'Código do Concurso': conc['Código do Concurso'],
                'Lista de vagas': conc['Lista de vagas']
            })

    #monta a estrutura de saída
    resultado = {
        'Nome': candidato['Nome'],
        'Data de Nascimento': candidato['Data de Nascimento'],
        'CPF': candidato['CPF'],
        'Profissões': candidato['Profissões'],
        'vagas disponíveis': concursos_filtrados
    }
    
    return jsonify(resultado), 200

@app.route('/candidatos/<codigo>', methods=['GET'])
def get_candidatos_por_codigo(codigo):
    """
    Rota que retorna, para um determinado Código de Concurso, 
    os dados do concurso e a lista de candidatos que se encaixam no perfil.
    """
    concurso = next((c for c in concursos if c['Código do Concurso'] == codigo), None)
    if not concurso:
        return jsonify({'error': 'Concurso não encontrado'}), 404

    #extrai as vagas do concurso
    vagas = concurso['Lista de vagas'].strip('[]').split(',')
    vagas = [v.strip() for v in vagas]

    #lista de candidatos que possuam alguma profissão nas vagas do concurso
    candidatos_filtrados = []
    for cand in candidatos:
        profissoes = cand['Profissões'].strip('[]').split(',')
        profissoes = [p.strip() for p in profissoes]
        
        if any(prof in vagas for prof in profissoes):
            candidatos_filtrados.append({
                'Nome': cand['Nome'],
                'Data de Nascimento': cand['Data de Nascimento'],
                'CPF': cand['CPF']
            })
    
    #monta a estrutura de saída
    resultado = {
        'Órgão': concurso['Órgão'],
        'Edital': concurso['Edital'],
        'Código do Concurso': concurso['Código do Concurso'],
        'Lista de vagas': concurso['Lista de vagas'],
        'candidatos': candidatos_filtrados
    }

    return jsonify(resultado), 200

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5010) 
    