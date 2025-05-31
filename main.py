from controllers.processing_controller import ProcessingController
from controllers.discussing_controller import DiscussingController
from time import time
from colorama import init, Fore, Style, Back
init(autoreset=True)

def menu():
    print("===== ETL DE RATEIO DE CUSTOS =====")
    print("1 - Iniciar processo de transformação")
    print("2 - Discutir resultados com o agente")
    print("Qualquer tecla pra sair")
    return input("Escolha uma opção:\n> ")

def main():
    while True:
        escolha = menu()

        if escolha == '1':
            processador_dados = ProcessingController()
            max_tentativas = 3
            tentativas = 0
            success = False

            while tentativas < max_tentativas:
                try:
                    start = time()
                    success, path = processador_dados.run()
                    end = time()
                    break
                except Exception as e:
                    print('Ocorreu um erro na execução:', e)
                    tentativas+=1
                    if tentativas == max_tentativas:
                        print('Número máximo de tentativas atingido!')

            if success:
                print()
                print(Style.BRIGHT + Back.GREEN + f"Sucesso! Relatório salvo em: {path}")
                print(Style.BRIGHT + Fore.GREEN + f"Tempo total de execução: {(end - start):.2f}")
                print()
            else:
                print("Falha ao gerar relatório.")
        
        elif escolha == '2':
            discussor_dados = DiscussingController()
            discussor_dados.run()    
        
        else:
            print("Saindo...")
            break

if __name__ == "__main__":
    main()