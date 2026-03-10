week_days = []
for i in range(0, 7):
    value_invoiced = float(input(f"Digite o valor faturado no dia {i+1}"))
    while(value_invoiced < 0):
        print("Valor inválido!")
        value_invoiced = float(input(f"Digite o valor faturado no dia {i+1}"))