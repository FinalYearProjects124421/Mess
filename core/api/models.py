from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from django.utils import timezone

# Create your models here.
class NewUser(models.Model):
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=200, null=True)

@receiver(post_save, sender=NewUser)
def new_user_add(sender, instance, created, **kwargs):
    if created:  # Only send if the order is newly created
        orders_data = {'id': instance.id, 'phone_number': instance.phone_number, 'full_name': instance.full_name}
        serialized_order = json.dumps(orders_data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('admin_group', {'type': 'show_users', 'message': serialized_order})


class User(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    phone_number=models.CharField(max_length=15)
    address = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    fees = models.CharField(max_length=200, null=True)
    exp_date=models.CharField(max_length=200,null=True)



class Menu(models.Model):
    food_name_morning = models.CharField(max_length=15)
    food_img_uri_morning = models.CharField(max_length=200, null=True)
    food_name_evening = models.CharField(max_length=15)
    food_img_uri_evening = models.CharField(max_length=200, null=True)
    


class FoodItems(models.Model):
    food_name = models.CharField(max_length=15)
    food_img_uri = models.CharField(max_length=200, null=True)

@receiver(post_save, sender=FoodItems)
def food_item_add(sender, instance, created, **kwargs):
    if created:  # Only send if the order is newly created
        foods_data = {'id': instance.id, 'food_name': instance.food_name, 'food_img_uri': instance.food_img_uri}
        serialized_order = json.dumps(foods_data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('admin_group_food_items', {'type': 'show_food_items', 'message': serialized_order})



class Poll(models.Model):
    morning_poll_1 = models.CharField(max_length=200)
    morning_poll_1_value = models.IntegerField(default=0)
    morning_poll_2 = models.CharField(max_length=200)
    morning_poll_2_value = models.IntegerField(default=0)
    evening_poll_1 = models.CharField(max_length=200)
    evening_poll_1_value = models.IntegerField(default=0)
    evening_poll_2 = models.CharField(max_length=200)
    evening_poll_2_value = models.IntegerField(default=0)

    def __str__(self):
        return f"Morning Polls: {self.morning_poll_1} ({self.morning_poll_1_value}), {self.morning_poll_2} ({self.morning_poll_2_value}), Evening Polls: {self.evening_poll_1} ({self.evening_poll_1_value}), {self.evening_poll_2} ({self.evening_poll_2_value})"

class FoodItem(models.Model):
 

    name = models.CharField(max_length=100)
    food_type = models.CharField(max_length=20)
    
    cost = models.CharField(max_length=20)
class Orders(models.Model):
    STATUS_CHOICES = [
        (0, 'Not Completed'),
        (1, 'Completed'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tableno = models.IntegerField(max_length=100)
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    order_list=models.CharField(max_length=800,default=" ")
      # Add session_id field

    def __str__(self):
        return f"Order: {self.id}, Status: {self.get_status_display()}, Table No: {self.tableno}"


@receiver(post_save, sender=Orders)
def send_order_to_waiters(sender, instance, created, **kwargs):
    if created:  # Only send if the order is newly created
        orders_data = {'id': instance.id, 'status': instance.status, 'tableno': instance.tableno,'order_list':instance.order_list}
        serialized_order = json.dumps(orders_data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('admin_group', {'type': 'send_order', 'message': serialized_order})

class Histroy(models.Model):
    phone_no = models.CharField(max_length=15)
    title = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=200, null=True)
    user_name=models.CharField(max_length=200)
    

class Leves(models.Model):
    time = models.CharField(max_length=15)
    name=models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=15)


class NewOders(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    phone_number=models.CharField(max_length=15)
    address = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    data = models.CharField(max_length=200, null=True)

class Notification(models.Model):
    phone_no = models.CharField(max_length=15)
    data = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=200, null=True)
   