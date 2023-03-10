from django.urls import include, path

from rest_framework import routers

from diary_api.views import del_diary_Item, delete_diary, get_itemlist_diary,Update_diary, Update_diary_item, create_diary, create_diary_item, get_lists_diary, login_user, register_user

router = routers.DefaultRouter()



urlpatterns = [
   path('', include(router.urls)),
   path(r'register',register_user), 
   path(r'userLogin',login_user),
   path(r'createDiary',create_diary),
   path(r'updateDiary',Update_diary),
   path(r'deleteDiary',delete_diary),
   path(r'diaryLists',get_lists_diary),
   path(r'createDiaryItem',create_diary_item),
   path(r'updateDiaryItem',Update_diary_item),
   path(r'diaryItemLists',get_itemlist_diary),
   path(r'deleteDiaryItem',del_diary_Item)
]