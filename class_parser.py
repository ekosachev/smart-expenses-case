from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from urllib.parse import urljoin

class Database:
    def __init__(self, db_name='ppr_support.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT NOT NULL UNIQUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS qa_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    link TEXT,
                    FOREIGN KEY (article_id) REFERENCES articles (id)
                )
            ''')
            conn.commit()
    
    def save_article(self, title, content, url):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (title, content, url) 
                VALUES (?, ?, ?)
            ''', (title, content, url))
            conn.commit()
            return cursor.lastrowid
            
    def save_qa_pair(self, article_id, question, answer, link=None):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO qa_pairs 
                (article_id, question, answer, link) 
                VALUES (?, ?, ?, ?)
            ''', (article_id, question, answer, link))
            conn.commit()

class Parser:
    def __init__(self, base_url, db):
        self.base_url = base_url
        self.db = db
        self.session = requests.Session()
        self.visited_urls = set()
    
    def get_page(self, url):
        try:
            response = self.session.get(url)
            return BeautifulSoup(response.text, 'html.parser'), response.text
        except:
            return None, None
    
    def save_main_page_html(self):
        _, html_content = self.get_page(self.base_url)
        if html_content:
            with open('main_page.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        return False
    
    def parse_article(self, url):
        if url in self.visited_urls:
            return None
            
        self.visited_urls.add(url)
        soup, _ = self.get_page(url)
        if not soup:
            return None
        
        title = soup.find('div', class_='menu-item__link-label')
        title = title.text.strip() if title else ''
        
        content = soup.find('div', class_='article-content')
        content = content.text.strip() if content else ''
        
        return {
            'title': title,
            'content': content,
            'url': url
        }
    
    def parse_site(self):
        total_articles = 0
        self.save_main_page_html()
        
        main_page, _ = self.get_page(self.base_url)
        if not main_page:
            return 0
        
        article_links = main_page.find_all('a', attrs={
            'data-v-2cbd6786': True,
            'class': lambda x: x and ('menu-item__link' in x or 'router-link-active' in x)
        })
        
        print(f"Найдено ссылок: {len(article_links)}")
        
        for link in article_links:
            article_url = urljoin(self.base_url, link.get('href', ''))
            print(f"Обработка ссылки: {article_url}")
            
            article_data = self.parse_article(article_url)
            
            if article_data:
                self.db.save_article(
                    title=article_data['title'],
                    content=article_data['content'],
                    url=article_data['url']
                )
                total_articles += 1
            
            time.sleep(0.1)
        
        return total_articles

    def parse_qa_from_article(self, url):
        soup, _ = self.get_page(url)
        if not soup:
            return None
            
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM articles WHERE url = ?', (url,))
            result = cursor.fetchone()
            if not result:
                return None
            article_id = result[0]
            
        article_cards = soup.find_all('div', class_='article__card')
        
        qa_pairs = []
        for card in article_cards:
            question_elem = card.find('h2', class_='article__card-title')
            if not question_elem:
                continue
            question = question_elem.text.strip()
            
            answer_block = card.find_all('p')
            answer_text = []
            link = None
            
            for p in answer_block:
                a_tag = p.find('a')
                if a_tag and a_tag.get('href'):
                    link = a_tag.get('href')
                answer_text.append(p.text.strip())
            
            answer = ' '.join([text for text in answer_text if text])
            
            if question and answer:
                self.db.save_qa_pair(article_id, question, answer, link)
                qa_pairs.append((question, answer, link))
                
        return qa_pairs

    def parse_qa_for_all_articles(self):
        with sqlite3.connect(self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT url FROM articles')
            urls = cursor.fetchall()
            
        total_qa_pairs = 0
        for (url,) in urls:
            qa_pairs = self.parse_qa_from_article(url)
            if qa_pairs:
                total_qa_pairs += len(qa_pairs)
                print(f"Обработана статья: {url}")
                for q, a, l in qa_pairs:
                    print(f"Вопрос: {q}")
                    print(f"Ответ: {a}")
                    if l:
                        print(f"Ссылка: {l}")
                    print("-" * 50)
            time.sleep(0.1)
            
        return total_qa_pairs

def main():
    try:
        db = Database()
        parser = Parser(base_url='https://support.petrolplus.ru', db=db)
        
        # Парсим статьи
        print("Начинаем парсинг статей...")
        parser.parse_site()
        
        # Парсим вопросы и ответы
        print("\nНачинаем парсинг вопросов и ответов...")
        total = parser.parse_qa_for_all_articles()
        print(f"\nОбработано пар вопрос-ответ: {total}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main() 