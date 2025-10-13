from django.db import models

class QueryLog(models.Model):
    user_query = models.TextField()
    decision = models.CharField(max_length=50)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.decision} - {self.user_query[:40]}"
