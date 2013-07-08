from django.db import models

		
class Organizations(models.Model) :
	idref            = models.CharField(max_length=11)
	name             = models.TextField()
	kind             = models.TextField()
	location         = models.TextField()
	summary          = models.TextField()

class People(models.Model) :
	idref            = models.CharField(max_length=11)
	name             = models.TextField()
	organizations    = models.ManyToManyField(Organizations)
	kind             = models.TextField()
	location         = models.TextField()
	summary          = models.TextField()


class Crises(models.Model) :
	idref            = models.CharField(max_length=11)
	name             = models.TextField()
	organizations    = models.ManyToManyField(Organizations)
	people           = models.ManyToManyField(People)
	kind             = models.TextField()
	date             = models.DateField()
	time             = models.TimeField()
	summary          = models.TextField()
	
class List_Item(models.Model) :
	idref            = models.CharField(max_length=11)
	list_type        = models.TextField()
	href             = models.TextField()
	embed            = models.TextField()
	text             = models.TextField()
	body             = models.TextField()
