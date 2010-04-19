from gridurls.models import Url
from django.http import HttpResponse, HttpResponseRedirect
import hashlib, string, random, re
from uuid import uuid4
import settings

def index(request):
	# Simply redirect to project homepage until a proper index page is written
	return HttpResponseRedirect("http://zoni.nl/django-gridurl")

def update(request, name):
	# Update can only be used with POST request method
	if request.method != "POST":
		response = HttpResponse(mimetype='text/plain', status=405)
		response['Allow'] = "POST"
		response.write("Method " + request.method + " not allowed. Allowed methods: POST")
		return response

	response = HttpResponse(mimetype='text/plain')

	# Assume blank password if omitted
	if 'password' in request.POST.keys():
		password = request.POST['password']
	else:
		password = ''

	try:
		r = Url.objects.get(name=name)
	except Url.DoesNotExist:
		response['status'] = 404
		response.write("Requested name not found")
		return response

	hash = hashlib.sha256(r.password_salt + password).hexdigest()
	if hash == r.password_hash:
		if 'url' in request.POST.keys():
			r.inworld_url = request.POST['url']
		if 'newpassword' in request.POST.keys():
			if request.POST['newpassword'] == "__GENERATE__":
				newpassword = "".join([random.choice(string.letters+string.digits) for x in range(settings.PASSWORD_LENGTH)])
			else:
				newpassword = request.POST['newpassword']
			r.password = hashlib.sha256(r.salt + newpassword).hexdigest()

		r.save()
		response.write("OK")
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
		response.write("Requested name not found")
		return response

	if r.inworld_url == "":
		return HttpResponse("'{0}' is currently disabled".format(name), mimetype='text/plain', status=503)
	else:
		response.write(r.inworld_url)
		return response

def go(request, name):
	try:
		r = Url.objects.get(name=name)
	except Url.DoesNotExist:
		return HttpResponse("Requested name not found", mimetype='text/plain', status=404)

	if r.inworld_url == "":
		return HttpResponse("'{0}' is currently disabled".format(name), mimetype='text/plain', status=503)
	else:
		return HttpResponseRedirect(r.inworld_url)

def register(request):
	response = HttpResponse(mimetype='text/plain')

	# Get name from POST values if present, generate unique ID used as name otherwise
	if request.method == "POST" and 'name' in request.POST.keys():
		name = request.POST['name']
	else:
		name = str(uuid4())
	# Get password from POST values if present, generate random one otherwise
	if request.method == "POST" and 'password' in request.POST.keys():
		password = request.POST['password']
	else:
		password = "".join([random.choice(string.letters+string.digits) for x in range(settings.PASSWORD_LENGTH)])
	# And for the url, blank if not passed along in the request
	if request.method == "POST" and 'url' in request.POST.keys():
		url = request.POST['url']
	else:
		url = ""

	if Url.objects.filter(name=name).count() > 0:
		response['status'] = 403
		response.write("{0} is already registered".format(name))
	# Allow only a-z, A-Z ,0-9, _ and - characters in name
	elif re.search(r'[^\w-]+', name) != None:
		response['status'] = 403
		response.write("'{0}' contains illegal characters. Only [a-zA-Z0-9-_] allowed".format(name))
	else:
		# Generate random password salt consisting of salt_length (Configured in settings.py)
		# characters in the range A-Z,a-z,0-9
		salt = "".join([random.choice(string.letters+string.digits) for x in range(settings.SALT_LENGTH)])
		# Compute the hash of the salt+password
		hash = hashlib.sha256(salt + password).hexdigest()

		r = Url(name=name, password_salt=salt, password_hash=hash, inworld_url=url)
		r.save()
		
		response.write("OK;{0};{1}".format(name,password))

	return response

