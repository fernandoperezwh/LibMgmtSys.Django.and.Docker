from django import template

register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key: return dict_data.get(key)


@register.filter('join_authores')
def join_authores(lista_autores):
    string = ""
    for autor in lista_autores:
        string += "{} {}, ".format(autor.apellidos, autor.nombre)
    return string