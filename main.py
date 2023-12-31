#%%
import pandas as pd
import numpy as np
from SRC import soporte
from SRC import soporte_queries_creacion_bbdd as query
from SRC import soporte_bbdd_abc as soporte_bbdd
#%%
df = soporte.leer_csv('DATA.csv')

# %%
df= soporte.columnas_a_minusculas(df)

# %%
df = soporte.convertir_texto_num(df)
# %%
df= soporte.limpiar_columnas(df)
# %%
df= soporte.limpiar_puntos(df)
# %%
df = soporte.corregir_sintaxis(df)
# %%
df = soporte.corregir_valores_negativos(df)
# %%
df = soporte.corregir_valores_columna(df)
# %%
df= soporte.categorizar_gender(df)
# %%
df = soporte.homogeneizar_booleanos(df)
# %%
df = soporte.categorizar_valores_numericos(df)
# %%
df = soporte.manejar_nulos_categoricos(df)
# %%
df = soporte.analizar_columnas_numericas_nulas(df)

columnas_a_imputar= ['environmentsatisfaction', 'hourlyrate','totalworkingyears', 'worklifebalance']
df = soporte.imputar_valores_nulos(df,columnas_a_imputar)

#%%
columnas_a_eliminar= ['environmentsatisfaction', 'environmentsatisfaction_knn', 'hourlyrate', 'hourlyrate_knn', 'totalworkingyears', 'totalworkingyears_knn', 'worklifebalance', 'worklifebalance_knn']

df = soporte.eliminar_columnas(df,columnas_a_eliminar)

columnas_renombrar= {'age': 'age', 'attrition': 'attrition', 'businesstravel': 'businesstravel', 
                    'dailyrate': 'dailyrate', 'department': 'department', 
                    'distancefromhome': 'distancefromhome', 'education': 'education', 
                    'education_cat': 'education_cat', 'educationfield': 'educationfield', 
                    'employeecount': 'employeecount', 'employeenumber': 'employeenumber', 
                    'environmentsatisfaction_cat': 'environmentsatisfaction_cat', 'gender': 'gender', 
                    'gender_cat': 'gender_cat', 'jobinvolvement': 'jobinvolvement', 
                    'jobinvolvement_cat': 'jobinvolvement_cat', 'joblevel': 'joblevel', 
                    'jobrole': 'jobrole', 'jobsatisfaction': 'jobsatisfaction', 
                    'maritalstatus': 'maritalstatus', 'monthlyrate': 'monthlyrate', 
                    'numcompaniesworked': 'numcompaniesworked', 'over18': 'over18', 
                    'overtime': 'overtime', 'percentsalaryhike': 'percentsalaryhike', 
                    'performancerating': 'performancerating', 
                    'relationshipsatisfaction': 'relationshipsatisfaction', 
                    'relationshipsatisfaction_cat': 'relationshipsatisfaction_cat', 
                    'standardhours': 'standardhours', 'stockoptionlevel': 'stockoptionlevel', 
                    'trainingtimeslastyear': 'trainingtimeslastyear', 
                    'worklifebalance_cat': 'worklifebalance_cat', 'yearsatcompany': 'yearsatcompany', 
                    'yearsincurrentrole': 'yearsincurrentrole', 
                    'yearssincelastpromotion': 'yearssincelastpromotion', 
                    'yearswithcurrmanager': 'yearswithcurrmanager', 
                    'sameasmonthlyincome': 'sameasmonthlyincome', 
                    'datebirth': 'datebirth', 'salary': 'salary', 
                    'roledepartament': 'roledepartament', 'numberchildren': 'numberchildren', 
                    'remotework': 'remotework', 
                    'environmentsatisfaction_iterativo': 'environmentsatisfaction', 
                    'hourlyrate_iterativo': 'hourlyrate', 
                    'totalworkingyears_iterativo': 'totalworkingyears', 
                    'worklifebalance_iterativo': 'worklifebalance'}
df = soporte.renombrar_columnas(df,columnas_renombrar)

soporte.generacion_csv(df,'definitivo')

soporte_bbdd.creacion_bbdd_tablas(query.query_creacion_bbdd, 'AlumnaAdalab')

soporte_bbdd.creacion_bbdd_tablas(query.query_creacion_tabla_salario 'AlumnaAdalab', 'abc_corporation')

soporte_bbdd.creacion_bbdd_tablas(query.query_creacion_tabla_abandono_satisfaccion 'AlumnaAdalab', 'abc_corporation')

soporte_bbdd.creacion_bbdd_tablas(query.query_creacion_tabla_detalles_personales 'AlumnaAdalab', 'abc_corporation')

soporte_bbdd.creacion_bbdd_tablas(query.query_creacion_tabla_condiciones 'AlumnaAdalab', 'abc_corporation')

df = pd.read_csv('SRC/definitivo.csv')
datos_tabla = list(set(zip(df)))
soporte_bbdd.insertar_datos(query.query_insertar_salario, 'AlumnaAdalab', 'abc_corporation', datos_tabla)
soporte_bbdd.insertar_datos(query.query_insertar_abandono_satisfaccion, 'AlumnaAdalab', 'abc_corporation', datos_tabla)
soporte_bbdd.insertar_datos(query.query_insertar_detalles_personales, 'AlumnaAdalab', 'abc_corporation', datos_tabla)
soporte_bbdd.insertar_datos(query.query_insertar_condiciones, 'AlumnaAdalab', 'abc_corporation', datos_tabla)
