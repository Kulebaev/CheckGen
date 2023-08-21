import pdfkit
import os
from celery import shared_task
from .models import Check


CONFIGWKHTML = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')


@shared_task
def generate_kitchen_check_pdf_async(checkObj):

    check_id = checkObj.id

    try:
        check = Check.objects.get(id=check_id)
    except Check.DoesNotExist:
        return
    
    # Путь к выходному файлу PDF r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    pdf_output_path = f'checkGenApp/media/pdf/{check_id}_kitchen_check.pdf'

    # Проверяем, существует ли файл PDF по указанному пути
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    # Генерируем PDF-файл для кухонного чека, используя шаблон kitchen_check.html
    generate_pdf_from_template(f'checkGenApp/templates/kitchen_check.html', {'check': check}, pdf_output_path)


    #update_check_status_to_rendering(check_id)

    check.status = 'rendered'
    check.pdf_file = pdf_output_path
    check.save()


@shared_task
def generate_client_check_pdf_async(checkObj):

    check_id = checkObj.id

    try:
        check = Check.objects.get(id=check_id)
    except Check.DoesNotExist:
        return
    
    # Путь к выходному файлу PDF r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    pdf_output_path = f'checkGenApp/media/pdf/{check_id}_clien_check.pdf'

    # Проверяем, существует ли файл PDF по указанному пути
    if os.path.exists(pdf_output_path):
        os.remove(pdf_output_path)

    # Генерируем PDF-файл для кухонного чека, используя шаблон clien_check.html
    generate_pdf_from_template(f'checkGenApp/templates/clien_check.html', {'check': check}, pdf_output_path)


    #update_check_status_to_rendering(check_id)

    check.status = 'rendered'
    check.pdf_file = pdf_output_path
    check.save()


def generate_pdf_from_template(template_path, context, output_path):
    
    html_file_path = template_path

    # Путь для сохранения PDF
    pdf_output_path = output_path

    # Устанавливаем путь к исполняемому файлу wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Формируем и сохраняем PDF из HTML
    pdfkit.from_file(html_file_path, pdf_output_path, configuration=config)

