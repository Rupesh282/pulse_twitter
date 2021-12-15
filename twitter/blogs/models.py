from django.db import models

# Create your models here.

class Posts(models.Model) : 
    published_date = models.DateField('date published')
    text_data = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return str(self.id) + " " + self.text_data
    
class PostToTags(models.Model) : 
    tag_name = models.CharField(max_length=10)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.tag_name + " " + str(self.post.id)