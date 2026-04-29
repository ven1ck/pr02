from django.db import models
from django.contrib.auth.models import User

class QRCode(models.Model):
    ERROR_CORRECTION_CHOICES = [
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Квартиль', 'Квартиль'),
        ('Высокий', 'Высокий'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='qr_codes')
    text = models.TextField()
    size = models.PositiveIntegerField(default=300)
    error_correction = models.CharField(max_length=10, choices=ERROR_CORRECTION_CHOICES, default='Средний')
    fg_color = models.CharField(max_length=7, default='#000000')
    bg_color = models.CharField(max_length=7, default='#FFFFFF')
    image = models.ImageField(upload_to='qr_codes/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR: {self.text[:30]}..."