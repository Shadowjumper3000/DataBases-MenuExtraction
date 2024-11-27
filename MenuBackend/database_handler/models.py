from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MenuSection(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MenuItem(models.Model):
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DietaryRestriction(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class ItemRestriction(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    dietary_restriction = models.ForeignKey(
        DietaryRestriction, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("menu_item", "dietary_restriction")


class ProcessingLog(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    description = models.TextField()
    action_time = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=255)
