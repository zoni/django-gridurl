from gridurls.models import Url
from django.http import HttpResponse, HttpResponseRedirect
import hashlib, string, random
from uuid import uuid4
import settings

def index(request):
	# Simply redirect to project homepage until a proper index page is written
	return HttpResponseRedirect("http://zoni.nl/django-gridurl/")

def register(request, name):
	# Register can only be used with POST request method
	if request.method != "POST":
		response = HttpResponse(mimetype='text/plain', status=405)
		response['Allow'] = "POST"
		response.write("Method " + request.method + " not allowed. Allowed methods: POST")
		return response

	response = HttpResponse(mimetype='text/plain')

	if 'password' in request.POST.keys():
		password = request.POST['password']
	else:
		password = ''

	if 'url' in request.POST.keys():
		url = request.POST['url']
	else:
		url = ''

	# Try and get <name> from the database. If <name> does not exist, create it
	# with the values passed in the request. This makes registering custom name+password
	# combinations possible
	try:
		r = Url.objects.get(name=name)
	except Url.DoesNotExist:
		# Generate random password salt consisting of salt_length (Configured in settings.py)
		# characters in the range A-Z,a-z,0-9
		salt = "".join([random.choice(string.letters+string.digits) for x in range(settings.SALT_LENGTH)])
		hash = hashlib.sha256(salt + password).hexdigest()

		r = Url(name=name, password_salt=salt, password_hash=hash, inworld_url=url)
		r.save()
		response.write("OK")
		return response

	hash = hashlib.sha256(r.password_salt + password).hexdigest()
	if hash == r.password_hash:
		response.write("OK")
		r.inworld_url = url
		r.save()
	else:
		response['status'] = 401
		response.write("Password incorrect")

	return response

def get(request, name):
	response = HttpResponse(mimetype='text/plain')
	
	try:
		r = Url.objects.get(name=name)
	except Url.DoesNotExist:
		response['status'] = 404
		response.write("{0} not found".format(name))
		return response
	
	if r.inworld_url == "":
		return HttpResponse("{0} currently disabled".format(name), mimetype='text/plain', status=503)
	else:
		response.write(r.inworld_url)
		return response

def go(request, name):
	try:
		r = Url.objects.get(name=name)
	except Url.DoesNotExist:
		return HttpResponse("{0} not found".format(name), mimetype='text/plain', status=404)
	
	if r.inworld_url == "":
		return HttpResponse("{0} currently disabled".format(name), mimetype='text/plain', status=503)
	else:
		return HttpResponseRedirect(r.inworld_url)

def generate(request):
	name = str(uuid4())
	# Generate random password salt consisting of salt_length (Configured in settings.py)
	# characters in the range A-Z,a-z,0-9
	salt = "".join([random.choice(string.letters+string.digits) for x in range(settings.SALT_LENGTH)])
	# Same for the actual password
	password = "".join([random.choice(string.letters+string.digits) for x in range(settings.PASSWORD_LENGTH)])
	hash = hashlib.sha256(salt + password).hexdigest()

	r = Url(name=name, password_salt=salt, password_hash=hash)
	r.save()
	
	response = HttpResponse(mimetype='text/plain')
	response.write("OK;{0};{1}".format(name,password))
	return response

