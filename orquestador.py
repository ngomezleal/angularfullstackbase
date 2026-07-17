import os
import re
from crewai import Agent, Task, Crew, LLM

# =====================================================================
# 1. RUTAS DE TUS ARCHIVOS (Configuradas exactamente a tu proyecto)
# =====================================================================
RUTA_HTML_TARGET = "src/app/componentes/demo-sensor/demo-sensor.html"
RUTA_STYLE_GUIDE = "style-guide.md"

# =====================================================================
# 2. CONFIGURACIÓN DEL MODELO LOCAL
# =====================================================================
MODELO_LOCAL = "ollama/qwen2.5-coder:7b"
BASE_URL_OLLAMA = "http://localhost:11434"

llm_local = LLM(
    model=MODELO_LOCAL,
    base_url=BASE_URL_OLLAMA
)

# =====================================================================
# 3. CARGAR LOS ARCHIVOS UTILIZANDO LAS RUTAS EXACTAS
# =====================================================================
def cargar_recursos():
    # Verificar si los archivos realmente existen antes de continuar
    if not os.path.exists(RUTA_HTML_TARGET):
        raise FileNotFoundError(f"❌ Error: No se encontró el HTML en '{RUTA_HTML_TARGET}'")
    if not os.path.exists(RUTA_STYLE_GUIDE):
        raise FileNotFoundError(f"❌ Error: No se encontró la guía en '{RUTA_STYLE_GUIDE}'")

    # Leer el HTML con malas prácticas
    with open(RUTA_HTML_TARGET, "r", encoding="utf-8") as f:
        html_sucio = f.read()
        
    # Leer las reglas de juego de la Guía de Estilos
    with open(RUTA_STYLE_GUIDE, "r", encoding="utf-8") as f:
        guia_estilos = f.read()
        
    return html_sucio, guia_estilos


# =====================================================================
# 4. AGENTE Y TAREA (EL CORAZÓN DEL ORQUESTADOR)
# =====================================================================
def ejecutar_refactorizacion():
    try:
        html_original, guia = cargar_recursos()
    except Exception as e:
        print(e)
        return

    # Definimos nuestro único programador experto para evitar dilución de atención en 1.5B
    programador_frontend = Agent(
        role="Especialista en Refactorización Angular y Bootstrap 5",
        goal="Corregir archivos HTML eliminando malas prácticas y aplicando Bootstrap 5 de forma estricta.",
        backstory=(
            "Eres un desarrollador frontend experto. Tu única obsesión es el código limpio. "
            "No toleras los estilos en línea (atributos 'style') ni las clases obsoletas. "
            "Reescribes el HTML respetando al 100% el comportamiento original del componente."
        ),
        verbose=True,
        llm=llm_local
    )

    # Creamos la tarea pasándole el HTML y la guía leídos
    tarea_limpieza = Task(
        description=(
            f"Tu misión es reescribir el siguiente código HTML:\n\n"
            f"--- HTML ORIGINAL ---\n"
            f"{html_original}\n"
            f"---------------------\n\n"
            f"Debes aplicar estrictamente las reglas de esta guía de estilos:\n\n"
            f"--- GUÍA DE ESTILOS (.md) ---\n"
            f"{guia}\n"
            f"-----------------------------\n\n"
            f"INSTRUCCIONES CLAVE:\n"
            f"1. Elimina CUALQUIER atributo 'style=...' (Prohibidos estilos inline).\n"
            f"2. Utiliza únicamente clases nativas de Bootstrap 5 para márgenes, paddings, bordes y anchos.\n"
            f"3. Mantén los textos y las etiquetas intactos. Solo modifica las clases CSS y elimina los estilos inline.\n"
            f"4. Devuelve ÚNICAMENTE el código HTML limpio. No agregues explicaciones, notas ni introducciones."
        ),
        expected_output="El código HTML limpio y corregido, estructurado únicamente con Bootstrap 5.",
        agent=programador_frontend
    )

    # Creamos la tripulación con el agente y su tarea
    orquestador = Crew(
        agents=[programador_frontend],
        tasks=[tarea_limpieza],
        verbose=True
    )

    print(f"🚀 Iniciando la limpieza de: {RUTA_HTML_TARGET} ...")
    resultado_raw = orquestador.kickoff()
    
    # Extraemos el código HTML limpio (en caso de que el LLM devuelva bloques ```html ... ```)
    codigo_limpio = limpiar_resultado(str(resultado_raw))
    
    # Guardamos el resultado directamente sobreescribiendo el archivo original en su ruta correspondiente
    with open(RUTA_HTML_TARGET, "w", encoding="utf-8") as f:
        f.write(codigo_limpio)
        
    print(f"\n✅ ¡Listo! El archivo '{RUTA_HTML_TARGET}' ha sido actualizado y corregido con éxito.")


# =====================================================================
# 5. FUNCIÓN AUXILIAR PARA EVITAR COMILLAS EXTRAÑAS DE MARKDOWN
# =====================================================================
def limpiar_resultado(texto_raw: str) -> str:
    """Extrae el HTML si el modelo lo envolvió en bloques de código de markdown"""
    texto = texto_raw.strip()
    match = re.search(r"```html\s*(.*?)\s*```", texto, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Remover marcas generales de bloques si existen
    lineas = texto.splitlines()
    lineas_filtradas = [l for l in lineas if not l.strip().startswith("```")]
    return "\n".join(lineas_filtradas).strip()


if __name__ == "__main__":
    ejecutar_refactorizacion()