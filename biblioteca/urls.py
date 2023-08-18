"""djbiblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
# Local imports
from biblioteca.views import (
    # function view
    autor_listado,  autor_form,  autor_delete,
    editor_listado, editor_form, editor_delete,
    libro_listado,  libro_form,  libro_delete,
    # class based view
    AutorListView,  AutorCreateView,  AutorUpdateView,  AutorDeleteView,
    EditorListView, EditorCreateView, EditorUpdateView, EditorDeleteView,
    LibroListView,  LibroCreateView,  LibroUpdateView,  LibroDeleteView,
    # aditional - class based view
    AutorDetailView,
    # raw class based view
    AutorRawListView, AutorRawCreateView, AutorRawUpdateView, AutorRawDeleteView,

)

urlpatterns = [
    url(r'^$', libro_listado),
    
    #region function views
    url(r'^autores/$', autor_listado, name="autores"),
    url(r'^crear/autor/$', autor_form),
    url(r'^modificar/autor/(\d+)/$', autor_form),
    url(r'^eliminar/autor/(\d+)/$', autor_delete),
    #endregion
    #region class based views 
    url(r'^autores_cbv/$', AutorListView.as_view(), name="autores_cbv"),
    url(r'^crear/autor_cbv/$', AutorCreateView.as_view()),
    url(r'^modificar/autor_cbv/(?P<pk>[0-9]+)/$', AutorUpdateView.as_view()),
    url(r'^eliminar/autor_cbv/(?P<pk>[0-9]+)/$', AutorDeleteView.as_view()),
    url(r'^autor_cbv/(?P<pk>[0-9]+)/$', AutorDetailView.as_view()),
    #endregion
    #region class based views with master class based views "View"
    url(r'^autores_v/$', AutorRawListView.as_view(), name="autores_v"),
    url(r'^crear/autor_v/$', AutorRawCreateView.as_view()),
    url(r'^modificar/autor_v/(?P<pk>[0-9]+)/$', AutorRawUpdateView.as_view()),
    url(r'^eliminar/autor_v/(?P<pk>[0-9]+)/$', AutorRawDeleteView.as_view()),
    #endregion


    
    #region function views
    url(r'^editores/$', editor_listado, name="editores"),
    url(r'^crear/editor/$', editor_form),
    url(r'^modificar/editor/(\d+)/$', editor_form),
    url(r'^eliminar/editor/(\d+)/$', editor_delete),
    #endregion
    #region class based views
    url(r'^editores_cbv/$', EditorListView.as_view(), name="editores_cbv"),
    url(r'^crear/editor_cbv/$', EditorCreateView.as_view()),
    url(r'^modificar/editor_cbv/(?P<pk>[0-9]+)/$', EditorUpdateView.as_view()),
    url(r'^eliminar/editor_cbv/(?P<pk>[0-9]+)/$', EditorDeleteView.as_view()),
    #endregion


    
    #region function views
    url(r'^libros/$', libro_listado, name="libros"),
    url(r'^crear/libro/$', libro_form),
    url(r'^modificar/libro/(\d+)/$', libro_form),
    url(r'^eliminar/libro/(\d+)/$', libro_delete),
    #endregion
    #region class based views
    url(r'^libros_cbv/$', LibroListView.as_view(), name="libros_cbv"),
    url(r'^crear/libro_cbv/$', LibroCreateView.as_view()),
    url(r'^modificar/libro_cbv/(?P<pk>[0-9]+)/$', LibroUpdateView.as_view()),
    url(r'^eliminar/libro_cbv/(?P<pk>[0-9]+)/$', LibroDeleteView.as_view()),
    #endregion


]
