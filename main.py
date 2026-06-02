from api_client import fetch_prices, search_items, print_prices, analyze_prices

if __name__ == "__main__":

    while True:
        print("Enter 1 to Search for an item price: ")
        print("Enter 2 to print prices: ",)
        print("Enter 3 to calculate the best buy and sell prices: ")
        print("Enter 4 to exit: ")

        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            search_item = input("Enter the item you want to search for: ")

            print("Cities Name: Bridgewatch, Caerleon, Lymhurst, Martlock, Thetford, Fort Sterling,Black Market")
            location = input("Enter the location(comma seperated): ")

            matched_items = search_items(search_item)

            if not matched_items:
                print("No items found matching your search.")
                continue

            else:
                for i, item in enumerate(matched_items):
                    print(f"{i + 1}. {item}")
                user_pick = int(input("Pick A Number..:")) - 1
                item_id = matched_items[user_pick].split(": ")[1]
                item_id = item_id.strip()
                data = fetch_prices(item_id, location)
               
        elif user_choice == '2':
            print("===== Price Data =====")
            print_prices(data)
        elif user_choice == '3':
            analyze_prices(data)
        elif user_choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice.Please try again.")