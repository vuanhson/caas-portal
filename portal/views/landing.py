from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, login

import json, requests
import os

def landing(request):
	return render(request, 'portal/landing.html')
