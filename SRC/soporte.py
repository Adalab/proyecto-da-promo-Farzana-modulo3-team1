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
def leer_csv(csv):
    """
    Esta función lee un archivo csv y devuelve una copia del archivo 
    convertido en dataframe.
    
    Parametros:
    El único parametro que recibe es el archivo csv.

    Crea un dataframe con la copia del archivo original y maximiza todas las columnas
    del archivo para poderlo visualizar correctamente.

    Return:
    dataframe de la copia del csv.

  
    """
    try:
        df_data_original = pd.read_csv(csv, index_col=0)
        df_data_copy = df_data_original.copy()
        return df_data_copy
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None
#%%
def columnas_a_minusculas(df):
    """
    Cambia los nombres de las columnas a minusculas
    parametros:
    dataframe del que sacamos las columnas
    diccionario_columnas:Diccionario que mapea nombres de columnas a sus nuevos nombres
    return:
    dataframe modificado
    """
    df.columns = map(str.lower, df.columns)
    df.columns

    return df

#%%
#Age:
def convertir_texto_num(df):
    """
    Cremos una lista de tuplas ya definidas.Cada tupla tiene dos elementos: 
    el [0] es el string que hay que convertir
    el [1] es el numero que se quiere conseguir


    Parametros:
    un dataframe
   
    Return:
    un dataframe modificado
    """

   
    lista_tuplas = [("twenty-six","26"),("twenty-four","24"),("thirty-two","32"),("thirty-six","36"),("thirty-seven","37"),("thirty-one","31"),("thirty","30"),("forty-seven","47"),("fifty-two","52"),("fifty-five","55"),("fifty-eight","58")]
    #df = df.copy()  # Para evitar modificar el DataFrame original

    for texto, numero in lista_tuplas:
        df['age'] = df['age'].replace(texto, numero)
    df['age'] = df['age'].astype(int)

    return df

#%%

def limpiar_columnas(df):
    """
    Limpia las columnas 'Worklifebalance' y 'employeenumber' en un DataFrame.

    Parameters:
    DataFrame que queremos modificar.

    Returns:
    DataFrame con las columnas 'Worklifebalance' y 'employeenumber' modificadas.
    """
    # Limpieza de la columna 'Worklifebalance'
    df['worklifebalance'] = df['worklifebalance'].str.replace(',0', '', regex=False)
    df['worklifebalance'] = pd.to_numeric(df['worklifebalance'], errors='coerce')

    # Limpieza de la columna 'employeenumber'
    df['employeenumber'] = df['employeenumber'].str.replace(',0', '', regex=False)
    df['employeenumber'] = pd.to_numeric(df['employeenumber'], errors='coerce')

    # Limpieza de la columna 'totalworkingyears'
    df['totalworkingyears'] = df['totalworkingyears'].str.replace(',0', '', regex=False)
    df['totalworkingyears'] = pd.to_numeric(df['totalworkingyears'], errors='coerce')

    # Limpieza de la columna 'monthlyincome'
    df['monthlyincome'] = df['monthlyincome'].str.replace(',0', '', regex=False)
    df['monthlyincome'] = pd.to_numeric(df['monthlyincome'], errors='coerce')
    
    # Limpieza de la columna 'monthlyrate'
    df['hourlyrate'] = df['hourlyrate'].str.replace('Not Available', '', regex=False)
    df['hourlyrate'] = pd.to_numeric(df['hourlyrate'], errors='coerce')

    return df

#%%

def limpiar_puntos(df):
    """  
    Limpia la columna 'dailyrate' quitandole el simbolo de dolar
    y convirtiendola de string a float.

    Parameters:
    DataFrame que queremos modificar.

    Returns:
    DataFrame con la columna 'dailyrate' modificada.
   
    """
    df['dailyrate'] = df['dailyrate'].str.replace('.', '', regex=False)
    df['dailyrate'] = pd.to_numeric(df['dailyrate'], errors='coerce')
 
    return df   

#%%
def corregir_sintaxis(df):
    """
    Corrige errores ortograficos.
    Parametros:
    dataframe 
    
    Return:
    dataframe modificado
    """
    df['maritalstatus']= df['maritalstatus'].str.lower().replace("marreid","married")

    return df

#%%
def corregir_valores_negativos(df):
    """
    Convierte los valores negativos en la columna 
    'distancefromhome' a nulos.

    Parametros:
    DataFrame que queremos modificar.

    Returns:
    DataFrame modificado.
    """
    # Convierte los valores negativos a NaN
    df['distancefromhome'] = df['distancefromhome'].apply(lambda x: x if x >= 0 else pd.NA)

    return df

#%%
#Environmentalsatisfaction: modificar valores diferentes a 1-4 a nulos.

def corregir_valores_columna(df):
    """
    Convierte los valores diferentes de 1, 2, 3 , 4 y 5 en la columna especificada a nulos.
    Lo haremos en las siguientes columnas : Environmentalsatisfaction
    Parameters:
    df (DataFrame): DataFrame que vamos a modificar.

    Returns:
    DataFrame modificado.
    """
    valores_permitidos = {1, 2, 3, 4,5}
    
    # Convierte los valores diferentes de 1, 2, 3 , 4  y 5 a NaN
    df['environmentsatisfaction'] = df['environmentsatisfaction'].apply(lambda x: x if x in valores_permitidos else pd.NA)
    df['relationshipsatisfaction'] = df['relationshipsatisfaction'].apply(lambda x: x if x in valores_permitidos else pd.NA)
    df['worklifebalance'] = df['worklifebalance'].apply(lambda x: x if x in valores_permitidos else pd.NA)
    df['worklifebalance'] = df['worklifebalance'].astype('Int64')

    return df

# %%

def categorizar_gender(df):
    """
    Esta funcion crea una columna con la categorizacion de los valores 
    de la columna, si es 0 pondrá male y si es 1 pondremos female

    Parametros:
    Recibe un dataframe
    Returns:
    Devuelve el dataframe modificado
    """

    df['gender_cat'] = np.where(df['gender'] == 0, 'male', 'female')
    df.insert(12, 'gender_cat', df.pop('gender_cat'))
    return df

# %%

def homogeneizar_booleanos(df):
    """
    Esta función recorre todos los valores y los homegeiza a dos : Yes y No
    Parámetros:
    Recibe un dataframe
    Returns:
    Devuelve el dataframe modificado
    """
    df['remotework'] = df['remotework'].apply(lambda x: 'Yes' if x in [True, 1, '1', 'yes', 'si'] else 'No')
    df['remotework'] = df['remotework'].apply(lambda x: 'Yes' if x in [True, 1, '1', 'yes', 'si'] else 'No')
    #poner aqui la columna de attrition
    return df
#2. environmentsatisfaction,relationshipsatisfaction,worklifebalance
# ~/Desktop/adalab/Modulo3/proyecto-da-promo-Farzana-modulo3-team1/SRC/soporte.py
#%%
def categorizar_valores_numericos(df):
    """
    Esta función asigna valores transformados a las siguientes columnas del DataFrame y
    crea nuevas columnas '_cat' en las posiciones indicadas.
    
    Parámetros:
    - df: DataFrame de pandas.
    
    Returns:
    - DataFrame modificado.
    """
    valores = {
        1: 'Very Low',
        2: 'Low',
        3: 'Medium',
        4: 'High',
        5: 'Very High'
    }

    # Transformar y mover la columna 'environmentsatisfaction'
    df['environmentsatisfaction_cat'] = df['environmentsatisfaction'].map(valores)
    df.insert(11, 'environmentsatisfaction_cat', df.pop('environmentsatisfaction_cat'))

    # Transformar y mover la columna 'relationshipsatisfaction'
    df['relationshipsatisfaction_cat'] = df['relationshipsatisfaction'].map(valores)
    df.insert(28, 'relationshipsatisfaction_cat', df.pop('relationshipsatisfaction_cat'))

    # Transformar y mover la columna 'worklifebalance'
    df['worklifebalance_cat'] = df['worklifebalance'].map(valores)
    df.insert(34, 'worklifebalance_cat', df.pop('worklifebalance_cat'))

    # Transformar y mover la columna 'jobinvolvement'
    df['jobinvolvement_cat'] = df['jobinvolvement'].map(valores)
    df.insert(16, 'jobinvolvement_cat', df.pop('jobinvolvement_cat'))
    
    return df


#%%
def categorizar_education(df):
    """
    Esta función las siguientes columnas del dataframe() asigna valores
    transformados y crea nuevas columnas '..._cat'.
    Parámetros:
    Recibe un dataframe
    Returns:
    Devuelve el dataframe modificado
    """
    mapping = {
        1: 'middle school',
        2: 'high school',
        3: 'college',
        4: 'university',
        5: 'master'
    }
    df['education_cat'] = df['education'].map(mapping)
    df.insert(7, 'education', df.pop('education_cat'))

#%%
def manejar_nulos_categoricos(df):
    """
    Esta función busca los valores nulos en las columnas de tipo 'object' de un DataFrame.
    Rellena los nulos de la columna 'performancerating' con la moda de esa columna,
    y el resto de las columnas se llenan con 'Unknown'.

    Parámetros:
    Recibe un dataframe
    Returns:
    Devuelve el dataframe modificado
    """
    # Obtener las columnas de tipo 'object' con valores nulos
    columnas_nulos = df.select_dtypes(include='object').columns[df.select_dtypes(include='object').isnull().any()].tolist()
    # Manejar los nulos en la columna 'performancerating'
    if 'performancerating' in columnas_nulos:
        moda = df['performancerating'].mode()[0]
        df['performancerating'].fillna(moda, inplace=True)

    # Manejar los nulos en el resto de las columnas
    for columna in columnas_nulos:
        if columna != 'performancerating':
            df[columna].fillna('Unknown', inplace=True)

    return df

# %%




# %%



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
def imputar_valores_nulos(dataframe, lista_columnas):
    for x in lista_columnas:
        imputer_iterative = IterativeImputer(max_iter=20, random_state=42)
        imputer_knn = KNNImputer(n_neighbors=5)
        imputer_iterative_imputado = imputer_iterative.fit_transform(dataframe[x])
        dataframe[[col + '_iterativo' for col in x]] = imputer_iterative_imputado
        imputer_knn_imputado = imputer_knn.fit_transform(dataframe[x])
        dataframe[[col + '_knn' for col in x]] = imputer_knn_imputado

    return dataframe
# %%
def eliminar_columnas(dataframe, lista_columnas):
    """Esta funcion elimina las columnas de un dataframe de una lista aportada
        Parametros:
            Dataframe
            lista de columnas que se quieren eliminar
        Returns:
            Dataframe actualizado
    """
    for x in lista_columnas:
        dataframe.drop(x, axis=1, inplace=True)
    return dataframe
# %%
def renombrar_columnas(dataframe, diccionario_nombres):
    """
    Esta función  renombra las columnas de un DataFrame.
    Parámetros:
    Recibe un dataframe y un diccionario con los nombres de las columnas(anteriores y actuales)
    Returns:
    Devuelve el dataframe modificado
    """
    dataframe.rename(columns=diccionario_nombres, inplace=True)
    return dataframe
# %%
def gestionar_duplicados(dataframe, columna):
    """
    Esta función busca los duplicados en una columna y devuelve la cantidad.
    Parámetros:
    Recibe un dataframe y el nombre de la columna a buscar duplicados
    Returns:
    Devuelve un dataframe con los duplicados y la cantidad de duplicados.
    """
    cantidad_duplicados = dataframe[columna].duplicated().sum()
    df_duplicados = dataframe[dataframe.duplicated(subset=columna, keep=False)].sort_values(by=columna, ascending=False)
    return cantidad_duplicados, df_duplicados

def generacion_csv(dataframe,nombre):
    """ Esta función genera un csv con el dataframe proporcionado
    Parametros:
        dataframe -dataframe que queremos convertir en csv
        nombre - nombre que le queremos dar al csv
    return: Nada, solamente lo genera
    """
    dataframe.to_csv(f'{nombre}.csv' )