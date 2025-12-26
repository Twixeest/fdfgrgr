[app]

# Название приложения
title = Telegram Clone
package.name = telegramclone
package.domain = org.telegram

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Версия
version = 1.0
requirements = python3,kivy

# Разрешения Android
android.permissions = INTERNET

# Настройки Android
android.api = 34
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.arch = arm64-v8a

# Ориентация
orientation = portrait

# Полный экран
fullscreen = 0

# Иконка
icon.filename = %(source.dir)s/icon.png

# Лого запуска
presplash.filename = %(source.dir)s/presplash.png
