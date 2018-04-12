from rest_framework import serializers
from match_ms.models import *
from rest_framework.validators import UniqueTogetherValidator
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class UsersMatchSerializer(serializers.ModelSerializer):

    """
    def validate(self, data):
        request = self.context.get('request')
        users_matches=UsersMatch.objects.filter(id_user_one=data['id_user_one'],id_user_two=data['id_user_two'])|UsersMatch.objects.filter(id_user_one=data['id_user_two'],id_user_two=data['id_user_one'])
        if request.method!='PUT':
            if len(users_matches)> 0:
                for match in users_matches:
                    match.state_user_two=1
                    match.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return data
        else:
            if len(user_one)==0 or len(user_two)==0:
                raise serializers.ValidationError("Usuarios no se han cruzado")
        return data

    def create(self,validate_data):
        obj=UsersMatch.objects.create(**validate_data)
        obj.save()
        obj2=UserAccepted.objects.create(id_user=validate_data['id_user_one'],id_user_accepted=validate_data['id_user_two'])
        obj.state_user_one=1
        obj.save()
        return obj



    def create(self,validate_data):

        created = UsersMatch.objects.filter(id_user_one=validate_data['id_user_one'],id_user_two=validate_data['id_user_two']).count()
        created2 = UsersMatch.objects.filter(id_user_one=validate_data['id_user_two'],id_user_two=validate_data['id_user_one']).count()
        if created == 1 and created2==0:
            obj=UsersMatch.objects.get(id_user_one=validate_data['id_user_one'],id_user_two=validate_data['id_user_two'])
            if 'state_user_two' in validate_data:
                obj.state_user_two=validate_data['state_user_two']
                obj.save()
                if validate_data['state_user_two']==2:
                    rejected=UserRejected.objects.create(id_user=obj.id_user_one, id_user_rejected=obj.id_user_two)
        if created == 0 and created2==1:
            obj=UsersMatch.objects.get(id_user_one=validate_data['id_user_two'],id_user_two=validate_data['id_user_one'])
            if 'state_user_one' in validate_data:
                obj.state_user_two=validate_data['state_user_one']
                obj.save()
                if validate_data['state_user_one']==2:
                    rejected=UserRejected.objects.create(id_user=obj.id_user_two, id_user_rejected=obj.id_user_one)
        elif created==0 and created2==0:
            obj=UsersMatch.objects.create(**validate_data)
            obj.state_user_one=validate_data['state_user_one']
            if validate_data['state_user_one'] == 2:
                obj.state_user_two=2
                obj.save()
                rejected=UserRejected.objects.create(id_user=obj.id_user_one, id_user_rejected=obj.id_user_two)

            obj.save()
        return obj
    """
    class Meta:
        model = UsersMatch
        fields = '__all__'


class UserAcceptedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccepted
        fields = '__all__'
        read_only_fields=('id_user','id_user_accepted')



class UserRejectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRejected
        fields = '__all__'
        read_only_fields=('id_user','id_user_rejected')
