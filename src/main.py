import requests

money = int(input("""
USD to ???
1. UZS
2. RUB
3. TRY
4. EUR
\nSelect: """))

match money:
    case 1:
        money = "UZS"
    case 2:
        money = "RUB"
    case 3:
        money = "TRY"
    case 4:
        money = "EUR"


value = int(input("\nValue: "))

def get_exchange_rate(api_key, base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"]

def convert_currency(amount, rate_from, rate_to):
    return amount * (rate_to / rate_from)

rates = get_exchange_rate(api_key="b1413fd51e124e848f9e5ccfe509d79d")
user_money = convert_currency(value, rates["USD"], rates[money])

formatted_amount = f"{user_money:,}".replace(",", " ")
print(f"{value} USD = {formatted_amount} {money}")