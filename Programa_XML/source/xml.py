from xml.dom import minidom
import pandas as pd

def read_xml(path):
    dict_info = {
        'sequence': [],
        'Locus': [],
        'Length': [],
        'Update date': [],
        'Creation date': [],
        'Pubmed accesion code number 1': [],
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
                sequence = general[i].getElementsByTagName("INSDSeq_sequence")[0].firstChild.data
            except IndexError:
                sequence = ""

            qualifiers = {}
            qualifiers_names = general[i].getElementsByTagName("INSDQualifier_name")
            qualifiers_values = general[i].getElementsByTagName("INSDQualifier_value")

            for name, value in zip(qualifiers_names, qualifiers_values):
                qualifiers[name.firstChild.data] = value.firstChild.data.capitalize()

            pubmed_codes = []
            if general[i].getElementsByTagName('INSDReference_pubmed'):
                access = general[i].getElementsByTagName('INSDReference_pubmed')
                pubmed_codes = [code.firstChild.data for code in access]
            else:
                pubmed_codes = [""]

            temp_info = {
                'sequence': i + 1,
                'Locus': locus,
                'Length': length,
                'Update date': update_date,
                'Creation date': creation_date,
                'Pubmed accesion code number 1': pubmed_codes,
                'Country': qualifiers.get("country", ""),
                'Host': qualifiers.get("host", ""),
                'Collection_date': qualifiers.get("collection_date", ""),
                'Nucleotide Sequence': sequence.upper()
            }

            dict_info['sequence'].append(temp_info['sequence'])
            dict_info['Locus'].append(temp_info['Locus'])
            dict_info['Length'].append(temp_info['Length'])
            dict_info['Update date'].append(temp_info['Update date'])
            dict_info['Creation date'].append(temp_info['Creation date'])
            dict_info['Pubmed accesion code number 1'].append(temp_info['Pubmed accesion code number 1'])
            dict_info['Country'].append(temp_info['Country'])
            dict_info['Host'].append(temp_info['Host'])
            dict_info['Collection_date'].append(temp_info['Collection_date'])
            dict_info['Nucleotide Sequence'].append(temp_info['Nucleotide Sequence'])

    dict_df = pd.DataFrame(dict_info)
    return dict_df