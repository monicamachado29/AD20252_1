import numpy as np
import json
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
import kagglehub
import zipfile
import os

class DataGenerator:
    """
    Clase para generar, leer y escribir datos en formatos JSON, TXT y XLSX
    """

    def __init__(self):
        pass

    def _validar_limites(self, inferior, superior):
        if not (isinstance(inferior, (int, float)) and isinstance(superior, (int, float))):
            raise ValueError("Los límites deben ser numéricos (int o float).")
        if inferior >= superior:
            raise ValueError("El límite inferior debe ser menor que el límite superior.")

    def generar_datos_completos(self, n, categorias, x=4, limite_inferior=1, limite_superior=100):
        self._validar_limites(limite_inferior, limite_superior)

        columna_categorica = np.random.choice(categorias, size=n)
        columna_enteros = np.random.randint(int(limite_inferior), int(limite_superior), size=n)
        columna_decimales = np.random.uniform(0, 1, size=n)
        columna_reales = np.random.normal(0, 1, size=n)

        columnas = [columna_categorica, columna_enteros, columna_decimales, columna_reales]
        nombres = ["categoria", "enteros", "decimal", "reales"]

        data = np.column_stack(columnas[:x])
        self.column_names = nombres[:x]
        return data

    def escribir_datos(self, data, tipo='json', ruta='datos_salida'):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
        if tipo == 'json':
            with open(f"{ruta}.json", 'w') as f:
                json.dump(data.tolist(), f)
        elif tipo == 'txt':
            np.savetxt(f"{ruta}.txt", data, fmt='%s')
        elif tipo == 'xlsx':
            columnas = getattr(self, 'column_names', [f"col_{i}" for i in range(data.shape[1])])
            df = pd.DataFrame(data, columns=columnas)
            df.to_excel(f"{ruta}.xlsx", index=False)

    def leer_datos(self, tipo='json', ruta='datos_salida'):
        if tipo == 'json':
            with open(f"{ruta}.json", 'r') as f:
                return np.array(json.load(f))
        elif tipo == 'txt':
            return np.loadtxt(f"{ruta}.txt", dtype=str)
        elif tipo == 'xlsx':
            df = pd.read_excel(f"{ruta}.xlsx")
            return df.to_numpy()

    def leer_ruta(self,ruta=""):
        ruta = ruta
        df=pd.DataFrame()
        df = pd.read_csv(ruta,delimiter=";")
        return df
    
    def download_dataset_zip(self,url = ""):
        print("Descargando dataset desde Kaggle...")
        dataset_path = kagglehub.dataset_download(url)
        print("Ruta al dataset:", dataset_path)
        return dataset_path
    
    def extract_zip_files(self,dataset_path):
        zip_files = [f for f in os.listdir(dataset_path) if f.endswith('.zip')]
        if zip_files:
            zip_file = os.path.join(dataset_path, zip_files[0])
            extract_dir = os.path.join(dataset_path, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            print(f"Extrayendo {zip_file} en {extract_dir}...")
            with zipfile.ZipFile(zip_file, "r") as z:
                z.extractall(extract_dir)
            return extract_dir
        else:
            # Si no se encuentra un ZIP, se verifica si existen archivos CSV en la ruta
            csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
            if csv_files:
                print("No se encontró archivo ZIP pero se detectaron archivos CSV; se asume que el dataset ya se encuentra extraído.")
                return dataset_path
            else:
                raise FileNotFoundError("No se encontró ningún archivo .zip ni archivos .csv en la ruta del dataset")

    def create_csv(self,csv_dir):
        #os.makedirs('src/static/csv', exist_ok=True)
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No se encontraron archivos CSV en el directorio extraído")

        for file in csv_files:
            file_path = os.path.join(csv_dir, file)
            print(f"Leyendo {file_path}...")
            try:
                df = pd.read_csv(file_path, encoding="latin1")
            except Exception as e:
                print(f"Error al leer {file}: {e}")
                continue
            print(f"Creando/actualizando ")
        print("cvs creado correctamente en ")
        return df
    
    def columna_regex(self,df_datos =pd.DataFrame(), reg = r"",columna ="",n_columnas = []):
        df = df_datos.copy()
        df[n_columnas] = df[columna].str.extract(reg).astype(int)
        return df
    
    def limpieza_nan_null(self,df_datos =pd.DataFrame(), name_col="", reemplezar=""):
        if df_datos[name_col].isnull().sum()>0:
            df = df_datos.copy()
            df[name_col]=df[name_col].fillna(reemplezar)
            print("cantidad antes {}/{}  despues {}/{} ".format(df_datos[name_col].isnull().sum(),len(df_datos),df[name_col].isnull().sum(),len(df)))
            return df
        print("no hay nulos")
        return df_datos