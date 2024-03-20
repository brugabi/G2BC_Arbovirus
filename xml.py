from xml.dom import minidom
import pandas as pd

def read_xml(path):
    dict_info = {
        'Sequence': [],
        'Locus': [],
        'Length': [],
        'Update date': [],
        'Creation date': [],
        'Pubmed accession': [],
        'Country': [],
        'Host': [],
        'Collection_date': [],
        'Nucleotide Sequence': []
    }

    with open(path, "r") as file:
        xml = minidom.parse(file)
        general = xml.getElementsByTagName("INSDSeq")

        for i in range(len(general)):
            try:
                locus = general[i].getElementsByTagName("INSDSeq_locus")[0].firstChild.data
            except IndexError:
                locus = ""

            try:
                length = general[i].getElementsByTagName("INSDSeq_length")[0].firstChild.data
            except IndexError:
                length = ""

            try:
                update_date = general[i].getElementsByTagName('INSDSeq_update-date')[0].firstChild.data
            except IndexError:
                update_date = ""

            try:
                creation_date = general[i].getElementsByTagName('INSDSeq_create-date')[0].firstChild.data
            except IndexError:
                creation_date = ""

            try:
                if len(general[i].getElementsByTagName("INSDSeq_sequence")[0].firstChild.data) >= 200:
                    Sequence = general[i].getElementsByTagName("INSDSeq_sequence")[0].firstChild.data
                else:
                    Sequence = ""
            except IndexError:
                Sequence = ""

            qualifiers = {}
            qualifiers_names = general[i].getElementsByTagName("INSDQualifier_name")
            qualifiers_values = general[i].getElementsByTagName("INSDQualifier_value")

            for name, value in zip(qualifiers_names, qualifiers_values):
                
                if name.firstChild is not None and value.firstChild is not None: 
                    qualifiers[name.firstChild.data] = value.firstChild.data.capitalize()     
                else:
                    print(f"Um ou mais objetos no arquivo {path} não tem o atributo data - NoneType")

            pubmed_codes = []
            if general[i].getElementsByTagName('INSDReference_pubmed'):
                access = general[i].getElementsByTagName('INSDReference_pubmed')
                pubmed_codes = [code.firstChild.data for code in access]
            else:
                pubmed_codes = [""]

            temp_info = {
                'Sequence': i + 1,
                'Locus': locus,
                'Length': length,
                'Update date': update_date,
                'Creation date': creation_date,
                'Pubmed accession': pubmed_codes,
                'Country': qualifiers.get("country", ""),
                'Host': qualifiers.get("host", ""),
                'Collection_date': qualifiers.get("collection_date", ""),
                'Nucleotide Sequence': Sequence.upper()
            }

            dict_info['Sequence'].append(temp_info['Sequence'])
            dict_info['Locus'].append(temp_info['Locus'])
            dict_info['Length'].append(temp_info['Length'])
            dict_info['Update date'].append(temp_info['Update date'])
            dict_info['Creation date'].append(temp_info['Creation date'])
            dict_info['Pubmed accession'].append(temp_info['Pubmed accession'])
            dict_info['Country'].append(temp_info['Country'])
            dict_info['Host'].append(temp_info['Host'])
            dict_info['Collection_date'].append(temp_info['Collection_date'])
            dict_info['Nucleotide Sequence'].append(temp_info['Nucleotide Sequence'])

    dict_df = pd.DataFrame(dict_info)
    return dict_df