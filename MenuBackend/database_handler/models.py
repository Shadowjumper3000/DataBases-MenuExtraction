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
    version = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other versions of this menu
            Menu.objects.filter(restaurant=self.restaurant, is_active=True).update(
                is_active=False
            )
        super().save(*args, **kwargs)


class MenuSection(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, default=1
    )  # Provide a default value
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DietaryRestriction(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class FoodItemRestriction(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    dietary_restriction = models.ForeignKey(
        DietaryRestriction, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("food_item", "dietary_restriction")


class ProcessingLog(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    description = models.TextField()
    action_time = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=255)
