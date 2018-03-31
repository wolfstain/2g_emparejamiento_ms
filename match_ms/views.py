from django.shortcuts import render
from match_ms.models import *
from match_ms.serializers import *
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route,api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

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
                    obj.state_user_two=serializer.data['state_user_two']
                    obj.save()
                    if serializer.data['state_user_two']==2:
                        rejected=UserRejected.objects.create(id_user=obj.id_user_one, id_user_rejected=obj.id_user_two)

                return Response(serializer.data, status=status.HTTP_200_OK)
            if created == 0 and created2==1:
                obj=UsersMatch.objects.get(id_user_one=serializer.data['id_user_two'],id_user_two=serializer.data['id_user_one'])
                if 'state_user_one' in serializer.data:
                    obj.state_user_two=serializer.data['state_user_one']
                    obj.save()
                    if serializer.data['state_user_one']==2:
                        rejected=UserRejected.objects.create(id_user=obj.id_user_two, id_user_rejected=obj.id_user_one)

                return Response(serializer.data, status=status.HTTP_200_OK)
            elif created==0 and created2==0:
                obj=UsersMatch.objects.create(id_user_one=serializer.data['id_user_one'],id_user_two=serializer.data['id_user_two'], state_user_one=serializer.data['state_user_one'])
                obj.state_user_one=serializer.data['state_user_one']
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

# Create your views here.

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
