# Create your models here.
import os
from django.db import models
from cryptography.fernet import Fernet


class PasswordEntry(models.Model):
    service_name = models.CharField(max_length=255, unique=True)
    encrypted_password = models.TextField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        encryption_key = os.getenv("ENCRYPTION_KEY") or 'ev6MaCaQRcITRUBlHM2TXXHTyZDMmjeN7QYGMiPvfLc='
        self.cipher_suite = Fernet(encryption_key)

    def set_password(self, password):
        self.encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()

    def get_password(self):
        return self.cipher_suite.decrypt(self.encrypted_password.encode()).decode()
