from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    comment = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} commented {self.comment}"
    
    def get_likes_count(self):
        return Likes.objects.filter(comment_id=self).count()
    
class Likes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="commented")

    def __str__(self):
        return f"{self.user_id} liked {self.comment_id}"