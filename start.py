"""
Запускает веб-приложение Flask в режиме разработки.

Этот скрипт инициализирует и запускает веб-сервер Flask, используя настройки
конфигурации, определённые в экземпляре приложения Flask. Включение режима отладки
позволяет автоматически перезагружать приложение при изменениях в коде и предоставляет
доступ к интерактивному отладчику при возникновении исключений.

Использование:
    Запуск из командной строки как основной программы:
    ```
    $ python start.py
    ```

Предупреждение:
    Режим отладки должен быть выключен при развертывании приложения в продакшн.
"""

from application import app

# if __name__ == "__main__":
#     app.run(debug=True)

# for docker
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
