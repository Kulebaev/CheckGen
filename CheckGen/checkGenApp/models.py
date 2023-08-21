from django.db import models


class Printer(models.Model):
    TYPE_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('client', 'Client'),
    ]

    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, unique=True)
    check_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name
    

class Check(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('rendered', 'Rendered'),
        ('printed', 'Printed'),
    ]

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('kitchen', 'Kitchen'), ('client', 'Client')])
    order = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    pdf_file = models.FileField(upload_to='pdf/', null=True, blank=True)
    order_id = models.IntegerField()


    def __str__(self):
        return f"Check {self.pk} - {self.type} - {self.status}"

