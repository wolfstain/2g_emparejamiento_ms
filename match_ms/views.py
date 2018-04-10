from django.shortcuts import render
from match_ms.models import *
from match_ms.serializers import *
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route,api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import views
from django.http import JsonResponse


from match_ms.calcClass import CalcClass


#EMPAREJAMIENTO

@api_view(['GET','POST'])
def match(request):
    if request.method=='POST':
        serializer=UsersMatchSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            created = UsersMatch.objects.filter(id_user_one=serializer.data['id_user_one'],id_user_two=serializer.data['id_user_two']).count()
            created2 = UsersMatch.objects.filter(id_user_one=serializer.data['id_user_two'],id_user_two=serializer.data['id_user_one']).count()
            if created == 1 and created2==0:
                obj=UsersMatch.objects.get(id_user_one=serializer.data['id_user_one'],id_user_two=serializer.data['id_user_two'])
                if 'state_user_two' in serializer.data:
                    if obj.state_user_two==0:
                        obj.state_user_two=serializer.data['state_user_two']
                    obj.save()

                    if serializer.data['state_user_two']==1:
                        rejected=UserAccepted.objects.create(id_user=obj.id_user_one, id_user_accepted=obj.id_user_two)

                    elif serializer.data['state_user_two']==2:
                        rejected=UserRejected.objects.create(id_user=obj.id_user_one, id_user_rejected=obj.id_user_two)

                return Response(serializer.data, status=status.HTTP_200_OK)
            if created == 0 and created2==1:
                obj=UsersMatch.objects.get(id_user_one=serializer.data['id_user_two'],id_user_two=serializer.data['id_user_one'])
                if 'state_user_one' in serializer.data:
                    if obj.state_user_two==0:
                        obj.state_user_two=serializer.data['state_user_one']
                    obj.save()
                    if serializer.data['state_user_two']==1:
                        rejected=UserAccepted.objects.create(id_user=obj.id_user_two, id_user_accepted=obj.id_user_one)

                    elif serializer.data['state_user_one']==2:
                        rejected=UserRejected.objects.create(id_user=obj.id_user_two, id_user_rejected=obj.id_user_one)

                return Response(serializer.data, status=status.HTTP_200_OK)
            elif created==0 and created2==0:
                obj=UsersMatch.objects.create(id_user_one=serializer.data['id_user_one'],id_user_two=serializer.data['id_user_two'], state_user_one=serializer.data['state_user_one'])
                obj.state_user_one=serializer.data['state_user_one']
                if serializer.data['state_user_one'] == 1:
                    obj.state_user_one=1
                    obj.save()
                    accepted=UserAccepted.objects.create(id_user=obj.id_user_one, id_user_accepted=obj.id_user_two)

                if serializer.data['state_user_one'] == 2:
                    obj.state_user_two=2
                    obj.save()
                    rejected=UserRejected.objects.create(id_user=obj.id_user_one, id_user_rejected=obj.id_user_two)

                obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='GET':
        queryset=UsersMatch.objects.all()
        serializer= UsersMatchSerializer(queryset,many=True)
        return Response(serializer.data)





@api_view(['GET'])
def listMatchUser(request,pk):
    queryset=UsersMatch.objects.filter(id_user_one=pk,state_user_one=1,state_user_two=1)|UsersMatch.objects.filter(id_user_two=pk,state_user_one=1,state_user_two=1)
    serializer= UsersMatchSerializer(queryset,many=True)
    return Response(serializer.data)



@api_view(['POST'])
def possibleMatch(request):
    return Response({'received data': request.data})


#USUARIOS ACEPTADOS

@api_view(['GET'])
def listUsersAccepted(request):
    queryset=UserAccepted.objects.all()
    serializer= UserAcceptedSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listUserAcceptedByUser(request,pk):
    queryset=UserAccepted.objects.filter(id_user=pk)
    serializer= UserAcceptedSerializer(queryset,many=True)
    return Response(serializer.data)


#USUARIOS RECHAZADOS

@api_view(['GET'])
def listUsersRejected(request):
    queryset=UserRejected.objects.all()
    serializer= UserRejectedSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listUserRejectedByUser(request,pk):
    queryset=UserRejected.objects.filter(id_user=pk)
    serializer= UserRejectedSerializer(queryset,many=True)
    return Response(serializer.data)

class filterUserPleasures(views.APIView):
    def post(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        element={}
        res=[]
        dic=[]
        for x in request.data:
            get_arg1 = x.get('name', None)
            get_arg2 = x.get('description', None)
            get_arg3 = x.get('user_id', None)
            get_arg4 = x.get('subcategory_id', None)
            # Any URL parameters get passed in **kw
            myClass = CalcClass(get_arg1, get_arg2, get_arg3, get_arg4, *args, **kw)
            result = myClass.subcategory()
            dic.append(result)

        element["subcategorys"]=dic
        print(element)
        return Response(element)




class UsersMatchList(ModelViewSet):
    queryset=UsersMatch.objects.all()
    serializer_class=UsersMatchSerializer

    """
    @detail_route(methods=['del'],url_path='actualizar')
    def set_state(self,request,pk=None):
        if request.method =='put':
            serializer=UsersMatchSerializer(data=request.data,context={'request':request})

            if serializer.is_valid():
                matches=UsersMatch.objects.filter(id_user_one=serializer.data['id_user_one'],id_user_two=serializer.data['id_user_two'])
                for match in matches:
                    match.state_user_two=1
                    match.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            obj=UsersMatch.objects.get(id=pk)
            serializer=UsersMatchSerializer(obj,context={'request':request})
            return Response(serializer.data)
    """
    def get_serializer_context(self):
        return {'request': self.request}

class UserAcceptedList(ModelViewSet):
    queryset=UserAccepted.objects.all()
    serializer_class=UserAcceptedSerializer

class UserAcceptedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=UserAccepted.objects.all()
    serializer_class=UserAcceptedSerializer

class UserRejectedList(ModelViewSet):
    queryset=UserRejected.objects.all()
    serializer_class=UserRejectedSerializer

class UserRejectedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=UserRejected.objects.all()
    serializer_class=UserRejectedSerializer
