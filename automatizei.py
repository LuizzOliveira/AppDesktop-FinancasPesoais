import json
import webbrowser
import subprocess
import time
import platform
import pygetwindow as gw
import customtkinter as ctk
import psutil
from tkinter import messagebox


# Caminho do arquivo JSON
arquivo_dados = "banco_dados.json"

# Inicializa o CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Função para ler o arquivo 'banco_dados.json'
def lendo_dados():
    try:
        with open(arquivo_dados, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    except (FileNotFoundError, json.JSONDecodeError):
        return {"sites": [], "apps": []}

# Função para salvar sites e apps no arquivo 'banco_dados.json'
def salvando_dados(dados):
    with open(arquivo_dados, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# Função para exibir o menu principal
def mostrar_menu():
    for widget in root.winfo_children():
        widget.destroy()

    btn_add_site = ctk.CTkButton(root, text="Adicionar Site", command=adicionar_site, corner_radius=10)
    btn_add_site.pack(padx=25, pady=10)

    btn_add_app = ctk.CTkButton(root, text="Adicionar App", command=adicionar_app, corner_radius=10)
    btn_add_app.pack(padx=25, pady=10)

    btn_ver_sites_apps = ctk.CTkButton(root, text="Ver Sites/Apps", command=mostrar_sites_apps, corner_radius=10)
    btn_ver_sites_apps.pack(padx=25, pady=10)

    btn_ativar_ambiente = ctk.CTkButton(root, text="Ativar Ambiente", command=ativar_ambiente, corner_radius=10)
    btn_ativar_ambiente.pack(padx=25, pady=10)

    # btn_fechar_ambiente = ctk.CTkButton(root, text="Fechar Apps", command=fechar_apps_navegadores, corner_radius=10)
    # btn_fechar_ambiente.pack(padx=25, pady=10)

    btn_excluir = ctk.CTkButton(root, text="Excluir Ambiente", command=excluir_ambiente, corner_radius=10)
    btn_excluir.pack(padx=25, pady=10)

    btn_voltar = ctk.CTkButton(root, text="Voltar", command=mostrar_pagina_principal, corner_radius=10, fg_color="black", width=50)
    btn_voltar.pack(pady=10)

# Função para mostrar instruções
def mostrar_instrucoes():
    for widget in root.winfo_children():
        widget.destroy()

    instrucoes = {
        "Adicionar Site": "Adiciona uma URL ao sistema.",
        "Adicionar App": "Adiciona um aplicativo para abrir posteriormente.",
        "Ver Sites/Apps": "Mostra os sites e aplicativos que você salvou.",
        "Ativar Ambiente": "Abre todos os sites e aplicativos salvos.",
        # "Fechar Apps": "Fecha todos os aplicativos e navegadores abertos.",
        "Excluir Ambiente": "Remove todos os sites e aplicativos salvos.",
    }

    for funcao, descricao in instrucoes.items():
        btn_instrucao = ctk.CTkButton(root, text=funcao, command=lambda desc=descricao: mostrar_descricao(desc), corner_radius=10)
        btn_instrucao.pack(padx=10, pady=5)

    btn_voltar = ctk.CTkButton(root, text="Voltar", command=mostrar_pagina_principal, corner_radius=10, fg_color="black", width=50)
    btn_voltar.pack(pady=10)

# Função para mostrar a descrição
def mostrar_descricao(descricao):
    messagebox.showinfo("Instrução", descricao)

# Função para mostrar informações sobre o sistema
def mostrar_sobre():
    for widget in root.winfo_children():
        widget.destroy()

    texto_sobre = ctk.CTkTextbox(root, width=400, height=200)
    texto_sobre.pack(padx=10, pady=10, fill="both", expand=True)

    informacao = (
        "Sobre o Automatizei:\n\n"
        "  Este sistema permite gerenciar sites e aplicativos, "
        "facilitando a abertura\n de múltiplos recursos de uma só vez.\n\n"
        " É útil para quem trabalha com várias ferramentas e deseja otimizar\n seu tempo."
    )
    texto_sobre.insert("end", informacao)
    texto_sobre.configure(state="disabled", font=("Helvetica", 14))  # Aumenta a fonte e define como negrito

    btn_voltar = ctk.CTkButton(root, text="Voltar", command=mostrar_pagina_principal, corner_radius=10)
    btn_voltar.pack(pady=10)

# Função para mostrar a página principal
def mostrar_pagina_principal():
    for widget in root.winfo_children():
        widget.destroy()

    btn_iniciar = ctk.CTkButton(root, text="Iniciar", command=mostrar_menu, corner_radius=10)
    btn_iniciar.pack(padx=25, pady=10)

    btn_instrucoes = ctk.CTkButton(root, text="Instruções de uso", command=mostrar_instrucoes, corner_radius=10)
    btn_instrucoes.pack(padx=25, pady=10)

    btn_sobre = ctk.CTkButton(root, text="Sobre", command=mostrar_sobre, corner_radius=10)
    btn_sobre.pack(padx=25, pady=10)

# Função para adicionar um novo site
def adicionar_site():
    site = ctk.CTkInputDialog(text="Cole a URL do site:", title="Adicionar Site").get_input()
    if site:
        dados = lendo_dados()
        dados["sites"].append(site)
        salvando_dados(dados)
        messagebox.showinfo("Sucesso", "Site adicionado com sucesso!")
    mostrar_menu()

# Função para adicionar um novo aplicativo
def adicionar_app():
    app = ctk.CTkInputDialog(text="Informe o nome do app (ex: 'bloco de notas'):", title="Adicionar App").get_input()
    if app:
        dados = lendo_dados()
        dados["apps"].append(app.lower())
        salvando_dados(dados)
        messagebox.showinfo("Sucesso", "App adicionado com sucesso!")
    mostrar_menu()

# Função para mostrar sites e aplicativos salvos
def mostrar_sites_apps():
    for widget in root.winfo_children():
        widget.destroy()

    dados = lendo_dados()
    sites = [site.split('/')[2] if '//' in site else site for site in dados["sites"]]
    sites = "\n  ".join(sites) if sites else "Nenhum site salvo."
    apps = "\n  ".join(dados["apps"]) if dados["apps"] else "Nenhum aplicativo salvo."

    texto = ctk.CTkTextbox(root)
    texto.pack(padx=10, pady=10, fill="both", expand=True)
    texto.insert("end", "Sites:\n  " + sites + "\n\nAplicativos:\n  " + apps)
    texto.configure(state="disabled")

    btn_voltar = ctk.CTkButton(root, text="Voltar", command=mostrar_menu, corner_radius=10)
    btn_voltar.pack(pady=10)

# Função para buscar o comando correto para abrir o aplicativo
def buscar_aplicativo(nome):
    sistema = platform.system()
    if sistema == "Windows":
        mapeamento_apps = {
            "word": "winword",
            "calculadora": "calc",
            "bloco de notas": "notepad",
            "explorador de arquivos": "explorer",
            "paint": "mspaint",
            "windows media player": "wmplayer",
            "gerenciador de tarefas": "taskmgr",
            "prompt de comando": "cmd",
            "powershell": "powershell",
            "explorador de internet": "iexplore",
            "microsoft edge": "msedge",
            "editor de vídeo": "videoeditor",
            "gravador de voz": "soundrecorder",
            "wordpad": "write",
            "microsoft word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "microsoft store": "ms-windows-store:",
            "configurações": "ms-settings:",
            "teclado virtual": "osk",
            "gerenciador de dispositivos": "devmgmt.msc",
            "gerenciamento de disco": "diskmgmt.msc",
            "painel de controle": "control",
            "narrador": "narrator",
            "visualizador de eventos": "eventvwr.msc",
            "conexão de área de trabalho remota": "mstsc",
            "explorer": "explorer",
            "cortana": "searchui",
            "solicitador de feedback": "feedback-hub:",
            "ferramenta de recorte": "SnippingTool",
            "mapas": "bingmaps:",
            "central de ações": "ms-actioncenter:",
            "agenda": "outlookcal:",
            "calendário": "outlookcal:",
            "fotos": "microsoft.photos:",
            "alarme e relógio": "ms-clock:",
            "calculadora gráfica": "calcgraphical:",
            "captura de tela": "ms-screenclip:",
            "notícias e interesses": "bingweather:",
            "notas autoadesivas": "ms-stickynotes:",
            "xbox": "xboxapp:",
            "suporte remoto": "msra"
        }
        nome_correto = mapeamento_apps.get(nome.lower(), nome)
        return f'start {nome_correto}.exe'
    elif sistema == "Linux":
        return f'xdg-open {nome}'
    elif sistema == "Darwin":
        return f'open -a "{nome}"'
    else:
        raise Exception("Sistema operacional não suportado.")

# Função para abrir os sites salvos
def abrir_sites():
    dados = lendo_dados()
    for site in dados["sites"]:
        webbrowser.open(site)
        time.sleep(2)

# Função para abrir os aplicativos salvos
def abrir_apps():
    dados = lendo_dados()
    for app in dados["apps"]:
        try:
            subprocess.Popen(buscar_aplicativo(app), shell=True)
            time.sleep(2)  # Aguarda o aplicativo abrir
            # Minimiza a janela
            janelas = gw.getWindowsWithTitle(app)
            for janela in janelas:
                janela.minimize()
            time.sleep(2)  # Aguarda um pouco antes de abrir o próximo
        except Exception as e:
            print(f"Erro ao abrir {app}: {e}")

# # Função para fechar processos
# def fechar_processos_por_nome(nomes):
#     for processo in psutil.process_iter(['pid', 'name']):
#         for nome in nomes:
#             if nome.lower() in processo.info['name'].lower():
#                 try:
#                     p = psutil.Process(processo.info['pid'])
#                     p.terminate()
#                 except Exception as e:
#                     print(f"Erro ao fechar {processo.info['name']}: {e}")

# # Função para fechar janelas
# def fechar_apps_navegadores():
#     janelas = gw.getAllWindows()
#     id_janela_principal = root.winfo_id()  # Obtém ID da janela principal
#     # Fecha todas as janelas, exceto a principal
#     for janela in janelas:
#         if janela._hWnd != id_janela_principal and janela.visible:
#             try:
#                 janela.close()  # Fecha a janela
#                 time.sleep(1)  # Espera um pouco antes de fechar a próxima
#             except Exception as e:
#                 print(f"Erro ao fechar {janela.title}: {e}")

#     # Lista de processos para fechar
#     processos_a_fechar = [
#         'chrome.exe', 'firefox.exe', 'msedge.exe', 'explorer.exe', 
#         'notepad.exe', 'calc.exe', 'WINWORD.EXE', 'excel.exe', 
#         'powerpnt.exe', 'outlook.exe'
#     ]
    
#     # Fechar processos sem abrir janela do Windows
#     for processo in processos_a_fechar:
#         subprocess.call(["taskkill", "/F", "/IM", processo], creationflags=subprocess.CREATE_NO_WINDOW)

# # Função adicional para fechar processos por nome
# def fechar_processos_por_nome(processos):
#     for processo in processos:
#         subprocess.call(["taskkill", "/F", "/IM", processo], creationflags=subprocess.CREATE_NO_WINDOW)

#     # Lista de processos para fechar
#     processos_a_fechar = [
#         'chrome.exe', 'firefox.exe', 'msedge.exe', 'explorer.exe', 
#         'notepad.exe', 'calc.exe', 'WINWORD.EXE', 'excel.exe', 
#         'powerpnt.exe', 'outlook.exe'
#     ]
#     fechar_processos_por_nome(processos_a_fechar)




# Função para excluir o ambiente
def excluir_ambiente():
    dados = {"sites": [], "apps": []}
    salvando_dados(dados)
    messagebox.showinfo("Sucesso", "Ambiente excluído com sucesso!")
    mostrar_menu()

# Função para ativar o ambiente
def ativar_ambiente():
    abrir_sites()
    abrir_apps()
    messagebox.showinfo("Sucesso", "Ambiente ativado com sucesso!")

# Configurações da janela
root = ctk.CTk()
root.title("Gerador Automatizado Ambiente Desktop")
root.geometry("500x400")

mostrar_pagina_principal()
root.mainloop()
