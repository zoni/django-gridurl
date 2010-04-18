from django.db import models

class Url(models.Model):
	name = models.CharField(max_length=255, unique=True)
	inworld_url = models.CharField(max_length=255)
	password_salt = models.CharField(max_length=32)
	password_hash = models.CharField(max_length=65)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)

