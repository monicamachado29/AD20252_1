


from SRC.Clases AD.datagenerator import DataGenerator
import pandas as pd

class Entregable_dos():

    def obtener_datos_kaggle(self,url=""):
        df = pd.DataFrame()
        datagen= DataGenerator()
        dataset = datagen.download_dataset_zip(url) 
        csv_dir =datagen.extract_zip_files(dataset)
        df = datagen.create_csv(csv_dir)
        return df
    
    def enriquecer_df(self,df = pd.DataFrame()):
        df = df
        df["A"]=""
        df["B"]=0
        return df
    
    def generar_imagenes(self,df = pd.DataFrame()):
        print("se guardaron las imagenes")


entdos= Entregable_dos()
df = entdos.obtener_datos_kaggle(("nikhilmaurya1324/swiggy-restaurant-data-india"))
print(df.head(2))