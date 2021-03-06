#-*- coding: utf-8-*-
import matplotlib.pyplot as plt
import pandas as pd
import sys
import StrategyGraph as st
import StrategyFile as sf
import string 
import os
import sys

pedirParametros = int(sys.argv[2]) 

if(pedirParametros == 1):
    # Pedimos los parámetros que nos van a hacer falta
    tipoGrafica = int(input('Indique que gráfica desea ver:\n\t 1. Gráfica de Líneas.\n\t 2. Gráfica de Barras.\n\t 3. Gráfica de puntos.\n\t 4. Gráfico Circular.\n\t 5. Gráfico de Escaleras.\n\t 6. Gráfico de Dispersión. \n\t 7. Poligono de Frecuencia. \n\t 8. Resumen.\n > '))
    if tipoGrafica != 1:
        elementoX = int(input('Indique el valor del eje X\n > '))
        elementoY = int(input('Indique el valor del eje Y\n > '))
    else:
        elementoX = input('Indique los valores del eje X a representar separados por comas.\n > ')
    elementoAgrupar = input('Indique el elemento por el que desea agrupar. Si no desea agrupar clicke enter \n > ')
    if elementoAgrupar:
        tipoRepresentacion = int(input('En caso de colisión de datos similares al agrupar ¿Que desea hacer?:\n\t 1. Suma. \n\t 2. Máximo. \n\t 3. Mínimo. \n\t 4. Ninguno. \n  > '))
    else:
        tipoRepresentacion = 4
    elementoFiltrar = input('Indique el elemento por el que desea filtrar. Si no desea filtrar clicke enter \n > ')
    if elementoFiltrar:
        elementoRepresentar = input('Indique los valores a representar separados por comas. Si desea todos escriba "Todos" o "T". \n > ')
    else:
        elementoRepresentar = "T"
    nombreFichero = ""
else:
    # Pedimos los parámetros que nos van a hacer falta
    tipoGrafica = int(sys.argv[3]) 
    elementoX = sys.argv[4]
    elementoY = int(sys.argv[5]) 
    elementoAgrupar = int(sys.argv[6]) 
    tipoRepresentacion = int(sys.argv[7]) 
    elementoFiltrar = int(sys.argv[8])
    elementoRepresentar = sys.argv[9]
    nombreFichero = sys.argv[10]

#Cargamos los datos de un fichero csv
file = sys.argv[1] 
fichero = os.path.splitext(file)
fichero = fichero[0] + ".csv"

if file.endswith('.csv'):
    fileSelected = sf.Csv(file, fichero)
    df = fileSelected.collect()
elif file.endswith('.json'):
    fileSelected= sf.Json(file, fichero)
    df = fileSelected.collect()
elif file.endswith('.xlsx'):
    fileSelected= sf.Xlsx(file, fichero)
    df = fileSelected.collect()
else:
    print("Formato no soportado")
    sys.exit()

if tipoGrafica != 1:
    nombreElementoX = df.columns[elementoX]
    nombreElementoY = df.columns[elementoY]

# Filtramos por las columnas indicadas anteriormente (si procede)
if(elementoRepresentar != "Todos" and elementoRepresentar != "T"):
    elementoFiltrar = df.columns[int(elementoFiltrar)]
    elementosEjeX = elementoRepresentar.split(",")
    elementosEjeX = df[elementoFiltrar].isin(elementosEjeX)
    df = df[elementosEjeX]

# Agrupamos los valores por una columna específica (pasada por linea de comandos)
if tipoRepresentacion != 4:
    elementoAgrupar = df.columns[int(elementoAgrupar)]
    if tipoRepresentacion == 1:
        df = df.groupby(elementoAgrupar, as_index=False).sum()
    elif tipoRepresentacion == 2:
        df = df.groupby(elementoAgrupar, as_index=False).max()
    elif tipoRepresentacion == 3:
        df = df.groupby(elementoAgrupar, as_index=False).min()

# Cogemos las columnas necesarias para las gráficas (pasadas por parámetro)
if tipoGrafica != 1:
    X = df.loc[:,nombreElementoX]
    Y = df.loc[:,nombreElementoY]

# Representamos los valores
if tipoGrafica == 1:
    graficaFinal= st.Lineas("","","","",nombreFichero)
    graficaFinal.grafica(elementoX.split(","), elementoFiltrar, df)
elif tipoGrafica == 2:
    graficaFinal= st.Barras(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
elif tipoGrafica == 3:
    graficaFinal= st.Puntos(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
elif tipoGrafica == 4:
    graficaFinal= st.Circular(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
elif tipoGrafica == 5:
    graficaFinal= st.Escalera(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
elif tipoGrafica == 6:
    graficaFinal= st.DiagramaDispersion(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
elif tipoGrafica == 7:
    graficaFinal= st.PoligonoFrecuencia(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()
else:
    graficaFinal= st.Resumen(X,Y,nombreElementoX,nombreElementoY,nombreFichero)
    graficaFinal.grafica()