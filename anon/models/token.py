from django.db import models


# Model to store blacklisted tokens
class BlacklistedToken(models.Model):
    refresh_token = models.TextField()
    access_token = models.TextField()

    class Meta:
        db_table = "blacklisted_tokens"
