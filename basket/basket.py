from decimal import Decimal

from store.models import Product


class Basket():
    """
   Gerektiğinde miras alınabilen veya geçersiz kılınabilen bazı varsayılan davranışlar sağlayan
   bir temel sepet sınıfı
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        oturum verisine ürün ekler
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
        else:
            self.update(product_id, qty)
        self.save()

    def __iter__(self):
        """
        collect the product_id in the session data to query the database and
        return products.
        sessiondaki product idleri getirir
        :return:
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)

        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
         # yeni bir şey sepete eklendiği zaman o an sepet güncelleniyor fakat refresh
     edince varsayılan değere geliyor. o yüzden sessiondan data göndermeliyiz.
     base html içinde kullanıalcak. bunlar context procesor tarafından oluyor
        :return:
        """

        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product_id):
        """
        delete item from session data
        :param product_id:
        :return:
        """
        product_id = str(product_id)
        print(type(product_id))
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product_id, product_qty):
        product_id = str(product_id)
        product_qty = product_qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self.save()

    def save(self):
        self.session.modified = True
