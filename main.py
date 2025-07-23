from storage import Storage
import os
import subprocess

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/MacOS
    else:
        os.system('clear')
    

def display_menu():
    print("\nOptions:")
    print('''
    > Enter article number to display
    > Enter keyword or tag to search by
    > Enter 'c' to create an article
    > Enter 'q' to exit
          ''')

def display_list(articles: list[tuple]):

    # Check if list is empty
    if len(articles) == 0:
        print("<No Articles>")
        return

    # Print titles
    print(f"Articles:")
    i = 0
    for article in articles:
        print(f"{i}. {article[0]}")
        i += 1

def display_search_result(results: list[tuple], articles: list[tuple]):
    for article in results:
        print(f"{articles.index(article)}. {article[0]}")

def is_number(s: str):
    try:
        num = int(s)
        return True
    except ValueError:
        return False
    
def display_article(title: str, content: str):
    clear_terminal()
    print(f"\ntitle: {title}\n\ncontent: {content}")
    print("\nEnter 'e' to edit\nEnter 'd' to delete\nOr leave empty to continue")


def edit_article(storage: Storage, article_id: str):
    """Edit an article using the storage interface."""

    # Get updated data from user
    title = input("Enter new title: ").strip()
    content = input("Enter new content: ").strip()
    tags = input("Enter tags (seperated by comma): ").replace(' ', '').split(',')

    # Update article
    storage.edit_article(
        {
            "id": article_id,
            "title": title,
            "content": content,
            "tags": tags
        }
    )

    print("\n[+] Article was successfully edited.\n")
    input()  # Wait for enter


def create_article(storage: Storage):
    """Create an article using the storage interface."""

    # Get data from user
    title = input("Enter article title: ").strip()
    content = input("Enter article content: ").strip()
    tags = input("Enter tags (seperated by comma): ").replace(' ', '').split(',')

    # Create article
    storage.create_article(
        {
            "title": title,
            "content": content,
            "tags": tags
        }
    )

    print("\n[+] Article was created successfully.\n")
    input()  # Wait for enter


def delete_article(storage: Storage, article_id):

    storage.del_article(article_id)

    print("\n[+] Article was deleted successfully.\n")
    input()  # Wait for enter

def main():
    
    # Initialize storage manager
    storage = Storage()

    # Retrieve all articles (titles and IDs)
    articles = storage.get_articles()
    
    
    # Main Loop
    while True:

        clear_terminal()

        # Print titles
        display_list(articles)
        
        display_menu()
        user_choice = input()
        
        while not user_choice:
            clear_terminal()
            display_list(articles)
            display_menu()
            user_choice = input()

        # Parse user input
        if is_number(user_choice):
            article_index = int(user_choice)

            if article_index < len(articles):

                # Fetch and display article content
                article_id = articles[article_index][1]
                content = storage.get_article_content(article_id)
                title = articles[article_index][0]

                display_article(title, content)

                # e - edit, d - delete, empty - continue
                user_input = input()
                if user_input == 'e':
                    edit_article(storage, article_id)

                    # Update articles list
                    articles = storage.get_articles()

                elif user_input == 'd':
                    delete_article(storage, article_id)

                    # Update articles list
                    articles = storage.get_articles()

        elif user_choice == 'c':
            create_article(storage)

            # Update articles list
            articles = storage.get_articles()

        elif user_choice == 'q':
            break

        else:
            # Search by keyword or tag
            search_result = storage.search(user_choice.split()[0])  # Take only first word of input
            print(">>> Search results:\n")
            display_search_result(search_result, articles)
            input()
    

    storage.close()

if __name__ == "__main__":
    main()