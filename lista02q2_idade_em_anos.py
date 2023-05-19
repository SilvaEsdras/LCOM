idade_em_dias = int(input("Qual sua idade?(Em dias)"))

anos = idade_em_dias // 365
meses = (idade_em_dias % 365) // 30
dias = (idade_em_dias % 365) % 30


print(f' Parabéns, Você tem {anos} anos {meses} meses e {dias} dias de vida.')


