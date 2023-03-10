from rest_framework import serializers

from diary_api.models import User,Diarylist,Diaryitems

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('user_id', 'password', 'created_time','user_name')

class DiarylistSerializer(serializers.ModelSerializer):
   class Meta:
       model = Diarylist
       fields = ('user_id', 'diary_title', 'diary_id','created_time','updated_time')

class DiaryitemsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Diaryitems
       fields = ('diary_id ','diary_body','created_time','updated_time')