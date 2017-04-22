# coding=utf-8
"""
Exporta main.tex a informe.tex (template sin archivos externos).
Cambia versión y fecha a archivos.

Autor: PABLO PIZARRO @ github.com/ppizarror
Fecha: ABRIL 2017
Licencia: MIT
"""

# Importación de librerías
import time
from subprocess import call
from ziputility import ZipUtility as Zip

# Constantes
CODEVERSION = '\def\\templateversion{0}{1}% Versión del template\n '
CODEVERSIONPOS = 19
EXAMPLEFILE = 'example.tex'
HEADERSIZE = 13
HEADERVERSIONPOS = 2
MAINFILE = 'main.tex'
MAINFILESINGLE = 'auxiliar.tex'
VERSIONHEADER = '% Versión:      {0} ({1})\n'

# Configuraciones
AUTOCOMPILE = True
ADDWHITESPACE = False
DELETECOMMENTS = True

# Archivos a revisar
FILES = {
    'lib/config.tex': [],
    'lib/functions.tex': [],
    'lib/imports.tex': [],
    'lib/initconf.tex': [],
    'lib/pageconf.tex': [],
    'lib/styles.tex': [],
    EXAMPLEFILE: [],
    MAINFILE: []
}
FILEDELCOMMENTS = {
    'lib/config.tex': False,
    'lib/functions.tex': True,
    'lib/imports.tex': True,
    'lib/index.tex': True,
    'lib/initconf.tex': True,
    'lib/pageconf.tex': True,
    'lib/styles.tex': True,
    EXAMPLEFILE: False,
    MAINFILE: False
}
FILESTRIP = {
    'lib/config.tex': False,
    'lib/functions.tex': True,
    'lib/imports.tex': True,
    'lib/index.tex': True,
    'lib/initconf.tex': True,
    'lib/pageconf.tex': True,
    'lib/styles.tex': True,
    EXAMPLEFILE: False,
    MAINFILE: False
}

# Se pide la versión
version = raw_input('Ingrese la nueva version: ')
version = version.strip()

# Se obtiene el día
dia = time.strftime("%d/%m/%Y")

# Se crea el header de la version
versionhead = VERSIONHEADER.format(version, dia)
versionstrlen = max(0, 15 - (len(version) - 5))
versioncode = CODEVERSION.format('{' + version + '}', ' ' * versionstrlen)

# Carga los archivos y cambia las versiones
for f in FILES.keys():
    data = FILES[f]
    # noinspection PyBroadException
    try:
        fl = open(f, 'r')
        for line in fl:
            data.append(line)
        fl.close()
    except:
        print('Error al cargar el archivo {0}'.format(f))

    # Se cambia la versión
    data[HEADERVERSIONPOS] = versionhead

    # Sólo para el archivo principal se cambia la version
    if f == MAINFILE:
        data[CODEVERSIONPOS] = versioncode

    # Se reescribe el archivo
    newfl = open(f, 'w')
    for j in data:
        newfl.write(j)
    newfl.close()

# Se crea el archivo unificado
fl = open(MAINFILESINGLE, 'w')
data = FILES[MAINFILE]
data.pop(1)  # Se elimina el tipo de documento del header
data.insert(1, '% Advertencia:  Documento generado automáticamente a partir '
               'del main.tex y los\n%               archivos .tex de la '
               'carpeta lib/ para crear un sólo archivo.\n')
line = 0
for d in data:
    write = True
    if line < CODEVERSIONPOS + 1:
        fl.write(d)
        write = False
    # Si es una línea en blanco se agrega
    if d == '\n' and write:
        fl.write(d)
    else:
        # Si es un import pega el contenido
        # noinspection PyBroadException
        try:
            if d[0:6] == '\input':
                libr = d.replace('\input{', '').replace('}', '').strip()
                libr = libr.split(' ')[0]
                libr = libr + '.tex'
                if libr != EXAMPLEFILE:

                    # Se escribe desde el largo del header en adelante
                    libdata = FILES[libr]  # Datos del import
                    libstirp = FILESTRIP[libr]  # Eliminar espacios en blanco
                    libdelcom = FILEDELCOMMENTS[libr]  # Borrar comentarios

                    for libdatapos in range(HEADERSIZE, len(libdata)):
                        srclin = libdata[libdatapos]

                        # Se borran los comentarios
                        if DELETECOMMENTS and libdelcom:
                            if '%' in srclin:
                                comments = srclin.strip().split('%')
                                if comments[0] is '':
                                    srclin = ''
                                else:
                                    srclin = srclin.replace('%' + comments[1],
                                                            '')
                            elif srclin.strip() is '':
                                srclin = ''

                        # Se ecribe la linea
                        if srclin is not '':
                            # Se aplica strip dependiendo del archivo
                            if libstirp:
                                fl.write(srclin.strip())
                            else:
                                fl.write(srclin)

                    fl.write('\n')  # Se agrega espacio vacío

                else:
                    fl.write(d)
                write = False
        except Exception, e:
            pass
        # Se agrega un espacio en blanco a la pagina despues del comentario
        if line >= CODEVERSIONPOS + 1 and write:
            if d[0:2] == '% ' and d[3] != ' ':
                if d != '% FIN DEL DOCUMENTO\n' and ADDWHITESPACE:
                    fl.write('\n')
                d = d.replace('IMPORTACIÓN', 'DECLARACIÓN')
                if d == '% RESUMEN O ABSTRACT\n':
                    d = '% ========================= RESUMEN O ABSTRACT ' \
                        '=========================\n'
                fl.write(d)
            else:
                fl.write(d)

    # Aumenta la linea
    line += 1

fl.close()

# Compila el archivo
if AUTOCOMPILE:
    call(['pdflatex', MAINFILESINGLE])

# Se exporta el proyecto normal
export_normal = Zip('export/Template-Auxiliar.zip')
export_normal.add_file('main.tex')
export_normal.add_folder('images')
export_normal.add_folder('lib')
export_normal.add_file(EXAMPLEFILE)
export_normal.save()

# Se exporta el proyecto unico
export_single = Zip('export/Template-Auxiliar-Single.zip')
export_single.add_file('auxiliar.tex')
export_single.add_folder('images')
export_single.add_file(EXAMPLEFILE)
export_single.save()
