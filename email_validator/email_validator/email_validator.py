import argparse
import re
import socket


# --- Логика валидации ---

class EmailValidationError(Exception):
    """Базовый класс для всех ошибок, связанных с валидацией email."""
    pass

class InvalidEmailFormatError(EmailValidationError):
    """Ошибка, если формат email не соответствует шаблону."""
    pass

class DomainNotFoundError(EmailValidationError):
    """Ошибка, если домен из email не найден в DNS."""
    pass

class EmailValidator:
    """
    Класс для валидации email-адресов.
    """
    _EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    @classmethod
    def validate_format(cls, email: str) -> None:
        """
        Проверяет формат email.
        Вызывает InvalidEmailFormatError, если формат неверный.
        """
        if not re.match(cls._EMAIL_REGEX, email):
            raise InvalidEmailFormatError(f"Неверный формат email: {email}")

    @classmethod
    def check_domain_exists(cls, email: str, timeout: int = 5) -> None:
        """
        Проверяет существование домена из email через DNS-запрос.
        Вызывает DomainNotFoundError, если домен не найден.
        """
        try:
            domain = email.split('@')[1]
            socket.setdefaulttimeout(timeout)
            socket.gethostbyname(domain)
        except (socket.gaierror, IndexError):
            raise DomainNotFoundError(f"Домен для email '{email}' не найден или недоступен.")
        except socket.timeout:
            raise DomainNotFoundError(f"Превышено время ожидания ответа от DNS-сервера для домена.")

    @classmethod
    def validate(cls, email: str, check_domain: bool = True) -> bool:
        """
        Полная валидация email.

        Args:
            email: Строка с email-адресом.
            check_domain: Флаг для проверки существования домена.

        Returns:
            True, если валидация прошла успешно.

        Raises:
            InvalidEmailFormatError: Если формат неверный.
            DomainNotFoundError: Если домен не найден и check_domain=True.
        """
        cls.validate_format(email)
        if check_domain:
            cls.check_domain_exists(email)
        return True

# --- Интерфейс командной строки (CLI) с циклом ---

def main() -> None:
    """
    Точка входа консольного приложения с интерактивным циклом.
    """
    parser = argparse.ArgumentParser(
        description='Интерактивный валидатор email-адресов.'
    )
    parser.add_argument(
        '--no-domain-check',
        action='store_true',
        help='Отключить проверку существования домена.'
    )

    args = parser.parse_args()

    print("-- Валидатор email --")
    print("Введите 'q' или 'quit' для выхода.\n")

    while True:
        try:
            user_input = input("Введите email-адрес для валидации: ").strip()

            # Условие выхода из цикла
            if user_input.lower() in ('q', 'quit'):
                print("Выход из программы. До свидания!")
                break

            if not user_input:
                print("Пожалуйста, введите адрес.")
                continue

            # Выполняем валидацию
            EmailValidator.validate(
                email=user_input,
                check_domain=not args.no_domain_check
            )

            # Если валидация прошла без ошибок
            print(f"✅ Email-адрес '{user_input}' является валидным.\n")

        except EmailValidationError as e:
            # Обработка всех ошибок валидации
            print(f"❌ Ошибка валидации: {e}\n")

if __name__ == '__main__':
    main()