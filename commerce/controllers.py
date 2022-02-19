from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4
from django.contrib.auth import get_user_model

from account.authorization import GlobalAuth
from commerce.models import Product, Label,artist, Category,City, Item, Order, OrderStatus,Address
from commerce.schemas import (ProductOut,  LabelOut, MessageOut, CategoryOut, ArtistOut ,CitiesOut,
                             CitySchema, ItemOut, 
                             ItemSchema, ItemCreate, Add_address, AddressSchema,AddressOut,OrderSchema)




User = get_user_model()


address_controller = Router(tags=['addresses'])
order_controller = Router(tags=['orders'])
city_controller = Router(tags=['City'])
checkout_controller = Router(tags=['checkout'])
commerce_controller = Router(tags=['products'])
order_controller = Router(tags=['order'])

@commerce_controller.get('products', response={
    200: List[ProductOut],
})
def list_products(request):
    products = Product.objects.all()
    # products = products.filter(name='tshirt')
    return products


@commerce_controller.get('products/{id}', response={
    200: ProductOut
})
def retrieve_product(request, id):
    return get_object_or_404(Product, id=id)






@commerce_controller.get('Label', response={
    200: List[LabelOut],
})
def list_label(request):
    label = Label.objects.all()
    # label = Label.filter(name='tshirt')
    return label


@commerce_controller.get('Label/{id}', response={
    200: LabelOut
})
def retrieve_Label(request, id):
    return get_object_or_404(Label, id=id)








def list_Artists(request):
    Artists = artist.objects.all()
    return Artists


@commerce_controller.get('Artists/{id}', response={
    200: ArtistOut
})
def retrieve_Artist(request, id):
    return get_object_or_404(artist, id=id)




# create all crud operations for Label, Merchant, Artist, Category

@commerce_controller.get('Categorys', response={
    200: List[CategoryOut],
})
def list_Categorys(request):
    categorys = Category.objects.all()

    return categorys


@commerce_controller.get('Categorys/{id}', response={
    200: CategoryOut
})
def retrieve_Category(request, id):
    return get_object_or_404(Category, id=id)




#------------------------------------- Address -------------------------------------
#-----------------------------------------------------------------------------------

@address_controller.get('address', response={
    200: List[AddressOut],
    404: MessageOut
})
def list_Address(request):
    Address_qs = Address.objects.all()

    if  Address_qs:
        return Address_qs

    return 404, {'detail': 'No Address found'}



@address_controller.get('address/{id}', response={
    200: AddressOut,
    404: MessageOut
})
def retrieve_address(request, id: UUID4):
    return get_object_or_404(Address, id=id)


@address_controller.post('', response={
    201: AddressOut,
    400: MessageOut
})
def create_address(request, address_in:  Add_address):
    city_instance = City.objects.get(id=address_in.city)
    del address_in.city
    address = Address.objects.create(**address_in.dict(), city=city_instance, user=User.objects.first())
    address.save()
    return 201, address


@address_controller.put('/{id}', response={
    200: AddressOut,
    404: MessageOut
})
def update_address(request, id: UUID4, new_data:Add_address):
    address = get_object_or_404(Address, id=id)
    city_instance = City.objects.get(id=new_data.city)
    new_data.city = city_instance
    for attr, value in new_data.dict().items():
        setattr(address, attr, value)
    address.save()
    return 200, address


@address_controller.delete('addresses/{id}', response={
    204: MessageOut
})
def delete_address(request, id: UUID4):
    city = get_object_or_404(Address, id=id)
    city.delete()
    return 204, {'detail': ''}




@order_controller.get('cart', response={
    200: List[ItemOut],
    404: MessageOut
})
def view_cart(request):
    cart_items = Item.objects.filter(user=User.objects.first(), ordered=False)

    if cart_items:
        return cart_items

    return 404, {'detail': 'Your cart is empty, go shop like crazy!'}


@order_controller.post('add-to-cart', response={
    200: MessageOut,
    # 400: MessageOut
})
def add_update_cart(request, item_in: ItemCreate):
    try:
        item = Item.objects.get(product_id=item_in.product_id, user=User.objects.first())
        item.item_qty += 1
        item.save()
    except Item.DoesNotExist:
        Item.objects.create(**item_in.dict(), user=User.objects.first())

    return 200, {'detail': 'Added to cart successfully'}


@order_controller.post('item/{id}/reduce-quantity', response={
    200: MessageOut,
})
def reduce_item_quantity(request, id: UUID4):
    item = get_object_or_404(Item, id=id, user=User.objects.first())
    if item.item_qty <= 1:
        item.delete()
        return 200, {'detail': 'Item deleted!'}
    item.item_qty -= 1
    item.save()

    return 200, {'detail': 'Item quantity reduced successfully!'}


@order_controller.delete('item/{id}', response={
    204: MessageOut
})
def delete_item(request, id: UUID4):
    item = get_object_or_404(Item, id=id, user=User.objects.first())
    item.delete()

    return 204, {'detail': 'Item deleted!'}


def generate_ref_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 6))






#----------------------- Create Order ------------------------------------------
#-------------------------------------------------------------------------------


@order_controller.post('create-order', response=MessageOut)
def create_order(request):
    
    
    order_qs = Order(
        user=User.objects.first(),
        status=OrderStatus.objects.get(is_default=True),
        ref_code=generate_ref_code(),
        ordered=False,
    )

    user_items = Item.objects.filter(user=User.objects.first(), ordered=False)
    user_items.update(ordered=True)
    

    
    order_qs.items.add(*user_items)
    order_qs.total = order_qs.order_total
    user_items.update(ordered=True)
    order_qs.save()

    return {'detail': 'order created successfully'}









#---------------------------- CheckOut --------------------------------
#----------------------------------------------------------------------


@checkout_controller.post('create-checkout', response=
{ 200: MessageOut})

def create_checkout(request,order_in:OrderSchema,note:str=None):
   

    if get_object_or_404(City):
        check_order=Order(
            user=User.objects.first(),
            status=OrderStatus.objects.get(title='SHIPPED'),
           

        )
        
        check_order.note=note
        check_order.ordered=True
        check_order.address=Address.objects.get(id=order_in.address)
        check_order.save()
        return {'detail': ' checkout created successfully'}
    else:
        return MessageOut

    