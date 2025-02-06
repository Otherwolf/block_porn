from urllib.parse import urlparse

# Путь к файлу hosts (обычно требуется запуск от имени администратора)
HOSTS_FILE_PATH = './hosts'

# IP-адрес, который будет ассоциирован с добавленными доменами
IP_ADDRESS = "127.0.0.1"


def extract_domain(url):
    """Извлекает домен из ссылки без схемы и параметров."""
    parsed_url = urlparse(url)
    return parsed_url.netloc or parsed_url.path


def add_to_hosts(domain):
    """Добавляет домен в файл hosts."""
    try:
        # Проверяем, есть ли уже домен в файле
        with open(HOSTS_FILE_PATH, "r") as hosts_file:
            lines = hosts_file.readlines()
            if any(f' {domain}' in line for line in lines):
                print(f"Домен {domain} уже добавлен в файл hosts.")
                return

        # Добавляем домен в файл
        with open(HOSTS_FILE_PATH, "a") as hosts_file:
            hosts_file.write(f"{IP_ADDRESS}     {domain}\n")
        print(f"Домен {domain} успешно добавлен в файл hosts.")
    except PermissionError:
        print("Ошибка: требуется запуск с правами администратора.")
    except Exception as e:
        print(f"Ошибка при добавлении домена в файл hosts: {e}")


def main():
    """Основной цикл ожидания ввода пользователя."""
    print("Введите URL (или 'exit' для выхода):")
    while True:
        url = input("> ").strip()
        if url.lower() == "exit":
            print("Выход из программы.")
            break

        urls = [u.strip() for u in url.split() if u.strip()]
        for url in urls:

            domain = extract_domain(url)
            if domain:
                add_to_hosts(domain)
            else:
                print("Некорректный URL. Попробуйте снова.")
                break


if __name__ == "__main__":
    main()
