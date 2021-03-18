import re
from .decorators import with_value, with_log
import string
from string import digits
from .tools import replace_list, drop_list, drop_underscore, load_stop_words
from nltk.stem import SnowballStemmer 

@with_value
def to_lower(text):
    '''Transforma todo el texto a minusculas'''
    for line in text:
        yield line.lower()


word_regex = re.compile(r'\w')


@with_value
def drop_punctuations(text):
    '''Elimina todos los signos de puntuacion
        Caso 1.Signo de puntuacion tiene al menos un carácter de espacio
            alrededor.
            - Elimina simplemente el caracter
        Caso 2. Signo de puntuación no tiene ningun carácter de espacio
            alrededor.
            - Es asignado un espacio en lugar del signo de puntuacion.

        Nota. Debe ser corrido despues de ajustar los hashtag y/o nombres de usuarios.
        Nota. Tanto los usuarios como hashtag pueden contener el signo de puntuación
        _. Este no va ser eliminado si se encuentra en una palabra que empieza con
        $ = user|hashtag
    '''
    punctuations = ["”", "“"] + list(string.punctuation)
    for line in text:
        yield replace_list(line, punctuations, ' ')


@with_value
def drop_stop_words(text):
    '''Remueve todas las palabras vacias del lenguaje espanol'''
    stop_words = load_stop_words()

    for line in text:
        new_line = ''
        for word in line.split():
            if word not in stop_words:
                new_line += f' {word}'
        
        yield new_line+ '\n'


@with_value
def write_to_file(text, fd):
    for line in text:
        fd.write(line)


@with_value
def tee_and_write_to_file(text, fd):
    for line in text:
        fd.write(line)
        yield line


@with_value
def drop_numbers(text):
    remove_digits = str.maketrans('', '', digits)

    for line in text:
        yield line.translate(remove_digits)        


@with_value
def stem(text):
    s = SnowballStemmer('english')

    for line in text:
        for word in line.split(): 
            yield s.stem(word) + ' '