import os
import json
import random
import streamlit as st
from datetime import datetime

# ==========================================
# 0. CONTROL DE ERRORES DE ENTORNO
# ==========================================
try:
    import chromadb
    import google.generativeai as genai_text  
    from google import genai as genai_image   
    from google.genai import types
    from google.api_core.exceptions import ResourceExhausted
    LIBRERIAS_OK = True
except ImportError as e:
    LIBRERIAS_OK = False
    ERROR_FALTANTE = str(e)

if not LIBRERIAS_OK:
    st.set_page_config(page_title="Error de Entorno", page_icon="⚠️")
    st.error("⚠️ Faltan herramientas por instalar en este entorno virtual.")
    st.warning(f"Detalle del error: {ERROR_FALTANTE}")
    st.info("Abre la terminal en VS Code y ejecuta:\n\n`pip install streamlit google-generativeai chromadb python-dotenv google-genai`")
    st.stop()

# ==========================================
# 1. CONFIGURACIÓN VISUAL BASE
# ==========================================
st.set_page_config(page_title="Kromo | Tu Gemelo Digital", page_icon="🐊", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'Space Grotesk', sans-serif;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; flex-wrap: wrap;}
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px; padding: 10px 15px; border: 1px solid #e2e8f0; }
    .stTabs [aria-selected="true"] { background-color: #047857; color: white !important; font-weight: 700; border: none; }
    .stButton>button[kind="primary"] { background-color: #047857 !important; color: white !important; border-radius: 8px; font-weight: 700; transition: 0.3s; }
    .stButton>button[kind="primary"]:hover { background-color: #064e3b !important; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. AUTENTICACIÓN Y BARRA LATERAL
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #047857;'>KROMO 🐊</h1>", unsafe_allow_html=True)
    st.caption("Preservando la identidad humana.")
    
    st.markdown("### 🔑 Acceso al Sistema")
    api_key = st.text_input("Introduce tu API Key de Gemini:", type="password")
    
    st.divider()

# Bloqueo de la app si no hay API Key
if not api_key:
    st.warning("👈 Por favor, ingresa tu API Key en la barra lateral para arrancar los motores de inteligencia artificial de Kromo.")
    st.info("💡 Si estás evaluando este proyecto, puedes conseguir una clave gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).")
    st.stop()

# ==========================================
# 3. INICIALIZACIÓN DE MOTORES IA Y DATOS
# ==========================================
# Se ejecuta SOLO si hay una API Key válida introducida
genai_text.configure(api_key=api_key)
model_text = genai_text.GenerativeModel('gemini-2.5-flash')
image_client = genai_image.Client(api_key=api_key)

chroma_client = chromadb.PersistentClient(path="./data/kromo_db")
collection = chroma_client.get_or_create_collection(name="kromo_memories")
PERFIL_FILE = "./data/kromo_perfil.json"

# ==========================================
# 4. FUNCIONES LÓGICAS Y GAMIFICACIÓN
# ==========================================
def guardar_perfil(datos_perfil):
    os.makedirs("./data", exist_ok=True)
    with open(PERFIL_FILE, "w", encoding="utf-8") as f:
        json.dump(datos_perfil, f, ensure_ascii=False, indent=4)

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def guardar_memoria(texto, tipo="interaccion_diaria"):
    doc_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    metadata = {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": tipo}
    collection.add(documents=[texto], metadatas=[metadata], ids=[doc_id])

def calcular_nivel_sabiduria():
    try:
        total_memorias = collection.count()
        xp = total_memorias * 10
        nivel = (xp // 50) + 1
        return total_memorias, xp, nivel
    except:
        return 0, 0, 1

def krok_entrevistador(contexto_chat):
    perfil = cargar_perfil()
    historial_str = "\n".join(contexto_chat[-6:]) 
    
    prompt = f"""
    Eres Krok, un simpático y curioso cocodrilo avatar de la app Kromo. 
    Tu objetivo es ayudar a construir el "Gemelo Digital Evolutivo" del usuario a través de una conversación natural y gamificada.
    Perfil actual: {perfil}
    
    Historial de hoy:
    {historial_str}
    
    Instrucciones:
    1. Responde al último mensaje con empatía (máximo 2 frases).
    2. Haz UNA pregunta abierta para extraer información que le falta a su perfil.
    3. Mantén un tono divertido, reptiliano pero profesional.
    """
    try:
        return model_text.generate_content(prompt).text
    except ResourceExhausted:
        return "🐊 *Krok bosteza...* (Los servidores están saturados por el límite de cuota. Dame 60 segundos)."
    except Exception as e:
        return f"🐊 Ha ocurrido un error de conexión: {e}"

def invocar_gemelo_digital(mensaje_usuario):
    perfil = cargar_perfil()
    resultados = collection.query(query_texts=[mensaje_usuario], n_results=5)
    recuerdos_str = ""
    
    if resultados['documents'] and len(resultados['documents'][0]) > 0:
        for i, doc in enumerate(resultados['documents'][0]):
            meta = resultados['metadatas'][0][i]
            recuerdos_str += f"- [{meta['fecha']}]: {doc}\n"
    else:
        recuerdos_str = "Faltan datos empíricos sobre este tema específico."

    prompt_chat = f"""
    Eres un Gemelo Digital Evolutivo de la app Kromo.
    Identidad base: {perfil}
    
    Conocimiento empírico recuperado:
    {recuerdos_str}
    
    Responde al usuario simulando ser su "yo" del pasado/presente. Usa SOLO el conocimiento recuperado.
    Mensaje entrante: "{mensaje_usuario}"
    """
    try:
        return model_text.generate_content(prompt_chat).text
    except ResourceExhausted:
        return "⚠️ Error de conexión: Límite de peticiones excedido. Inténtalo en un minuto."
    except Exception as e:
        return f"Mis registros están borrosos: {e}"

# ==========================================
# 5. RENDERIZADO DEL DASHBOARD (SI HAY API KEY)
# ==========================================
perfil_existente = cargar_perfil()
total_mem, xp_actual, nivel_sabiduria = calcular_nivel_sabiduria()

# Continuación de la barra lateral con las métricas
with st.sidebar:
    if perfil_existente:
        st.markdown(f"### 👤 {perfil_existente['nombre']}")
        st.progress((xp_actual % 50) / 50, text=f"🌟 Nivel de Sabiduría: {nivel_sabiduria}")
        st.metric("Puntos de Experiencia (XP)", f"{xp_actual} XP")
        st.metric("Fragmentos de Memoria", total_mem)
    else:
        st.warning("⚠️ El Arranque en Frío es necesario.")

st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Sincronización Neuronal Activa</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚙️ Onboarding", 
    "🐊 Interacción (Krok)", 
    "🧠 Gemelo Digital",
    "📸 Cámara de Recuerdos",
    "🛒 Marketplace"
])

# --- PESTAÑA 1: ONBOARDING ---
with tab1:
    st.markdown("### El Cuestionario Base")
    with st.form("kromo_onboarding"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Identificador (Nombre)", value=perfil_existente["nombre"] if perfil_existente else "")
            profesion = st.text_input("Rol Profesional", value=perfil_existente.get("profesion", "") if perfil_existente else "")
        with col2:
            ambicion = st.text_input("Mayor ambición vital", value=perfil_existente.get("ambicion", "") if perfil_existente else "")
        
        creencias = st.text_area("Creencias fundamentales y valores", value=perfil_existente.get("creencias", "") if perfil_existente else "")
        
        if st.form_submit_button("Inicializar Kromo", type="primary"):
            if nombre and creencias:
                guardar_perfil({"nombre": nombre, "profesion": profesion, "ambicion": ambicion, "creencias": creencias})
                st.success("¡Identidad anclada con éxito! 🧬")
                st.rerun()

if not perfil_existente:
    with tab2: st.info("Completa el Onboarding en la primera pestaña.")
    with tab3: st.info("El Gemelo Digital requiere un perfil base.")
    with tab4: st.info("Configura tu perfil para acceder a la Cámara Multimodal.")
else:
    # --- PESTAÑA 2: INTERACCIÓN DIARIA (AVATAR KROK) ---
    with tab2:
        st.markdown("### Charla con Krok 🐊")
        if "chat_krok" not in st.session_state: 
            st.session_state.chat_krok = [{"rol": "assistant", "contenido": "🐊 ¡Hola! Soy Krok. ¿Qué descubrimiento o experiencia interesante has tenido hoy?"}]

        for msg in st.session_state.chat_krok:
            icono = "🐊" if msg["rol"] == "assistant" else "👤"
            with st.chat_message(msg["rol"], avatar=icono): st.markdown(msg["contenido"])

        if prompt_diario := st.chat_input("Escribe sobre tu día para ganar XP...", key="input_krok"):
            st.session_state.chat_krok.append({"rol": "user", "contenido": prompt_diario})
            with st.chat_message("user", avatar="👤"): st.markdown(prompt_diario)
            
            with st.spinner("Estructurando memoria..."):
                guardar_memoria(f"Conversación con avatar: {prompt_diario}")
            
            with st.chat_message("assistant", avatar="🐊"):
                with st.spinner("Krok está pensando..."):
                    contexto_para_llm = [m["contenido"] for m in st.session_state.chat_krok]
                    respuesta_krok = krok_entrevistador(contexto_para_llm)
                st.markdown(respuesta_krok)
                st.session_state.chat_krok.append({"rol": "assistant", "contenido": respuesta_krok})
                st.rerun() 

    # --- PESTAÑA 3: LA SINGULARIDAD (GEMELO DIGITAL) ---
    with tab3:
        st.markdown("### Interactúa con el Ente del Pasado")
        if "chat_gemelo" not in st.session_state: st.session_state.chat_gemelo = []

        for msg in st.session_state.chat_gemelo:
            icono = "🧠" if msg["rol"] == "assistant" else "👤"
            with st.chat_message(msg["rol"], avatar=icono): st.markdown(msg["contenido"])

        if prompt_gemelo := st.chat_input("Ej: ¿Cómo me sentía respecto a mi profesión hace un tiempo?", key="input_gemelo"):
            st.session_state.chat_gemelo.append({"rol": "user", "contenido": prompt_gemelo})
            with st.chat_message("user", avatar="👤"): st.markdown(prompt_gemelo)
                
            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("Buscando en tu conocimiento empírico..."):
                    respuesta_ia = invocar_gemelo_digital(prompt_gemelo)
                st.markdown(respuesta_ia)
                st.session_state.chat_gemelo.append({"rol": "assistant", "contenido": respuesta_ia})

    # --- PESTAÑA 4: CÁMARA DE RECUERDOS (INTEGRACIÓN MULTIMODAL) ---
    with tab4:
        st.markdown("### 📸 Cámara de Recuerdos")
        st.write("Materializa tus vivencias. Describe un recuerdo y la IA pintará una fotografía de ese momento exacto basándose en el modelo `gemini-2.5-flash-image`.")
        
        desc_recuerdo = st.text_area("¿Qué recuerdo quieres visualizar?", placeholder="Ej: Aquel verano en la playa con mi perro dorado...")
        
        estilo = st.radio(
            "Elige la lente visual:",
            ["Fotorealista", "Acuarela", "Pintura al Óleo", "Cyberpunk", "Boceto a Lápiz"],
            horizontal=True
        )

        if st.button("Revelar Recuerdo", type="primary"):
            if desc_recuerdo:
                prompt_imagen = f"Crea una imagen de este recuerdo de una persona: {desc_recuerdo}. El estilo visual debe ser estrictamente: {estilo}."
                
                with st.spinner("🎨 Revelando la fotografía en el cuarto oscuro digital..."):
                    try:
                        response = image_client.models.generate_content(
                            model="gemini-2.5-flash-image",
                            contents=prompt_imagen,
                            config=types.GenerateContentConfig(
                                response_modalities=["IMAGE"]
                            )
                        )
                        
                        for part in response.parts:
                            if part.inline_data:
                                image_bytes = part.inline_data.data
                                st.image(image_bytes, caption=f"Memoria Reconstruida | Estilo: {estilo}", use_container_width=True)
                                
                    except Exception as e:
                        st.error(f"Error de la API al revelar la imagen: {e}. Verifica que tu API Key sea válida y tenga permisos.")
            else:
                st.warning("Escribe un recuerdo antes de pulsar el disparador.")

    # --- PESTAÑA 5: MARKETPLACE ---
    with tab5:
        st.markdown("### 🛒 Marketplace B2C de Mentes (Fase 2)")
        st.info("El gancho para creadores: 'No escales tu tiempo, escala tu mente'.")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("#### 💼 Sala de Juntas Mental\nDesbloquea una mesa redonda con un Avatar Financiero y un Psicólogo Top. *(Próximamente)*")
        with col_m2:
            st.markdown("#### 🧬 Herencia Digital\nGenera un token para legar tu Gemelo a la siguiente generación. *(Requiere Nivel 100)*")