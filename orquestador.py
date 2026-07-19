import os
import re
from crewai import Agent, Task, Crew, Process, LLM

# =====================================================================
# 1. RUTAS DE TUS ARCHIVOS
# =====================================================================
RUTA_HTML_TARGET = "src/app/componentes/demo-sensor/demo-sensor.html"
RUTA_STYLE_GUIDE = "style-guide.md"

# =====================================================================
# 2. CONFIGURACIÓN DEL MODELO LOCAL (Usamos el potente 7b)
# =====================================================================
MODELO_LOCAL = "ollama/qwen2.5-coder:7b"
BASE_URL_OLLAMA = "http://localhost:11434"

llm_local = LLM(
    model=MODELO_LOCAL,
    base_url=BASE_URL_OLLAMA
)

# =====================================================================
# 3. CARGAR RECURSOS
# =====================================================================
def cargar_recursos():
    if not os.path.exists(RUTA_HTML_TARGET):
        raise FileNotFoundError(f"❌ Error: No se encontró el HTML en '{RUTA_HTML_TARGET}'")
    if not os.path.exists(RUTA_STYLE_GUIDE):
        raise FileNotFoundError(f"❌ Error: No se encontró la guía en '{RUTA_STYLE_GUIDE}'")

    with open(RUTA_HTML_TARGET, "r", encoding="utf-8") as f:
        html_sucio = f.read()
    with open(RUTA_STYLE_GUIDE, "r", encoding="utf-8") as f:
        guia_estilos = f.read()
        
    return html_sucio, guia_estilos


# =====================================================================
# 4. CONFIGURACIÓN DE LA TRIPULACIÓN MULTI-AGENTE
# =====================================================================
def ejecutar_refactorizacion():
    try:
        html_original, guia = cargar_recursos()
    except Exception as e:
        print(e)
        return

    # -----------------------------------------------------------------
    # Agente 1: El Auditor (Solo busca problemas)
    # -----------------------------------------------------------------
    auditor = Agent(
        role="Auditor de Código y Estilos",
        goal="Identificar estilos en línea, clases obsoletas y violaciones a la guía de estilos.",
        backstory=(
            "Eres un inspector de calidad de software sumamente estricto. Tu trabajo no es escribir código, "
            "sino analizar el HTML original y compararlo con la guía de estilos para listar detalladamente "
            "qué elementos violan las reglas (como los atributos 'style' o clases de Bootstrap incorrectas)."
        ),
        verbose=True,
        llm=llm_local
    )

    # -----------------------------------------------------------------
    # Agente 2: El Diseñador (Propone soluciones visuales)
    # -----------------------------------------------------------------
    disenador = Agent(
        role="Diseñador UI Especialista en Bootstrap 5",
        goal="Traducir los problemas detectados en soluciones visuales modernas usando Bootstrap 5.",
        backstory=(
            "Eres un experto en diseño de interfaces y Bootstrap 5. Tomas el reporte de errores del auditor "
            "y decides exactamente qué clases modernas de Bootstrap 5 se deben aplicar para reemplazar "
            "los estilos inline y hacer que el componente sea responsivo y limpio."
        ),
        verbose=True,
        llm=llm_local
    )

    # -----------------------------------------------------------------
    # Agente 3: El Programador Angular (Escribe el código final)
    # -----------------------------------------------------------------
    programador = Agent(
        role="Programador Senior Angular",
        goal="Escribir el HTML final limpio aplicando las propuestas de diseño y protegiendo la lógica de Angular.",
        backstory=(
            "Eres un desarrollador frontend senior muy minucioso. Tu trabajo es tomar las especificaciones "
            "del diseñador y reescribir el HTML. Te aseguras de que no quede ningún estilo inline "
            "y de que la estructura sea semánticamente perfecta, sin romper bindings ni directivas de Angular."
        ),
        verbose=True,
        llm=llm_local
    )

    # -----------------------------------------------------------------
    # Agente 4: El QA / Tester (Filtro de seguridad final)
    # -----------------------------------------------------------------
    qa_tester = Agent(
        role="Ingenior de QA y Control de Calidad Frontend",
        goal="Verificar que el HTML final cumpla estrictamente con la guía de estilos y no tenga errores sintácticos.",
        backstory=(
            "Eres un tester frontend implacable. Tu trabajo es revisar el código final del programador. "
            "Si encuentras un solo estilo inline, una clase obsoleta o una etiqueta mal cerrada, "
            "rechazarás el entregable y reportarás el fallo. Tu palabra es la última antes de ir a producción."
        ),
        verbose=True,
        llm=llm_local
    )

    # =====================================================================
    # 5. DEFINICIÓN DE TAREAS EN CADENA
    # =====================================================================

    # Tarea 1: Auditoría
    tarea_auditoria = Task(
        description=(
            f"Analiza este HTML original:\n\n{html_original}\n\n"
            f"Y compáralo con esta guía de estilos:\n\n{guia}\n\n"
            f"Genera un reporte detallando cada línea o elemento que viole las reglas."
        ),
        expected_output="Un informe detallado en Markdown con los problemas encontrados.",
        agent=auditor
    )

    # Tarea 2: Diseño (Toma como contexto implícito el resultado de la auditoría)
    tarea_diseno = Task(
        description=(
            f"Toma el reporte del Auditor. Para cada problema detectado en el HTML original, "
            f"propón la clase exacta de Bootstrap 5 que debe reemplazarlo. Asegura un diseño responsivo."
        ),
        expected_output="Una guía de reemplazos y clases de Bootstrap 5 recomendadas para el componente.",
        agent=disenador
    )

    # Tarea 3: Programación (Aplica el diseño final al HTML original)
    tarea_programacion = Task(
        description=(
            f"Toma las propuestas del Diseñador UI y reescribe por completo el HTML original:\n\n"
            f"--- HTML ORIGINAL ---\n{html_original}\n---------------------\n\n"
            f"Genera el código HTML final. Asegúrate de eliminar todos los atributos 'style' "
            f"y de entregar únicamente el código limpio, sin explicaciones."
        ),
        expected_output="El código HTML limpio corregido de inicio a fin. Sin bloques de markdown extras.",
        agent=programador
    )

    # Tarea 4: Control de Calidad (Toma como contexto directo el HTML del programador)
    tarea_qa = Task(
        description=(
            f"Toma el código HTML final generado por el Programador y realiza una auditoría de cierre.\n"
            f"Verifica de forma estricta contra esta guía:\n\n{guia}\n\n"
            f"REGLAS DE VALIDACIÓN:\n"
            f"1. Si queda ALGÚN atributo 'style=...', elimínalo de inmediato.\n"
            f"2. Asegúrate de que las etiquetas estén perfectamente estructuradas y cerradas.\n"
            f"3. Tu salida debe ser ÚNICAMENTE el código HTML 100% aprobado y limpio, listo para guardarse."
        ),
        expected_output="El código HTML definitivo, verificado, limpio y libre de errores o estilos inline.",
        agent=qa_tester
    )

    # =====================================================================
    # 6. ORQUESTACIÓN SECUENCIAL
    # =====================================================================
    orquestador = Crew(
        agents=[auditor, disenador, programador, qa_tester],
        tasks=[tarea_auditoria, tarea_diseno, tarea_programacion, tarea_qa],
        process=Process.sequential,  # <-- ESTO ejecuta las tareas en orden (1 -> 2 -> 3)
        verbose=True
    )

    print(f"🚀 Iniciando flujo de trabajo multi-agente para: {RUTA_HTML_TARGET} ...")
    resultado_raw = orquestador.kickoff()
    
    # Extraemos el código HTML final y lo limpiamos
    codigo_limpio = limpiar_resultado(str(resultado_raw))
    
    # Guardamos el archivo actualizado
    with open(RUTA_HTML_TARGET, "w", encoding="utf-8") as f:
        f.write(codigo_limpio)
        
    print(f"\n✅ ¡Listo! El pipeline multi-agente ha finalizado. Archivo actualizado en: {RUTA_HTML_TARGET}")


# =====================================================================
# 7. FUNCIÓN AUXILIAR DE LIMPIEZA
# =====================================================================
def limpiar_resultado(texto_raw: str) -> str:
    texto = texto_raw.strip()
    match = re.search(r"```html\s*(.*?)\s*```", texto, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    lineas = texto.splitlines()
    lineas_filtradas = [l for l in lineas if not l.strip().startswith("```")]
    return "\n".join(lineas_filtradas).strip()


if __name__ == "__main__":
    ejecutar_refactorizacion()