## MCA WORKSHOP 26

### code - папка для Ваших скриптов

 - loader_vk.py - скрипт сбора с vk комментариев, каким бы я его написал
   - Ваш токен к vk должен храниться в переменной среды VK_TOKEN_KEY
   - Ключи при запуске скрипта:
     - --resourses, -r - список пабликов для загрузки
     - --request_latency, -rl - ключ использования задержки между запросами к vk
     - --request_latency_period, -rlp - время задержки между запросами
     - --post_count, -pc - количество постов для загрузки
     - --comment_count, -сс - количество комментариев и их ответов для загрузки
     - --data_path, -dp - путь для сохранения файла выгрузки
   - Пример запуска: python3 loader_vk.py -r mudakoff,lentach -rl -pc 10 -cc 1 \
   Скачивание первых десяти постов с группы mudakoff и lentach и загрузка первого комментария под постом и ветки его ответов
   
 ### labeler - папка с файлами разметчика

 Ссылка на блокнот в колабе https://colab.research.google.com/drive/1PQ-YRpEth4c0R88A-N2rcJZ1MXFnah36?usp=sharing#scrollTo=OT9lyxu5skpA


### lesson - папка с блокнотами уроков

 - embeddings - папка с материалами занятия про векторное представление текста
