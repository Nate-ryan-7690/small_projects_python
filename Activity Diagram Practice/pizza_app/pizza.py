# Pizza order - Aktivitaetsdiagramm Uebung

size_prices = {
    "small":  {"price":  8.00, "factor": 1.0},
    "medium": {"price": 10.00, "factor": 1.4},
    "large":  {"price": 12.00, "factor": 1.8},
}

toppings = {
    "salami":       1.20,
    "ham":          1.20,
    "mushrooms":    1.00,
    "bell pepper":  0.90,
    "onions":       0.70,
    "olives":       1.00,
    "corn":         0.70,
    "pineapple":    1.00,
    "tuna":         1.80,
    "anchovies":    1.80,
    "arugula":      1.20,
    "mozzarella":   2.00,
    "gorgonzola":   2.00,
    "chili pepper": 0.70,
    "artichokes":   1.50,
}

sauces = {
    "garlic": 0.80,
    "chili":  0.80,
    "bbq":    1.00,
}

size_by_number = {"1": "small", "2": "medium", "3": "large"}


# --- 1. size ---
size_choice = input("Please choose your pizza size\n1: small\n2: medium\n3: large\n").strip()

while size_choice not in size_by_number:
    size_choice = input("Please enter 1, 2 or 3: ").strip()

size = size_by_number[size_choice]
base_price = size_prices[size]["price"]
factor = size_prices[size]["factor"]

total = base_price
chosen_toppings = []


# --- 2. toppings (loop) ---
topping_menu = ", ".join(toppings)
print("\nAvailable toppings:", topping_menu)

while True:
    choice = input("Choose a topping (or 'done' to finish): ").strip().lower()

    if choice == "done":
        break

    if choice not in toppings:
        print("Unknown topping, please try again.")
        continue

    total += toppings[choice] * factor
    chosen_toppings.append(choice)
    print(f"{choice} added.")


# --- 3. extra sauce (decision) ---
sauce_menu = ", ".join(sauces)
wants_sauce = input(f"\nWould you like an extra sauce? (yes/no) ").strip().lower()

chosen_sauce = None
if wants_sauce in ("yes", "y", "ja", "j"):
    print("Available sauces:", sauce_menu)

    sauce_choice = input("Choose a sauce: ").strip().lower()
    while sauce_choice not in sauces:
        sauce_choice = input("Unknown sauce, please choose again: ").strip().lower()

    total += sauces[sauce_choice] * factor
    chosen_sauce = sauce_choice


# --- 4. total ---
print("\n--- Your order ---")
print(f"Size:     {size} ({base_price:.2f} EUR)")
print(f"Toppings: {', '.join(chosen_toppings) if chosen_toppings else 'none'}")
print(f"Sauce:    {chosen_sauce if chosen_sauce else 'none'}")
print(f"Total:    {total:.2f} EUR")