from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

# super user : admin_beritahoo, pass : beritahoo

# class Categories(object): 
# 	CHOICES = (('Deep Learning', 'Deep Learning'),
#               ('Machine Learning', 'Machine Learning'),
#               ('Python', 'Python'),
#               ('Math', 'Math'),
#               ('Text Analysis', 'Text Analysis'))

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	category = models.TextField()
	# category = models.TextField(choices=Categories.CHOICES)
	date_post = models.DateTimeField(default=timezone.now)
	editor = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})


