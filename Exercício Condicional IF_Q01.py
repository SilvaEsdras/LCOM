velocidade_do_carro = int(input("Digita a velocidade do carro: "))
multa = (velocidade_do_carro > 80)

if multa:
    print(f"Você foi multado! {multa} Sua velocidade foi de: {velocidade_do_carro}")
