import json  # Manipulação de arquivos JSON
import webbrowser  # Abre sites no navegador
import subprocess  # Executa comandos do SO
import time  # Controla intervalos no script
import platform  # Identifica o SO
import pygetwindow as gw  # Gerencia janelas
import tkinter as tk  # Janelas gráficas
from tkinter import messagebox  # Caixas de diálogo
import psutil  # Gerencia processos

def adicionando_site(novo_item, nome_lista):
    nome_lista.append(novo_item)
    with open("sites.json", "w", encoding="utf-8") as arquivo:
        json.dump(nome_lista, arquivo, ensure_ascii=False, indent=4)

def lendo_sites():
    try:
        with open("sites.json", "r", encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
        return lista
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def adicionando_app(novo_item, nome_lista):
    nome_lista.append(novo_item)
    with open("apps.json", "w", encoding="utf-8") as arquivo:
        json.dump(nome_lista, arquivo, ensure_ascii=False, indent=4)

def lendo_apps():
    try:
        with open("apps.json", "r", encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
        return lista
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_sites():
    sites = lendo_sites()
    while True:
        site = input("Cole aqui a URL do site: ")
        adicionando_site(site, sites)
        if input("Deseja adicionar mais sites? s/n ").lower() == 'n':
            break
    return sites

def add_apps():
    apps = lendo_apps()
    while True:
        app = input("Informe o nome do app: ").lower()
        adicionando_app(app, apps)
        if input("Deseja adicionar mais apps? s/n ").lower() == 'n':
            break
    return apps

def buscar_aplicativo(nome):
    sistema = platform.system()
    if sistema == "Windows":
        mapeamento_apps = {
            "bloco de notas": "notepad",
            "calculadora": "calc",
            "explorador de arquivos": "explorer",
            "microsoft word": "winword",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt"
        }
        nome_correto = mapeamento_apps.get(nome.lower(), nome)
        return f'start {nome_correto}.exe'
    elif sistema == "Linux":
        return f'xdg-open {nome}'
    elif sistema == "Darwin":
        return f'open -a "{nome}"'
    else:
        raise Exception("SO não suportado.")

def abrir_sites(sites):
    for site in sites:
        print(f"Abrindo {site}...")
        webbrowser.open(site)
        time.sleep(2)

def abrir_aplicativos(apps):
    for app in apps:
        try:
            print(f"Abrindo {app}...")
            subprocess.Popen(buscar_aplicativo(app), shell=True)
            time.sleep(2)
            janelas = gw.getWindowsWithTitle(app)
            if janelas:
                for janela in janelas:
                    janela.minimize()
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao abrir {app}: {e}")

def fechar_processos_por_nome(nomes):
    for processo in psutil.process_iter(['pid', 'name']):
        for nome in nomes:
            if nome.lower() in processo.info['name'].lower():
                try:
                    psutil.Process(processo.info['pid']).terminate()
                    print(f"Fechando {processo.info['name']}...")
                except Exception as e:
                    print(f"Erro ao fechar {processo.info['name']}: {e}")

def fechar_apps_navegadores():
    janelas = gw.getAllWindows()
    for janela in janelas:
        try:
            if not janela.isMinimized and janela.isVisible():
                print(f"Fechando {janela.title}...")
                janela.close()
                time.sleep(1)
        except Exception as e:
            print(f"Erro ao fechar {janela.title}: {e}")

    processos_a_fechar = ['chrome', 'firefox', 'edge', 'explorer', 'notepad', 'calc']
    fechar_processos_por_nome(processos_a_fechar)

def excluir():
    with open("sites.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii=False, indent=4)
    with open("apps.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii=False, indent=4)
    print("Ambientes excluídos.")

def confirmar_fechamento():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes("-topmost", True)
    resposta = messagebox.askyesno("Fechar Apps", "Deseja fechar aplicativos e navegadores abertos?")
    root.destroy()
    return resposta

def main():
    while True:
        print('''
    AUTOMATIZEI
    
(1) - CRIAR AMBIENTE
(2) - ATIVAR AMBIENTE
(3) - EXCLUIR AMBIENTE
(0) - SAIR
''')
        try:
            menu = int(input("Opção menu: "))
        except ValueError:
            print("Informe apenas números.")
            continue

        match menu:
            case 1:
                add_sites()
                add_apps()
            case 2:
                if confirmar_fechamento():
                    fechar_apps_navegadores()
                sites = lendo_sites()
                apps = lendo_apps()
                if sites or apps:
                    abrir_sites(sites)
                    abrir_aplicativos(apps)
                else:
                    print("\n(vazio)")
            case 3:
                excluir()
            case 0:
                break
            case _:
                print('Opção Inválida')

if __name__ == "__main__":
    main()
