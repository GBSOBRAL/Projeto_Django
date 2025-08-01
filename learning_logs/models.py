from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    """Um assunto sobre o qual o usuário está aprendendo"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devolve uma representação em String do modelo"""
        return self.text

class Entry(models.Model):
    """Algo específico aprendido sobre um assunto"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Diz ao Django o plural correto do nome da tabela, se não ele só colocará um 's'"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """Devolve uma representação em String do modelo"""
        return self.text[:50] +'...'