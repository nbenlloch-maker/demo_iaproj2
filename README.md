<h1 align="center">🧬 K R O M O</h1>
<h3 align="center">EL PRIMER GEMELO DIGITAL EVOLUTIVO</h3>

> *"No estamos construyendo un diario. Estamos programando la inmortalidad cognitiva mediante Inteligencia Artificial."*

Kromo es una arquitectura de software diseñada para capturar, procesar y replicar la identidad humana. A través de un sistema conversacional proactivo, la aplicación extrae el conocimiento empírico del usuario, lo vectoriza y entrena a un **Gemelo Digital** capaz de razonar, recordar e interactuar en el futuro utilizando la personalidad exacta de su creador.

---

## 🛠️ ARQUITECTURA TÉCNICA Y STACK DE DESARROLLO

Para lograr que una IA simule la conciencia de un usuario en tiempo real sin alucinaciones, hemos descartado los prompts estáticos y hemos implementado una arquitectura **RAG (Retrieval-Augmented Generation)** de última generación.

### 1. Motor de Memoria Vectorial (ChromaDB)
El cerebro de Kromo no es una base de datos relacional tradicional (SQL). Utilizamos **ChromaDB** para almacenar los recuerdos como *embeddings* vectoriales. Cuando el usuario hace una pregunta a su Gemelo Digital, el sistema realiza una búsqueda de similitud semántica (K-Nearest Neighbors) para inyectar en el contexto del LLM únicamente los recuerdos empíricos relevantes. **Resultado: Cero alucinaciones, 100% de precisión autobiográfica.**

### 2. Orquestación Multimodal (Ecosistema Gemini)
Kromo no depende de un solo modelo, sino de una orquestación inteligente de la API de Google Gemini:
* **Razonamiento Lógico e Interacción:** Impulsado por `gemini-2.5-flash`. Este modelo se encarga de dar vida a *Krok* (el agente conversacional de extracción de datos) y de simular la personalidad del Gemelo Digital basándose en el contexto inyectado por ChromaDB.
* **Inmersión Visual:** Integración directa con el SDK `google-genai` para invocar al modelo generador de imágenes. Transforma descripciones de recuerdos en representaciones visuales fotorrealistas o artísticas bajo demanda.

### 3. Frontend Reactivo y Gestión de Estado (Streamlit)
La interfaz está construida íntegramente en Python mediante **Streamlit**. Hemos desarrollado un complejo sistema de `st.session_state` para mantener el historial de los chats, aislar la memoria temporal del usuario de la base de datos persistente y renderizar una interfaz fluida estilo *Single Page Application (SPA)*.

### 4. Resiliencia y Control de Errores (Error Handling)
La aplicación cuenta con captura activa de excepciones (`google.api_core.exceptions.ResourceExhausted`). Si la API alcanza su límite de cuota, el sistema no colapsa: intercepta el error y la interfaz de usuario responde con un mensaje orgánico (ej. *"Los servidores están saturados, dame 60 segundos"*), protegiendo la Experiencia de Usuario (UX) en entornos de producción.

---

## 🚀 FLUJO DEL PRODUCTO (FASE 1: MVP)

Kromo está estructurado en cuatro módulos interconectados que retroalimentan el sistema:

#### LA INICIALIZACIÓN (ARRANQUE EN FRÍO)
Para evitar el síndrome de la página en blanco que mata la retención de los usuarios en las apps de *journaling*, exigimos un **Onboarding Estratégico**. El usuario define su identificador, rol profesional, ambición vital y creencias fundamentales. Estos datos se guardan en un JSON local (`kromo_perfil.json`) que actúa como el *System Prompt* fundacional de todas las interacciones futuras.

#### EL EXTRACTOR DE DATOS (AGENTE KROK)
El usuario interactúa diariamente con un avatar gamificado. Mediante encadenamiento de prompts (*Prompt Chaining*), Krok lee el historial reciente y genera **preguntas dinámicas y psicológicas** diseñadas específicamente para extraer información que aún no existe en la base de datos vectorial del usuario, maximizando la eficiencia de la recolección de datos.

#### LA SINGULARIDAD (INVOCACIÓN DEL GEMELO)
El módulo de salida. El usuario lanza un *query* a su yo del pasado. La arquitectura RAG entra en acción, recupera los 5 vectores más cercanos al *query* y obliga al LLM a generar una respuesta utilizando **ESTRICTAMENTE** esos documentos, simulando una conversación real y coherente con uno mismo.

#### LA CÁMARA MULTIMODAL
Traducción de texto a píxeles. El usuario introduce una memoria nostálgica y Kromo utiliza la inyección de prompts para estructurar una petición visual perfecta, devolviendo una fotografía generada por IA del momento exacto.

---

## 💻 DESPLIEGUE EN ENTORNOS LOCALES

Si eres un desarrollador y quieres auditar o escalar esta arquitectura en tu propia máquina, sigue estos pasos de clonación:

1. Clona el repositorio e inicializa un entorno virtual aislado:
   ```bash
   python3 -m venv venv
   source venv/bin/activate