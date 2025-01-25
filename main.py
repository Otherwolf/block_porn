import os
import shutil
import platform
import ctypes


def is_admin():
    """Проверяет, запущен ли скрипт с правами администратора."""
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0


def backup_and_replace(system_path, local_path):
    """Резервное копирование и замена файла."""
    # Проверяем наличие локального файла
    if not os.path.exists(local_path):
        print(f"Локальный файл {local_path} не найден!")
        return False

    # Создаем резервную копию системного файла
    backup_path = f"{system_path}.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(system_path, backup_path)
        print(f"Резервная копия создана: {backup_path}")
    else:
        print("Резервная копия уже существует.")

    # Заменяем системный файл
    shutil.copy2(local_path, system_path)
    print(f"Файл {system_path} был заменён.")
    return True


def protect_file(path):
    """Устанавливает атрибуты защиты от изменений и удаления."""
    if platform.system() == "Windows":
        os.system(f"attrib +R +S +H {path}")
    elif platform.system() == "Linux":
        if shutil.which("chattr"):
            os.system(f"chattr +i {path}")
        else:
            print("Команда 'chattr' не найдена. Установите утилиту 'e2fsprogs', чтобы использовать эту функцию.")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"chmod 444 {path}")
        os.system(f"chflags schg {path}")
    else:
        print(f"Операционная система {platform.system()} не поддерживает защиту файлов.")
    print(f"Файл {path} защищён от изменений и удаления.")


def main():
    # Определяем путь к файлу hosts в зависимости от ОС
    system = platform.system()
    if system == "Windows":
        system_hosts = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    elif system in ["Linux", "Darwin"]:  # Darwin — это macOS
        system_hosts = "/etc/hosts"
    else:
        print(f"Операционная система {system} не поддерживается.")
        return

    local_hosts = "./hosts"  # Файл hosts в текущей директории

    # Проверяем права администратора
    if not is_admin():
        print("Скрипт должен быть запущен с правами администратора!")
        return

    # Подменяем файл и защищаем его
    if backup_and_replace(system_hosts, local_hosts):
        protect_file(system_hosts)
        print("Операция завершена успешно!")


if __name__ == "__main__":
    main()
