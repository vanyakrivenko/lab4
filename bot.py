import telebot
import requests
from bs4 import BeautifulSoup
bot = telebot.TeleBot("7251817952:AAFF-EjpzHSuktw6li_5PcMzgfHvt2yLc7o")
NEWS_URL= "https://ria.ru/"

def fetch_latest_news():
  try:
    response = requests.get(NEWS_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = []
    for item in soup.find_all('a', class_ = "cell-list__item-link")[:5]:
      title = item.get_text(strip = True)
      link = item['href']
      headlines.append(f"[{title}]({link})")
    return headlines
  except Exception as e:
    return["Ошибка получения новостей: " + str(e)]

def search_news(topic):
  try:
    search_url = f"{NEWS_URL}search/?query={topic.replace(' ', '+')}"
    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('a', class_ = "list-item__title")[:5]:
      title = item.get_text(strip = True)
      link = item['href']
      results.append(f"[{title}]({link})")

    return results if results else ["Новости по вашей теме не найдены."]

  except Exception as e:
    return ["Ошибка поиска новостей: " + str(e)]


@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
  bot.reply_to(
    message,
      """Привет! Я новостной бот для российских пользователей. Вот, что я умею:
        /latest - Получить последние новости.
        /search <тема> - Найти новости по теме.

        Напиши /help для просмотра команд!""",
  )
@bot.message_handler(commands =['latest'])
def send_latest_news(message):
  news=fetch_latest_news()
  response = "\n\n".join(news)
  bot.reply_to(message, response, parse_mode = 'Markdown')


@bot.message_handler(commands=['search'])
def send_search_results(message):
  topic = message.text.replace('/search', '').strip()
  if topic:
    news = search_news(topic)
    response = "\n\n".join(news)
  else:
    response = "Пожалуйста, укажите тему для поиска! Например: /search технологии"
  bot.reply_to(message, response, parse_mode = 'Markdown')


@bot.message_handler(func = lambda message: True)
def handle_all_messages(message):
  bot.reply_to(
    message,
      "Я вас не понял. Напишите /help. Чтобы узнат, что я умею!",
  )


if __name__ == "__main__":
  print("Бот запущен...")
  bot.infinity_polling()
