from django.contrib import admin
from .models import Memory, Caretaker, Patient

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at") 
    search_fields = ("title", "description")  
    list_filter = ("created_at",)

@admin.register(Caretaker)
class CaretakerAdmin(admin.ModelAdmin):
    list_display = ("name", "get_email")  
    search_fields = ("name", "email")

    @admin.display(description="Email")
    def get_email(self, obj):
        return obj.user.email

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')  
    list_filter = ('date_of_birth',)

