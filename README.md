
# Predicción del abandono de clientes mediante minería de datos

## Descripción

Este proyecto corresponde al Componente Práctico Experimental de la asignatura Minería de Datos.

El objetivo consiste en aplicar técnicas de minería de datos para desarrollar un modelo predictivo capaz de identificar clientes con riesgo de abandonar los servicios de una empresa de telecomunicaciones.

## Dataset

Se utilizó el conjunto de datos **Telco Customer Churn**, compuesto por:

- 7.043 registros
- 21 variables originales
- Variable objetivo: `Churn`

Durante el procesamiento se generaron además las variables derivadas:

- `NumServices`
- `TenureGroup`

## Proceso realizado

El proyecto incluye:

- Comprensión y exploración de datos.
- Análisis estadístico descriptivo.
- Identificación de valores faltantes.
- Verificación de registros duplicados.
- Análisis de valores atípicos mediante IQR.
- Preprocesamiento y transformación de datos.
- Feature Engineering.
- Codificación de variables categóricas.
- Escalado de variables numéricas.
- División de datos en entrenamiento y prueba.
- Entrenamiento de Regresión Logística.
- Entrenamiento de Random Forest.
- Validación cruzada con 5 particiones.
- Evaluación mediante Accuracy, Precision, Recall y F1-Score.
- Curva ROC y AUC.
- Interpretación de variables.
- Almacenamiento del modelo.
- Desarrollo de API con FastAPI.
- Desarrollo de WebApp con Streamlit.

## Modelos evaluados

### Regresión Logística

- Accuracy: 0.8013
- Precision: 0.6567
- Recall: 0.5267
- F1-Score: 0.5846
- AUC: 0.8413

### Random Forest

- Accuracy: 0.7786
- Precision: 0.6062
- Recall: 0.4733
- F1-Score: 0.5315

La Regresión Logística fue seleccionada como modelo final debido a que presentó mejores resultados en las métricas evaluadas.

## Variables relevantes

El análisis de importancia por permutación identificó como principales variables predictoras:

1. `tenure`
2. `Contract`
3. `InternetService`

## Despliegue

El modelo fue integrado mediante:

- API desarrollada con FastAPI.
- Aplicación web desarrollada con Streamlit.

La aplicación permite ingresar los datos de un cliente y obtener:

- Predicción de abandono.
- Probabilidad estimada.
- Grupo de permanencia.
- Número de servicios contratados.

## Estructura del proyecto

CPE-Mineria-Datos-Telco-Churn/

- `data/`
  - Dataset utilizado.
- `model/`
  - Modelo entrenado.
- `api/`
  - Código fuente de la API.
- `webapp/`
  - Código fuente de la aplicación web.
- `requirements.txt`
  - Dependencias del proyecto.
- `README.md`
  - Documentación general.
- `CPE_Mineria_Datos_Telco_Churn.ipynb`
  - Cuaderno completo del análisis.

## Tecnologías utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- FastAPI
- Streamlit
- Joblib
- Google Colab

## Autor

Proyecto académico desarrollado para la asignatura Minería de Datos.
