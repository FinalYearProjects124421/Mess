from django.urls import path
from .views import NewUserApiView,CheckPhoneNo,RemoveUser,GetCountNewUsers,RemoveFoodItem,AddFoodItem,NewUserAPI,GetAllUsers,UpdateUser,RemoveExitsUser,GetUser,GetFoodItems,AddMenu,GetMenu,AddPoll,VotePoll,ShowPoll,GetAllHistory,GetUserHistory,AddLeveRequest,GetAllLeves,AddHistory,GetALLOrders,GetAllNotification,GetUserNotification


urlpatterns = [
    # Existing URL patterns
    path('newuser/', NewUserApiView.as_view()),
    path('checkphoneno/',CheckPhoneNo.as_view()),
    path('removeuser/',RemoveUser.as_view()),
    path('getcountnewusers/',GetCountNewUsers.as_view()),
    path('removeFoodItem/',RemoveFoodItem.as_view()),
    path('addFoodItem/',AddFoodItem.as_view()),
    path('creaternewUser/',NewUserAPI.as_view()),
    path('getAllUsers/',GetAllUsers.as_view()),
    path('updateUser/',UpdateUser.as_view()),
    path('removeExitsUser/',RemoveExitsUser.as_view()),
    path('getUser/',GetUser.as_view()),
    path('getFoodItems/',GetFoodItems.as_view()),
    path('addMenu/',AddMenu.as_view()),
    path('getMenu/',GetMenu.as_view()),
    path('addPoll/',AddPoll.as_view()),
    path('votePoll/',VotePoll.as_view()),
    path('showPoll/',ShowPoll.as_view()),
    path('getAllHistory/',GetAllHistory.as_view()),
    path('getUserHistory/',GetUserHistory.as_view()),
    path('addLeveRequest/',AddLeveRequest.as_view()),
    path('getAllLeves/',GetAllLeves.as_view()),
    path('addHistory/',AddHistory.as_view()),
    path('getALLOrders/',GetALLOrders.as_view()),
    path('getAllNotification/',GetAllNotification.as_view()),
    path('getUserNotification/',GetUserNotification.as_view())

    
]