import requests
from bs4 import BeautifulSoup
from time import sleep


def send_request(id):
    headers = {
        "User-Agent": "Opera/9.71 (X11; Linux i686; en-US) Presto/2.8.161 Version/12.00"
    }
    r = requests.get(f'https://www.dicio.com.br/palavras-mais-buscadas/{id}/', headers=headers)
    return (r.content).decode('utf-8')

def sort_alphabetical_order(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    lines.sort()

    with open(filename, "w") as file:
        file.writelines(lines)    
    print(f"Feito, um total de {len(lines)} palavras foram extraídas")

def prepare_list(list):
    new_list = []
    for item in list:
        if " " in item:
            for i in item.split(" "):
                new_list.append(i)
                print(i)
        else:
            new_list.append(item)
            print(item)
    return new_list

def write_file(words):
    words = prepare_list(words)
    with open('words.txt', 'a+') as file:
        file.writelines("\n".join(words))
        file.write("\n")

def extract_values(html):
    soup = BeautifulSoup(html, 'html.parser')
    words_list = soup.find("ul", {"class":"list"})
    tags = words_list.find_all("a")

    if(len(tags) < 1): return "done"
    words = []                  # Algumas palavras ficam com um espaço no final
    for tag in tags:            # Vai remover o último caracter da palavras
        if tag.text[-1] == ' ': # se ele for um espaço (" ")
            words.append(tag.text[0:-1])
        else:
            words.append(tag.text)
    
    return words


def start_loop(delay, total):
    count = 1
    while True:
        request_data = send_request(count)
        if not request_data: return

        words = extract_values(request_data)
        if words == "done": break

        write_file(words)
        if count == total: break
        sleep(delay)
        count+=1
    sort_alphabetical_order("words.txt")

if __name__ == '__main__':
    start_loop(delay=1, total=999999)