from django.db import models

class User(models.Model):
   user_id = models.AutoField(primary_key=True)
   user_name = models.CharField(max_length=10,default=None,db_index=True)
   password = models.CharField(max_length=8,blank=False)
   created_time = models.CharField(max_length=20)

   def __str__(self):
      return self.user_name +"-" + str(self.user_id) + "-"+self.password +"-"+str(self.created_time)


class Diarylist(models.Model):
   user_id = models.IntegerField()
   diary_title = models.CharField(max_length=20)
   diary_id = models.AutoField(primary_key=True)
   created_time = models.CharField(max_length=20)
   updated_time = models.CharField(max_length=20)

   def __str__(self):
        return str(self.user_id) + " "+ self.diary_title + " "+ str(self.diary_id) + " "+ str(self.created_time)+ " "+str(self.updated_time)

class Diaryitems(models.Model):
   diary_id = models.IntegerField()
   dairy_item_id = models.AutoField(primary_key=True)
   diary_body = models.CharField(max_length=1000000)
   created_time = models.CharField(max_length=20)
   updated_time = models.CharField(max_length=20)
   title = models.CharField(max_length=50,default='')


