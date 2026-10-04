import streamlit as st
import requests

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

API_BASE_URL = "https://cpe-mineria-datos-telco-churn-api.onrender.com"
API_PREDICCION_URL = f"{API_BASE_URL}/predecir"

st.set_page_config(
    page_title="Predicción de abandono de clientes",
    page_icon="📊",
    layout="centered"
)

# ==========================================================
# ENCABEZADO
# ==========================================================

st.title("📊 Predicción de abandono de clientes")

st.write(
    """
    Esta aplicación utiliza un modelo de minería de datos para
    estimar la probabilidad de que un cliente de telecomunicaciones
    abandone el servicio.
    """
)

st.subheader("Datos del cliente")

# ==========================================================
# DATOS DEL CLIENTE
# ==========================================================

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
    value=2,
    step=1
)

PhoneService = st.selectbox(
    "Servicio telefónico",
    ["Yes", "No"]
)

# Si no tiene teléfono, la opción correcta es No phone service
if PhoneService == "No":
    MultipleLines = "No phone service"
    st.info("Múltiples líneas: No phone service")
else:
    MultipleLines = st.selectbox(
        "Múltiples líneas",
        ["No", "Yes"]
    )

InternetService = st.selectbox(
    "Servicio de Internet",
    ["DSL", "Fiber optic", "No"],
    index=1
)

# Si no tiene Internet, las variables asociadas se ajustan automáticamente
if InternetService == "No":

    OnlineSecurity = "No internet service"
    OnlineBackup = "No internet service"
    DeviceProtection = "No internet service"
    TechSupport = "No internet service"
    StreamingTV = "No internet service"
    StreamingMovies = "No internet service"

    st.info(
        "El cliente no posee servicio de Internet. "
        "Los servicios asociados fueron establecidos automáticamente "
        "como 'No internet service'."
    )

else:

    OnlineSecurity = st.selectbox(
        "Seguridad en línea",
        ["No", "Yes"]
    )

    OnlineBackup = st.selectbox(
        "Respaldo en línea",
        ["No", "Yes"]
    )

    DeviceProtection = st.selectbox(
        "Protección de dispositivos",
        ["No", "Yes"]
    )

    TechSupport = st.selectbox(
        "Soporte técnico",
        ["No", "Yes"]
    )

    StreamingTV = st.selectbox(
        "Streaming de TV",
        ["No", "Yes"],
        index=1
    )

    StreamingMovies = st.selectbox(
        "Streaming de películas",
        ["No", "Yes"],
        index=1
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
    value=85.0,
    step=0.01
)

TotalCharges = st.number_input(
    "Cargo total",
    min_value=0.0,
    value=170.0,
    step=0.01
)

# ==========================================================
# BOTÓN DE PREDICCIÓN
# ==========================================================

if st.button("Realizar predicción"):

    datos = {
        "gender": gender,
        "SeniorCitizen": int(SeniorCitizen),
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": int(tenure),
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
        "MonthlyCharges": float(MonthlyCharges),
        "TotalCharges": float(TotalCharges)
    }

    try:

        with st.spinner(
            "Conectando con la API y realizando la predicción..."
        ):

            # --------------------------------------------------
            # 1. Comprobar / despertar la API de Render
            # --------------------------------------------------

            comprobacion = requests.get(
                API_BASE_URL,
                timeout=120
            )

            if comprobacion.status_code != 200:
                st.error(
                    "La API no se encuentra disponible en este momento."
                )

                st.write(
                    "Código de estado:",
                    comprobacion.status_code
                )

                st.stop()

            # --------------------------------------------------
            # 2. Enviar los datos a la API
            # --------------------------------------------------

            respuesta = requests.post(
                API_PREDICCION_URL,
                json=datos,
                timeout=120
            )

        # ======================================================
        # RESPUESTA CORRECTA
        # ======================================================

        if respuesta.status_code == 200:

            resultado = respuesta.json()

            st.subheader("Resultado de la predicción")

            st.metric(
                "Probabilidad de abandono",
                f"{resultado['probabilidad_abandono']:.2f} %"
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

        # ======================================================
        # ERROR DEVUELTO POR LA API
        # ======================================================

        else:

            st.error(
                "La API no pudo procesar la solicitud."
            )

            st.write(
                "**Código de estado:**",
                respuesta.status_code
            )

            st.write(
                "**Respuesta de la API:**"
            )

            st.code(
                respuesta.text
            )

    # ==========================================================
    # ERRORES DE CONEXIÓN
    # ==========================================================

    except requests.exceptions.Timeout:

        st.error(
            "La API tardó demasiado en responder."
        )

        st.warning(
            "Los servicios gratuitos de Render pueden entrar en "
            "modo de suspensión después de un periodo de inactividad. "
            "Espera unos segundos e intenta nuevamente."
        )

    except requests.exceptions.ConnectionError as error:

        st.error(
            "No fue posible establecer conexión con la API."
        )

        st.write(
            "Detalle:",
            str(error)
        )

    except Exception as error:

        st.error(
            "Se produjo un error inesperado."
        )

        st.write(
            "Detalle:",
            str(error)
        )
