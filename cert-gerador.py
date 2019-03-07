import csv
import os
import sys

#Gerador de documentos dinamicos com base no modelo SVG

#Arquivo modelo
template = 'certificado07b.svg'
fileNameBase = 'base'
fileNamePrefix = 'cert'

#Recupera dados do CSV
#ex: NOME,PERIODO,HORAS
with open('lista_certificados.csv','r') as f:
    reader = csv.reader(f)
    dados = list(reader)
    #print(dados)

#Argumentos
#ex: python cert-gerador.py [svg/png/pdf] [prefixo-nome-arquivo]
g = sys.argv
action = 'all'
if (g[1].lower() == 'svg'):
    action = 'svg'
    print '> gera somente SVG'
elif (g[1].lower() == 'png'):
    action = 'png'
    print '> gera somente PNG'
elif (g[1].lower() == 'pdf'):
    action = 'pdf'
    print '> gera somente PDF'
else:
    print '> gera todos os arquivos'

if (os.path.isfile(fileNameBase+'-0.svg') or (action == 'all' or 'svg')):
    #lorem
    print('Gerando modelos...')
else:
    sys.exit('Modelos SVGs nao gerados.')

#Recupera MODELO SVG
with open(template, 'r') as file :
  filedata = file.read()

for index, item in enumerate(dados):
#Para cada linha do CSV o seguinte:
    #Nome do arquivo SVG personalizado
    fileName = fileNameBase+'-'+str((index+1))+'.svg'

    #Alteracoes com base nas palavras-chave dentro do MODELO
    newFiledata = filedata
    newFiledata = newFiledata.replace('%VAR_nome%', str(dados[index][0]))
    newFiledata = newFiledata.replace('%VAR_part%', str(dados[index][1]))
    newFiledata = newFiledata.replace('%VAR_horas%', str(dados[index][2]))

    #Grava novo arquivo
    if (action == 'all' or action =='svg'):
        with open(fileName, 'w') as file:
            file.write(newFiledata)

    #Comando para gerar PDF [bug] --export-pdf-version="1.5"
    callPDF = 'inkscape '+fileNameBase+'-'+str((index+1))+'.svg -d200 -T --export-pdf='+fileNamePrefix+'-'+str((index+1))+'.pdf'

    #Comando para gerar PNG
    callPNG = 'inkscape '+fileNameBase+'-'+str((index+1))+'.svg -d300 -T --export-png='+fileNamePrefix+'-'+str((index+1))+'.png'

    #Converte SVG em PNG
    if (action == 'all' or action =='png'):
        print(callPNG)
        os.system(callPNG)

    #Converte SVG em PDF
    if (action == 'all' or action =='pdf'):
        print(callPDF)
        os.system(callPDF)

fileTotal = len(dados)
if (action == 'all'):
    fileTotal * 3
print('=============================')
print(str(fileTotal)+' gerados de '+str(len(dados))+' registros')
