import json
import os
import time
import threading
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer
from .models import FoodItem,NewUser,Orders,FoodItems,NewOders
import dialogflow as dialogflow
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from django.http import JsonResponse
import json
import os
import time
from threading import Timer
from channels.generic.websocket import WebsocketConsumer
import dialogflow_v2 as dialogflow
class ShowNewUsers(WebsocketConsumer):
    def show_users(self, event):
        data=json.loads(event['message'])
        name=data.get('full_name')
        phone_no = data.get('phone_number')
        new_users = NewUser.objects.all()
        # print(new_users)

    # Prepare the data to send
        data = []
        for user in new_users:
            data.append({
                'id':user.id,
                'phone_number': user.phone_number,
                'full_name': user.full_name
        })
        print("Data Saved")
        
        self.send(text_data=json.dumps({'users':data}))
        


    def connect(self):
        self.accept()
        self.room_name = 'admin_group'
        self.room_group_name = 'admin_group'

        # Add the admin to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print("Connection Opened !")
        new_users = NewUser.objects.all()
        # print(new_users)

    # Prepare the data to send
        data = []
        for user in new_users:
            data.append({
                'id':user.id,
                'phone_number': user.phone_number,
                'full_name': user.full_name
        })
        print(data)
        
        self.send(text_data=json.dumps({'users':data}))
       
        

    def disconnect(self, close_code):
        print("Connection Closed !")
        pass

    def receive(self, text_data):
        receive_dict = json.loads(text_data)
        print(text_data)
        self.code=receive_dict.get('code')
        if self.code=="1":
            new_users = NewUser.objects.all()
            # print(new_users)

            # Prepare the data to send
            data = []
            for user in new_users:
                data.append({
                    'id':user.id,
                    'phone_number': user.phone_number,
                    'full_name': user.full_name
            })
            print(data)
        
        self.send(text_data=json.dumps({'users':data}))
        
        
        # print(self.tableno)
        # message = receive_dict.get('message') 
        # self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':response.query_result.fulfillment_text}))
       
    






     
        
    def disconnect(self, close_code):
        pass
    

def get_str_from_food_dict(food_dict:dict):
        return ", ".join([f"{int(value)} {key}" for key ,value in food_dict.items()])
class MyConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inprogress_orders = {}
        self.session_connections = {}  # Dictionary to store WebSocket connections by session ID
        self.last_checked_timestamp = timezone.now()
        # Start the thread to check for completed orders
        # self.order_check_thread = threading.Thread(target=self.check_orders)
        # self.order_check_thread.daemon = True
        # self.order_check_thread.start()
        self.tableno=''
        self.SESSION_ID = f"session_{int(time.time())}"
        self.USER='sir'
        self.DIALOGFLOW_PROJECT_ID='test-2-rao-taca'
        self.DIALOGFLOW_LANGUAGE_CODE='en'

        # Specify the full path to the JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-2-rao-taca-ff0592e78dce.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_file_path
        self.inprogress_orders={}
        self.session_connections[self.SESSION_ID] = self 

    def connect(self):
        self.accept()
        self.isTableGet=False
        

    

    
    
        
        

    def disconnect(self, close_code):
        del self.session_connections[self.SESSION_ID]
        pass

    def receive(self, text_data):
        receive_dict = json.loads(text_data)
        print(text_data)
        self.tableno=receive_dict.get('tableno')
        print(self.tableno)
        message = receive_dict.get('message')
        if receive_dict.get('code')=="odercom":
            print("oder placed")
            full_name=receive_dict.get('full_name')
            phone_number=receive_dict.get('phone_number')
            address=receive_dict.get('address')
            status="no"
            data=self.inprogress_orders[self.SESSION_ID]
            new_order = NewOders.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                address=address,
                status=status,
                data=data
            )
    
            new_order.save()

            return
        
        print(message)
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
        text_input = dialogflow.types.TextInput(text=message, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
            intent = response.query_result.intent.display_name
            data = response.query_result.parameters.fields
            print(intent)
            # print("Dora:", response.query_result.fulfillment_text)
            if intent == "order.add - context: ongoing-order":
                self.add_order(data)  # Call add_order method
            elif intent == "order.complete - context: ongoing-order":
                self.complete_order()
                # self.send(response.query_result.fulfillment_text)
                pass
                # complete_order()
            elif intent == "ask-menu":
                self.Menu(data)
                pass
                # complete_order()
            elif intent=="order.remove - context: ongoing-order":
                self.remove_oder()
           
            else:
                self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':response.query_result.fulfillment_text}))
                # self.send(text_data=response.query_result.fulfillment_text)
                # self.send(text_data=response.query_result.fulfillment_text)
            # Handle different intents here
        except Exception as e:
            print("Error:", e)

    def add_order(self, data):
        food_items = [item.string_value for item in data['food-item'].list_value.values]  # Access the list of food items
        numbers_of_items = [int(item.number_value) for item in data['number'].list_value.values]

        if len(food_items) != len(numbers_of_items):
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':"Sorry, I didn't understand. Can you please specify food items and quantities?"}))
        else:
            new_food_dict = {}

            for item, quantity in zip(food_items, numbers_of_items):
                new_food_dict[item] = quantity

            if self.SESSION_ID in self.inprogress_orders:
                current_food_dict = self.inprogress_orders[self.SESSION_ID]
                current_food_dict.update(new_food_dict)
                self.inprogress_orders[self.SESSION_ID] = current_food_dict
            else:
                self.inprogress_orders[self.SESSION_ID] = new_food_dict




            print(self.inprogress_orders)



            order_str = get_str_from_food_dict(self.inprogress_orders[self.SESSION_ID])
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':f"So far you have: {order_str}. Do you need anything else?"}))
    def Menu(self,data):
        
        food_type_str = data['type-food'].string_value
        print(food_type_str)
        if not food_type_str:
            print("All Menu")
            text_menu=""
            food_items = FoodItem.objects.filter(food_type="vegetarian")
            names = []
            costs = []

            for item in food_items:
                names.append(item.name)
                costs.append(item.cost)

        
            print(names)  
            print(costs)  

   
            text_menu=text_menu+self.generate_menu_text("Vegetarian",names,costs)
            food_items = FoodItem.objects.filter(food_type="non vegetarian")
            names = []
            costs = []

            for item in food_items:
                names.append(item.name)
                costs.append(item.cost)

        
            print(names)  
            print(costs)
            text_menu=text_menu+"\n"+self.generate_menu_text("Non vegetarian",names,costs)
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':text_menu}))
        elif food_type_str=="non vegetarian":
            print("Non veg")
            food_items = FoodItem.objects.filter(food_type=food_type_str)
            names = []
            costs = []

   
            for item in food_items:
                names.append(item.name)
                costs.append(item.cost)

           
            print(names)  
            print(costs)  
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':self.generate_menu_text("Non vegetarian",names,costs)}))

        elif food_type_str=="vegetarian":
            food_items = FoodItem.objects.filter(food_type="vegetarian")
            names = []
            costs = []

            for item in food_items:
                names.append(item.name)
                costs.append(item.cost)

        
            print(names)  
            print(costs)
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':self.generate_menu_text("Vegetarian",names,costs)})) 

    def complete_order(self):
        try:
            if self.tableno:
                total_bill = self.calculate_total_bill(self.inprogress_orders[self.SESSION_ID])
                print("Order placed for table:", self.tableno)
                order = Orders.objects.create(status=0, tableno=self.tableno, session_id=self.SESSION_ID,order_list=self.inprogress_orders[self.SESSION_ID])
                self.send(text_data=json.dumps({'code':'oderdone','session_id':self.SESSION_ID,'msg':f"Your order has been placed. "}))

            else:
                print("Tableno not set")
                self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':'Tableno not set. Unable to place order.'}))
        except Exception as e:
            print("Error placing order:", e)
            self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':'An error occurred while placing the order.'}))
    def calculate_total_bill(self,inprogress_order):
        total_bill = 0

        for item_name, quantity in inprogress_order.items():
            try:
                food_item = FoodItem.objects.get(name=item_name)
                item_cost = float(food_item.cost)  # Assuming cost is a numeric field
                total_bill += item_cost * quantity
            except FoodItem.DoesNotExist:
                print(f"Item '{item_name}' not found in the database.")
            except ValueError:
                print(f"Invalid cost for item '{item_name}'.")
    
            return total_bill 

    def remove_oder(self):
        
        pass






     
        
    def disconnect(self, close_code):
        pass
    
    def generate_menu_text(self,menu_title,food_items, costs):
        menu_text = menu_title+"\n\n"
        # menu_text += "MENU\n"
        
        # Determine the maximum length of item name and cost
        max_item_length = max(len(item) for item in food_items)
        max_cost_length = max(len(str(cost)) for cost in costs)
        
        # Header row
        menu_text += f"{'Item':<{max_item_length}} | {'Price (Rs.)':<{max_cost_length}}\n"
        menu_text += "-" * (max_item_length + max_cost_length + 3) + "\n"
        
        # Items row
        for item, cost in zip(food_items, costs):
            menu_text += f"{item:<{max_item_length}} | Rs. {cost:>{max_cost_length}}\n"
        
        return menu_text
class ShowItems(WebsocketConsumer):
    def show_food_items(self, event):
        data=json.loads(event['message'])
        name=data.get('food_name')
        phone_no = data.get('food_img_uri')
        food_items = FoodItems.objects.all()
        # print(new_users)

    # Prepare the data to send
        data = []
        for item in food_items:
            data.append({
                'id':item.id,
                'food_name': item.food_name,
                'food_img_uri': item.food_img_uri
        })
        print("Data Saved")
        
        self.send(text_data=json.dumps({'food_items':data}))
        


    def connect(self):
        self.accept()
        self.room_name = 'admin_group_food_items'
        self.room_group_name = 'admin_group_food_items'

        # Add the admin to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print("Connection Opened !")
        food_items = FoodItems.objects.all()
        # print(new_users)

    # Prepare the data to send
        data = []
        for item in food_items:
            data.append({
                'id':item.id,
                'food_name': item.food_name,
                'food_img_uri': item.food_img_uri
        })
        
        
        self.send(text_data=json.dumps({'food_items':data}))
        
       
        

    def disconnect(self, close_code):
        print("Connection Closed !")
        pass

    def receive(self, text_data):
        receive_dict = json.loads(text_data)
        print(text_data)
        self.code=receive_dict.get('code')
        if self.code=="1":
            food_items = FoodItems.objects.all()
        # print(new_users)

    # Prepare the data to send
            data = []
            for item in food_items:
                data.append({
                    'id':item.id,
                    'food_name': item.food_name,
                    'food_img_uri': item.food_img_uri
                })
            
            
            self.send(text_data=json.dumps({'food_items':data}))
        
        
        
        
        
        # print(self.tableno)
        # message = receive_dict.get('message') 
        # self.send(text_data=json.dumps({'session_id':self.SESSION_ID,'msg':response.query_result.fulfillment_text}))
       
    






     
        
    def disconnect(self, close_code):
        pass
    
   