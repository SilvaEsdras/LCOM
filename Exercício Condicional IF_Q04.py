salario_bruto = float(input("Digita aqui o seu salário: "))

if (salario_bruto < 1000):
    imposto_de_renda = salario_bruto * 0.00
    inss = salario_bruto * 0.00
    salario_liquido = salario_bruto - imposto_de_renda - inss
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")

if (salario_bruto >= 1000 and salario_bruto < 2000):
    imposto_de_renda = salario_bruto * 0.10
    inss = salario_bruto * 0.11
    salario_liquido = salario_bruto - imposto_de_renda - inss
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")

if (salario_bruto > 2000 and salario_bruto <= 3000):
    imposto_de_renda = salario_bruto * 0.20
    inss = salario_bruto * 0.15
    salario_liquido = salario_bruto - imposto_de_renda - inss
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")
    
if (salario_bruto > 3000):
    imposto_de_renda = salario_bruto * 0.20
    inss = salario_bruto * 0.15
    salario_liquido = salario_bruto - imposto_de_renda - inss
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")

print(f"Se salário é {salario_bruto}, Com os impostos agora seu salário será R$ {salario_liquido}")