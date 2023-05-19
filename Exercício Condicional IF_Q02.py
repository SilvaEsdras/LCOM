velocidade_do_carro = int(input("Digita a velocidade do carro: "))

if velocidade_do_carro <= 80:
    print(f"Sua velocidade foi de: {velocidade_do_carro}")
    print(f"Escapou da Multa :)")

if velocidade_do_carro > 80:
    valor_multa = (velocidade_do_carro - 80) * 10.00
    print(f"Você foi multado! Em R$ {valor_multa} Sua velocidade foi de: {velocidade_do_carro}")
    print("Agora é pagar :)")
