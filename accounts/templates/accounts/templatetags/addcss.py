from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field,attributes):
    className,idname = attributes.split("+")
    return field.as_widget(attrs={"class":className,"id":idname})


