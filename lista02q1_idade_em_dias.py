anos = int(input("Qual é sua idade?(Em anos): "))
meses = int(input("Qual é sua idade?(Em meses): "))
dias = int(input("Qual é sua idade?(Em dias): "))

idade_em_dias = anos * 365 + meses * 30 + dias

print(f' Parabéns, Você tem {idade_em_dias} dias de vida.')