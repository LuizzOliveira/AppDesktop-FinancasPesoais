
from datetime import date
import json

def lendo_documento_():
        #caminho do arquivo json com os dados
        caminho = "bancoDados.json"
        try:
            #carregar lista com dados
            with open(caminho, "r", encoding="utf-8") as arquivo:
                lista = json.load(arquivo)
            return lista
        except:
            return {
                    "receitas": [],
                    "despesas": []
            }


def adicionando_itens_no_arquivo(tipo,novo_item,baseDados):    

    baseDados[tipo].append(novo_item)   
    with open("bancoDados.json","w", encoding= "utf-8") as arquivo:
        json.dump(baseDados, arquivo, ensure_ascii=False, indent=4) 
        
def excluir_lista(tipo,tipo1, baseDados):      
    baseDados[tipo].clear()    
    baseDados[tipo1].clear()    
    with open("bancoDados.json","w", encoding= "utf-8") as arquivo:
        json.dump(baseDados, arquivo, ensure_ascii=False, indent=4) 


def criando_arquivo(tipo_lista):      
    with open("bancoDados.json","w", encoding= "utf-8") as arquivo:
        json.dump(tipo_lista, arquivo, ensure_ascii=False, indent=4)

bancoDados = lendo_documento_()


while True:

    print('''
                FINACE PERSONAL

            (1) - ADICIONAR RECEITAS
            (2) - ADICIONAR DESPESAS
            (3) - VER HISTÓRICO 
            (4) - EXCLUIR HISTÓRICO 
            (5) - VER SALDO
            (0) - SAIR
    ''')

    try:

        menu = int(input("Escolha opção:"))

    except:

        print("Informe opção válida!")

    else:

        match menu:

            case 1:
                #RECEITA

                tipoReceita = input("Informe tipo da receita: ")
                valor = float(input("Informe valor (R$): "))

                receita = {
                    "tipo": tipoReceita,
                    "valor": valor,
                    "data":date.today().strftime("%d/%m/%Y")
                }

                adicionando_itens_no_arquivo("receitas", receita,bancoDados)

            case 2:
                #DESPESAS

                tipoDespesa = input("Informe tipo despesa: ")
                valor = float(input("Informe valor despesa: "))
                
                despesa = {
                    "tipo": tipoDespesa,
                    "valor": valor,
                    "data":date.today().strftime("%d/%m/%Y")
                }

                
  
                adicionando_itens_no_arquivo("despesas",despesa,bancoDados)



            case 3:
                #VER HISTÓRICO

                print(''' 
            BUSCAR HISTÓRICO

            (1) - RECEITAS
            (2) - DESPESAS 
            (3) - TODOS
                ''')
                menu = int(input("Opção menu: "))

                match menu:

                    case 1:
                        #RECEITAS
                        print(''' 
            BUSCAR HISTÓRICO

            (1) - POR DIA
            (2) - POR MÊS
            (3) - POR ANO
            (4) - TIPO
                        ''')
                        menu = int(input("Opção menu: "))

                    case 2:
                        #DESPESAS
                        print(''' 
            BUSCAR HISTÓRICO

            (1) - POR DIA
            (2) - POR MÊS
            (3) - POR ANO
            (4) - TIPO
                ''')
                        menu = int(input("Opção menu: "))
                    
                    case 3:
                        #TODOS

                        print(''' 
            BUSCAR HISTÓRICO

            (1) - POR DIA
            (2) - POR MÊS
            (3) - POR ANO
            (4) - TIPO
                        ''')
                        menu = int(input("Opção menu: "))

                

            case 4:
                #EXCLUIR HISTÓRICO
                
                excluir_lista("despesas","receitas", bancoDados)
                print("\t(Histórico apagado!)")

            case 5:
                #VER SALDO
                
                receita = 0
                despesa = 0

                for tipo, itens in bancoDados.items():
                    for item in itens:
                        if tipo == "receitas":
                            receita += item['valor']
                        else:
                            despesa += item['valor']


                print(f"\nRECEITAS:\n")

                for tipo, itens in bancoDados.items():

                    for item in itens:
                        if tipo == "receitas":
                            print(f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n")


                print(f"\nDESPESAS:\n")

                for tipo, itens in bancoDados.items():

                    for item in itens:
                        if tipo == "despesas":
                            print(f"  tipo: {item['tipo']} | valor: R${item['valor']:.2f} | data: {item['data']}\n")


                print(f"\nSaldo: R${receita - despesa:.2f}")
                
            case 0:
                #SAIR
                break
            
