from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,NewUser,FoodItems,Menu,Poll,Histroy ,Leves,NewOders,Notification
from datetime import datetime
# Create your views here.
class NewUserApiView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        phone_no=request.data.get('phone_no')
        name=request.data.get('name')
        new_user = NewUser.objects.create(
            phone_number=phone_no,
            full_name=name
        )
        
        # You might want to return some response here
        return Response({"code": "1"})

class CheckPhoneNo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_no = request.data.get('phone_no')
        if phone_no:
            # Check if the phone number exists in the User model
            user_exists = User.objects.filter(phone_number=phone_no).exists()
            if user_exists:
                return Response({'code': "1"})
            else:
                return Response({'code': "0"})
        else:
            return Response({'error': 'Phone number not provided'}, status=400)
        pass

class RemoveUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_user = request.data.get('id')
        try:
            # Attempt to get the user with the provided ID
            user = NewUser.objects.get(id=id_user)
            user.delete()  # Delete the user from the database
            return Response({'message': 'User removed successfully'})
        except NewUser.DoesNotExist:
            return Response({'error': 'User not found'})
        except Exception as e:
            return Response({'error': str(e)})



class GetCountNewUsers(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_count = NewUser.objects.count()
        print(user_count)
        return Response({'user_count': user_count})

        
class RemoveFoodItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_user = request.data.get('id')
        try:
            # Attempt to get the user with the provided ID
            user = FoodItems.objects.get(id=id_user)
            user.delete()  # Delete the user from the database
            return Response({'message': 'User removed successfully'})
        except FoodItems.DoesNotExist:
            return Response({'error': 'User not found'})
        except Exception as e:
            return Response({'error': str(e)})
        
class AddFoodItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        food_name = request.data.get('food_name')
        img_uri = request.data.get('food_img_uri')
        food_item = FoodItems(food_name=food_name, food_img_uri=img_uri)

        # Save the instance
        food_item.save()

        # Return success response
        return Response({"message": "Food item saved successfully"})

class NewUserAPI(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')
        category = request.data.get('category')
        fees = request.data.get('fees')
        if fees == 'Paid':
            # Set exp_date to current date in string format
            exp_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # Set exp_date to None if fees is 'Remaining'
            exp_date = 'null'

        # Create User instance
        user = User(full_name=full_name, phone_number=phone_number, address=address,
                    category=category, fees=fees, exp_date=exp_date)

        # Save the instance
        user.save()

        # Return success response
        return Response({"message": "User saved successfully"})

class GetAllUsers(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        users = User.objects.all()

    # Convert queryset to list of dictionaries
        users_list = list(users.values())
        return Response({'users_list': users_list, 'code': '0'})
class GetUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        print(phone)
        try:
            user = User.objects.filter(phone_number=phone)
            # user_data = {
            #     'full_name': user.full_name,
            #     'phone_number': user.phone_number,
            #     'address': user.address,
            #     'category': user.category,
            #     'fees': user.fees,
            #     'exp_date': user.exp_date
            # }
            user_data=list(user.values())
            if not user_data:
                return Response({"code":"0"})
            else:
                print(user_data)
                return Response({"code":"1","user":user_data})


            
        except User.DoesNotExist:
            print("not")
            return Response({"code":"0"})


class UpdateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')
        category = request.data.get('category')
        fees = request.data.get('fees')

        # Check if fees is 'Paid'
        if fees == 'Paid':
            # Set exp_date to current date in string format
            exp_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # Set exp_date to None if fees is 'Remaining'
            exp_date = 'null'

        # Update or create User instance
        user, created = User.objects.update_or_create(
            phone_number=phone_number,
            defaults={'full_name': full_name, 'address': address, 'category': category, 'fees': fees, 'exp_date': exp_date}
        )

        # Return appropriate response
        if created:
            return Response({"message": "User created successfully"},)
        else:
            return Response({"message": "User updated successfully"})


class RemoveExitsUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_user = request.data.get('id')
        try:
            # Attempt to get the user with the provided ID
            user = User.objects.get(id=id_user)
            user.delete()  # Delete the user from the database
            return Response({'message': 'User removed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'})
        except Exception as e:
            return Response({'error': str(e)})


class GetFoodItems(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        food_items = FoodItems.objects.all()
        list_food=list(food_items.values())
        return Response({"food_list":list_food})
    


class AddMenu(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        food_name_morning = request.data.get('food_name_morning')
        food_name_evening = request.data.get('food_name_evening')

        # Query FoodItems to get the corresponding image URIs
        food_item_morning = FoodItems.objects.filter(food_name=food_name_morning).first()
        food_item_evening = FoodItems.objects.filter(food_name=food_name_evening).first()

        if food_item_morning and food_item_evening:
            # Check if there's an existing menu
            existing_menu = Menu.objects.first()
            if existing_menu:
                # If there's an existing menu, update its fields
                existing_menu.food_name_morning = food_name_morning
                existing_menu.food_img_uri_morning = food_item_morning.food_img_uri
                existing_menu.food_name_evening = food_name_evening
                existing_menu.food_img_uri_evening = food_item_evening.food_img_uri
                existing_menu.save()
            else:
                # If there's no existing menu, create a new one
                menu = Menu(
                    food_name_morning=food_name_morning,
                    food_img_uri_morning=food_item_morning.food_img_uri,
                    food_name_evening=food_name_evening,
                    food_img_uri_evening=food_item_evening.food_img_uri
                )
                menu.save()
            return Response({"message": "Menu added/updated successfully"})
        else:
            return Response({"error": "One or both food items not found"}, status=400)


class GetMenu(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       
      
        try:
            existing_menu = Menu.objects.first()
            if existing_menu:
                # Serialize Menu object data
                menu_data = {
                    'food_name_morning': existing_menu.food_name_morning,
                    'food_img_uri_morning': existing_menu.food_img_uri_morning,
                    'food_name_evening': existing_menu.food_name_evening,
                    'food_img_uri_evening': existing_menu.food_img_uri_evening,
                }
                return Response({"menu_data": menu_data})
            else:
                return Response({'message': 'Menu not found'})
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'})
        



class AddPoll(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        food_name_evening_1 = request.data.get('food_name_evening_1')
        food_name_evening_2 = request.data.get('food_name_evening_2')
        food_name_morning_1 = request.data.get('food_name_morning_1')
        food_name_morning_2 = request.data.get('food_name_morning_2')
        poll_instance, created = Poll.objects.get_or_create(id=1)
        poll_instance.morning_poll_1_value = 0
        poll_instance.morning_poll_2_value = 0
        poll_instance.evening_poll_1_value = 0
        poll_instance.evening_poll_2_value = 0

        # Update the Poll instance with the new values
        poll_instance.morning_poll_1 = food_name_morning_1
        poll_instance.morning_poll_2 = food_name_morning_2
        poll_instance.evening_poll_1 = food_name_evening_1
        poll_instance.evening_poll_2 = food_name_evening_2

        # Save the updated instance
        poll_instance.save()

        return Response({"message": "Poll updated successfully"})

class VotePoll(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve user's selections for morning and evening polls
        selected_morning_poll = request.data.get('selected_morning_poll')
        selected_evening_poll = request.data.get('selected_evening_poll')

        # Get the Poll instance
        if Poll.objects.exists():
            poll_instance = Poll.objects.first()
        else:
            return Response({"error": "No polls available"}, status=400)

        # Increment the value fields for the selected polls
        if selected_morning_poll == '1':
            poll_instance.morning_poll_1_value += 1
        elif selected_morning_poll == '2':
            poll_instance.morning_poll_2_value += 1

        if selected_evening_poll == '1':
            poll_instance.evening_poll_1_value += 1
        elif selected_evening_poll == '2':
            poll_instance.evening_poll_2_value += 1

        # Save the Poll instance
        poll_instance.save()

        # Calculate percentages for morning polls
        total_morning_votes = poll_instance.morning_poll_1_value + poll_instance.morning_poll_2_value

        morning_poll_1_percentage = round((poll_instance.morning_poll_1_value / total_morning_votes) * 100) if total_morning_votes > 0 else 0
        morning_poll_2_percentage = round((poll_instance.morning_poll_2_value / total_morning_votes) * 100) if total_morning_votes > 0 else 0

        # Calculate percentages for evening polls
        total_evening_votes = poll_instance.evening_poll_1_value + poll_instance.evening_poll_2_value

        evening_poll_1_percentage = round((poll_instance.evening_poll_1_value / total_evening_votes) * 100) if total_evening_votes > 0 else 0
        evening_poll_2_percentage = round((poll_instance.evening_poll_2_value / total_evening_votes) * 100) if total_evening_votes > 0 else 0

        # Prepare response data
        response_data = {
            "morning_poll_1": poll_instance.morning_poll_1,
            "morning_poll_1_value": poll_instance.morning_poll_1_value,
            "morning_poll_1_percentage": morning_poll_1_percentage,
            "morning_poll_2": poll_instance.morning_poll_2,
            "morning_poll_2_value": poll_instance.morning_poll_2_value,
            "morning_poll_2_percentage": morning_poll_2_percentage,
            "evening_poll_1": poll_instance.evening_poll_1,
            "evening_poll_1_value": poll_instance.evening_poll_1_value,
            "evening_poll_1_percentage": evening_poll_1_percentage,
            "evening_poll_2": poll_instance.evening_poll_2,
            "evening_poll_2_value": poll_instance.evening_poll_2_value,
            "evening_poll_2_percentage": evening_poll_2_percentage,
        }
        print(response_data)

        return Response({"poll":response_data})

class AddPoll(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        food_name_evening_1 = request.data.get('food_name_evening_1')
        food_name_evening_2 = request.data.get('food_name_evening_2')
        food_name_morning_1 = request.data.get('food_name_morning_1')
        food_name_morning_2 = request.data.get('food_name_morning_2')
        poll_instance, created = Poll.objects.get_or_create(id=1)
        poll_instance.morning_poll_1_value = 0
        poll_instance.morning_poll_2_value = 0
        poll_instance.evening_poll_1_value = 0
        poll_instance.evening_poll_2_value = 0

        # Update the Poll instance with the new values
        poll_instance.morning_poll_1 = food_name_morning_1
        poll_instance.morning_poll_2 = food_name_morning_2
        poll_instance.evening_poll_1 = food_name_evening_1
        poll_instance.evening_poll_2 = food_name_evening_2

        # Save the updated instance
        poll_instance.save()

        return Response({"message": "Poll updated successfully"})

class ShowPoll(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve user's selections for morning and evening polls
        poll_instance = Poll.objects.first()

        # Prepare response data
        response_data = {
            "morning_poll_1": poll_instance.morning_poll_1,
        
            "morning_poll_2": poll_instance.morning_poll_2,
           
            "evening_poll_1": poll_instance.evening_poll_1,
           
            "evening_poll_2": poll_instance.evening_poll_2,
           
        }
        print(response_data)

        return Response({"poll_data":response_data})
    


class GetAllHistory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve all history rows
        all_history = Histroy.objects.all()

        # Convert the queryset into dictionary format
        history_data = [
            {
                'phone_no': history.phone_no,
                'title': history.title,
                'date': history.date,
                'time': history.time,
                'user_name': history.user_name
            }
            for history in all_history
        ]

        # Now history_data contains the data in dictionary format

        # Send the data in the response
        return Response({'UserHistory': history_data})
    

class GetUserHistory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone')
        print(phone_number)
        
        # Retrieve all history rows where phone_no matches
        filtered_history = Histroy.objects.filter(phone_no=phone_number)

        # Convert the filtered queryset into dictionary format
        history_data = [
            {
                'phone_no': history.phone_no,
                'title': history.title,
                'date': history.date,
                'time': history.time,
                'user_name': history.user_name
            }
            for history in filtered_history
        ]

        # Now history_data contains the data in dictionary format

        # Send the data in the response
        return Response({'UserHistory': history_data})
    


        



class AddLeveRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract data from request
        name = request.data.get('name')
        time = request.data.get('time')
        date = request.data.get('date')
        phone_no = request.data.get('phone_no')
        print(name)

        print(time)
        print(date)
        print(phone_no)

        # Validate the data
        if not all([name, time, date]):
            return Response({"code": "0"})

        # Create and save Leves instance
        leve = Leves(name=name, time=time, date=date, phone_no=phone_no)
        leve.save()

        return Response({"code": "1"})
    

class GetAllLeves(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve all history rows
        all_Leves = Leves.objects.all()

        # Convert the queryset into dictionary format
        history_data = [
            {
                'phone_no': history.phone_no,
                
                'date': history.date,
                'time': history.time,
                'name': history.name
            }
            for history in all_Leves
        ]

        # Now history_data contains the data in dictionary format

        # Send the data in the response
        return Response({'leves': history_data})
    

class AddHistory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_no = request.data.get('phone_no')
        title = request.data.get('title')
        date = request.data.get('date')
        time = request.data.get('time')
        user_name = request.data.get('user_name')
        history = Histroy(
            phone_no=phone_no,
            title=title,
            date=date,
            time=time,
            user_name=user_name
        )
        history.save()

        return Response({"code": "1"})
class GetALLOrders(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        all_orders = NewOders.objects.all()

        # Convert the queryset into dictionary format
        history_data = [
            {
                'full_name': history.full_name,
                
                'phone_number': history.phone_number,
                'address': history.address,
                'status': history.status,
                'data': history.data,

            }
            for history in all_orders
        ]

        # Now history_data contains the data in dictionary format

        # Send the data in the response
        return Response({'orders': history_data})
class GetAllNotification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve all history rows
        all_notifications = Notification.objects.exclude(phone_no="1")

        # Convert the queryset into dictionary format
        notification_data = [
            {
                'phone_no': notification.phone_no,
                'data': notification.data,
                'date': notification.date,
                'time': notification.time
            }
            for notification in all_notifications
        ]

        # Send the data in the response
        return Response({'all_notifications': notification_data})
class GetUserNotification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Retrieve all history rows
        phone_no = request.data.get('phone_no')

        # Retrieve all notifications matching the phone number
        all_notifications = Notification.objects.filter(phone_no=phone_no)

        # Convert the queryset into dictionary format
        notification_data = [
            {
                'phone_no': notification.phone_no,
                'data': notification.data,
                'date': notification.date,
                'time': notification.time
            }
            for notification in all_notifications
        ]

        # Send the data in the response
        return Response({'user_notifications': notification_data})
    
