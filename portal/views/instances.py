from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import json, requests
from .authentication import *

def instances(request):
	if check_auth(request) == False:
		return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})

	compute_detail_url = 'http://' + IP[0] + ':8774/v2.1/servers/detail'
	compute_detail_res = requests.get(compute_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	image_detail_url = 'http://' + IP[0] + ':9292/v2/images'
	image_detail_res = requests.get(image_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	flavor_detail_url = 'http://' + IP[0] + ':8774/v2.1/flavors'
	flavor_detail_res = requests.get(flavor_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	if compute_detail_res.status_code == 200:
		context = {
			'user_name' : request.session.get('user_name','Not logged in'),
			'data': compute_detail_res.json(),
			'image_detail' : image_detail_res.json(),
			'flavor_detail' : flavor_detail_res.json()
		}
		return render(request, 'portal/instances.html',context)
	return render(request, 'portal/instances.html')
def instance_action(request, action, instance_id):
	if check_auth(request) == False:
		return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
	null = None
	action_url = 'http://' + IP[0] + ':8774/v2.1/servers/' + instance_id + '/action'
	if action == 'stop' or action == 'start':
		action_exec = requests.post(action_url, data = json.dumps({"os-" + action : null}) ,headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if action == 'suspend' or action == 'resume' or action == 'confirmResize':
		action_exec = requests.post(action_url, data = json.dumps({action : null}) ,headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if action == 'delete':
		action_url = 'http://' + IP[0] + ':8774/v2.1/servers/' + instance_id
		action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	return HttpResponseRedirect(reverse('portal:instances'))

def mgr_instances(request):
	compute_detail_url = 'http://' + IP[0] + ':8774/v2.1/servers/detail?all_tenants=1'
	compute_detail_res = requests.get(compute_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	image_detail_url = 'http://' + IP[0] + ':9292/v2/images'
	image_detail_res = requests.get(image_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	flavor_detail_url = 'http://' + IP[0] + ':8774/v2.1/flavors'
	flavor_detail_res = requests.get(flavor_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if compute_detail_res.status_code == 200:
		context = {
			'user_name' : request.session.get('user_name','Not logged in'),
			'data': compute_detail_res.json(),
			'image_detail' : image_detail_res.json(),
			'flavor_detail' : flavor_detail_res.json()
		}
		return render(request, 'portal/mgr_instances.html',context)
	return render(request, 'portal/mgr_instances.html')

def mgr_instance_action(request, action, instance_id):
	if check_auth(request) == False:
		return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
	null = None
	action_url = 'http://' + IP[0] + ':8774/v2.1/servers/' + instance_id + '/action'
	if action == 'stop' or action == 'start':
		action_exec = requests.post(action_url, data = json.dumps({"os-" + action : null}) ,headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if action == 'suspend' or action == 'resume':
		action_exec = requests.post(action_url, data = json.dumps({action : null}) ,headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	if action == 'delete':
		action_url = 'http://' + IP[0] + ':8774/v2.1/servers/' + instance_id
		action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	return HttpResponseRedirect(reverse('portal:mgr_instances'))
