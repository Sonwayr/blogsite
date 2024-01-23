from django import template

register = template.Library()


@register.inclusion_tag('blog/post_tag.html')
def show_post_tag(post, a_lot=False, draft=False):
    return {'post': post, 'a_lot': a_lot, 'draft': draft}


@register.inclusion_tag('blog/info_tag.html')
def show_info(title):
    return {'title': title}


@register.inclusion_tag('blog/form_tag.html')
def show_form(form, btn_name, delete=False):
    return {'form': form, 'btn_name': btn_name, 'delete': delete}


@register.inclusion_tag('pagination.html')
def paginate(page_obj):
    return {'page_obj': page_obj}
