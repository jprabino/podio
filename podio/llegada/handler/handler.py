"""
Module to load and sort the results table
"""
import pandas as pd
import datetime as dt

def init_dataframe(file_path = None):

    if not file_path:
        return data_loader("/home/juan/workspace/dev/podio/podio/static/tabula-resultados colon.csv")


def data_loader(file_path, extension = 'CSV'):
    """
    
    :param file_path: path to the csv file containing the static
    :return: pandas Dataframe with the static
    """
    loaders = {'CSV': pd.read_csv,
               'XLS': pd.read_excel,
               'XLSX': pd.read_excel,}

    return loaders.get(extension, pd.read_excel)(file_path)

def dataframe_format(df):
    df['Tiempo'] = pd.to_datetime(df['Tiempo'], format='%H:%M:%S').dt.time

def get_categories(df):
    """
    Toma las categorias del dataframe y le agrega la categoria general
    :param df: 
    :return: 
    """
    cat = set(df['Categoria'])
    cat.add('General')
    return cat

def get_athletes(df):
    """
    
    :return: 
    """
    athletes_list = []
    for idx, row in df.iterrows():

        if row['Sexo'] == 'Masculino':
            gender = 'M'
        elif row ['Sexo'] == 'Femenino':
            gender = 'F'
        else:
            gender = 'O'
        athletes_list.append({'first_name': row['Nombre'],
               'last_name': row['Apellido'],
               'gender': gender,
               'age': int(row['Edad'])
               })
    return athletes_list


def get_sorted_by_categories(df, podium_len=5):
    """
    Returns a dictionary with the sorted series of each 
    :param df: 
    :param podium_len: 
    :return: 
    """

    categories = get_categories(df)

    results = {}
    for cat in categories:

        if cat == 'General':
            results[cat] = df.sort_values(by = 'Tiempo').head(podium_len)
        else:
            results[cat] = df[df['Categoria'] == cat].sort_values(by='Tiempo').head(podium_len)
    return results
