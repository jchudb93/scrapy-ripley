import pandas as pd
import json
import glob
import io

def nombrar_archivo(archivo):
    nombre = ''.join(archivo.split('.')[:-1]).split('\\')[-1]
    return nombre
def main():
    archivos = glob.glob('./*.json')
    for archivo in archivos:
        
        df = pd.read_json(archivo, encoding='utf8')
        df['precio'] = df['precio'].str.replace('S/','')
        df['precio'] = df['precio'].str.replace(',','')
        df['precio'] = df['precio'].str.replace('No Disponible','0')
        df['precio'] = df['precio'].astype(float)
        gp = df.groupby(['categoria','tipo_producto']).agg({'precio': 'mean'}).reset_index()
        nombre_archivo = nombrar_archivo(archivo)
        gp.to_csv(f'./{nombre_archivo}.csv', encoding='utf8')
        
if __name__ == '__main__':
    main()