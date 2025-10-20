from blog import models as BlogModels
from about import models as AboutModels

class GlobalPageMixin:
    """Mixin untuk menambahkan context slider dan artikel."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_banners'] = BlogModels.SliderBanner.objects.filter(n_istatus='1')
        context['arctile1'] = BlogModels.Artikel1.objects.filter(n_istatus='1')
        return context