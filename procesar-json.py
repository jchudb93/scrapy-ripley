import pandas as pd
import json
import glob
import io

def nombrar_archivo(archivo):
    nombre = ''.join(archivo.split('.')[:-1]).split('\\')[-1]
    return nombre

def procesar_archivos():
    archivos = glob.glob('./*.json')
    for archivo in archivos:
        
        df = pd.read_json(archivo, encoding='utf8')
        df['precio'] = df['precio'].str.replace('S/','')
        df['precio'] = df['precio'].str.replace(',','')
        df['precio'] = df['precio'].str.replace('No Disponible','0')
        df['precio'] = df['precio'].astype(float)
        gp = df.groupby(['categoria','tipo_producto']).agg({'precio': 'mean'}).reset_index()
        nombre_archivo = nombrar_archivo(archivo)
        gp.to_csv(f'./productos/{nombre_archivo}.csv', encoding='utf8', index=False)
        
def generar_json():
    archivos = glob.glob('./productos/*.csv')
    lst_df = [pd.read_csv(archivo) for archivo in archivos]
    df_final = pd.concat(lst_df)
    df_final = df_final.reset_index(drop=True)
    df_final['id'] = range(1, len(df_final) + 1)
    cols = df_final.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_final = df_final[cols]
    df_final.to_json('productos.json', orient='record')

def main():
    procesar_archivos()
if __name__ == '__main__':
    main()