from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests, yaml
import os

from .authentication import *

def stacks(request):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    stack_detail_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks'
    stack_detail_res = requests.get(stack_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if stack_detail_res.status_code == 200:
        context = {
            'user_name' : request.session.get('user_name','Not logged in'),
            'data': stack_detail_res.json()
        }
        return render(request, 'portal/stacks.html',context)
    return render(request, 'portal/stacks.html')

def stack_action(request, action, stack_name, stack_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    null = None
    stack_template_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id + '/template'
    stack_template_res = requests.get(stack_template_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    if action == 'delete':
        action_url = 'http://'+ IP[0] + ':8004/v1/'+ request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id
        action_exec = requests.delete(action_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    if action == 'suspend' or action == 'resume' or action == 'check':
        action_url = 'http://'+ IP[0] + ':8004/v1/'+ request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id + '/actions'
        action_exec = requests.post(action_url, data = json.dumps({action : null}) ,headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    
    if action == 'download':
        # json_str = json.dumps(stack_template_res.json(),sort_keys=True, indent=4)
        yaml_str=yaml.dump(yaml.load(json.dumps(stack_template_res.json())), default_flow_style=False)
        response = HttpResponse(yaml_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename='+stack_name+'.yml'
        return response

    if action == 'update':
        parameters = {}
        for key in stack_template_res.json().get('parameters',{}):
            parameters[key] = request.POST.get(key, False)
        payload = {}
        payload['parameters'] = parameters
        payload['template'] = stack_template_res.json()
        # payload['stack_name'] = stack_name

        stack_exec_url = 'http://'+ IP[0] + ':8004/v1/'+ request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id 
        stack_update_exec = requests.patch(stack_exec_url, data=json.dumps(payload), headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )


    return HttpResponseRedirect(reverse('portal:stacks'))



def stack_detail(request, stack_name, stack_id):
    if check_auth(request) == False:
        return render(request,'portal/login.html',{'login_status': "401: Session Expired or you are not logged in",})
    stack_detail_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id
    stack_detail_res = requests.get(stack_detail_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    stack_resource_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id + '/resources'
    stack_resource_res = requests.get(stack_resource_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )
    stack_template_url = 'http://'+ IP[0] + ':8004/v1/' + request.session.get('project_id','Not logged in') + '/stacks/' + stack_name + '/' + stack_id + '/template'
    stack_template_res = requests.get(stack_template_url, headers={"X-Auth-Token":request.session.get('X_Auth_Token', 'Not logged in')} )

    context = {
        'stack_detail' : stack_detail_res.json(),
        'stack_resource' : stack_resource_res.json(),
        'stack_template' : stack_template_res.json()
    }
    return render(request, 'portal/stack_details.html',context)



