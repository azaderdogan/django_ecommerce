from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)

    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        # sepettekiler ve yeni eklenenleri toplamak istiyoruz
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response


def basket_delete(request):
    # session objemizi çağırıyoruz
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))

        basket.update(product_id=product_id, product_qty=product_qty)

        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_total})
        return response