# CheckGen

файл task.py генерация pdf файлов 



файл views.py 
Функция создания чека create_check(request) 
request == {"point_id": Число(целое),
            "order_id": Число(целое)}
Возвращает струтктуру

функция получения всех чеков(у которых статус не "printed") unprinted_check(request)
request == {"printer_api": Число(целое)}
Возвращает струтктуру чеков

функция печатает чеки printed_check(request)
request == {"printer_api": Число(целое),
            "order_id": Число(целое)}
Возвращает путь к файлу чека
