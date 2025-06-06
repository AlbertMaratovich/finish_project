# Task for rostelecom (internship)

UI testing with Selenium+pytest for rostelecom.

Файл с тестами страниц авторизации ростелекома "test_auth_pages.py" лежит в папке tests.
Файл с тестом главной страницы ростелекома "test_rostelecom_base_page.py".

Проверки:

Основные тесты написаны для страницы входа и регистрации, которая открывается при редиректе с ЕЛК Web. Данные тесты практически в неизменном виде можно адаптировать под страницы авторизации каждого сайта из таблицы "Сервисы" спецификации-брифинга.
Также есть тест, который проверяет форматирование страниц входа и наличие/отсутствие вариантов входа в соответствии с сервисом для каждого сервиса указанного в брифинге.
Помимо проверок UI элементов и работы различных ссылок/редиректов также есть тесты для проверки валидирования разных полей системой.

Перед запуском автотестов необходимо:


	установить библиотеки, указанные в файле requirements.txt. (обязательна установка селениум версии 4.6+)
 
	если потребуется многократный запуск автотестов, то нужно изменять данные в переменных
 	random_email (используется для регистрации), а также может потребоваться изменение valid_email (используется для входа в аккаунт) в конфиге.
	
	сервисы ростелекома работают только из РБ и РФ. (Для других локаций поребуется VPN для запуска)
	
Для запуска:
Файлы с тестами можно запускать просто кнопкой run в IDE.
