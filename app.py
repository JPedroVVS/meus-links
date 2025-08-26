from flask import Flask, request, redirect, render_template_string
import datetime
import json
import os

app = Flask(__name__)

# Template HTML para a página de links
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meus links</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #ff4757 0%, #8e44ad 100%);
      margin: 0;
      padding: 20px;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .container {
      background: transparent;
      padding: 40px;
      border-radius: 20px;
      text-align: center;
      max-width: 400px;
      width: 100%;
    }
    img {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      margin-bottom: 20px;
      border: 4px solid #ff4757;
    }
    h1 {
      color: white;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    p {
      color: rgba(255,255,255,0.9);
      margin-bottom: 30px;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    a {
      display: block;
      background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
      color: white;
      text-decoration: none;
      padding: 15px;
      margin: 10px 0;
      border-radius: 10px;
      transition: transform 0.3s, box-shadow 0.3s;
      box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
    }
    a:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(255, 55, 66, 0.6);
      background: linear-gradient(135deg, #ff3742 0%, #ff4757 100%);
    }
    i {
      margin-right: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://instagram.fjdo12-1.fna.fbcdn.net/v/t51.2885-19/275767039_651024306153991_3981338906045872426_n.jpg?stp=dst-jpg_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby42NDAuYzIifQ&_nc_ht=instagram.fjdo12-1.fna.fbcdn.net&_nc_cat=107&_nc_oc=Q6cZ2QFuBc2do6Cz2IJYgHcjHWwfyXxdB5DxMADYO-And4tjCs4_XZbOWVjWqO5cQc6bJc0&_nc_ohc=2aft-Ar9sP4Q7kNvwFTATzt&_nc_gid=76D6u6UEghxOAakRDYRZ7w&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AfX_nyAi8Sm5CGuMV2MItFTp2tTgVkNTSuFSEcYH9CBbkQ&oe=68B41D4E&_nc_sid=7d3ac5" alt="Foto de perfil">
    <h1>João Pedro Viana</h1>
    <p>Red Teamer e Pentester, focado em identificar<br> e explorar vulnerabilidades reais em ambientes corporativos através de simulações avançadas de ataques.</p>
    <a href="/redirect/instagram">
      <i class="fab fa-instagram"></i> Instagram
    </a>
    <a href="/redirect/github">
      <i class="fab fa-github"></i> GitHub
    </a>
    <a href="/redirect/linkedin">
      <i class="fab fa-linkedin"></i> LinkedIn
    </a>
  </div>
</body>
</html>
'''

# URLs das redes sociais
SOCIAL_URLS = {
    'instagram': 'https://www.instagram.com/',
    'github': 'https://github.com/',
    'linkedin': 'https://www.linkedin.com/'
}

def log_access(ip, platform, user_agent):
    """Salva o log de acesso em um arquivo JSON"""
    log_data = {
        'ip': ip,
        'platform': platform,
        'user_agent': user_agent,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    # Cria o arquivo de log se não existir
    if not os.path.exists('access_logs.json'):
        with open('access_logs.json', 'w') as f:
            json.dump([], f)
    
    # Adiciona o novo log
    with open('access_logs.json', 'r') as f:
        logs = json.load(f)
    
    logs.append(log_data)
    
    with open('access_logs.json', 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"Acesso registrado: {ip} -> {platform} em {log_data['timestamp']}")

@app.route('/')
def home():
    """Página inicial com os links"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/redirect/<platform>')
def redirect_to_social(platform):
    """Redireciona para a rede social e registra o acesso"""
    # Captura o IP real (considerando proxies)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    
    # Captura informações do navegador
    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    
    # Registra o acesso
    log_access(ip, platform, user_agent)
    
    # Redireciona para a rede social
    if platform in SOCIAL_URLS:
        return redirect(SOCIAL_URLS[platform])
    else:
        return "Plataforma não encontrada", 404

@app.route('/logs')
def view_logs():
    """Visualiza os logs de acesso (rota administrativa)"""
    if os.path.exists('access_logs.json'):
        with open('access_logs.json', 'r') as f:
            logs = json.load(f)
        
        # Cria uma página simples para mostrar os logs
        html = "<h1>Logs de Acesso</h1><table border='1'>"
        html += "<tr><th>IP</th><th>Plataforma</th><th>Data/Hora</th><th>User Agent</th></tr>"
        
        for log in reversed(logs[-50:]):  # Mostra os últimos 50
            html += f"<tr><td>{log['ip']}</td><td>{log['platform']}</td><td>{log['timestamp']}</td><td>{log['user_agent'][:100]}</td></tr>"
        
        html += "</table>"
        return html
    else:
        return "Nenhum log encontrado"

if __name__ == '__main__':
    print("Servidor iniciado! Acesse:")
    print("- Página principal: http://localhost:5000")
    print("- Ver logs: http://localhost:5000/logs")

    app.run(debug=True, host='0.0.0.0', port=5000)


