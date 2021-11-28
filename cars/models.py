from django.db   import models

class Brand(models.Model):
  brandName    = models.CharField(max_length = 50)
  brandNameEng = models.CharField(max_length = 50, blank=True, default="")
  country      = models.CharField(max_length = 50, blank=True, default="")

  class Meta :
    db_table = 'brands'


class Model(models.Model):
  brand     = models.ForeignKey('Brand', on_delete = models.CASCADE)
  modelName = models.CharField(max_length = 50)

  class Meta:
    db_table = 'models'


class Tire(models.Model):
  width        = models.PositiveIntegerField()
  aspect_ratio = models.PositiveIntegerField()
  wheel_size   = models.PositiveIntegerField()

  class Meta:
    db_table = 'tires'


class Trim(models.Model):
  model      = models.ForeignKey('Model', on_delete = models.CASCADE, null=True)
  front_tire = models.ForeignKey('cars.Tire', on_delete = models.CASCADE, related_name = "front_trims")
  rear_tire  = models.ForeignKey('cars.Tire', on_delete = models.CASCADE, related_name = "rear_trims")
  user       = models.ManyToManyField('users.User', through = 'UserTrim')
  trimName   = models.CharField(max_length = 50)


  class Meta:
    db_table = 'trims'


class UserTrim(models.Model):
  user = models.ForeignKey('users.User', on_delete = models.CASCADE)
  trim = models.ForeignKey('Trim', on_delete = models.CASCADE)

  class Meta:
    db_table = 'users_trims'