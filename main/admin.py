from django.contrib import admin
from .models import Modelnames,CustomUser,Projects,Files
from dynamic_models.models import ModelSchema


admin.site.register(CustomUser)
admin.site.register(Projects)
admin.site.register(Modelnames)
admin.site.register(Files)

# try:

#     models = Modelnames.objects.all()
#     for model in models:
#         try:
#             reg_model = ModelSchema.objects.get(name=model.modelname).as_model()
#             admin.site.register(reg_model)
#         except Exception as e:
#             print("admin error :  " ,model.modelname ,e)
# except Exception as e:
#     print("error in admin file : ", e)

# class Table1Admin(admin.ModelAdmin):
#     pass

