


from SRC.clases_ad.datagenerator import DataGenerator
import pandas as pd
import matplotlib.pyplot as plt

class Entregable_dos():

    def obtener_datos_kaggle(self,url=""):
        df = pd.DataFrame()
        datagen= DataGenerator()
        dataset = datagen.download_dataset_zip(url) 
        csv_dir =datagen.extract_zip_files(dataset)
        df = datagen.create_csv(csv_dir)
        return df
    
    def enriquecer_df(self, df = pd.DataFrame()):
        if df.empty:
            print("❌ DataFrame vacío.")
            return df
        
        # Columna nueva 1: acidez total
        df["total_acidity"] = df["fixed acidity"] + df["volatile acidity"] + df["citric acid"]

        # Columna nueva 2: clasificación del alcohol
        def alcohol_level(alc):
            if alc < 10:
                return "Bajo"
            elif alc < 12:
                return "Medio"
            else:
                return "Alto"

        df["alcohol_level"] = df["alcohol"].apply(alcohol_level)

        return df
    
    
    def generar_imagenes(self,df = pd.DataFrame()):
        if df.empty:
            print("❌ DataFrame vacío. No se pueden generar gráficos.")
            return
        print("✅ Generando gráficos con pandas...")

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Gráfico 1: Dispersión - alcohol vs calidad
        if 'alcohol' in df.columns and 'quality' in df.columns:
            df.plot(kind='scatter', x='alcohol', y='quality', ax=axes[0], title='Alcohol vs Calidad', color='blue')
        else:
            axes[0].text(0.5, 0.5, 'Faltan columnas', ha='center')
        
        # Gráfico 2: Densidad - total_acidity
        if 'total_acidity' in df.columns and df["total_acidity"].nunique() > 1:
            df['total_acidity'].plot(kind='kde', ax=axes[1], title='Densidad Acidez Total', color='green')
        else:
            axes[1].text(0.5, 0.5, 'Datos insuficientes', ha='center')

        # Gráfico 3: Histograma - alcohol
        if 'alcohol' in df.columns:
            df['alcohol'].plot(kind='hist', bins=10, ax=axes[2], title='Histograma Alcohol', color='purple', edgecolor='black')
        else:
            axes[2].text(0.5, 0.5, 'Columna faltante', ha='center')

        plt.tight_layout()
        plt.savefig("entregable2.jpg")
        print("✅ Gráfico guardado como 'entregable2.jpg'")    


entdos= Entregable_dos()
df = entdos.obtener_datos_kaggle(("abdullah0a/wine-quality-red-white-analysis-dataset"))
print(df.head(2))
print("*****************************************************************************************************************************")
df = entdos.enriquecer_df(df)
print(df.head(2))
print("*****************************************************************************************************************************")
df.to_csv("datos.entregable2.csv", index=False)
entdos.generar_imagenes(df)

