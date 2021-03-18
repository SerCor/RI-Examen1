import requests


def download_stopwords():
    url = "https://gist.githubusercontent.com/sebleier/554280/raw/7e0e4a1ce04c2bb7bd41089c9821dbcf6d0c786c/NLTK's%2520list%2520of%2520english%2520stopwords"
    path = "stop_words_en.txt"
    response = requests.get(url)

    if response:
        with open(path, 'w', encoding='utf8') as file:
            file.write(response.text)

        print(f'Fin de recoleccion de stopwords. El resultado esta en {path}')
    else:
        print('Error al intentar recolectar las stopwords')
