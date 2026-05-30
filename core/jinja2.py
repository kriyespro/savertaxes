from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
import datetime
import json


def inr(value):
    """Format number as Indian Rupee: ₹1,23,456"""
    try:
        value = int(round(float(value)))
        if value < 0:
            return f"-₹{_inr_format(abs(value))}"
        return f"₹{_inr_format(value)}"
    except (ValueError, TypeError):
        return "₹0"


def _inr_format(n):
    s = str(n)
    if len(s) <= 3:
        return s
    # Indian number system: last 3 digits, then groups of 2
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.append(rest)
    parts.reverse()
    return ','.join(parts) + ',' + last3


def inr_short(value):
    """₹1.2L, ₹3.4Cr format for large numbers"""
    try:
        value = float(value)
        if value >= 10000000:
            return f"₹{value/10000000:.1f}Cr"
        elif value >= 100000:
            return f"₹{value/100000:.1f}L"
        elif value >= 1000:
            return f"₹{value/1000:.1f}K"
        return inr(value)
    except (ValueError, TypeError):
        return "₹0"


def pct(value, decimals=1):
    """Format as percentage: 22.0%"""
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "0%"


def usd(value):
    """Format number as US Dollar: $1,234,567"""
    try:
        value = int(round(float(value)))
        if value < 0:
            return f"-${abs(value):,}"
        return f"${value:,}"
    except (ValueError, TypeError):
        return "$0"


def usd_short(value):
    """$1.2M, $3.4K format for large numbers"""
    try:
        value = float(value)
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"${value/1_000:.1f}K"
        return usd(value)
    except (ValueError, TypeError):
        return "$0"


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'now': datetime.datetime.now,
        'settings': settings,
        'CURRENT_FY': settings.CURRENT_FY,
        'CURRENT_AY': settings.CURRENT_AY,
        'GA_ID': settings.GA_MEASUREMENT_ID,
        'ADSENSE_CLIENT_ID': settings.ADSENSE_CLIENT_ID,
        'ADSENSE_ENABLED': settings.ADSENSE_ENABLED,
    })
    env.filters.update({
        'inr': inr,
        'inr_short': inr_short,
        'usd': usd,
        'usd_short': usd_short,
        'pct': pct,
        'from_json': json.loads,
        'inr_no_symbol': lambda v: _inr_format(int(round(float(v)))) if v else '0',
    })
    return env
