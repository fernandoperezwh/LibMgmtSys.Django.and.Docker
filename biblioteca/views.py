from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
# Local imports
from biblioteca.models import Libro, Autor, Editor
from biblioteca.forms import SearchForm, AutorForm, EditorForm, LibroForm


#region utils
def generic_delete(request, instance, tpl_name, redirect, success_message=None):
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."
    if request.method == "POST":
        instance.delete()
        messages.success(request, success_message or DEFAULT_SUCCESS_MESSAGE)
        return HttpResponseRedirect( redirect )
    return render(request, tpl_name, { "object": instance })
#endregion


"""
---------------------------------------------------------------
function views
---------------------------------------------------------------
"""

#region autor views
def autor_listado(request):
    form, datasource = SearchForm(request.GET), []

    # filter
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            datasource = Autor.objects.all().values()
        else:
            datasource = Autor.objects.filter(
                Q(nombre__icontains=cd['q'])    |
                Q(apellidos__icontains=cd['q']) |
                Q(email__icontains=cd['q'])
            ).values()
    return render(request, "autor_listado.html", {
        "buscador": form,
        "object_list": datasource,
        "fields": [
            { "label": "Nombre",    "key": "nombre" },
            { "label": "Apellidos", "key": "apellidos" },
            { "label": "Email",     "key": "email" },
        ],
        "actions": {
            "create": { "label": "Crear Autor", "redirect": "/crear/autor" },
            "update": { "label": "Modificar",   "redirect": "/modificar/autor" },
            "delete": { "label": "Eliminar",    "redirect": "/eliminar/autor" },
        }
    })



def autor_form(request, autor_id=None):
    # Se verifica la existencia
    autor_instance = get_object_or_404(Autor, id=autor_id) if autor_id else None
    # Update/create
    if request.method == "POST":
        form = AutorForm(request.POST, instance=autor_instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente el autor <strong>{} {}</strong>'.format(
                    "modifico" if autor_instance else "agrego",
                    autor_instance.nombre if autor_instance else form.cleaned_data.get('nombre'),
                    autor_instance.apellidos if autor_instance else form.cleaned_data.get('apellidos'),
                )
            )
            return HttpResponseRedirect("/autores")
    else:
        form = AutorForm(instance=autor_instance) if autor_instance else AutorForm()
    return render(request, "autor_form.html", {
        "form":   form,
        "action": "Modificar" if autor_instance else "Crear",
    })



def autor_delete(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return generic_delete(
        request=request,
        instance=autor,
        tpl_name="autor_delete.html",
        redirect="/autores/",
        success_message="Se elimino el registro del autor: <strong>{} {}</strong>".format(autor.nombre, autor.apellidos)
    )
    
#endregion




#region Editor views
def editor_listado(request):
    form, datasource = SearchForm(request.GET), []
    # filter
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            datasource = Editor.objects.all().values()
        else:
            datasource = Editor.objects.filter(
                Q(nombre__icontains=cd['q']) |
                Q(ciudad__icontains=cd['q']) |
                Q(estado__icontains=cd['q']) |
                Q(pais__icontains=cd['q'])
            ).values()
    return render(request, "editor_listado.html", {
        "buscador": form,
        "object_list": datasource,
        "fields": [
            { "label": "Nombre",        "key": "nombre" },
            { "label": "Domicilio",     "key": "domicilio" },
            { "label": "Ciudad",        "key": "ciudad" },
            { "label": "Estado",        "key": "estado" },
            { "label": "Pais",          "key": "pais" },
            { "label": "Sitio oficial", "key": "website", "is_link":True },
        ],
        "actions": {
            "create": { "label": "Crear Editor",     "redirect": "/crear/editor" },
            "update": { "label": "Modificar Editor", "redirect": "/modificar/editor" },
            "delete": { "label": "Eliminar Editor",  "redirect": "/eliminar/editor" },
        }
    })



def editor_form(request, editor_id=None):
    # Se verifica la existencia
    editor_instance = get_object_or_404(Editor, id=editor_id) if editor_id else None
    # Update/create
    if request.method == "POST":
        form = EditorForm(request.POST, instance=editor_instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente el editor <strong>{}</strong>'.format(
                    "modifico" if editor_instance else "agrego",
                    editor_instance.nombre if editor_instance else form.cleaned_data.get('nombre')
                )
            )
            return HttpResponseRedirect("/editores")
    else:
        form = EditorForm(instance=editor_instance) if editor_instance else EditorForm()
    return render(request, "editor_form.html", {
        "form":   form,
        "action": "Modificar" if editor_instance else "Crear",
    })



def editor_delete(request, editor_id):
    editor = get_object_or_404(Editor, id=editor_id)
    return generic_delete(
        request=request,
        instance=editor,
        tpl_name="editor_delete.html",
        redirect="/editores/",
        success_message="Se elimino el registro del editor: <strong>{}</strong>".format(editor.nombre)
    )
#endregion




#region Libro views
def libro_listado(request):
    # Template context
    form, datasource = SearchForm(request.GET), []
    
    # filter
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            datasource = (Libro.objects
                .select_related("editor")
                .all()
            )
        else:
            datasource = (Libro.objects
                .select_related("editor")
                .filter(titulo__icontains=cd['q'])
            )
    return render(request, "libro_listado.html", {
        "buscador": form,
        "object_list": datasource,
    })



def libro_form(request, libro_id=None):
    # Se verifica la existencia del libro
    libro_instance = get_object_or_404(Libro, id=libro_id) if libro_id else None

    # Update/create
    if request.method == "POST":
        form = LibroForm(request.POST, request.FILES, instance=libro_instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente el libro <strong>{}</strong>'.format(
                    "modifico" if libro_instance else "agrego",
                    libro_instance.titulo if libro_instance else form.cleaned_data['titulo']
                )
            )
            return HttpResponseRedirect("/libros")
    else:
        form = LibroForm(instance=libro_instance) if libro_instance else LibroForm()

    return render(request, "libro_form.html", {
        "form":   form,
        "action": "Modificar" if libro_instance else "Crear",
    })



def libro_delete(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return generic_delete(
        request=request,
        instance=libro,
        tpl_name="libro_delete.html",
        redirect="/libros/",
        success_message="Se elimino el registro del libro: <strong>{}</strong>".format(libro.titulo)
    )
#endregion


"""
---------------------------------------------------------------
Class based views
---------------------------------------------------------------
"""

#region autor clase-based views
class AutorListView(ListView):
    model = Autor
    template_name = "autor_listado__cbv.html"



class AutorCreateView(SuccessMessageMixin, CreateView):
    model = Autor
    form_class = AutorForm
    template_name = "autor_form__cbv.html"
    success_url = reverse_lazy("autores_cbv")
    success_message = "Se agrego correctamente el autor <strong>%(nombre)s %(apellidos)s</strong>"



class AutorUpdateView(SuccessMessageMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = "autor_form__cbv.html"
    success_url = reverse_lazy("autores_cbv")
    success_message = "Se modifico correctamente el autor <strong>%(nombre)s %(apellidos)s</strong>"



class AutorDeleteView(SuccessMessageMixin, DeleteView):
    model = Autor
    form_class = AutorForm
    template_name = "autor_delete__cbv.html"
    success_url = reverse_lazy("autores_cbv")
    success_message = "Se elimino correctamente el autor <strong>%(nombre)s %(apellidos)s</strong>"


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(AutorDeleteView, self).delete(request, *args, **kwargs)

#endregion




#region editor clase-based views
class EditorListView(ListView):
    model = Editor
    template_name = "editor_listado__cbv.html"


class EditorCreateView(SuccessMessageMixin, CreateView):
    model = Editor
    form_class = EditorForm
    template_name = "editor_form__cbv.html"
    success_url = reverse_lazy("editores_cbv")
    success_message = "Se agrego correctamente el editor <strong>%(nombre)s</strong>"


class EditorUpdateView(SuccessMessageMixin, UpdateView):
    model = Editor
    form_class = EditorForm
    template_name = "editor_form__cbv.html"
    success_url = reverse_lazy("editores_cbv")
    success_message = "Se modifico correctamente el editor <strong>%(nombre)s</strong>"



class EditorDeleteView(SuccessMessageMixin, DeleteView):
    model = Editor
    form_class = EditorForm
    template_name = "editor_delete__cbv.html"
    success_url = reverse_lazy("editores_cbv")
    success_message = "Se elimino correctamente el editor <strong>%(nombre)s</strong>"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EditorDeleteView, self).delete(request, *args, **kwargs)

#endregion




#region libro clase-based views
class LibroListView(ListView):
    model = Libro
    template_name = "libro_listado__cbv.html"
  

class LibroCreateView(SuccessMessageMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro_form__cbv.html"
    success_url = reverse_lazy("libros_cbv")
    success_message = "Se agrego correctamente el libro <strong>%(titulo)s</strong>"



class LibroUpdateView(SuccessMessageMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = "libro_form__cbv.html"
    success_url = reverse_lazy("libros_cbv")
    success_message = "Se modifico correctamente el libro <strong>%(titulo)s</strong>"



class LibroDeleteView(SuccessMessageMixin, DeleteView):
    model = Libro
    form_class = LibroForm
    template_name = "libro_delete__cbv.html"
    success_url = reverse_lazy("libros_cbv")
    success_message = "Se elimino correctamente el libro <strong>%(titulo)s</strong>"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(LibroDeleteView, self).delete(request, *args, **kwargs)
#endregion



# V-37 Class based views
class AutorDetailView(DetailView):
    model = Autor
    template_name = "autor_detail__cbv.html"


"""
---------------------------------------------------------------
Master class "View"
---------------------------------------------------------------
"""

#region autor raw class-based view
class AutorRawListView(View):
    model = Autor
    template_name = "autor_listado__cbv.html"
    queryset = Autor.objects.all()

    def get_queryset(self):
        return self.queryset


    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        # filter
        if form.is_valid():
            cd = form.cleaned_data
            if not cd['q']:
                self.queryset = self.model.objects.all()
            else:
                self.queryset = self.model.objects.filter(
                    Q(nombre__icontains=cd['q'])    |
                    Q(apellidos__icontains=cd['q']) |
                    Q(email__icontains=cd['q'])
                )
        return render(request, self.template_name, {
            "buscador": form,
            "object_list": self.get_queryset(),
        })


class AutorRawCreateView(View):
    model = Autor
    form_class = AutorForm
    template_name = "autor_form__cbv.html"
    success_url = "/autores_v"
 
    def get(self, request, *args, **kwargs):
        context = { "form": self.form_class() }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = { "form": self.form_class(request.POST) }
        if context["form"].is_valid:
            context["form"].save()
            messages.success( request,
                'Se agrego correctamente el autor <strong>{} {}</strong>'.format(context["form"].cleaned_data.get('nombre'), context["form"].cleaned_data.get('apellidos'))
            )
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context)


class AutorRawUpdateView(View):
    model = Autor
    form_class = AutorForm
    template_name = "autor_form__cbv.html"
    success_url = "/autores_v"

    def get_object(self):
        _id = self.kwargs.get("pk")
        if _id is not None:
            return get_object_or_404(self.model, id=_id)
        return


    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context["form"] = self.form_class(instance=obj)
            context["object"] = obj
        return render(request, self.template_name, context)


    def post(self, request, id=None, *args, **kwargs):
        context = { "object": self.get_object() }
        if context["object"] is not None:
            context["form"] = self.form_class(request.POST, instance=context["object"])
            if context["form"].is_valid:
                context["form"].save()
                messages.success( request,
                    'Se modifico correctamente el autor <strong>{} {}</strong>'.format(context["object"].nombre, context["object"].apellidos)
                )
                return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context)


class AutorRawDeleteView(View):
    model = Autor
    form_class = AutorForm
    template_name = "autor_delete__cbv.html"
    success_url = "/autores_v"

    def get_object(self):
        _id = self.kwargs.get("pk")
        if _id is not None:
            return get_object_or_404(self.model, id=_id)
        return


    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context["object"] = obj
        return render(request, self.template_name, context)


    def post(self, request, id=None, *args, **kwargs):
        context = { "object": self.get_object() }
        if context["object"] is not None:
            context["object"].delete()
            messages.success( request,
                'Se elimino el registro del autor<strong>{} {}</strong>'.format(context["object"].nombre, context["object"].apellidos)
            )
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context)

#endregion