from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class UsersMatch(models.Model):
    id_user_one= models.IntegerField()
    id_user_two= models.IntegerField()
    # 0 para espera, 1 para aceptado, 2 para rechazado
    state_user_one= models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)])
    state_user_two= models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)])


class UserAccepted(models.Model):
    id_user= models.IntegerField()
    id_user_accepted= models.IntegerField()

class UserRejected(models.Model):
    id_user= models.IntegerField()
    id_user_rejected= models.IntegerField()
