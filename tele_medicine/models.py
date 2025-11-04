from django.db import models

class CustomUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=255)  # Store hashed passwords only!
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'telehealth_users'


