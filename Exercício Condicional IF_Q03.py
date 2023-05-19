salario = float(input("Digita aqui o seu salário: "))

if (salario > 1250):
    aumento_superior = salario * 0.10
    salaria_final = salario + aumento_superior
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")

if (salario <= 1250):
    aumento_inferior = salario * 0.15
    salaria_final = salario + aumento_inferior
    #print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")
    
print(f"Se salário era de {salario}, Agora seu salário será R$ {salaria_final}")