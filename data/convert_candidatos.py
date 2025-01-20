# -*- coding: utf-8 -*-

def txt_para_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as file:
        #escrever cabeçalho no formato CSV
        file.write("Nome,Data de Nascimento,CPF,Profissões\n")
        
        #se realmente existe um cabeçalho na primeira linha do arquivo original, você pode começar do lines[1:]. Caso não exista cabeçalho, use lines[0:].
        for line in lines[0:]:
            line = line.strip()
            
            #ignora linhas vazias, se houver
            if not line:
                continue
            
            # 1) Separar a parte de profissões (entre colchetes) do resto faz um rsplit usando '[', pois a parte das profissões começa no último '['
            left_part, right_part = line.rsplit('[', 1)
            
            #a parte das profissões termina com ']', então removemos o último caractere e tiramos possíveis espaços extras
            profissoes = right_part[:-1].strip()  # remove o ']'
            
            # 2) Separar Nome, Data de Nascimento e CPF supondo que Data de Nascimento e CPF sejam sempre os dois últimos "tokens" separados por espaço
            left_tokens = left_part.split()
            
            #o CPF é o último token
            cpf = left_tokens[-1]
            #a data de nascimento é o penúltimo token
            data_nascimento = left_tokens[-2]
            #o nome é tudo que vem antes desses dois tokens
            nome = " ".join(left_tokens[:-2])
            
            # 3) Escrever no arquivo CSV
            file.write(f'{nome},{data_nascimento},{cpf},"{profissoes}"\n')