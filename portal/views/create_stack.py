from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import json, requests

from .authentication import *

def create_stack(request):
	if check_auth(request) == False:
	    return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
	
	flavor_detail_url = 'http://'+ IP[0] + ':8774/v2.1/flavors/detail'
	flavor_detail_res = requests.get(flavor_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	image_detail_url = 'http://'+ IP[0] + ':9292/v2/images'
	image_detail_res = requests.get(image_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	keypair_detail_url = 'http://'+ IP[0] + ':8774/v2.1/os-keypairs'
	keypair_detail_res = requests.get(keypair_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
	network_detail_url = 'http://'+ IP[0] + ':9696/v2.0/networks'
	network_detail_res = requests.get(network_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )


	context = {
	    'flavor_list': flavor_detail_res.json(),
	    'image_list' : image_detail_res.json(),
	    'keypair_list' : keypair_detail_res.json(),
	    'network_list' :network_detail_res.json()
	}


	return render(request, 'portal/create_stack.html', context)
def stack_exec(request):
	stack_exec_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks'
	
	if request.POST.get('keypair', False) == 'true':
		disable_rollback = False
	else: 
		disable_rollback = True

	if request.POST.get('stack', False) == 'galeradb':
		payload = {
		    "disable_rollback": disable_rollback,
		    "parameters": {
		        "key_name": request.POST.get('keypair', False),
		        "image" : request.POST.get('image', False),
		        "flavor" : request.POST.get('flavor', False),
		        "network" : request.POST.get('network', False),
		        "db_password" : request.POST.get('db_password', False)
		    },
		    "template_url": "https://s3-ap-northeast-1.amazonaws.com/vusonhust/heat-template/galera.yml",
		    "stack_name": request.POST.get('stack_name', False),
		    "timeout_mins": request.POST.get('stack_timeout', False)
		}
		stack_add_exec = requests.post(stack_exec_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	if request.POST.get('stack', False) == 'HAProxy':
		payload = {
		    "disable_rollback": disable_rollback,
		    "parameters": {
		        "key_name": request.POST.get('keypair', False),
		        "image" : request.POST.get('image', False),
		        "flavor" : request.POST.get('flavor', False),
		        "network" : request.POST.get('network', False)
		    },
		    "template_url": "https://s3-ap-northeast-1.amazonaws.com/vusonhust/heat-template/HAProxyLB.yaml",
		    "stack_name": request.POST.get('stack_name', False),
		    "timeout_mins": request.POST.get('stack_timeout', False)
		}
		stack_add_exec = requests.post(stack_exec_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

	if request.POST.get('stack', False) == 'GlusterFS':
		payload = {
		    "disable_rollback": disable_rollback,
		    "parameters": {
		        "key_name": request.POST.get('keypair', False),
		        "image" : request.POST.get('image', False),
		        "flavor" : request.POST.get('flavor', False),
		        "network" : request.POST.get('network', False)
		    },
		    "template_url": "https://s3-ap-northeast-1.amazonaws.com/vusonhust/heat-template/GlusterFS4_centos_distributed.yaml",
		    "stack_name": request.POST.get('stack_name', False),
		    "timeout_mins": request.POST.get('stack_timeout', False)
		}
		stack_add_exec = requests.post(stack_exec_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )


	if request.POST.get('stack', False) == 'WP':
		payload = {
		    "disable_rollback": disable_rollback,
		    "parameters": {
		        "key_name": request.POST.get('keypair', False),
		        "image" : request.POST.get('image', False),
		        "flavor" : request.POST.get('flavor', False),
		        "network" : request.POST.get('network', False),
		        "db_name" : request.POST.get('db_name', False),
		        "db_password" : request.POST.get('db_password', False)
		    },
		    "template_url": "https://s3-ap-northeast-1.amazonaws.com/vusonhust/heat-template/wordpress.yml",
		    "stack_name": request.POST.get('stack_name', False),
		    "timeout_mins": request.POST.get('stack_timeout', False)
		}
		stack_add_exec = requests.post(stack_exec_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )


	return HttpResponseRedirect(reverse('portal:stacks'))