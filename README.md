# inobi-sizer

**inobi-sizer** - это API для основной функциональности

**Stack**:
1. language - python (version 3.7)
2. framework - django (version 2.1.3)
3. Database - PostgreSQL (version 10)


# Для разработчиков
 - Тестов и Свагера пока нету

# Описание роутов
 - /sizer/photos/ POST Добавить фотографию
 - /sizer/photos/<photo_id>/ GET получить url на фотографию (два параметра width height)
 - /sizer/photos/<photo_id>/download/ GET скачать файл (два параметра width height)
 - /sizer/photos/<photo_id>/download/ GET скачать zip файл 9 штук (два параметра width height)