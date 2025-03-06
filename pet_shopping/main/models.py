from django.db import models

class Pet(models.Model):
    CATEGORY_CHOICES = [
        ('dogs', '狗狗'),
        ('cats', '貓咪'),
        ('small', '小型寵物'),
    ]

    name = models.CharField(max_length=100, verbose_name='名稱')
    breed = models.CharField(max_length=100, verbose_name='品種')
    price = models.CharField(max_length=20, verbose_name='價格')
    status = models.CharField(max_length=20, default='可預購', verbose_name='狀態')
    statusClass = models.CharField(max_length=20, default='status-available', verbose_name='狀態樣式類別')
    vaccine = models.CharField(max_length=100, default='已完成基礎疫苗', verbose_name='疫苗情況')
    image = models.CharField(max_length=255, verbose_name='圖片路徑')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='分類')
    description = models.TextField(verbose_name='描述')
    def __str__(self):
        return self.name
    
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email})"