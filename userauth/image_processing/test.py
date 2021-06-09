from card import detect_card, search_pesel

card=detect_card("3.jpg")
print(len(search_pesel(card)))
