"""API REST de la calculadora (Práctica 2)."""
import os

from flask import Flask, jsonify, request

from src.calculos import OPERACIONES, calcular

app = Flask(__name__)
APP_NAME = os.getenv("APP_NAME", "calculadora-devops")


@app.get("/")
def inicio():
    return jsonify(
        app=APP_NAME,
        mensaje="API de la calculadora. Usa /calcular?op=suma&a=2&b=3",
        operaciones=list(OPERACIONES),
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/calcular")
def endpoint_calcular():
    op = request.args.get("op", "")
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="Los parámetros 'a' y 'b' son obligatorios y numéricos"), 400
    try:
        resultado = calcular(op, a, b)
    except (ValueError, ZeroDivisionError) as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(operacion=op, a=a, b=b, resultado=resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
