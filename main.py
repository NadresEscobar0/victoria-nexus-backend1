from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import re

app = Flask(__name__)
CORS(app)  # Permite que el frontend se conecte

API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def limpiar_markdown(texto):
    texto = re.sub(r"(\*\*|\*)", "", texto)
    texto = texto.replace("__", "")
    return texto.strip()

def construir_prompt(pregunta, estilo):
    base = (
        "Eres VictorIA Nexus, un asistente académico creativo y adaptativo. "
        "Primero, responde de forma concisa y clara a la pregunta, en un solo párrafo. "
        "Luego, proporciona una explicación creativa, profunda y adaptada al estilo de aprendizaje indicado, "
        "usando analogías, metáforas o ejemplos originales, como si explicaras a un estudiante curioso. "
        "Evita respuestas automáticas o superficiales. "
        "No uses formato Markdown ni asteriscos, pero sí puedes usar listas o numeraciones si ayudan a la comprensión."
    )
    if estilo == "Visual":
        detalle = (
            "La explicación creativa debe incluir diagramas, esquemas visuales o mapas conceptuales. "
            "Si es posible, describe un diagrama usando texto (por ejemplo, usa flechas, cajas, relaciones, como si dibujaras un mapa mental en ASCII). "
            "No expliques otros estilos."
        )
    elif estilo == "Auditivo":
        detalle = (
            "La explicación creativa debe incluir ejemplos auditivos, relatos, metáforas sonoras, explicaciones habladas o historias narradas. "
            "No expliques otros estilos."
        )
    else:
        detalle = (
            "La explicación creativa debe sugerir actividades prácticas, ejemplos kinestésicos, ejercicios paso a paso y propuestas que impliquen acción física. "
            "No expliques otros estilos."
        )
    return f"{base} {detalle} Pregunta: {pregunta}"

@app.route("/consulta", methods=["POST"])
def consulta():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    estilo = data.get("estilo", "Visual")
    if not pregunta.strip():
        return jsonify({"respuesta": "Por favor, escribe una pregunta académica."})
    prompt = construir_prompt(pregunta, estilo)
    try:
        respuesta = model.generate_content(prompt)
        texto_plano = limpiar_markdown(respuesta.text)
        return jsonify({"respuesta": texto_plano})
    except Exception as e:
        return jsonify({"respuesta": f"Error al generar respuesta: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
