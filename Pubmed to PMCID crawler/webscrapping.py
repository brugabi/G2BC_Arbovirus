from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

""" para sistemas com Linux, usando o Firefox:
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService 
from webdriver_manager.firefox import GeckoDriverManager 
"""

from selenium.webdriver.common.by import By

def extract_pcmid(pubmed_list):
    '''
    '''
    # Preparando o driver
    options = webdriver.EdgeOptions()
    options.add_argument('--headles')
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),options=options)
    
    """opção firefox - linux:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headles')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
    """

    # configurando o tempo de espera par aparição dos elementos
    driver.implicitly_wait(10)

    pmcid = []
    count = 1
    for pubmed in pubmed_list:
        url = f'https://pubmed.ncbi.nlm.nih.gov/{pubmed}/'
        driver.get(url=url)

        #driver.find_element(By.ID,'id_term').send_keys(pubmed)
        #driver.find_element(By.CLASS_NAME,'search-btn').click()

        try:
            pcmidText = driver.find_element(By.CSS_SELECTOR,'#full-view-identifiers > li:nth-child(2) > span > a')
            if 'PMC' in pcmidText.text:
                tupla = (pubmed,pcmidText.text)
            else:
                tupla = (pubmed,None)
            pmcid.append(tupla)
            print(f"Pubmed: {pubmed}, Number: {count}")
        except:
            tupla = (pubmed,None)
            pmcid.append(tupla)
            print(f"Pubmed: {pubmed}, Number: {count}")

        count+=1
    
    driver.close()
    return pmcid