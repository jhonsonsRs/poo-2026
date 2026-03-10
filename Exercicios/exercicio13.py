def total_invoicing(list):
    sum = 0
    for i in list:
        sum += i
    return sum

def day_higher_invoicing(list):
    value = 0
    for i in list:
        if i > value:
            value = i
    return value

week_days = []
for i in range(0, 7):
    value_invoiced = float(input(f"Digite o valor faturado no dia {i+1}"))
    while(value_invoiced < 0):
        print("Valor inválido!")
        value_invoiced = float(input(f"Digite o valor faturado no dia {i+1}"))
    week_days.append(value_invoiced)
total = total_invoicing(week_days)
media = total / 7
bigger_value = day_higher_invoicing(week_days)
print(f"Valor total faturado: {total}")
print(f"Média diária: {media}")
print(f"Maior valor faturado: {bigger_value}")