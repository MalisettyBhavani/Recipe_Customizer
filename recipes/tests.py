from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe
from .forms import RecipeForm

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Test ingredients",
            instructions="Test instructions",
            servings=4,
        )

    def test_recipe_creation(self):
        self.assertIsInstance(self.recipe, Recipe)
        self.assertEqual(str(self.recipe), self.recipe.name)

class RecipeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Test ingredients",
            instructions="Test instructions",
            servings=4,
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipe_create_view(self):
        response = self.client.post(reverse('recipe_new'), {
            'name': 'New Test Recipe',
            'ingredients': 'New Test ingredients',
            'instructions': 'New Test instructions',
            'servings': 2,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe_detail', args=[2]))
        self.assertEqual(Recipe.objects.last().name, 'New Test Recipe')

    def test_recipe_update_view(self):
        response = self.client.post(reverse('recipe_edit', args=[self.recipe.pk]), {
            'name': 'Updated Test Recipe',
            'ingredients': 'Updated Test ingredients',
            'instructions': 'Updated Test instructions',
            'servings': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe_detail', args=[self.recipe.pk]))
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, 'Updated Test Recipe')

class RecipeFormTest(TestCase):
    def test_valid_recipe_form(self):
        data = {
            'name': 'Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'servings': 4,
        }
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        data = {
            'name': '',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'servings': 4,
        }
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())
