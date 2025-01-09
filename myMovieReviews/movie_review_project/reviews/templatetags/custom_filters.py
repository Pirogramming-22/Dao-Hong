from django import template

register = template.Library()

# 런타임을 시간과 분으로 변환하는 커스텀 필터
@register.filter
def hours(value):
    """런타임을 시간으로 변환"""
    return value // 60

@register.filter
def minutes(value):
    """런타임을 분으로 변환"""
    return value % 60
