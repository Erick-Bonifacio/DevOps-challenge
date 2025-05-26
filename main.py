from controllers.processing_controller import ProcessingController
from time import time
from colorama import init, Fore, Style, Back
init(autoreset=True)

def menu():
    print("===== ETL DE RATEIO DE CUSTOS =====")
    print("1 - Iniciar processo de transformação")
    print("2 - Discutir resultados com o agente")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def main():
    while True:
        escolha = menu()

        if escolha == '1':
            controller = ProcessingController()
            start = time()
            success, path = controller.run()
            end = time()
            if success:
                print()
                print(Style.BRIGHT + Back.GREEN + f"Sucesso! Relatório salvo em: {path}")
                print(Style.BRIGHT + Fore.GREEN + f"Tempo total de execução: {(end - start):.2f}")
                print()
            else:
                print("Erro: Falha ao gerar relatório.")
        
        elif escolha == '2':
            controller = ProcessingController()
            resposta, path = controller.run()
            print("\n===== RESPOSTA DO AGENTE =====")
            print(resposta)
        
        elif escolha == '0':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()