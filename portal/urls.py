from django.urls import path, include, re_path
from . import views

app_name = 'portal'
urlpatterns = [
	path('', views.landing, name = 'landing'),
	path('login_system/', views.login_system, name = 'login_system'),
	path('register/', views.register, name = 'register'),
	path('logout_system/', views.logout_system, name = 'logout_system'),
	path('home/', views.home, name = 'home'),

	path('instances/', views.instances, name = 'instances'),
	path('instances/<action>/<instance_id>/', views.instance_action, name = 'instance_action'),

	path('volumes/', views.volumes, name = 'volumes'),
	path('volumes/<action>/<volume_id>/', views.volume_action, name = 'volume_action'),

	path('images/', views.images, name = 'images'),
	path('images/<action>/<image_id>/', views.image_action, name = 'image_action'),

	path('keypairs/', views.keypairs, name = 'keypairs'),
	path('keypairs/<action>/<keypair_name>/', views.keypair_action, name = 'keypair_action'),

	path('networks/', views.networks, name = 'networks'),
	path('networks/<action>/<network_id>/', views.network_action, name = 'network_action'),

	path('flavors/', views.flavors, name = 'flavors'),
	path('flavors/<action>/<flavor_id>/', views.flavor_action, name = 'flavor_action'),

	path('stacks/', views.stacks, name = 'stacks'),
	path('create_stack/', views.create_stack, name = 'create_stack'),
	path('create_stack/exec', views.stack_exec, name = 'stack_exec'),
	path('stacks/detail/<stack_name>/<stack_id>/', views.stack_detail, name = 'stack_detail'),
	path('stacks/<action>/<stack_name>/<stack_id>/', views.stack_action, name = 'stack_action'),
	# Management site URLs
	path('manage/instances/', views.mgr_instances, name = 'mgr_instances'),
	path('manage/instances/<action>/<instance_id>/', views.mgr_instance_action, name = 'mgr_instance_action'),


	path('manage/', views.mgr_hypervisors, name = 'mgr_home'),
	path('manage/hypervisors/', views.mgr_hypervisors, name = 'mgr_hypervisors'),

	path('manage/users/', views.mgr_users, name = 'mgr_users'),
	path('manage/users/<action>/<user_id>/', views.mgr_user_action, name = 'mgr_user_action'),
	path('manage/users/create/', views.mgr_user_create, name = 'mgr_user_create'),

	path('manage/projects/', views.mgr_projects, name = 'mgr_projects'),
	path('manage/projects/<action>/<project_id>/', views.mgr_project_action, name = 'mgr_project_action'),
	path('manage/projects/create/', views.mgr_project_create, name = 'mgr_project_create'),

	path('manage/roles/', views.mgr_roles, name = 'mgr_roles'),
	path('manage/roles/<action>/<role_id>/', views.mgr_role_action, name = 'mgr_role_action'),
	path('manage/roles/create/', views.mgr_role_create, name = 'mgr_role_create'),

]
