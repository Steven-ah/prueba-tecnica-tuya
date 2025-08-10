import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv(".env.shared")
load_dotenv(".env.secret")


DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
FILE_PATH = os.getenv("ROOT_PATH")

def conn_bd():
    """
    Crea el engine de sqlalchemy para la conexión a la bd.
    """
    odbc_str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(odbc_str)
    return engine

def load_data_from_xlsx(table_name, data):
    """
    Carga la información de los archivos de excel a la base de datos.
    """
    try:
        engine = conn_bd()
        data.to_sql(table_name, engine, schema="rch", if_exists="append", index=False)
        print(f"Se han cargado los datos correctamente a la tabla {table_name}.")
    except SQLAlchemyError as e:
        print(f"Error al insertar a la base de datos: {e}")

sheets = ["historia", "retiros"]

for sheet in sheets:
    df = pd.read_excel(f"{FILE_PATH}/data/rachas.xlsx", sheet_name=sheet)
    load_data_from_xlsx(sheet, df)

# Se genera una tabla de fechas para poder identificar cuando un cliente ha omitido un periodo.
# Se toman solo el rango en base a la fecha máxima y mínima de los datos brindados
date_range = pd.date_range("2023-01-01", "2024-12-01", freq="MS")
dates_df = pd.DataFrame(date_range, columns=["date"])
dates_df = dates_df.rename(columns={
    "date": "fecha"
})
load_data_from_xlsx("fechas", dates_df)
