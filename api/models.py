from django.db import models


class User(models.Model):
    username = models.CharField(null=False,max_length=45)
    gender = models.CharField(null=False,max_length=1)
    register_date = models.CharField(blank=True,null=True,max_length=20)
    current_ip = models.CharField(blank=True,null=True,max_length=45)
    register_ip = models.CharField(blank=True,null=True,max_length=45)
    setting = models.ForeignKey('Setting', models.DO_NOTHING, blank=True, null=True)
    password = models.CharField(max_length=45)

    def __str__(self):
        return self.username


class Setting(models.Model):
    email = models.CharField(null=True, max_length=45)
    phone = models.CharField(null=True, max_length=25)
    language = models.CharField(default='English', max_length=45)
    themes = models.ForeignKey('Themes', models.DO_NOTHING)


class Country(models.Model):
    name = models.CharField(max_length=20, null=False)


class Themes(models.Model):
    name = models.CharField(null=False, max_length=25)
    description = models.CharField(max_length=25, null=False)



class Category(models.Model):
    name = models.CharField(max_length=45, null=False)


class City(models.Model):
    name = models.CharField(max_length=45, null=False)
    country = models.ForeignKey('Country', models.DO_NOTHING)


class ThemePhoto(models.Model):
    link = models.CharField(max_length=255, null=False)


class Advertiser(models.Model):
    name = models.CharField(max_length=50, blank=True, null=False)
    email = models.CharField(max_length=50, blank=True, null=False)
    password = models.CharField(max_length=1024, null=False)
    budget = models.FloatField(null=False)
    phone = models.CharField(max_length=20, null=False)


class TypedWords(models.Model):
    sentence = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)


class TargetedAge(models.Model):
   min_age = models.IntegerField(null=False)
   max_age = models.IntegerField(null=False)
   advertisement = models.ForeignKey('Advertisement', models.DO_NOTHING)



class Target(models.Model):
   targeted_age = models.ForeignKey('TargetedAge', models.DO_NOTHING)
   country = models.ForeignKey('Country', models.DO_NOTHING)
   city = models.ForeignKey('City', models.DO_NOTHING)


class Advertisement(models.Model):
   name = models.CharField(max_length=60,null=False)
   description = models.CharField(max_length=255,null=False)
   pub_date = models.DateField(null=False)
   target = models.ForeignKey('Target', models.DO_NOTHING, null=True)
   acceptance_id = models.IntegerField(null=True)
   rejection_id = models.IntegerField(null=True)
   advertiser = models.ForeignKey('Advertiser',models.DO_NOTHING, null=True)


class AcceptedAdvertisement(models.Model):
    accept_date = models.DateField(null=False)
    advertisement = models.ForeignKey('Advertisement', models.DO_NOTHING, null=True)
    advertiser = models.ForeignKey('Advertiser', models.DO_NOTHING)


class RejectedAdvertisement(models.Model):
    reason = models.CharField(max_length=255, null=False)
    date = models.DateField(null=False)
    advertisement = models.ForeignKey('Advertisement', models.DO_NOTHING, null=True)
    advertiser = models.ForeignKey('Advertiser', models.DO_NOTHING)




