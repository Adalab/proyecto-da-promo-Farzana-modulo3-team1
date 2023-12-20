#%%
import pandas as pd
from pandas import DataFrame
import numpy as np
pd.set_option('display.max_columns', None)  # Establece una opción de Pandas para mostrar todas las columnas de un DataFrame.
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid") 
sns.set_theme(style="dark") 
plt.style.use('Solarize_Light2')
import mysql.connector
from mysql.connector import errorcode

#%% 
df_data_original =pd.read_csv("DATA.CSV",index_col=0)
df_data_copy= df_data_original.copy()
#%%
#Age:
def texto_nro(cadena):
    cadena = cadena.replace("twenty-six","26").replace("twenty-four","24").replace("thirty-two","32").replace("thirty-six","36").replace("thirty-seven","37").replace("thirty-one","31").replace("thirty","30").replace("forty-seven","47").replace("fifty-two","52").replace("fifty-five","55").replace("fifty-eight","58")
    return int(cadena)

#%%
#Worklifebalance y employeenumber
def nro(cadena):
    try: 
        cadena = cadena.replace(",0","")
        return float(cadena)
    except: 
        return np.nan #tiene varios valores que son "nan"
#%%
#dailyrate 
def daily(nro):
    try:
        return float(nro.replace(",0$",""))
    except:
        return np.nan
# %%
# totalworkingyears", "monthlyincome", "monthlyrate: Cambio de string a float
def decimal(cadena):
    try: 
        return float(cadena.replace(",",".").replace("$","."))
    except: 
        return np.nan #tiene varios valores que son "nan"
#%%
# "hourlyrate", "monthlyrate" : cambio de string a float - no tienen decimales
def decimal3(cadena):
    try:
        return float(cadena)
    except:
        return np.nan
#%%
# educationfield (minúsculas), jobrole (minúsculas), maritalstatus(minúsculas y homogeneización)
def homogeneizar(cadena):
    try:
        return cadena.lower().replace("marreid","married")
    except:
        return np.nan

#%%    
#Distancefromhome - Valores negativos (192 valores) a nulos
def convertir_nulos(numero):
    if numero < 0:
        return np.nan
    else:
        return numero
    
#%%
#Environmentalsatisfaction: modificar valores diferentes a 1-4 a nulos
def convertir_nulos (numero):
    if numero == 1:
        return numero
    elif numero == 2: 
        return numero
    elif numero == 3:
        return numero
    elif numero == 4:
        return numero
    else:
        return np.nan

# %%
#1. Género
def categorizar_gender (numero):
    if numero == 0:
        return 'male'
    else:
        return 'female'
# %%
#2. environmentsatisfaction,relationshipsatisfaction,worklifebalance

def categorizar_environmentsatisfaction(valor):

    if valor == 4:
        return "maximun"
    elif valor == 3:
        return "medium"
    elif valor == 2:
        return "little"
    elif valor == 1:
        return "nothing"
    else:
        return "unknown"

# %%
#3. education
def categorizar_education(valor):
    if valor == 5:
        return "university"
    elif valor == 3:
        return "college"
    elif valor == 2:
        return "high school"
    elif valor == 1:
        return "middle school"
    else:
        return "Unknown"
# %%
#4."jobinvolvement"

def categorizar_jobinvolvement(valor):
    if valor == 4:
        return "very involved"
    elif valor == 3:
        return "involved"
    elif valor == 2:
        return "little involved"
    elif valor == 1:
        return "not involved"
    else:
        return "Unknown"

# %%

def eliminar_duplicados(dataframe):
    print("Cantidad de filas antes de eliminar duplicados:", len(dataframe))
    cantidad_duplicados = dataframe.duplicated().sum()
    dataframe = dataframe.drop_duplicates()
    print("Cantidad de filas después de eliminar duplicados:", len(dataframe))
    return dataframe



# %%
def mostrar_distribucion_nulos_categoricos(dataframe):
    nulos_esta_cat = dataframe[dataframe.columns[dataframe.isnull().any()]].select_dtypes(include="O").columns
    
    print("Las columnas categóricas que tienen nulos son:\n")
    print(nulos_esta_cat)
    
    for col in nulos_esta_cat:
        print(f"La distribución de las categorías para la columna {col.upper()}")
        print(dataframe[col].value_counts() / dataframe.shape[0])
        print("........................")

# %%
def reemplazar_nulos_con_unknown(dataframe, columnas):
    for columna in columnas:
        dataframe[columna] = dataframe[columna].fillna("Unknown")
    
    print("Después del reemplazo usando 'fillna', quedan los siguientes nulos:")
    print(dataframe[columnas].isnull().sum())
# %%
def analizar_columnas_numericas_nulas(dataframe):
    nulos_num = dataframe[dataframe.columns[dataframe.isnull().any()]].select_dtypes(include=np.number).columns
    print("Columnas numéricas con nulos:")
    print(nulos_num)
    porcentaje_nulos = (dataframe[nulos_num].isnull().sum() / dataframe.shape[0]) * 100
    print("% de nulos en las columnas numéricas con nulos:")
    print(porcentaje_nulos.reset_index())
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8, 10))
    axes = axes.flat
    for indice, col in enumerate(nulos_num):
        sns.boxplot(x=col, data=dataframe, ax=axes[indice])
        axes[indice].set_xlabel(col)
    
    plt.tight_layout()
    fig.delaxes(axes[-1])
    plt.show()
# %%
def imputar_valores_nulos(dataframe, columnas_para_imputar):
    imputer_iterative = IterativeImputer(max_iter=20, random_state=42)
    imputer_knn = KNNImputer(n_neighbors=5)
    imputer_iterative_imputado = imputer_iterative.fit_transform(dataframe[columnas_para_imputar])
    dataframe[[col + '_iterativo' for col in columnas_para_imputar]] = imputer_iterative_imputado
    imputer_knn_imputado = imputer_knn.fit_transform(dataframe[columnas_para_imputar])
    dataframe[[col + '_knn' for col in columnas_para_imputar]] = imputer_knn_imputado
    
    return dataframe
# %%
def eliminar_columnas(dataframe, columnas_a_eliminar):
    dataframe.drop(columnas_a_eliminar, axis=1, inplace=True)
    return dataframe
# %%
def renombrar_columnas(dataframe, diccionario_nombres):
    dataframe.rename(columns=diccionario_nombres, inplace=True)
    return dataframe
# %%
def gestionar_duplicados(dataframe, columna):
    cantidad_duplicados = dataframe[columna].duplicated().sum()
    df_duplicados = dataframe[dataframe.duplicated(subset=columna, keep=False)].sort_values(by=columna, ascending=False)
    return cantidad_duplicados, df_duplicados
# %%
def insertar_datos_mysql(dataframe, tabla, lista_columnas, user, password, host, database):
    # Reemplaza los valores NaN por None para la inserción en MySQL
    dataframe_none = dataframe.replace([np.nan], [None])
    lista_tuplas = [tuple(x) for x in dataframe_none[lista_columnas].values]
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    mycursor = cnx.cursor()
    posicion = ', '.join(['%s'] * len(lista_columnas))
    sql = f"INSERT INTO {tabla} ({', '.join(lista_columnas)}) VALUES ({posicion})"
    
    try:
        mycursor.executemany(sql, lista_tuplas)
        cnx.commit()
        print(f"{mycursor.rowcount} registros insertados en la tabla {tabla}")
    except Exception as e:
        print("Ha habido un error en la inserción:", e)
    
    # Cierra la conexión a la base de datos
    cnx.close()
# %%
