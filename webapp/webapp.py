
import streamlit as st
import requests

st.set_page_config(
    page_title="Predicción de abandono de clientes",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Predicción de abandono de clientes")

st.write(
    """
    Esta aplicación utiliza un modelo de minería de datos para
    estimar la probabilidad de que un cliente de telecomunicaciones
    abandone el servicio.
    """
)

st.subheader("Datos del cliente")

gender = st.selectbox(
    "Género",
    ["Male", "Female"]
)

SeniorCitizen = st.selectbox(
    "¿Es adulto mayor?",
    [0, 1],
    format_func=lambda x: "Sí" if x == 1 else "No"
)

Partner = st.selectbox(
    "¿Tiene pareja?",
    ["No", "Yes"]
)

Dependents = st.selectbox(
    "¿Tiene dependientes?",
    ["No", "Yes"]
)

tenure = st.number_input(
    "Meses de permanencia",
    min_value=0,
    max_value=100,
    value=12
)

PhoneService = st.selectbox(
    "Servicio telefónico",
    ["Yes", "No"]
)

MultipleLines = st.selectbox(
    "Múltiples líneas",
    ["No", "Yes", "No phone service"]
)

InternetService = st.selectbox(
    "Servicio de Internet",
    ["DSL", "Fiber optic", "No"]
)

OnlineSecurity = st.selectbox(
    "Seguridad en línea",
    ["No", "Yes", "No internet service"]
)

OnlineBackup = st.selectbox(
    "Respaldo en línea",
    ["No", "Yes", "No internet service"]
)

DeviceProtection = st.selectbox(
    "Protección de dispositivos",
    ["No", "Yes", "No internet service"]
)

TechSupport = st.selectbox(
    "Soporte técnico",
    ["No", "Yes", "No internet service"]
)

StreamingTV = st.selectbox(
    "Streaming de TV",
    ["No", "Yes", "No internet service"]
)

StreamingMovies = st.selectbox(
    "Streaming de películas",
    ["No", "Yes", "No internet service"]
)

Contract = st.selectbox(
    "Tipo de contrato",
    [
        "Month-to-month",
        "One year",
        "Two year"
    ]
)

PaperlessBilling = st.selectbox(
    "Facturación electrónica",
    ["Yes", "No"]
)

PaymentMethod = st.selectbox(
    "Método de pago",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

MonthlyCharges = st.number_input(
    "Cargo mensual",
    min_value=0.0,
    value=70.0,
    step=0.01
)

TotalCharges = st.number_input(
    "Cargo total",
    min_value=0.0,
    value=1000.0,
    step=0.01
)

if st.button("Realizar predicción"):

    datos = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    try:

        respuesta = requests.post(
            "https://cpe-mineria-datos-telco-churn-api.onrender.com/predecir",
            json=datos
        )

        if respuesta.status_code == 200:

            resultado = respuesta.json()

            st.subheader("Resultado de la predicción")

            st.metric(
                "Probabilidad de abandono",
                f"{resultado['probabilidad_abandono']} %"
            )

            if resultado["prediccion"] == 1:

                st.error(
                    "⚠️ Cliente con riesgo de abandono"
                )

            else:

                st.success(
                    "✅ Cliente con baja predicción de abandono"
                )

            st.write(
                "**Grupo de permanencia:**",
                resultado["grupo_permanencia"]
            )

            st.write(
                "**Número de servicios:**",
                resultado["numero_servicios"]
            )

        else:

            st.error(
                "La API no pudo procesar la solicitud."
            )

            st.write(
                "Código de estado:",
                respuesta.status_code
            )

            st.write(
                "Respuesta de la API:",
                respuesta.text
            )

    except Exception as error:

        st.error(
            "No fue posible conectarse con la API."
        )

        st.write(error)
