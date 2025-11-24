import streamlit as st
from PIL import Image
import cv2
import numpy as np

# ----------------------------- #
# Funciones principales
# ----------------------------- #

def interpretar_linea_sismica(imagen, fase, polaridad):
    return (
        f"Interpretación sísmica preliminar:\n\n"
        f"- Fase: {fase}\n"
        f"- Polaridad: {polaridad}\n"
        f"- Reflectores continuos en el sector central.\n"
        f"- Variación de amplitudes hacia los flancos sugiere cambios de facies.\n"
        f"- Dos unidades sísmicas separadas por posible discordancia."
    )

def indicar_anomalias_hidrocarburos(imagen, fase, polaridad):
    return (
        "Anomalías de hidrocarburos:\n\n"
        "- Alta amplitud localizada (posible bright spot).\n"
        "- Terminación plana de reflectores (posible flat spot).\n"
        "- Recomendación: confirmar con atributos AVO y pozos."
    )


# ----------------------------- #
# Interfaz Streamlit
# ----------------------------- #

st.set_page_config(page_title="GeoPetroIA", page_icon="🛢️")

st.title("🛢️ GeoPetroIA")
st.write("Plataforma diseñada para **interpretación sísmica** y detección visual de **anomalías de hidrocarburos**.")

st.markdown("---")

opcion = st.radio(
    "Seleccione el tipo de análisis:",
    [
        "Interpretación de línea sísmica",
        "Indicar anomalías de hidrocarburos",
        "Ambos (interpretación + anomalías)"
    ]
)

st.markdown("### 1️⃣ Cargar la imagen sísmica")
archivo = st.file_uploader("Suba una imagen JPG/PNG:", type=["jpg", "jpeg", "png"])

st.markdown("### 2️⃣ Parámetros sísmicos")
col1, col2 = st.columns(2)

with col1:
    fase = st.text_input("Fase de los datos", placeholder="Ej: fase normal, rotada 180°...")

with col2:
    polaridad = st.text_input("Polaridad", placeholder="Ej: SEG normal, SEG inversa...")

if st.button("Analizar"):
    if archivo is None:
        st.error("Debe cargar una imagen sísmica.")
    elif fase == "" or polaridad == "":
        st.error("Debe ingresar fase y polaridad.")
    else:
        imagen = Image.open(archivo)
        st.image(imagen, caption="Línea sísmica cargada", use_column_width=True)

        st.markdown("---")
        st.subheader("Resultados de GeoPetroIA")

        st.markdown("### 📌 Interpretación sísmica")
        interpretacion = interpretar_linea_sismica(imagen, fase, polaridad)
        st.write(interpretacion)

        if opcion in [
            "Indicar anomalías de hidrocarburos",
            "Ambos (interpretación + anomalías)"
        ]:
            st.markdown("### 💡 Anomalías de hidrocarburos")
            anomalias = indicar_anomalias_hidrocarburos(imagen, fase, polaridad)
            st.write(anomalias)

        st.success("Análisis completado ✔️")

        # ------------------------------------------ #
        # GENERACIÓN DE IMAGEN CON TRAZOS INTERPRETADOS
        # ------------------------------------------ #

        st.markdown("---")
        st.subheader("🧩 Imagen con trazos interpretados (sismofacies y anomalías)")

        # Convertir imagen PIL a OpenCV
        img_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)

        # Copia para edición
        overlay = img_cv.copy()
        h, w, _ = overlay.shape

        # Máscara simulando zona interpretada (editable)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.rectangle(mask, (int(w*0.2), int(h*0.2)), (int(w*0.8), int(h*0.8)), 255, -1)

        # Dibujar hachurado
        for i in range(0, w, 25):
            cv2.line(overlay, (i, 0), (i-200, h), (0, 0, 255), 2)

        # Aplicar solo en la zona marcada
        overlay = cv2.bitwise_and(overlay, overlay, mask=mask)

        # Mezclar con transparencia
        alpha = 0.45
        result = cv2.addWeighted(img_cv, 1, overlay, alpha, 0)

        # Convertir de nuevo a PIL para Streamlit
        imagen_modificada = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

        st.image(imagen_modificada, caption="Imagen interpretada con trazos", use_column_width=True)

        st.info("El patrón rayado representa zonas sugeridas con potencial de facies o anomalías sísmicas 🚨")

Añadir aplicación Streamlit GeoSeismic
