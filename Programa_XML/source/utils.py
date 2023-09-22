import os

def lista_de_arquivos(path):
    """
    Retorna uma lista com os títulos de todos os arquivos dentro de uma pasta.

    Args:
        path: O caminho da pasta.

    Returns:
        Uma lista com os títulos dos arquivos.
    """

    files = os.listdir(path)

    file_list = []
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            file_list.append(file)
    
    return file_list
