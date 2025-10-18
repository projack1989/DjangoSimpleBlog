from django import template

register = template.Library()

@register.inclusion_tag('blog/slidersection.html')
@register.inclusion_tag('blog/about.html')
@register.inclusion_tag('blog/categorySection.html')
@register.inclusion_tag('blog/cultureSection.html')
@register.inclusion_tag('blog/businessCategorySection.html')
@register.inclusion_tag('blog/lifeCategorySection.html')