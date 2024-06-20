from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    servings = models.IntegerField(default=1)

    def __str__(self):
        return self.name

