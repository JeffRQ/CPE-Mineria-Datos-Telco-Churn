
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

# Crear aplicación
app = FastAPI(
    title="API de Predicción de Churn",
    description="Predicción del abandono de clientes de telecomunicaciones",
    version="1.0"
)

# Cargar modelo
RUTA_MODELO = (
    Path(__file__).resolve().parents[1]
    / "model"
    / "modelo_churn_regresion_logistica.pkl"
)

modelo = joblib.load(RUTA_MODELO)

# Estructura de los datos de entrada
class Cliente(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


def calcular_num_servicios(df):

    columnas_servicios = [
        'PhoneService',
        'MultipleLines',
        'OnlineSecurity',
        'OnlineBackup',
        'DeviceProtection',
        'TechSupport',
        'StreamingTV',
        'StreamingMovies'
    ]

    df['NumServices'] = (
        df[columnas_servicios]
        .eq('Yes')
        .sum(axis=1)
    )

    df['NumServices'] += (
        df['InternetService'] != 'No'
    ).astype(int)

    return df


def calcular_tenure_group(tenure):

    if tenure <= 12:
        return 'Nuevo'

    elif tenure <= 48:
        return 'Intermedio'

    else:
        return 'Antiguo'


@app.get("/")
def inicio():

    return {
        "mensaje": "API de predicción de abandono de clientes activa"
    }


@app.post("/predecir")
def predecir(cliente: Cliente):

    # Convertir datos recibidos a DataFrame
    datos = pd.DataFrame([cliente.model_dump()])

    # Feature Engineering
    datos = calcular_num_servicios(datos)

    datos['TenureGroup'] = datos['tenure'].apply(
        calcular_tenure_group
    )

    # Orden utilizado durante entrenamiento
    columnas_modelo = [
        'gender',
        'SeniorCitizen',
        'Partner',
        'Dependents',
        'tenure',
        'PhoneService',
        'MultipleLines',
        'InternetService',
        'OnlineSecurity',
        'OnlineBackup',
        'DeviceProtection',
        'TechSupport',
        'StreamingTV',
        'StreamingMovies',
        'Contract',
        'PaperlessBilling',
        'PaymentMethod',
        'MonthlyCharges',
        'TotalCharges',
        'NumServices',
        'TenureGroup'
    ]

    datos = datos[columnas_modelo]

    # Predicción
    prediccion = int(
        modelo.predict(datos)[0]
    )

    probabilidad = float(
        modelo.predict_proba(datos)[0, 1]
    )

    if prediccion == 1:
        resultado = "Cliente con riesgo de abandono"
    else:
        resultado = "Cliente con baja predicción de abandono"

    return {
        "prediccion": prediccion,
        "probabilidad_abandono": round(
            probabilidad * 100,
            2
        ),
        "resultado": resultado,
        "grupo_permanencia": str(
            datos.iloc[0]['TenureGroup']
        ),
        "numero_servicios": int(
            datos.iloc[0]['NumServices']
        )
    }
