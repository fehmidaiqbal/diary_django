from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from diary_api.models import Diaryitems, Diarylist, User
from diary_api.serializers import DiaryitemsSerializer,DiarylistSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import datetime


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
       input = request.data
       input["created_time"] = "7-12-2022"
       serializer = UserSerializer(data=input)
       valid = serializer.is_valid()
       if valid == False:
            return JsonResponse({"error":"invalid data"})
       
       userName = input.get('user_name',' ')
       password = input.get('password',0)
        # check user name in users table
       userExist = User.objects.filter(user_name__exact=userName).exists()
       if(userExist == True):
            response = {"error":"user found, please login"}
            return JsonResponse(response,safe=False) 
       serializer.save()
    return JsonResponse(serializer.data,status = 201)

        # proceed user registration when userName not exist in user table 
        # when exist throw user alredy registered error 
        # when don't exist check for userName have no alphabetics and must be 10 in length 
        # when userName is valid insert into user table and return user id 
    response1 = {'error':'method not supported'}
    return JsonResponse(response1,safe=False)


@api_view(['POST'])
def login_user(request):
    
    input = request.data
    userName = input.get("user_name",' ')
    password = input.get("password",0)
    
    # validate request format
    if len(userName) == 0 or len(password) == 0 :
        return JsonResponse({"error":"invalid input"})

    if len(userName) != 10:
        return JsonResponse({"error":"user name is invalid"})

    #validate the password
    if len(password) != 6:
        return JsonResponse({"error":"password is  invalid"})

    valid = userName.isdigit()
    if valid == False:
        return JsonResponse({"error":"user name must not have any alphabetics"})

    #check user_id existance in the table

    isExist = User.objects.filter(user_name__exact = userName).exists()

    if isExist == False:
        return JsonResponse({"error":"user not found"})

    dbRow = User.objects.filter(user_name__exact = userName).values()
    dbData = dbRow.first()
    dbPassword = dbData["password"]

    # validate user name and password with DB data 
    if dbPassword == password :
        dbData["status"] = 1 
        return JsonResponse(dbData,status = 200)
    
    # if not throw "error:invalid user//re-enter correct password"
    return JsonResponse({"error":"password not matched"})


@api_view(['POST'])
def create_diary(request):
    # validate request json 
    input = request.data 
    userId = input.get('user_id',0)
    if len(userId) == 0:
        return JsonResponse(getError("userId missing in request"))

    userExist = User.objects.filter(user_id__exact=userId).exists()
    if userExist == False:
        return JsonResponse(getError("user not found"))
 
    diaryTitle = input.get('diary_title',' ')
    if len(diaryTitle) == 0:
        return JsonResponse(getError("diary title is missing in request"))

    # when input validation is right insert 
    currentTime = datetime.datetime.now()
    dairyListObj = Diarylist(user_id = userId,diary_title = diaryTitle, created_time= currentTime ,updated_time = currentTime) 
    dairyListObj.save()

    myDic = getDiaryListDicFromObj(dairyListObj)
    # return inserted row 
    return JsonResponse({"id":dairyListObj.diary_id},status = 201,safe=False)
   
    
def getDiaryListDicFromObj(diaryListObj):
    diaryDic = {}
    diaryDic['diary_id'] = diaryListObj.diary_id
    diaryDic['diary_title'] = diaryListObj.diary_title
    diaryDic['created_time'] = diaryListObj.created_time
    diaryDic['updated_time'] = diaryListObj.updated_time
    return diaryDic

def getError(errorMsg):
  return {"error":errorMsg}


@api_view(['POST'])
def Update_diary(request):
    input = request.data
    userId = input.get("user_id",0)
    diaryTitle = input.get("diary_title",' ')
    diaryId = input.get("diary_id",0)
    currentTime = datetime.datetime.now()
  
    if userId == '0':
        return JsonResponse(getError("userId missing in request"))

    if diaryId == '0':
        return JsonResponse(getError("diaryId is missing in request"))
    

    dairyListObjU = Diarylist(user_id = userId,diary_title = diaryTitle, diary_id = diaryId, created_time = currentTime,updated_time = currentTime ) 
    dairyListObjU.save()
    
    return JsonResponse({"Message":"Successfully Updated"},status = 201,safe=False)
    
@api_view(['DELETE'])
def delete_diary(request):
    input = request.data
    diaryId = input.get("diary_id",0)
    
    if  diaryId == 0:
         return JsonResponse(getError("diary_id is missing"))
    
    del_queryset = Diarylist.objects.filter(diary_id__exact = diaryId).delete()
        
    return JsonResponse({"Msg":"Selected diary deleted"},status=200) 



@api_view(['GET'])
def get_lists_diary(request):
    myInputs = request.query_params
    req_user_id = myInputs.get('user_id',0)
    searchString = myInputs.get('search_key',' ')

    ##SEARCH QUERY

    if len(searchString) == 0:
        queryList = Diarylist.objects.filter(user_id__exact = req_user_id).values()
        responseList = []
        for item in queryList:
            responseList.append(item)
        return JsonResponse(responseList,status=200,safe=False)

    else: 
        queryList = Diarylist.objects.filter(user_id__exact = req_user_id).filter(diary_title__contains = searchString).values()
        responseList = []
        for item in queryList:
            responseList.append(item)
        return JsonResponse(responseList,status=200,safe=False)
        
@api_view(['POST'])
def create_diary_item(request):
    input = request.data
    diaryId = input.get("diary_id",0)
    diaryItemTitle = input.get("diary_item_title",' ')
    diaryItemBody = input.get("diary_item_body",' ')
    time = datetime.datetime.now()

    if diaryId == 0:
        return JsonResponse(getError("diary_id is missing"))

    if len(diaryItemTitle) == 0:
        return JsonResponse(getError("diaryItemTitle is missing"))

    if len(diaryItemBody) == 0:
        return JsonResponse(getError("diaryItemBody is missing"))

    diaryItemObjC = Diaryitems(title = diaryItemTitle, updated_time = time, diary_body = diaryItemBody, diary_id = diaryId)
    diaryItemObjC.save()

    return JsonResponse({"diaryItemId":diaryItemObjC.dairy_item_id},status = 201,safe=False)
    
@api_view(['POST'])
def Update_diary_item(request):
    input = request.data
    diaryId = input.get("diary_id",0)
    diaryItemTitle = input.get("diary_item_title",' ')
    diaryItemBody = input.get("diary_item_body",' ')
    diaryItemId = input.get("dairy_item_id",0)

    time = datetime.datetime.now()

    if  diaryId == 0:
        return JsonResponse(getError("diary_id is missing"))
    if  diaryItemId == 0:
        return JsonResponse(getError("dairy_item_id is missing"))    
    

    diaryItemObjU = Diaryitems(title = diaryItemTitle, updated_time = time, dairy_item_id =diaryItemId ,  diary_body = diaryItemBody, diary_id = diaryId)
    diaryItemObjU.save()

    return JsonResponse({"Message":"Successfully Updated"},status = 201,safe=False)


@api_view(['GET'])
def get_itemlist_diary(request):
    if request.method == 'GET':
        input = request.query_params  
        diaryId = input.get('diary_id',0) 
        searchitem = input.get('search_key',' ')
        
        if  diaryId == 0:
         return JsonResponse(getError("diary_id is missing"))

    ##SEARCH QUERY
    if len(searchitem) == 0:
        querySet = Diaryitems.objects.filter(diary_id__exact = diaryId).values()
        responses = []
        for item in querySet:
            responses.append(item)
        return JsonResponse(responses,status = 200,safe=False)
    else:
        querySet = Diaryitems.objects.filter(diary_id__exact = diaryId).filter(title__contains = searchitem).values()
        responses = []
        for item in querySet:
            responses.append(item)
        return JsonResponse(responses,status = 200,safe=False)

@api_view(['DELETE'])
def del_diary_Item(request):
        input = request.data  
        diaryItemId = input.get('dairy_item_id',0)
       
        if  diaryItemId == 0:
         return JsonResponse(getError("dairy_item_id is missing"))

        del_queryset = Diaryitems.objects.filter(dairy_item_id__exact = diaryItemId).delete()
        
        return JsonResponse({"Msg":"Selected row deleted"},status=200)    


        
        