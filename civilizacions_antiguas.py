import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

def preparar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    palabras = word_tokenize(texto)
    palabras_irrelevantes = set(stopwords.words())
    
    palabras_limpias = []
    for palabra in palabras:
        if palabra and palabra not in palabras_irrelevantes:
            palabras_limpias.append(palabra)
    return palabras_limpias

def crear_indice_documentos(todos_los_documentos):
    indice = {}
    for id_documento, texto_documento in todos_los_documentos.items():
        palabras_del_doc = preparar_texto(texto_documento)
        for palabra in palabras_del_doc:
            if palabra not in indice:
                indice[palabra] = set()
            indice[palabra].add(id_documento)
    return indice

def buscar_en_indice(consulta_del_usuario, indice):
    def limpiar_palabra_consulta(palabra):
        palabra = palabra.lower()
        palabra = re.sub(r'[^a-z\s]', '', palabra)
        return palabra.strip()
    
    consulta_en_minusculas = consulta_del_usuario.lower() 

    if ' and ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' and ')
        p1 = limpiar_palabra_consulta(partes[0])
        p2 = limpiar_palabra_consulta(partes[1])
        return indice.get(p1, set()).intersection(indice.get(p2, set()))
        
    elif ' or ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' or ')
        p1 = limpiar_palabra_consulta(partes[0])
        p2 = limpiar_palabra_consulta(partes[1])
        return indice.get(p1, set()).union(indice.get(p2, set()))
        
    elif ' not ' in consulta_en_minusculas:
        partes = consulta_en_minusculas.split(' not ')
        p_positiva = limpiar_palabra_consulta(partes[0])
        p_negativa = limpiar_palabra_consulta(partes[1])
        return indice.get(p_positiva, set()) - indice.get(p_negativa, set())
        
    else:
        palabra_unica = limpiar_palabra_consulta(consulta_del_usuario)
        return indice.get(palabra_unica, set())

documentos_civilizaciones_ejemplo = {
    "doc1": "Los egipcios construyeron las piramides y desarrollaron una escritura jeroglifica.",
    "doc2": "La civilizacion romana fue una de las mas influyentes en la historia occidental.",
    "doc3": "Los mayas eran expertos astronomos y tenian un avanzado sistema de escritura.",
    "doc4": "La antigua Grecia sento las bases de la democracia y la filosofia moderna.",
    "doc5": "Los sumerios inventaron la escritura cuneiforme y fundaron las primeras ciudades."
}

print("Buscador de Documentos: Civilizaciones Antiguas")
indice_civilizaciones = crear_indice_documentos(documentos_civilizaciones_ejemplo)

while True:
    pregunta = input("Escribir busqueda (ej: egipcios AND piramides, o 'salir'): ")
    if pregunta.lower() == 'salir':
        break
    
    resultados_encontrados = buscar_en_indice(pregunta, indice_civilizaciones)
    print(f"Documentos encontrados: {resultados_encontrados}\n")