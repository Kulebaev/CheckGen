# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from .models import Check, Printer
from .task import generate_client_check_pdf_async, generate_kitchen_check_pdf_async

KITCHEN = 'kitchen'
CLIENT = 'client'


@csrf_exempt
def create_check(request):

    if request.method != 'POST':
        return JsonResponse({'message': 'Ожидается метод Post'}, status=404)
    
    data = json.loads(request.body)

    point_id = data.get('point_id')

    # Получаем ID заказа из запроса (здесь предполагается, что ID заказа передается в запросе)
    order_id = data.get('order_id')

    try:
        # Фильтруем принтеры для данной точки и типа (кухня и клиент)
        printer_obj_kitchen = Printer.objects.filter(point_id=point_id, check_type=KITCHEN)
        printer_obj_client = Printer.objects.filter(point_id=point_id, check_type=CLIENT)
    except Printer.DoesNotExist:
        return JsonResponse({'message': f'нет принтера на такой точке {point_id}'}, status=400)

    # Проверяем, существуют ли уже чеки для клиента и кухни для данного заказа и принтеров
    for printer in printer_obj_kitchen:
        try:
            kitchen_check = Check.objects.get(order_id=order_id, printer=printer, type=KITCHEN)
        except Check.DoesNotExist:
            kitchen_check = Check.objects.create(order_id=order_id, printer=printer, type=KITCHEN,  order=data)

    for printer in printer_obj_client:
        try:
            client_check = Check.objects.get(order_id=order_id, printer=printer, type=CLIENT)
        except Check.DoesNotExist:
            client_check = Check.objects.create(order_id=order_id, printer=printer, type=CLIENT, order=data)



    # Запускаем асинхронную задачу на генерацию PDF-файлов для чеков
    generate_client_check_pdf_async(client_check)
    generate_kitchen_check_pdf_async(kitchen_check)


    # Принимает api ключ принтера возвращает список не распечатанных чеков для этого принтера

    return JsonResponse({'message': f'Чеки успешно созданы'}, status=200)


@csrf_exempt
def unprinted_check(request):

    if request.method != 'POST':
        return JsonResponse({'message': 'Ожидается метод Get'}, status=404)

    data = json.loads(request.body)

    printer = data.get('printer_api')

    unprinted_checks = Check.objects.filter(~Q(status='printed') | Q(status__isnull=True), printer=printer).values('id')

    return list(unprinted_checks)


@csrf_exempt
def printed_check(request):

    if request.method != 'POST':
        return JsonResponse({'message': 'Ожидается метод Post'}, status=404)

    data = json.loads(request.body)

    printer_api = data.get('printer_api')
    order_id = data.get('order_id')

    printerObj = Printer.objects.filter(api_key=printer_api)
    orderCheck = Check.objects.get(order_id=order_id, printer=printerObj)
    
    orderCheck.status = 'printed'
    orderCheck.save()

    return JsonResponse({'путь': list(orderCheck.pdf_file)}, status=200)
