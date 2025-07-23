import json
import os
from collections import Counter
import re
from errors import StorageError
import traceback

ARTICLES_DIR = "articles"
INDEX_FILE = "articles\\index.json"

KEYWORDS_NUM = 3

class Storage:
    def __init__(self):
        """
        Initialize Storage object instance.
        
        - Load articles metadata
        """
        self.articles_data: list = self.load_articles()
        self.gen_id = self.id_generator()


    def load_articles(self) -> dict:
        """Loads all articles metadata from index.json."""
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'r') as index_h:
                return json.load(index_h)
            
        # Create file if does not exist
        with open(INDEX_FILE, 'w') as index_h:
            json.dump([], index_h)
            return []
        
    def get_articles(self) -> list:
        """Returns list of all articles titles and their IDs."""
        return [(article['title'], article['id']) for article in self.articles_data]
        
    def get_article_data(self, article_id) -> dict:
        """Returns an article's metadata by ID."""
        for article in self.articles_data:
            if article['id'] == article_id:
                return article
        return False

    def create_article(self, data: dict) -> None:
        """
        Add arcticle metadata to index file & Save content.

        `data` should include:
        - title
        - content
        - tags
        """
        # Get next article ID
        art_id: str = next(self.gen_id)
        
        art_content = data.get("content", "")

        # Create & save article metadata in index file
        art_metadata = {
            "id": art_id,
            "title": data.get("title", "N/A"),
            "tags": data.get("tags", []),
            "keywords": self.find_keywords(art_content, KEYWORDS_NUM),
            "content_length": len(art_content),
            "directory": f"/{ARTICLES_DIR}/{art_id}"
        }

        try:
            # Update metadata
            self.articles_data.append(art_metadata)
            
            # Create article directory & file
            os.mkdir(f"{ARTICLES_DIR}\\{art_id}")

            with open(f"{ARTICLES_DIR}\\{art_id}\\content.txt", 'w') as content_h:
                content_h.write(art_content)

        except Exception as e:
            # raise StorageError("Failed to create article.") from e
            print(traceback.format_exc())
        

    def find_keywords(self, content: str, n: int) -> list[str]:
        """Finds the n most frequent words in an article content."""

        # Stopwords to ignore
        stopwords = {'a', 'an', 'the', 'and', 'is', 'are', 'was', 'will', 'in', 'to', 'on', 'for', 'with', 'this', 'that', 'it', 'of', 'by', 'at'}

        # Remove non-alphanumeric characters (except spaces) and split into words
        words = [word for word in re.findall(r'\b\w+\b', content.lower()) if word not in stopwords]
        # Count the frequency of each word
        word_counts = Counter(words)

        # Get the n most common words
        return [word for word, _ in word_counts.most_common(n)]
    
    def edit_article(self, data: dict) -> None:
        """
        Edit an existing article.

        `data` should include:
        - id
        - title
        - content
        - tags
        """
        
        article_id = data.get("id")
        art_content = data.get("content", "")

        # Update metadata
        article = self.get_article_data(article_id)
        article['title'] = data.get("title", "")
        article['tags'] = data.get("tags", [])
        article['keywords'] = self.find_keywords(art_content, KEYWORDS_NUM)
        article['content_length'] = len(art_content)

        try:
            with open(f"{ARTICLES_DIR}\\{article_id}\\content.txt", 'w') as content_h:
                content_h.write(art_content)
        except Exception as e:
            raise StorageError("Failed to create article.") from e

    def get_article_content(self, article_id) -> None:
        """Fetch article content from storage by ID."""
        try:
            with open(f"{ARTICLES_DIR}\\{article_id}\\content.txt", 'r') as content_h:
                return content_h.read()
        except Exception as e:
            raise StorageError(f"Failed to fetch article {article_id} content.") from e
    
    def del_article(self, article_id) -> None:
        """Delete an article from system."""

        # Remove article metadata from index
        article = self.get_article_data(article_id)
        self.articles_data.remove(article)
        
        # Delete article content from storage
        try:
            os.remove(f"{ARTICLES_DIR}\\{article_id}\\content.txt")
            os.rmdir(f"{ARTICLES_DIR}\\{article_id}")
        except Exception as e:
            raise StorageError(f"Failed to delete article {article_id} content.") from e

    def search(self, word):
        """Search for article by keyword or tag."""
        
        result = []

        for article in self.articles_data:
            if word in article['tags'] or word in article['keywords']:
                result.append((article['title'], article['id']))
        
        return result

    
    def id_generator(self):
        """Article ID generator."""

        curr_id: str = f'A{len(self.articles_data) + 1}'

        while True:
            yield curr_id

            # Increment number
            curr_id = curr_id[:1] + str(int(curr_id[1:]) + 1)

    def close(self):
        with open(INDEX_FILE, 'w') as index_h:
            json.dump(self.articles_data, index_h)