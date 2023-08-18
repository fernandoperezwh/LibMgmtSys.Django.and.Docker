from django import forms
# local imports
from biblioteca.models import Autor, Editor, Libro

#region utilds
def build_attrs(key):
    return {
        "id":               key,
        "aria-describedby": "{}_errors".format(key),
        "class":            "form-control",
    }
#endregion



class SearchForm(forms.Form):
    q = forms.CharField(label="Buscador", max_length=50, required=False)
    
    
    
class AutorForm(forms.ModelForm):
    class Meta():
        model = Autor
        fields = [
            "nombre",
            "apellidos",
            "email",
        ]
        widgets = {
            "nombre":    forms.TextInput(attrs=build_attrs("nombre")),
            "apellidos": forms.TextInput(attrs=build_attrs("apellidos")),
            "email":     forms.EmailInput(attrs=build_attrs("email")),
        }
    


class EditorForm(forms.ModelForm):
    class Meta():
        model = Editor
        fields = [
            "nombre",
            "domicilio",
            "ciudad",
            "estado",
            "pais",
            "website",
        ]
        widgets = {
            "nombre":     forms.TextInput(attrs=build_attrs("nombre")),
            "domicilio":  forms.TextInput(attrs=build_attrs("domicilio")),
            "ciudad":     forms.TextInput(attrs=build_attrs("ciudad")),
            "estado":     forms.TextInput(attrs=build_attrs("estado")),
            "pais":       forms.TextInput(attrs=build_attrs("pais")),
            "website":    forms.TextInput(attrs=build_attrs("website")),
        }



class LibroForm(forms.ModelForm):
    class Meta():
        model = Libro
        fields = [
            "titulo",
            "fecha_publicacion",
            "portada",
            "autores",
            "editor",
        ]
        widgets = {
            "titulo":             forms.TextInput(attrs=build_attrs("titulo")),
            "fecha_publicacion":  forms.DateInput(attrs=build_attrs("fecha_publicacion")),
            "autores":            forms.SelectMultiple(attrs=build_attrs("autores")),
            "editor":             forms.Select(attrs=build_attrs("editor")),
        }
    