from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from . import token

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('signup2/', views.SignupAPIView2.as_view(), name='signup2'),
    path('token/', token.obtain_auth_token),
    path('user-projects/',views.UserProjects,name = "user-projects"),
    path("create/", views.create_table , name="create"),
    path('edit-project/<int:id>/',views.edit_project,name='delete-project'),
    path('project-models/<int:id>/',views.project_models,name = 'project-models'),
    path('user-model/', views.user_model, name='user-model'),
    path('data/<str:name>/',views.Model_data,name='data'),
    path('filtered-data/<str:name>/',views.Filtered_model_data,name="filtered-data"),
    path('data-enter/<str:name>/',views.Model_data_in,name="enter-data"),
    path('edit/<str:modelname>/<int:id>/',views.edit_pk,name='edit'),
    path('user/', views.user_list, name='user-list'),
    path('delete/<str:name>/', views.dele, name='delete'),
    path('fields/<str:model_name>/', views.dynamic_model_fields, name='dynamic-model-fields'),
    path('tokens/',views.token_list,name = 'tokens'),
    path('test/',views.test,name='test'),
    
    # path('signup/', views.test, name='signup'),
    # path('create-project/',views.CreateProject,name='create-project'),
    # path('model/<str:name>/', views.model_name, name='model-name'),
    # path('add/<str:name>/', views.add, name='add'),
    # path('update/<str:modelname>/<int:id>/',views.upd,name='update'),
    # path('deleteone/<str:modelname>/<int:id>/',views.del_pk,name='dele'),
    # path("create2/", views.Create2 , name="create2"),

]


