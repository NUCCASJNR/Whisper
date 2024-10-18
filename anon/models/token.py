from django.db import models


# Model to store blacklisted tokens
class BlacklistedToken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "blacklisted_tokens"
