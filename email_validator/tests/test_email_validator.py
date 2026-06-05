from unittest.mock import patch
import socket  # Добавляем этот импорт
import unittest # Добавляем этот импорт

from email_validator.email_validator import (
    EmailValidator,
    InvalidEmailFormatError,
    DomainNotFoundError,
)

class TestEmailValidator(unittest.TestCase):
    def test_validate_format_valid(self):
        # Проверка, что валидный формат не вызывает ошибку
        self.assertIsNone(EmailValidator.validate_format("user@example.com"))

    def test_validate_format_invalid(self):
        # Проверка, что неверный формат вызывает нужное исключение
        with self.assertRaises(InvalidEmailFormatError):
            EmailValidator.validate_format("invalid-email")

    @patch('socket.gethostbyname')
    def test_check_domain_exists_success(self, mock_gethostbyname):
        mock_gethostbyname.return_value = '127.0.0.1'
        # Проверка, что при существующем домене ошибки нет
        self.assertIsNone(EmailValidator.check_domain_exists("user@domain.com"))

    @patch('socket.gethostbyname', side_effect=socket.gaierror)
    def test_check_domain_exists_failure(self, mock_gethostbyname):
        # Проверка, что при несуществующем домене вызывается нужное исключение
        with self.assertRaises(DomainNotFoundError):
            EmailValidator.check_domain_exists("user@nonexistent.tld")

    @patch('email_validator.validator.EmailValidator.validate_format')
    @patch('email_validator.validator.EmailValidator.check_domain_exists')
    def test_validate_full_success(self, mock_check_domain, mock_validate_format):
        # Проверка полного цикла валидации с проверкой домена (по умолчанию)
        self.assertTrue(EmailValidator.validate("user@domain.com"))

    @patch('email_validator.validator.EmailValidator.validate_format')
    @patch('email_validator.validator.EmailValidator.check_domain_exists')
    def test_validate_no_domain_check(self, mock_check_domain, mock_validate_format):
        # Проверка полного цикла валидации БЕЗ проверки домена
        self.assertTrue(EmailValidator.validate("user@domain.com", check_domain=False))