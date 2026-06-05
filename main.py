from api_client import fetch_prices, search_items, print_prices, analyze_prices

if __name__ == "__main__":

    while True:
        print("Enter 1 to Search for an item price: ")
        print("Enter 2 to exit: ")

        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            search_item = input("Enter the item you want to search for: ")

            location = "Caerleon,Bridgewatch,Martlock,Lymhurst,Thetford,Fort Sterling,Black Market,Brecilien"


            matched_items = search_items(search_item)

            if not matched_items:
                print("No items found matching your search.")
                continue

            else:
                for i, item in enumerate(matched_items):
                    print(f"{i + 1}. {item['name']}")
                user_pick = int(input("Pick A Number..:")) - 1
                item_id = matched_items[user_pick]['id']
                data = fetch_prices(item_id, location)
                print_prices(data)
                analyze_prices(data)

        elif user_choice == '2':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice.Please try again.")