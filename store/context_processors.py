""" setting içerisinde templatesta yazım kurallarına uymak adına"""

from .models import Category


# Create your views here.
# bunu her sayfada sunmak için bu şekilde yazıp setting.py dosyasında templateslere eklememiz gerekir
def categories(request):
    return {
        'categories': Category.objects.all()
    }
