from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
	code = models.CharField(max_length = 50, null = False, blank = False)
	quantity = models.IntegerField(null = False , blank = False)
	description = models.CharField(max_length = 100, null = False, blank = False)


class Company(models.Model):
	ruc = models.IntegerField(null = False, blank = False)
	name = models.CharField(max_length = 100, null = False, blank = False) 
	address = models.CharField(max_length = 200, null = True, blank = True)


class Client(User):
	company = models.ForeignKey(Company, null = False, blank = False)

class Employee(models.Model):
	code = models.CharField(max_length = 50, null = False, blank = False)
	name = models.CharField(max_length = 100, null = False, blank = False)
	company = models.ForeignKey(Company, null = False, blank = False)
	time = models.IntegerField()

class HistoryFormats(models.Model):
	requeriment = models.IntegerField(null = False, blank = False) #El numero del requerimiento en el cual pertenece
#	content = models.TextField("How do a type pdf")
	company = models.ForeignKey(Company, null = False, blank = False) #Clase Compañia, el formato es completado de una compañia
	date_time = models.DateTimeField() #La fecha en el que se hizo la modificación del formato


class Meeting(models.Model):
	date = models.DateTimeField()
	title = models.CharField(max_length = 100, null = True, blank = True)
 
class Accident(models.Model):	
	code = models.CharField(max_length= 50, null = False, blank = False)
	title = models.CharField(max_length=100, null = False, blank = False)  
	content = models.TextField(null = True, blank = True)
#	type_accident = models.IntegerField("type", choises=TYPE, default = )
	company = models.ForeignKey(Company, null = False, blank = False)


class Task(models.Model):
	code = models.CharField(max_length = 50, null = False, blank = False)
	title = models.CharField(max_length=100, null = True, blank = True)
	date_time = models.DateTimeField()
	company = models.ForeignKey(Company, null = False, blank = False)
	type_calendar = models.IntegerField(null = False, blank = False)
	meeting	= models.ForeignKey(Meeting, null = True, blank = True)
	charge = models.CharField(max_length = 100, null = False, blank = False)  # responsable
	content = models.TextField(null = False, blank = False) #contenido 
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	#Falta añadir evidencia de tipo imagen
	#status = models.IntegerField("status", choises = STATUS, default = ) 
	expiration = models.DateTimeField()

class Report(models.Model):
	code = models.CharField(max_length = 50, null = False, blank = False)
	title = models.CharField(max_length=100, null = True, blank = True)
	content = models.TextField(null = True, blank = True)
	company = models.ForeignKey(Company, null = False, blank = False)

class Format(models.Model):
	requeriments = models.IntegerField(null = False, blank = False)
	document = models.FileField(upload_to = "archivos/%Y/%m/%d", null = True, blank = True)
	company = models.ForeignKey(Company, null = False, blank = False)

class Calendar(models.Model):
	company = models.ForeignKey(Company, null = False, blank = False)
#	type_calendar = models.IntegerField("type", choises =TYPE, default = )	

class UseProduct(models.Model):
	task = models.ForeignKey(Task, null = False, blank = False)
	product = models.ForeignKey(Product, null = False, blank = False)
	quantity = models.IntegerField(null = False, blank = False)

class Work(models.Model):
	employee = models.ForeignKey(Employee, null = False , blank = False)
	task = models.ForeignKey(Task, null = False, blank = False)
	time = models.DateTimeField()