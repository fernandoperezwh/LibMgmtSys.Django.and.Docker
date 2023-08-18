from django.contrib import admin
from biblioteca.models import Editor, Autor, Libro

@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'domicilio',
        'ciudad',
        'estado',
        'pais',
        'website',
    )

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellidos','email',)
    search_fields = ('nombre','apellidos', )


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        # 'autores',
        'editor',
        'fecha_publicacion',
        'portada',
    )
    list_filter = ( 'fecha_publicacion', )
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion', )
    # fields = (
    #     'titulo',
    #     'autores',
    #     'editor',
    #     'fecha_publicacion',
    # )
    filter_horizontal = ('autores', )
    raw_id_fields = ('editor',)
# Register your models here.
