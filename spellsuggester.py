# -*- coding: utf-8 -*-
import re
import numpy as np
import distancias

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self,
                 dist_functions,
                 vocab = [],
                 default_distance = None,
                 default_threshold = None):
        
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
cd
        Args:
           dist_functions es un diccionario nombre->funcion_distancia
           vocab es una lista de palabras o la ruta de un fichero
           default_distance debe ser una clave de dist_functions
           default_threshold un entero positivo

        """
        self.distance_functions = dist_functions
        self.set_vocabulary(vocab)
        if default_distance is None:
            default_distance = 'levenshtein'
        if default_threshold is None:
            default_threshold = 3
        self.default_distance = default_distance
        self.default_threshold = default_threshold

    def build_vocabulary(self, vocab_file_path):
        """Método auxiliar para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        tokenizer=re.compile("\W+")
        with open(vocab_file_path, "r", encoding="utf-8") as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard("")  # por si acaso
            return sorted(vocab)

    def set_vocabulary(self, vocabulary):
        if isinstance(vocabulary,list):
            self.vocabulary = vocabulary # atención! nos quedamos una referencia, a tener en cuenta
        elif isinstance(vocabulary,str):
            self.vocabulary = self.build_vocabulary(vocabulary)
        else:
            print(type(vocabulary))
            raise Exception("SpellSuggester incorrect vocabulary value")

    def suggest(self, term, distance=None, threshold=None, flatten=True):
        """

        Args:
            term (str): término de búsqueda.
            distance (str): nombre del algoritmo de búsqueda a utilizar
            threshold (int): threshold para limitar la búsqueda
        """
        if distance is None:
            distance = self.default_distance
        if threshold is None:
            threshold = self.default_threshold

        resul =[[] for _ in range(threshold+1)]  

        for term_vocab in self.vocabulary:
            if distance == 'levenshtein_m':
                dist = distancias.levenshtein_matriz(term, term_vocab, threshold)
            elif distance == 'levenshtein_r':
                dist = distancias.levenshtein_reduccion(term, term_vocab, threshold)
            elif distance == 'levenshtein':
                dist = distancias.levenshtein(term, term_vocab, threshold)
            elif distance == 'damerau_rm':
                dist = distancias.damerau_restricted_matriz(term, term_vocab, threshold)
            elif distance == 'damerau_r':
                dist = distancias.damerau_restricted(term, term_vocab, threshold)
            elif distance == 'damerau_im':
                dist = distancias.damerau_intermediate_matriz(term, term_vocab, threshold)
            elif distance == 'damerau_i':
                dist = distancias.damerau_intermediate(term, term_vocab, threshold)

            if dist <= threshold:
                resul[dist].append(term_vocab)
            
        if flatten:
            resul = [word for wlist in resul for word in wlist]
        

        return resul

