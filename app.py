import os
import base64
import streamlit as st
from openai import OpenAI


# -----------------------------
# Configuración general
# -----------------------------
st.set_page_config(
    page_title="Vision AI",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -----------------------------
# Estilos personalizados
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.20), transparent 28%),
            radial-gradient(circle at top right, rgba(168, 85, 247, 0.18), transparent 24%),
            linear-gradient(180deg, #0B1020 0%, #111827 45%, #0F172A 100%);
        color: #E5E7EB;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,41,59,0.85));
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 18px 40px rgba(0,0,0,0.28);
        backdrop-filter: blur(12px);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.6rem;
        color: #F8FAFC;
    }

    .hero-text {
        font-size: 1rem;
        line-height: 1.7;
        color: #CBD5E1;
        margin-bottom: 1rem;
    }

    .pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        margin-right: 0.45rem;
        margin-bottom: 0.45rem;
        font-size: 0.83rem;
        font-weight: 700;
        color: #E0E7FF;
        background: rgba(59,130,246,0.16);
        border: 1px solid rgba(96,165,250,0.28);
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 14px 32px rgba(0,0,0,0.24);
        backdrop-filter: blur(10px);
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        color: #F8FAFC;
    }

    .section-text {
        color: #CBD5E1;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    [data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 18px;
        padding: 0.8rem 1rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    }

    div.stButton > button {
        width: 100%;
        height: 3.1rem;
        border-radius: 14px;
        border: none;
        font-weight: 800;
        color: white;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
    }

    div.stButton > button:hover {
        filter: brightness(1.06);
    }

    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.72);
        border: 1px dashed rgba(125, 211, 252, 0.35);
        border-radius: 18px;
        padding: 0.75rem;
    }

    [data-testid="stTextInputRootElement"],
    [data-testid="stTextAreaRootElement"] {
        background: rgba(15, 23, 42, 0.78);
        border-radius: 14px;
    }

    .answer-box {
        background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.9));
        border: 1px solid rgba(96,165,250,0.22);
        border-left: 6px solid #38BDF8;
        border-radius: 20px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 14px 32px rgba(0,0,0,0.24);
        margin-top: 1rem;
    }

    .answer-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }

    .muted-note {
        color: #94A3B8;
        font-size: 0.92rem;
    }

    .footer-note {
        text-align: center;
        color: #94A3B8;
        font-size: 0.9rem;
        margin-top: 1.4rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Funciones auxiliares
# -----------------------------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


def reset_state():
    st.session_state["analysis_result"] = ""
    st.session_state["last_image_name"] = ""
    st.session_state["image_uploaded"] = False


if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = ""

if "last_image_name" not in st.session_state:
    st.session_state["last_image_name"] = ""

if "image_uploaded" not in st.session_state:
    st.session_state["image_uploaded"] = False


# -----------------------------
# Encabezado
# -----------------------------
hero_col1, hero_col2 = st.columns([1.3, 0.7], gap="large")

with hero_col1:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">Vision AI · Análisis inteligente de imágenes</div>
        <div class="hero-text">
            Sube una imagen, agrega una pregunta específica si lo necesitas y obtén una
            descripción o análisis en español con una interfaz más clara, elegante y fácil de usar.
        </div>
        <span class="pill">Visión computacional</span>
        <span class="pill">Análisis contextual</span>
        <span class="pill">Interfaz renovada</span>
    </div>
    """, unsafe_allow_html=True)

with hero_col2:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Cómo funciona</div>
        <div class="section-text">
            1. Ingresa tu API key.<br>
            2. Carga una imagen.<br>
            3. Haz clic en analizar.<br>
            4. Lee la respuesta generada.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# -----------------------------
# Barra de configuración
# -----------------------------
c1, c2, c3 = st.columns([1.2, 1.2, 0.8])

with c1:
    ke = st.text_input(
        "Clave de OpenAI",
        type="password",
        placeholder="Pega aquí tu API key"
    )

with c2:
    prompt_mode = st.selectbox(
        "Tipo de análisis",
        [
            "Descripción general",
            "Explicación detallada",
            "Objetos y elementos visibles",
            "Análisis técnico de la imagen"
        ]
    )

with c3:
    if st.button("Limpiar"):
        reset_state()
        st.rerun()

if ke:
    os.environ["OPENAI_API_KEY"] = ke


# -----------------------------
# Cliente OpenAI
# -----------------------------
client = None
if ke:
    try:
        client = OpenAI(api_key=ke)
    except Exception as e:
        st.error(f"No se pudo inicializar el cliente: {e}")


# -----------------------------
# Carga de imagen y opciones
# -----------------------------
left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Carga de imagen</div>
        <div class="section-text">Admite archivos JPG, JPEG y PNG.</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Sube una imagen",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.session_state["image_uploaded"] = True
        st.session_state["last_image_name"] = uploaded_file.name
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

with right:
    st.markdown("""
    <div class="glass-card">
        <div class="section-title">Pregunta opcional</div>
        <div class="section-text">
            Puedes pedir una descripción general o formular una consulta específica sobre la imagen.
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_details = st.toggle("Quiero hacer una pregunta específica", value=False)

    additional_details = ""
    if show_details:
        additional_details = st.text_area(
            "Escribe aquí tu pregunta o el contexto adicional",
            placeholder="Ejemplo: identifica objetos importantes, describe el entorno o explica la intención visual de la imagen.",
            height=170
        )

    analyze_button = st.button("Analizar imagen")


# -----------------------------
# Métricas rápidas
# -----------------------------
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Estado API", "Lista" if ke else "Pendiente")

with m2:
    st.metric("Imagen", "Cargada" if uploaded_file else "No cargada")

with m3:
    st.metric("Consulta", "Específica" if show_details else "General")


# -----------------------------
# Generación del prompt
# -----------------------------
def build_prompt(mode, extra_text=""):
    prompts = {
        "Descripción general": "Describe en español lo que ves en la imagen de manera clara, ordenada y útil.",
        "Explicación detallada": "Explica en español con bastante detalle lo que observas en la imagen, incluyendo elementos, ambiente, composición y posibles interpretaciones.",
        "Objetos y elementos visibles": "Identifica en español los objetos, personas, elementos y detalles visibles en la imagen de forma estructurada.",
        "Análisis técnico de la imagen": "Analiza en español la imagen desde un punto de vista visual y técnico: composición, iluminación, enfoque, color, jerarquía visual y posibles intenciones comunicativas."
    }

    prompt_text = prompts.get(mode, prompts["Descripción general"])

    if extra_text.strip():
        prompt_text += f"\n\nContexto o instrucción adicional del usuario:\n{extra_text.strip()}"

    return prompt_text


# -----------------------------
# Proceso de análisis
# -----------------------------
if analyze_button:
    if not ke:
        st.warning("Primero ingresa tu API key.")
    elif not uploaded_file:
        st.warning("Primero carga una imagen.")
    elif client is None:
        st.error("No fue posible crear el cliente de OpenAI.")
    else:
        try:
            with st.spinner("Analizando la imagen..."):
                base64_image = encode_image(uploaded_file)
                prompt_text = build_prompt(prompt_mode, additional_details)

                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                        ],
                    }
                ]

                full_response = ""
                message_placeholder = st.empty()

                for completion in client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1200,
                    stream=True
                ):
                    delta = completion.choices[0].delta.content
                    if delta is not None:
                        full_response += delta
                        message_placeholder.markdown(
                            f"""
                            <div class="answer-box">
                                <div class="answer-title">Resultado del análisis</div>
                                <div class="section-text">{full_response}▌</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.session_state["analysis_result"] = full_response

                message_placeholder.markdown(
                    f"""
                    <div class="answer-box">
                        <div class="answer-title">Resultado del análisis</div>
                        <div class="section-text">{st.session_state["analysis_result"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"Ocurrió un error durante el análisis: {e}")


# -----------------------------
# Pie
# -----------------------------
st.markdown(
    '<div class="footer-note">Interfaz renovada · estética oscura · experiencia visual más clara</div>',
    unsafe_allow_html=True
)
