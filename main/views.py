from django.shortcuts import render
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework import status
from rest_framework.response import Response 
from .models import Modelnames , Projects, CustomUser ,Files
from .serializers import dynamic_serializer ,UserRegistrationSerializer,UserSerializer,models_S,DynamicModelFieldSerializer,projects_S
from dynamic_models.models import ModelSchema, FieldSchema
from django.db import models ,connection
from django.urls import clear_url_caches
from importlib import import_module,reload
from django.contrib import admin
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from .permissions import Read , Write , No ,User1 , User2
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from mimetypes import guess_extension
from PIL import Image
import os
from io import BytesIO
import re



ftypes =['INTEGER','TEXT','REAL','BOOLEAN','DATE','FOREIGNKEY','BLOB']

COMPARISON_OPERATORS = {
    'lt': '<',
    'gt': '>',
    'lte': '<=',
    'gte': '>=',
    'ne': '!='
}   


@api_view(['GET','POST'])
@permission_classes([])
def test(request):  
    # modelName = request.POST['modelname']+"_"+str(request.user.id)

    print(request.data['file'])


    # 1- return the schema of a table : 
    # table_name  = modelName
    # sql_query = f"PRAGMA table_info({table_name})"
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_query)
    #     rows = cursor.fetchall()

    
    # schema_list = []
    # for row in rows:
    #     column_info = {
    #         'name': row[1],  
    #         'type': row[2],  
    #     }
    #     schema_list.append(column_info)

    
    # return JsonResponse(schema_list, safe=False)
    
    
    # 2- create a table   :
    
    # len_req = int(request.POST['nf'])
    # count = 1
    # try :
    #     field_definitions = []

    #     for x in range(len_req):
    #         field_name = request.POST.get('field' + str(count), '')
    #         data_type = request.POST.get('datatype' + str(count), '')
    #         is_unique = request.POST.get('unique' + str(count), False) == 'True'
    #         is_null = request.POST.get('null' + str(count), False) == 'True'
    #         max_length = int(request.POST.get('maxlen' + str(count), 255))
    #         default_value = request.POST.get('default' + str(count), '')

            
    #         field_definition = f"{field_name} {data_type} {'NOT NULL' if is_null else ''} {'UNIQUE' if is_unique else ''}"
    #         if default_value:
    #             field_definition += f" DEFAULT {default_value}"
    #         # if max_length:
    #         #     field_definition += f" CHECK (LENGTH({field_name}) <= {max_length})"

    #         field_definitions.append(field_definition)
            
    #         count += 1

        
    #     create_table_query = f"""
    #         CREATE TABLE {modelName} (
    #             id integer PRIMARY KEY AUTOINCREMENT,
    #             {', '.join(field_definitions)}
    #         )
    #     """
    #     print(create_table_query)
        
    #     cursor = connection.cursor()
    #     cursor.execute(create_table_query)
    #     cursor.close()
 
    # except Exception as e:
    #     return Response({'Err ': str(e)},status=status.HTTP_400_BAD_REQUEST)



    # 3- inserting :
    # try:
    #     table_name  = modelName
    #     sql_query = f"PRAGMA table_info({table_name})"
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_query)
    #         rows = cursor.fetchall()
            
    #     fields = [row[1] for row in rows[1:]]

    #     field_values = ("ali", False)
        
    #     insert_query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES {field_values}"

    #     cursor = connection.cursor()
    #     cursor.execute(insert_query)
    #     connection.commit()  

    #     cursor.close()
    
    # except Exception as e :
    #     return Response({'Error':str(e)} , status=status.HTTP_400_BAD_REQUEST)
        
        
        
    #  4- return the data in the table :
    # try :    
    #     cursor = connection.cursor()
    #     cursor.execute(f"SELECT * FROM {modelName} ")
    #     q = cursor.fetchall()
        
    #     column_names = [col[0] for col in cursor.description]

    #     result_list = []
    #     for row in q:
    #         result_dict = {}
    #         for i, col_name in enumerate(column_names):
    #             result_dict[col_name] = row[i]
    #         result_list.append(result_dict)
            
    #     cursor.close()
        
    #     return JsonResponse(result_list, safe=False)
    # except Exception as e:
    #     return Response({'Err ': str(e)},status=status.HTTP_400_BAD_REQUEST)

        
    return Response(status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class SignupAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['co_owner']=''
        data['read_P']='True'
        data['write_P']='True'
        data['user1']='True'
        data['user2']='False'
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@permission_classes([IsAdminUser | User1])
class SignupAPIView2(APIView):
    def post(self, request):
        data = request.data.copy()
        data['co_owner']=request.user.id
        data['user1']='False'
        data['user2']='True'
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView2(APIView):
    permission_classes = [IsAdminUser | User1]

    def post(self, request):
        try:
            data = request.data.copy()
            data['co_owner'] = request.user.id
            data['user1'] = 'False'
            data['user2'] = 'True'
            data['first_name']=''
            data['last_name']=''
            data['email']=''
            data['profile_picture']=''
            # Extract read and write permissions from the request data
            read_permission = data.get('read_P')
            write_permission = data.get('write_P')
            # Create the username using user ID and permissions
            permissions_part = []
            if read_permission == 'True':
                permissions_part.append('read')
            if write_permission == 'True':
                permissions_part.append('write')

            permissions_str = '_'.join(permissions_part)
            unique_username = f"{request.user.id}_{permissions_str}" if permissions_str else f"{request.user.id}_none"
            data['username'] = unique_username
            
            # Set a static password
            static_password = "StaticPassword123"  # Use a more secure password in production
            data['password'] = static_password
            
            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)     
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def token_list(request):
    
    try:
        user = request.user
        co = CustomUser.objects.filter(co_owner = user.id)
        co_id = [cos.id for cos in co]
        tokens = Token.objects.all()
        toks = []
        for token in tokens :
            if token.user.id in co_id:
                toks.append(token)
                
        token_data = [{'username': token.user.username,'Read':token.user.read_P,'Write':token.user.write_P, 'token': token.key} for token in toks]
        return Response(token_data, status=status.HTTP_200_OK) 
    
    except Exception as e:
        return Response({'Error' : str(e)} , status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def user_list(request):
    user = CustomUser.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Define allowed field types
ALLOWED_FIELD_TYPES = ['INTEGER', 'TEXT', 'REAL', 'BOOLEAN', 'DATE', 'BLOB']
ALLOWED_FIELD_NAME_REGEX = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

def validate_field_name(field_name):
    if not ALLOWED_FIELD_NAME_REGEX.match(field_name):
        raise ValueError(f"Invalid field name: {field_name}")

def validate_field_type(field_type):
    if field_type not in ALLOWED_FIELD_TYPES and field_type != 'FOREIGNKEY':
        raise ValueError(f"Invalid field type: {field_type}")

@api_view(['POST'])
@permission_classes([IsAdminUser | User1])
def create_table(request):
    model_name = request.data['modelname'] + "_" + str(request.user.id)
    project_name = request.data['project']
    
    try:
        project = Projects.objects.get(user=request.user, name=project_name)
    except Projects.DoesNotExist:
        return Response({'Error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    fields = []
    try:
        for i in range(int(request.data['nf'])):
            field_name = request.data[f'field{i+1}']
            field_type = request.data[f'datatype{i+1}']
            is_unique = request.data.get(f'unique{i+1}', 'False') == 'True'
            is_null = request.data.get(f'null{i+1}', 'False') == 'True'
            default_value = request.data.get(f'default{i+1}', None)

            # Validate field name and type
            validate_field_name(field_name)
            validate_field_type(field_type)
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'unique': is_unique,
                'null': is_null,
                'default': default_value,
                'related_model': request.data.get(f'related_model{i+1}', None)
            })
    except ValueError as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        field_definitions = []
        for field in fields:
            if field['type'] == 'FOREIGNKEY' and field['related_model']:
                related_model_name = field['related_model'] + "_" + str(request.user.id)
                validate_field_name(related_model_name)  # Validate related model name
                field_definition = f"{field['name']} INTEGER REFERENCES {related_model_name}(id) ON DELETE CASCADE"
                if not field['null']:
                    field_definition += " NOT NULL"
                if field['unique']:
                    field_definition += " UNIQUE"
                    
            else:
                field_definition = f"{field['name']} {field['type']}"
                if not field['null']:
                    field_definition += " NOT NULL"
                if field['unique']:
                    field_definition += " UNIQUE"
                if field['default'] is not None:
                    if field['type'] == 'TEXT' or field['type'] == 'DATE':
                        field_definition += f" DEFAULT '{field['default']}'"
                    else:
                        field_definition += f" DEFAULT {field['default']}"
            field_definitions.append(field_definition)

        create_table_query = f"""
            CREATE TABLE {model_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {', '.join(field_definitions)}
            ) STRICT;
        """

        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        Modelnames.objects.create(user=request.user, modelname=model_name, project=project)
        return Response({'message': 'Table created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# @permission_classes([IsAdminUser | User1])
# @api_view(['POST'])
# def Create(request):
        
#     len_req= request.data['nf']
#     project = request.data['project']
#     count = 0
        
#     modelName = request.data['modelname']+"_"+str(request.user.id)
        
#     user = request.user
    
#     try : 
#         project_model=Projects.objects.get(user=request.user.id,name = project)
#     except Exception as e:
#         return Response({'Project Error ':str(e)},status=status.HTTP_404_NOT_FOUND)
    
        
#     try:
#         field_definitions = []
#         len_req= int(request.data['nf'])
#         count = 0
#         for x in range(len_req):
#             count = count + 1
#             field_name = request.POST.get('field' + str(count), '')
#             data_type = request.POST.get('datatype' + str(count), '')
#             is_unique = request.POST.get('unique' + str(count), False) == 'True'
#             is_null = request.POST.get('null' + str(count), False) == 'True'
#             default_value = request.POST.get('default' + str(count), '')
            
#             if not field_name or not data_type:
#                 return Response({'Error': 'Field name and data type are required.'}, status=status.HTTP_400_BAD_REQUEST)

#             if request.POST['datatype'+ str(count)] not in ftypes:
#                 return Response({'Error':'Invalid data type !'} , status=status.HTTP_400_BAD_REQUEST)
            
            
#             if data_type == 'BOOLEAN':
                
#                 field_definition = f"{field_name} INTEGER {'NOT NULL' if not is_null else ''}"
                
#             elif data_type == 'DATE':
                
#                 field_definition = f"{field_name} TEXT {'NOT NULL' if not is_null else ''} CHECK ({field_name} IS date({field_name}))"
            
#             elif data_type == 'FOREIGNKEY':
#                 related_model = request.POST.get('related_model' + str(count), '')
#                 related_model = related_model+"_"+str(request.user.id)
#                 try :
#                     mod1 = Modelnames.objects.get(modelname=related_model)
#                 except Exception as e:
#                     return Response({'Error':str(e)},status = status.HTTP_404_NOT_FOUND)
    
#                 if request.user != mod1.user:
#                     return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
                 
#                 field_definition = f"{field_name} INTEGER REFERENCES {related_model}(id) ON DELETE CASCADE"
#             else:
#                 field_definition = f"{field_name} {data_type} {'NOT NULL' if not is_null else ''} {'UNIQUE' if is_unique else ''}"
#                 if default_value:
#                     field_definition += f" DEFAULT {default_value}"
            

#             field_definitions.append(field_definition)
            
        
        
#         try:
#             model_create = Modelnames.objects.create(user = user,modelname=modelName,project = project_model)
#         except Exception as e:
#             return Response({'Error':'invalid model name .'},status = status.HTTP_400_BAD_REQUEST)
        
#         create_table_query = f"""
#             CREATE TABLE {modelName} (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 {', '.join(field_definitions)}
#             )STRICT;
#         """
        
#         cursor = connection.cursor()
#         cursor.execute(create_table_query)
#         cursor.close()
        
#         return Response(status= status.HTTP_200_OK)
#     except Exception as e2:
#                 return Response({'Error':str(e2)},status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAdminUser | User1])
def UserProjects(request):
    if request.method == 'GET':
        try:
            projects =Projects.objects.filter(user=request.user.id)
            try:
                serializer = projects_S(projects, many=True)
                return Response(serializer.data ,status= status.HTTP_200_OK)
            
            except Exception as e1:
                return Response({'Error ':str(e1)}, status = status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'POST':
        user = request.user
        name = request.POST['name']
        try : 
            Projects.objects.create(user = user,name=name)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error ':str(e)},status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def project_models(request,id):

    try:
        owner = Projects.objects.get(id=id).user
        if request.user != owner:
            return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
        project = Projects.objects.get(id = id)
        models=Modelnames.objects.filter(user=request.user.id,project=project)
        
        for model in models:
            model.modelname = model.modelname.rsplit('_', 1)[0]

        serializer = models_S(models, many=True)
        return Response(serializer.data ,status= status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error ':str(e)}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE','PUT'])
@permission_classes([IsAdminUser | User1])
def edit_project(request,id):
    
    try:
        project = Projects.objects.get(id = id)
    except Projects.DoesNotExist :
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':   
        try :
            models =Modelnames.objects.filter(user=request.user.id,project=project).values()
            for m in models :
                model1 = ModelSchema.objects.get(name= m['modelname'])
                mod1 = Modelnames.objects.get(modelname=m['modelname'])
                model = model1.as_model()
                admin.site.unregister(model)
                mod1.delete()
                model1.delete()
                
            project.delete()
            reload(import_module(settings.ROOT_URLCONF))
            clear_url_caches()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PUT':
        try:
            serializer = projects_S(project , data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def user_model(request):
    try:
        models=Modelnames.objects.filter(user=request.user.id)
        try:
            for model in models:
                model.modelname = model.modelname.rsplit('_', 1)[0]

            serializer = models_S(models, many=True)
            return Response(serializer.data ,status= status.HTTP_200_OK)
        
        except Exception as e1:
            print("error:   " , e1)
            
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
        
    return Response(status = status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdminUser | User1])
def dele(request,name):
    try :
        modelName = name+"_"+str(request.user.id)
        mod1 = Modelnames.objects.get(modelname=modelName)
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_404_NOT_FOUND)
    
    if request.user != mod1.user:
        return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
    
    
    try:
        table_name  = modelName
        delete_query = f"DROP TABLE IF EXISTS {table_name}"

        with connection.cursor() as cursor:
            cursor.execute(delete_query)
            connection.commit()  

        mod1.delete()
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()
        
        return Response(status=status.HTTP_200_OK)
            
    except Exception as e :
        return Response({'Error':str(e)} , status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAdminUser | User1 | (User2 and Write)])
def Model_data_in(request, name):
    try:
        modelName = name + "_" + str(request.user.id)
        mod1 = Modelnames.objects.get(modelname=modelName)
    except Modelnames.DoesNotExist:
        return Response({'Error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if (mod1.user != request.user) and (mod1.user.co_owner != request.user):
        return Response({'Error': 'UNAUTHORIZED!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        table_name = modelName
        sql_query = f"PRAGMA table_info({table_name})"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()

        # Validate field names and types
        valid_fields = {row[1]: row[2] for row in rows[1:]}
        fields = []
        field_values = []

        for field, value in request.data.items():
            if field in valid_fields:
                field_type = valid_fields[field]
                if field_type == 'BLOB' and hasattr(value, 'file'):
                    try:
                        image = Image.open(value.file)
                        image.verify()  # Verify if it's an image
                        value.file.seek(0)  # Reset file pointer
                        value = value.file.read()
                    except (IOError, SyntaxError):
                        return Response({'Error': f'File for field {field} is not a valid image.'}, status=status.HTTP_400_BAD_REQUEST)
                elif field_type == 'BLOB' and not value:
                    value = None  # Handle empty BLOB field by setting it to None
                
                if not value:
                    value = None
                fields.append(field)
                field_values.append(value)

        field_values_tuple = tuple(field_values)

        # Using parameterized queries to prevent SQL injection
        insert_query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
        
        with connection.cursor() as cursor:
            cursor.execute(insert_query, field_values_tuple)
            connection.commit()

        return Response({'message': 'Data inserted successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAdminUser | User1 | (User2 and Write)])
# def Model_data_in2(request, name):
#     try:
#         modelName = name + "_" + str(request.user.id)
#         mod1 = Modelnames.objects.get(modelname=modelName)
#     except Exception as e:
#         return Response({'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)

#     if (mod1.user != request.user) and (mod1.user != request.user.co_owner):
#         return Response({'Error': 'UNAUTHORIZED!'}, status=status.HTTP_401_UNAUTHORIZED)

#     try:
#         table_name = modelName
#         sql_query = f"PRAGMA table_info({table_name})"
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query)
#             rows = cursor.fetchall()

#         fields = [row[1] for row in rows[1:] if (row[1] in request.data and request.data[row[1]] != '')]

#         b_fields = [row[1] for row in rows[1:] if row[2] == 'BLOB']

#         field_values = []
#         for field in fields:
#             value = request.data[field]
#             if field in b_fields and hasattr(value, 'file'):
#                 # Check if the file is an image
#                 try:
#                     image = Image.open(value.file)
#                     image.verify()  # Verify if it's an image
#                     value.file.seek(0)  # Reset file pointer
#                     value = value.file.read()
#                 except (IOError, SyntaxError) as e:
#                     return Response({'Error': f'File for field {field} is not a valid image.'}, status=status.HTTP_400_BAD_REQUEST)
#             field_values.append(value)

#         field_values_tuple = tuple(field_values)

#         cursor = connection.cursor()
#         insert_query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
#         cursor.execute(insert_query, field_values_tuple)
#         connection.commit()
#         cursor.close()

#         return Response(status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser | User1 | (User2 and Read)])
def Model_data(request, name):
    try:
        modelName = name + "_" + str(request.user.id)
        mod1 = Modelnames.objects.get(modelname=modelName)
    except Modelnames.DoesNotExist:
        return Response({'Error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if (mod1.user != request.user) and (mod1.user != request.user.co_owner):
        return Response({'Error': 'UNAUTHORIZED!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {modelName}")
        q = cursor.fetchall()

        column_names = [col[0] for col in cursor.description]

        cursor.execute(f"PRAGMA table_info({modelName})")
        table_info = cursor.fetchall()
        blob_fields = [row[1] for row in table_info if row[2] == 'BLOB']

        result_list = []
        index = 0
        for row in q:
            index += 1
            result_dict = {}
            for i, col_name in enumerate(column_names):
                if col_name in blob_fields and row[i] is not None:
                    file_name = f"{request.user.id}_{modelName}_{col_name}_{index}.JPG"
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    
                    # Convert image to JPG if necessary
                    image = Image.open(BytesIO(row[i]))
                    if image.format != 'JPEG':
                        image = image.convert('RGB')  # Convert to RGB before saving as JPEG
                    image.save(file_path, 'JPEG')
                    
                    result_dict[col_name] = request.build_absolute_uri(settings.MEDIA_URL + file_name)
                else:
                    result_dict[col_name] = row[i]
            result_list.append(result_dict)

        cursor.close()

        return JsonResponse(result_list, safe=False)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
   
def parse_query_param(key, value, valid_fields):
    match = re.match(r'(\w+)__(\w+)', key)
    if match:
        field, operator = match.groups()
        if field not in valid_fields:
            raise ValueError(f"Invalid field name: {field}")
        if operator not in COMPARISON_OPERATORS:
            raise ValueError(f"Invalid operator: {operator}")
        return field, COMPARISON_OPERATORS[operator], value
    elif key in valid_fields:
        return key, '=', value
    else:
        raise ValueError(f"Invalid field name: {key}")


@api_view(['GET'])
@permission_classes([IsAdminUser | User1 | (User2 & Read)])
def Filtered_model_data(request, name):
    try:
        modelName = name + "_" + str(request.user.id)
        mod1 = get_object_or_404(Modelnames, modelname=modelName)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if (mod1.user != request.user) and (mod1.user != request.user.co_owner):
        return Response({'Error': 'UNAUTHORIZED!'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        cursor = connection.cursor()
        
        # Get column names to validate against
        cursor.execute(f"PRAGMA table_info({modelName})")
        table_info = cursor.fetchall()
        valid_fields = [row[1] for row in table_info]
        blob_fields = [row[1] for row in table_info if row[2] == 'BLOB']
        
        # Build the base query
        base_query = f"SELECT * FROM {modelName} WHERE 1=1"
        
        # Add filters based on query parameters
        filters = []
        params = []
        for key, value in request.GET.items():
            try:
                field, operator, param_value = parse_query_param(key, value, valid_fields)
                filters.append(f"{field} {operator} %s")
                params.append(param_value)
            except ValueError as ve:
                return Response({'Error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        
        if filters:
            base_query += " AND " + " AND ".join(filters)
        
        cursor.execute(base_query, params)
        q = cursor.fetchall()
        
        column_names = [col[0] for col in cursor.description]

        result_list = []
        index = 0
        for row in q:
            index += 1
            result_dict = {}
            for i, col_name in enumerate(column_names):
                if col_name in blob_fields and row[i] is not None:
                    file_name = f"{request.user.id}_{modelName}_{col_name}_{index}.JPG"
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    
                    # Convert image to JPG if necessary
                    image = Image.open(BytesIO(row[i]))
                    if image.format != 'JPEG':
                        image = image.convert('RGB')  # Convert to RGB before saving as JPEG
                    image.save(file_path, 'JPEG')
                    
                    result_dict[col_name] = request.build_absolute_uri(settings.MEDIA_URL + file_name)
                else:
                    result_dict[col_name] = row[i]
            result_list.append(result_dict)

        cursor.close()

        return JsonResponse(result_list, safe=False)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE','PUT'])
@permission_classes([IsAdminUser | User1 | (User2 and Write)])
def edit_pk(request,modelname,id):
        
    modelName = modelname+"_"+str(request.user.id)
    if request.method == 'DELETE':
        try :
            owner = Modelnames.objects.get(modelname=modelName).user
            if ((request.user != owner) and (owner != request.user.co_owner)):
                return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)

            table_name  = modelName
            delete_query = f"DELETE FROM {table_name} WHERE id={id}"

            with connection.cursor() as cursor:
                cursor.execute(delete_query)
                connection.commit()
                
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try :
            owner = Modelnames.objects.get(modelname=modelName).user
            if ((request.user != owner) and (owner != request.user.co_owner)):
                return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
            table_name  = modelName
            sql_query = f"PRAGMA table_info({table_name})"
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                
                fields = [row[1] for row in rows[1:]]

                field_values = {field: f"'{request.data[field]}'" if isinstance(request.data[field], str) else request.data[field] for field in fields}

                update_query = f"UPDATE {table_name} SET {', '.join(f'{field}={value}' for field, value in field_values.items())} WHERE id={id}"

                cursor.execute(update_query)
                connection.commit()
            
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def dynamic_model_fields(request, model_name):
    
    modelName = model_name+"_"+str(request.user.id)
    try:
        owner = Modelnames.objects.get(modelname=modelName).user
        if request.user != owner:
            return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
                
        sql_query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{modelName}';"
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            create_table_statement = cursor.fetchone()[0]

        index = create_table_statement.find("(")

        create_table_statement = create_table_statement[index +1 :]

        schema_list = []
        columns = create_table_statement.split(",")
        
        for column in columns:
            column_info = {}
            column_parts = column.strip().split(" ")
            column_info['name'] = column_parts[0]
            column_info['type'] = column_parts[1]
            column_info['notnull'] = "NOT NULL" in column
            column_info['default_value'] = None
            column_info['is_key'] = "REFERENCES" in column
            column_info['related_model'] = None
            if "DEFAULT" in column:
                default_value_index = column_parts.index("DEFAULT") + 1
                column_info['default_value'] = column_parts[default_value_index]
            if "REFERENCES" in column:
                column_info['related_model'] = column_parts[3]
            
            column_info['is_unique'] = "UNIQUE" in column 
            schema_list.append(column_info)
        
    
        return Response(schema_list,status=status.HTTP_200_OK)
    except Exception as e: 
        return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        