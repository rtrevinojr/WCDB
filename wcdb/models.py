from django.db import models

		
class Organizations(models.Model) :
	idref            = models.CharField(max_length=11, primary_key=True, unique=True)
	name             = models.TextField()
	kind             = models.TextField(blank=True, null=True)
	location         = models.TextField(blank=True, null=True)
	summary          = models.TextField(blank=True, null=True)

class People(models.Model) :
	idref            = models.CharField(max_length=11, primary_key=True, unique=True)
	name             = models.TextField()
	organizations    = models.ManyToManyField(Organizations)
	kind             = models.TextField(blank=True, null=True)
	location         = models.TextField(blank=True, null=True)
	summary          = models.TextField(blank=True, null=True)


class Crises(models.Model) :
	idref            = models.CharField(max_length=11, primary_key=True, unique=True)
	name             = models.TextField()
	organizations    = models.ManyToManyField(Organizations)
	people           = models.ManyToManyField(People)
	kind             = models.TextField(blank=True, null=True)
	date             = models.DateField(blank=True, null=True)
	time             = models.TimeField(blank=True, null=True)
	summary          = models.TextField(blank=True, null=True)
	
class List_Item(models.Model) :
	idref            = models.CharField(max_length=11)
	list_type        = models.TextField(blank=True, null=True)
	href             = models.TextField(blank=True, null=True)
	embed            = models.TextField(blank=True, null=True)
	text             = models.TextField(blank=True, null=True)
	body             = models.TextField(blank=True, null=True)
