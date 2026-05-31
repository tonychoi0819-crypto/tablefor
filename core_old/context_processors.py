from .models import SiteSettings

def site_settings(request):
    settings = {}
    for s in SiteSettings.objects.all():
        settings[s.key] = s.value
    return {
        'site_name': settings.get('site_name', 'TableFor'),
        'site_tagline': settings.get('site_tagline', "Hong Kong's Honest Restaurant Guide"),
        'site_settings': settings,
    }
