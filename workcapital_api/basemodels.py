from django.db import models
import uuid

class BaseModel(models.Model):
    # ID como UUID (UUIDField)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Timestamps automáticos (DateTimeField)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Importante: Define a classe como abstrata, não cria tabela no DB
        abstract = True
        ordering = ['-created_at']