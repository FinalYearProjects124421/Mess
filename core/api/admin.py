from django.contrib import admin

from .models import User,NewUser,FoodItems,Menu,Poll,FoodItem,Orders,Histroy,Leves,NewOders,Notification
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =('id','phone_number')

@admin.register(NewUser)
class NewUserAdmin(admin.ModelAdmin):
    list_display =('id','phone_number')

@admin.register(FoodItems)
class FoodItemsAdmin(admin.ModelAdmin):
    list_display =('id','food_name','food_img_uri')
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display =('id','food_name_morning','food_name_evening')



class PollAdmin(admin.ModelAdmin):
    list_display = ('morning_poll_1', 'morning_poll_1_value', 'morning_poll_2', 'morning_poll_2_value', 'evening_poll_1', 'evening_poll_1_value', 'evening_poll_2', 'evening_poll_2_value')

admin.site.register(Poll, PollAdmin)
@admin.register(FoodItem)
class FoodAdmin(admin.ModelAdmin):
    list_display =('name','food_type','cost')


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display =('id','status','tableno','session_id')


@admin.register(Histroy)
class HistroyAdmin(admin.ModelAdmin):
    list_display =('id','phone_no','title','date','time','user_name')


@admin.register(Leves)
class LevesAdmin(admin.ModelAdmin):
    list_display =('id','time','name','phone_no','date')


@admin.register(NewOders)
class NewOdersAdmin(admin.ModelAdmin):
    list_display =('id','full_name','phone_number','address','status','data')

    

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display =('id','phone_no','data','date','time')
