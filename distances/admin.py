from django.contrib import admin

from distances.models import Exercise, Person

admin.site.register(Exercise)
admin.site.register(Person)

#class ExerciseAdmin(admin.ModelAdmin):
#	list_filter = ('sport', 'date')
