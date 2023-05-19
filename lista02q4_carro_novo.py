custo_de_fabrica = float(input("Preço do carro sem imposto: "))
porcentagem_do_distribuidor = custo_de_fabrica * 0.28
imposto_da_fabrica = custo_de_fabrica * 0.45

custo_ao_consumidor = custo_de_fabrica + porcentagem_do_distribuidor + imposto_da_fabrica

print(f'O preço do carro novo é: {custo_ao_consumidor}')

