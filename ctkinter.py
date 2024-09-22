from datetime import date
import json
import customtkinter as ctk
from tkinter import messagebox

# Funções para manipulação de dados
def lendo_documento_():
    caminho = "bancoDados.json"
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            lista = json.load(arquivo)
        return lista
    except FileNotFoundError:
        return {"receitas": [], "despesas": []}

def adicionando_itens_no_arquivo(tipo, novo_item, baseDados):
    baseDados[tipo].append(novo_item)
    with open("bancoDados.json", "w", encoding="utf-8") as arquivo:
        json.dump(baseDados, arquivo, ensure_ascii=False, indent=4)

def excluir_lista(tipo, tipo1, baseDados):
    baseDados[tipo].clear()
    baseDados[tipo1].clear()
    with open("bancoDados.json", "w", encoding="utf-8") as arquivo:
        json.dump(baseDados, arquivo, ensure_ascii=False, indent=4)

def obter_historico(tipo):
    despesas_text = "DESPESAS:\n"
    receitas_text = "RECEITAS:\n"
    
    if tipo == "receitas" :
        

        for item in bancoDados["receitas"]:
            receitas_text += f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n"
        

    
    if tipo == "despesas" :
        despesas_text = "DESPESAS:\n"
        for item in bancoDados["despesas"]:
            despesas_text += f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n"

    if tipo == "todos":
        

        for item in bancoDados["receitas"]:
            receitas_text += f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n"


        for item in bancoDados["despesas"]:
            despesas_text += f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n"
    
    return receitas_text + "\n" + despesas_text

def atualizar_historico(tipo):
    historico_text.configure(state='normal')
    historico_text.delete(1.0, ctk.END)
    historico_text.insert(ctk.END, obter_historico(tipo))
    historico_text.configure(state='disabled')

def mostrar_historico_frame():
    main_frame.pack_forget()
    formulario_frame.pack_forget()
    historico_frame.pack(fill="both", expand=True)
    tipo_var.set("todos")
    atualizar_historico("todos")

def voltar_para_principal():
    formulario_frame.pack_forget()
    historico_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def exibir_formulario(tipo_item):
    formulario_frame.pack(fill="both", expand=True)
    tipo_label.configure(text=f"Tipo de {tipo_item.capitalize()}:")
    tipo_entry.delete(0, ctk.END)
    valor_entry.delete(0, ctk.END)
    
    def salvar_item():
        tipo = tipo_entry.get()
        try:
            valor = float(valor_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número.")
            return
        
        if tipo and valor is not None:
            item = {
                "tipo": tipo,
                "valor": valor,
                "data": date.today().strftime("%d/%m/%Y")
            }
            if tipo_item == "receita":
                adicionando_itens_no_arquivo("receitas", item, bancoDados)
                messagebox.showinfo("Info", "Receita adicionada!")
            else:
                adicionando_itens_no_arquivo("despesas", item, bancoDados)
                messagebox.showinfo("Info", "Despesa adicionada!")
            
            resposta = messagebox.askyesno("Adicionar Novo", "Deseja adicionar mais itens?")
            if resposta:
                tipo_entry.delete(0, ctk.END)
                valor_entry.delete(0, ctk.END)
            else:
                formulario_frame.pack_forget()
                voltar_para_principal()
    
    salvar_btn.configure(command=salvar_item)

def excluir_historico():
    excluir_lista("despesas", "receitas", bancoDados)
    messagebox.showinfo("Info", "Histórico apagado!")

def mostrar_saldo():
    receita = sum(item['valor'] for item in bancoDados["receitas"])
    despesa = sum(item['valor'] for item in bancoDados["despesas"])
    saldo = receita - despesa
    messagebox.showinfo("Saldo", f"Saldo: R${saldo:.2f}")

# Configuração da interface gráfica
bancoDados = lendo_documento_()

# Inicializar CustomTkinter
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")  # Tema padrão

root = ctk.CTk()
root.title("Finance Personal")

# Criação dos frames
main_frame = ctk.CTkFrame(root)
historico_frame = ctk.CTkFrame(root)
formulario_frame = ctk.CTkFrame(root)

# Tela principal
welcome_label = ctk.CTkLabel(main_frame, text="Bem-vindo ao Finance Personal!\n\nUtilize as opções abaixo para gerenciar suas finanças.")
welcome_label.pack(padx=10, pady=(10, 20), fill="both", expand=True)

frame_buttons = ctk.CTkFrame(main_frame)
frame_buttons.pack(pady=(10, 0), fill="both", expand=True)

adicionar_receita_btn = ctk.CTkButton(frame_buttons, text="Adicionar Receita", command=lambda: exibir_formulario("receita"))
adicionar_receita_btn.pack(fill="x", pady=5)

adicionar_despesa_btn = ctk.CTkButton(frame_buttons, text="Adicionar Despesa", command=lambda: exibir_formulario("despesa"))
adicionar_despesa_btn.pack(fill="x", pady=5)

excluir_historico_btn = ctk.CTkButton(frame_buttons, text="Excluir Histórico", command=excluir_historico)
excluir_historico_btn.pack(fill="x", pady=5)

mostrar_saldo_btn = ctk.CTkButton(frame_buttons, text="Mostrar Saldo", command=mostrar_saldo)
mostrar_saldo_btn.pack(fill="x", pady=5)

mostrar_historico_btn = ctk.CTkButton(frame_buttons, text="Mostrar Histórico", command=mostrar_historico_frame)
mostrar_historico_btn.pack(fill="x", pady=5)

# Tela de histórico
tipo_var = ctk.StringVar(value="todos")
tipo_menu = ctk.CTkOptionMenu(historico_frame, variable=tipo_var, values=["receitas", "despesas", "todos"], command=lambda x: atualizar_historico(tipo_var.get()))
tipo_menu.pack(pady=10)

historico_text = ctk.CTkTextbox(historico_frame, width=600, height=300, state='disabled')
historico_text.pack(padx=10, pady=10, fill="both", expand=True)

voltar_btn = ctk.CTkButton(historico_frame, text="Voltar", command=voltar_para_principal)
voltar_btn.pack(pady=10)

# Tela de formulário
tipo_label = ctk.CTkLabel(formulario_frame, text="Tipo:")
tipo_label.pack(pady=10)
tipo_entry = ctk.CTkEntry(formulario_frame)
tipo_entry.pack(pady=10)

valor_label = ctk.CTkLabel(formulario_frame, text="Valor (R$):")
valor_label.pack(pady=10)
valor_entry = ctk.CTkEntry(formulario_frame)
valor_entry.pack(pady=10)

salvar_btn = ctk.CTkButton(formulario_frame, text="Salvar")
salvar_btn.pack(pady=20)

voltar_btn = ctk.CTkButton(formulario_frame, text="Voltar ao Início", command=voltar_para_principal)
voltar_btn.pack(pady=10)

# Inicializa a interface
main_frame.pack(fill="both", expand=True)
root.mainloop()
