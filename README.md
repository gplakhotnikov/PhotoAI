# PhotoAI by Grigory Plakhotnikov

PhotoAI - это выполненная в виде web-приложения фотостудия, позволяющая применять различные фильтры и эффекты к изображениям. Вы можете убирать цифровой шум, применять цветокоррекцию, делать скетчи, и т.д. Приложение написано в качестве финального проекта для курса Гарвардского университета CS50x. Оно попало в Галерею проектов на официальном сайте учебного заседения (https://cs50.harvard.edu/x/2021/gallery/).

PhotoAI is an online photo studio that allows you to apply different filters and effects to photos. You can reduce digital noise, make cool sketches, use color correction, etc. This web-application was developed as a final project for CS50x course by Harvard University. It fas featured in the Gallery of Projects on Harvard's official website (https://cs50.harvard.edu/x/2021/gallery/)

## Видеопрезентация / Video Presentation
https://www.youtube.com/watch?v=URMg17wQxJI

## Особенности / Features

- Загрузка JPEG файлов из Интернета или вашего компьютера
- Эффекты: создание скетчей, удаление цифрового шума, цветокоррекция
- Фильтры: блюр, выделение контура, детализирование, усиление контуров, тиснение, выделение краев, усиление резкости, смягчение
- Контактная форма для связи с администрацией
- Панель администратора для управления отзывами
----------
- Upload JPEG images from the web or your computer
- Effects: make a sketch, delete digital noise, color correction
- Filters: Blur, Contour, Detail, Edge Enhance, Emboss, Find Edges, Sharpen, Smooth
- Contact form to contact the administrator
- Admin Dashboard to manage the messages/feedback

## Стек технологий / Tech

- [Flask](https://flask.palletsprojects.com/) - a micro web framework written in Python
- [Flask-Session](https://flask-session.readthedocs.io/) - an extension for Flask that adds support for Server-side Session to the application
- [ImageIO](https://imageio.readthedocs.io) - a Python library that provides an easy interface to read and write a wide range of image data, including animated images, volumetric data, etc.
- [Pillow (PIL Fork)](https://pillow.readthedocs.io/) - a Python library library that adds support for opening, manipulating, and saving many different image file formats
- [SQLite](https://www.sqlite.org/) - a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine
- HTML, Bootstrap, CSS, Java Script, Python.

## Как запустить проект / Installation

Установите зависимости из файла requirements.txt и запустите Flask-сервер командой flask run. Перейдите по появившейся ссылке.
```sh
pip3 install -r requirements.txt
flask run
```
Install the dependencies from requirements.txt and start the Flask by typing flask run in the console. Click the link.