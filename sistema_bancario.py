print("Bem vindo ao Cash Bank🪙")

saldo = 150
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
SAQUE_MAXIMO = 500

# Menu de opções para o usuário
menu = """
================== MENU =====================

Por gentileza, escolha uma das opções abaixo:

[1] Depositar💰
[2] Sacar🤑
[3] Extrato📊
[4] Sair❌
=> """

while True:
    
    opcao = input(menu)

    # --- Opção de Depósito ---
    if opcao == "1":
        print("---------- Depósito💰 ----------")
        try:
            valor = float(input("Informe o valor do depósito: R$ "))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("❌ Operação falhou! O valor informado é inválido.")
        except ValueError:
            print("❌ Operação falhou! Por favor, insira um número válido.")

    # --- Opção de Saque ---
    elif opcao == "2":
        print("----------- Saque🤑 ------------")
        if numero_saques >= LIMITE_SAQUES:
            print("❌ Operação falhou! Número máximo de saques excedido.")
        else:
            try:
                valor = float(input("Informe o valor do saque: R$ "))

                excedeu_saldo = valor > saldo
                excedeu_limite = valor > SAQUE_MAXIMO

                if excedeu_saldo:
                    print(f"❌ Operação falhou! Você não tem saldo suficiente. Saldo atual: R$ {saldo:.2f}")
                elif excedeu_limite:
                    print(f"❌ Operação falhou! O valor do saque excede o limite de R$ {SAQUE_MAXIMO:.2f} por operação. Se quiser aumentar seu limite de saque baixe o app Cash Bank, lá você consegue ajustar seu limite com agilidade. Caso preferir vá até uma agência e fale com nosso time.")
                elif valor > 0:
                    saldo -= valor
                    extrato += f"Saque:    R$ {valor:.2f}\n"
                    numero_saques += 1
                    print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("❌ Operação falhou! O valor informado é inválido.")
            except ValueError:
                print("❌ Operação falhou! Por favor, insira um número válido.")


    # --- Opção de Extrato ---
    elif opcao == "3":
        print("\n================= EXTRATO📊 ==================")
        # Verifica se houve movimentações
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        print("=============================================")

    # --- Opção de Sair ---
    elif opcao == "4":
        print("✅ Obrigado por ser cliente Cash Bank!😍")
        break

    # --- Opção Inválida ---
    else:
        print("❌ Operação inválida, por favor selecione novamente a operação desejada.")
