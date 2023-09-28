from xml.dom import minidom
import pandas as pd

# Dicionário inicial vazio
dict_info = {
    'Sequence': [],
    'Locus': [],
    'Length': [],
    'Update date': [],
    'Creation date': [],
    'Pubmed accession number': [],
    'Country': [],
    'Host': [],  # Adicionando a coluna "Host"
    'Collection_date': [],
    'Nucleotide Sequence': []
}

with open("sequence.gbc.xml", "r") as file: 
    xml = minidom.parse(file) #parseando para criar o objeto xml dom

    general = xml.getElementsByTagName("INSDSeq")
  
    for i in range(len(general)):
        locus = general[i].getElementsByTagName("INSDSeq_locus")[0].firstChild.data
        length = general[i].getElementsByTagName("INSDSeq_length")[0].firstChild.data
        update_date = general[i].getElementsByTagName('INSDSeq_update-date')[0].firstChild.data
        creation_date = general[i].getElementsByTagName('INSDSeq_create-date')[0].firstChild.data

        qualifiers_names = general[i].getElementsByTagName("INSDQualifier_name")
        qualifiers_values = general[i].getElementsByTagName("INSDQualifier_value")

        temp_info = {
            'Sequence': i + 1,
            'Locus': locus,
            'Length': length,
            'Update date': update_date,
            'Creation date': creation_date,
            'Pubmed accession number': [], 
            'Country': [],
            'Host': [],  # Adicionando a coluna "Host"
            'Collection_date': [], 
            'Nucleotide Sequence': [] 
            #esses que tem colchetes é pq ainda n foi totalmente definido
        }

        #pegando os 3 qualificadores específicos que variam de acordo com sequencia
        for name, value in zip(qualifiers_names, qualifiers_values):
            if name.firstChild.data == "country":
                temp_info['Country'] = value.firstChild.data.capitalize()
            elif name.firstChild.data == "host":  # Incluindo "host" no dicionário
                temp_info['Host'] = value.firstChild.data.capitalize()
            elif name.firstChild.data == "collection_date":
                temp_info['Collection_date'] = value.firstChild.data.capitalize()

        #as varias condicoes do codigo pubmed
        if general[i].getElementsByTagName('INSDReference_pubmed'):
            access = general[i].getElementsByTagName('INSDReference_pubmed')
            for code in access:
                temp_info['Pubmed accession number'].append(code.firstChild.data)
        else:
            temp_info['Pubmed accession number'] = []

        #pegando apenas sequencias com no minimo 200 nucleotideos
        if general[i].getElementsByTagName("INSDSeq_sequence"):
            nucleotides = general[i].getElementsByTagName("INSDSeq_sequence")[0].firstChild.data
            if len(nucleotides) >= 200:
                temp_info['Nucleotide Sequence'].append(nucleotides)
            else:
                temp_info['Nucleotide Sequence'] = []

        
        dict_info['Sequence'].append(temp_info['Sequence'])
        dict_info['Locus'].append(temp_info['Locus'])
        dict_info['Length'].append(temp_info['Length'])
        dict_info['Update date'].append(temp_info['Update date'])
        dict_info['Creation date'].append(temp_info['Creation date'])
        dict_info['Pubmed accession number'].append(temp_info['Pubmed accession number'])
        dict_info['Country'].append(temp_info['Country'])
        dict_info['Host'].append(temp_info['Host'])  # Adicionando "Host"
        dict_info['Collection_date'].append(temp_info['Collection_date'])
        dict_info['Nucleotide Sequence'].append(temp_info['Nucleotide Sequence'])

# Converta o dicionário em um DataFrame
dict_df = pd.DataFrame(dict_info)

# Salve o DataFrame em um arquivo CSV e excel
dict_df.to_csv('collected_data.csv', index=False)
#dict_df.to_excel('collected_data.xlsx', index=False)

dados = pd.read_csv('collected_data.csv')

print(dict_df) 

print("\n\nLocus e códigos de acesso do pubmed:")
print(dict_df[['Locus', 'Pubmed accession number']])




