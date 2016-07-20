# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:31:04 2016

@author: Raul Bardaji

Libreria con dos funcones: 
    splitFile divide archivos binarios a un tamaño adecuado.
    joinFiles vuelve a unir los archivos.
Tanto los archvos divididos como los unidos, se crearan en la raiz.

Codigo adaptado a partir de: 
    http://bdurblg.blogspot.com.es/2011/06/python-split-any-file-binary-to.html 
"""

# define the function to split the file into smaller chunks
def splitFile(inputFile,chunkSize):
    """
    Input:
        inputFile: (string) path con el archivo que queremos dividir.
        chunkSize: (int) numero de bytes de cual querems dividir el archivo.
    Output:
        Arcivo info.txt, situado en la raiz, con los metadatos.
        Los arxivos divididos, situados en la raiz, con formato chunk[numero]
    Return:
        metadata: (dictionary) La misma informacion que se guarda en el archivo
            info.txt. Definicion del diccionario:
                metadata['inputFile'] = path del archivo completo.
                metadata['noOfChunks'] = numero de particiones que se han hecho.
                metadata['chunkSize'] = tamaño de las particiones.    
    """
    #read the contents of the file
    f = open(inputFile, 'rb')
    data = f.read() # read the entire content of the file
    f.close()
    
    # get the length of data, ie size of the input file in bytes
    bytesFile = len(data)
    
    #calculate the number of chunks to be created
    noOfChunks= int(bytesFile/chunkSize)
    if(bytesFile%chunkSize):
        noOfChunks+=1
    
    chunkNames = []
    for i in range(0, bytesFile+1, chunkSize):
        fn1 = "chunk%s" % i
        chunkNames.append(fn1)
        f = open(fn1, 'wb')
        f.write(data[i:i+ chunkSize])
        f.close()
    
    # create a info.txt file for writing metadata
    f = open('info.txt', 'w')
    f.write(inputFile+','+'chunk,'+str(noOfChunks)+','+str(chunkSize))
    f.close()
    
    # Creacion de un diccionario con los metadatos.
    metadata = {}
    metadata['inputFile'] = inputFile
    metadata['noOfChunks'] = noOfChunks
    metadata['chunkSize'] = chunkSize

    return metadata

def joinFiles(fileName,noOfChunks,chunkSize):
    """
    Une un archivo partido en un archivo completo.
    Input:
        inputFile: (string) path con el archivo que queremos unir.
        noOfChunks: (int) numero de arhivos partidos que queremos unir.
        chunkSize: (int) numero de bytes que tienen los archivos partidos.
    Output:
        El arcivo reconstruido en el path de la variable fileName
    Return:
        Nada
    """
    dataList = []
    for i in range(0,noOfChunks,1):
        chunkNum=i * chunkSize
        chunkName = 'chunk'+'%s'%chunkNum
   
        f = open(chunkName, 'rb')
        dataList.append(f.read())
        f.close()
    
    f = open(fileName, 'wb')
    for data in dataList:
        f.write(data)
    f.close()

if __name__=='__main__':
    # call the file splitting function
    metadata = splitFile('General idea.png',30)
    
    #call the function to join the splitted files
    joinFiles('reconstruido.png',metadata['noOfChunks'],metadata['chunkSize'])