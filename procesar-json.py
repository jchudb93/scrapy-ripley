import pandas as pd
import json
import glob
import io

def nombrar_archivo(archivo):
    nombre = ''.join(archivo.split('.')[:-1]).split('\\')[-1]
    return nombre

def procesar_archivos():
    archivos = glob.glob('./productos/*.json')
    print(archivos)
    for archivo in archivos:
        
        df = pd.read_json(archivo, encoding='utf8')
        df['price'] = df['price'].str.replace('S/','')
        df['price'] = df['price'].str.replace(',','')
        df['price'] = df['price'].str.replace('No Disponible','0')
        df['price'] = df['price'].astype(float)
        gp = df.groupby(['category','productType']).agg({'price': 'median', 'img': 'first'}).reset_index()
        nombre_archivo = nombrar_archivo(archivo)
        gp.to_csv(f'./productos/salida/{nombre_archivo}.csv', encoding='utf8', index=False)
        
def generar_json():
    archivos = glob.glob('./productos/salida/*.csv')
    lst_df = [pd.read_csv(archivo) for archivo in archivos]
    df_final = pd.concat(lst_df, sort=False)
    df_final = df_final.reset_index(drop=True)
    
    print(df_final)

    categorias = df_final['category'].unique()

    df_categorias = pd.DataFrame({"category": categorias})
    df_categorias['idCategory'] = range(1, len(categorias) + 1)
    df_final = pd.merge(df_final, df_categorias, how='left', left_on='category', right_on='category')
    
    df_categorias.to_json('./productos/salida/subida/categorias.json',orient='records')
    df_final['idProduct'] = range(1, len(df_final) + 1)
    df_final['productType'] = df_final['productType'].str.capitalize()
    df_final['productType'] = df_final['productType'].str.replace('-', ' ')
    df_final['productType'] = df_final['productType'].str.replace(' nino', ' niño')
    df_final['productType'] = df_final['productType'].str.replace(' nina', ' niña')
    df_final['productType'] = df_final['productType'].str.replace(' bano', ' baño')
    df_final['productType'] = df_final['productType'].str.replace(' una', ' uña')
    df_final['img'] = df_final['img'].str.replace('//home', 'home')
    df_final.drop('category', axis=1).to_json('./productos/salida/subida/productos.json', orient='records')

def main():
    procesar_archivos()
    generar_json()
if __name__ == '__main__':
    main()