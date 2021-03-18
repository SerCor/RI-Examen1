'''
    Eliminar signos de puntuación
    Eliminar los usuarios colocando la etiqueta $user.
    Eliminar los hashtag colocando la etiqueta $ht.
    Eliminar los emoticones colocando el tipo de emoticón, por ejemplo si es el emoticón es :) colocar la etiqueta SMILE.
    Pasar todo a minúscula.
'''
import argparse
import sys
import os
from text_processing.source import from_file
from text_processing.pipeline import (
    drop_punctuations, to_lower,
    write_to_file, drop_stop_words,
    drop_numbers, stem, 
)
from functools import partial
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(description='''\
Con el siguiente conjunto de datos, en donde cada línea del archivo viene especificada de la siguiente manera: USER tweeted TWEET.
Realizar primero un preprocesamiento:

Eliminar signos de puntuación
Eliminar los usuarios colocando la etiqueta $user.
Eliminar los hashtag colocando la etiqueta $ht.
Eliminar los emoticones colocando el tipo de emoticón, por ejemplo si es el emoticón es :) colocar la etiqueta SMILE.
Pasar todo a minúscula.\
''')
    parser.add_argument('-d', '--directory', type=str,
                        help='Flujo de entrada', default='documentos/originales/')
    return parser.parse_args()


def worker(path):
    print(f'[+] Inicio de procesamiento de {path}')
    try:
        with open(f'./documentos/modificados/{path.name}', 'w', encoding='utf8') as fd:
            base_pipeline = (
                from_file(path)
                >> drop_numbers
                >> drop_punctuations
                >> to_lower
                >> drop_stop_words
                >> stem
                >> partial(write_to_file, fd=fd)
            )

            # print(base_pipeline.value)
    except Exception as e:
        print(f'Error {e}')
    print(f'[+] Final de procesamiento de {path}')


def ls_directory(directory):
    '''Retorna una lista con todos la ruta a todos los documentos
    dentro del directorio'''
    basepath = Path(directory)
    return [item.expanduser() for item in basepath.iterdir()
            if item.is_file()]


def execute_batch(paths):
    with ProcessPoolExecutor() as executor:
        executor.map(worker, paths)


def main():
    args = get_args()
    print(ls_directory(args.directory))
    execute_batch(ls_directory(args.directory))
    print('Final de procesamiento')

if __name__ == '__main__':
    main()
