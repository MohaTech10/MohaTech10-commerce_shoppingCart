from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
def returnListProducts(request):
    all_products = Products.objects.all()

    all_current_stu_products = Products.objects.filter(student=request.user.student)
    # print(all_current_stu_products)

    # here we wanna do smth to change the button from add to cart to already
    # followed/purchased to that we have to grab the user items that they
    # clicked add to cart cuz since they do that theses items go to them
    # then check if the item get selected in their cart/Order or not that's it
    active_now_order = Orders.objects.filter(who_orders=request.user.student, is_ordered=False)


    all_THEcurrent_order_products = []  # list contains all the objects/product
    # has been ordered and added to the current active one order
    if active_now_order.exists():
        grab_the_active = active_now_order[0]
        all_current_order_query = grab_the_active.ordered_items.all()
        all_THEcurrent_order_products = [ordered_item.product for ordered_item in all_current_order_query]

    context = {
        'products_list': all_products,
        'current_order_products': all_THEcurrent_order_products,
        'student_courses': all_current_stu_products,
        'cart_icon': len(all_THEcurrent_order_products),
        'active_order': active_now_order

    }
    return render(request, 'AdvancedCart/all_courses.html', context)

# قيس على هذا اللوجيك حتى الاضافات والفولو نفس الطريقه بالزبط
def addToCart(request, pk_):
    # to know who will buy and also to check if a product being purchased
    # already belongs to the current user owner profile
    the_user = request.user.student

    # to know which item gets selected !
    the_item = Products.objects.get(id=pk_)
    # becomes_ordered, created = OrderedProducts.objects.get_or_create(product=the_item)

    #  now we will access the user products and for now they are empty
    if the_item in the_user.student_product.all():
        messages.info(request, 'you own this product')
        return redirect('all_products')
    # here it means this user owns nothing like in case right now
    # so we will add the item to be OrderedItem and take this item to
    # the OrderedItem row and put it there .

    # if the products not in the user profile so it is the first time for them
    # buy it so take it as OrderedITem and add it the cart/order and ordereditem

    # الفكره في هذا السطر زي ماقلنا get_or_create وكانها تلعب دور pk بحيث تجعلك تسوي new instance
    # مره واحده بعد كذا مهما جلست تضغط على زر ادد تو كارت من خلال هذا السطر لن يجعلك خلق ريو انستانس لا
    # لانها تشوف هل الانستانس الجديد موجود في المودل ؟ اذا ايوه تسويلو update اذا يحتاج تحديث غير كذا راح تطنشك
    # بمعنى ()it save فقط مره واحده !
    # هذي الايتم او العنصر او الكورس او الوجبه الي مهتم فيها اليوزر وييبغا يضيفها للكارت فنحن اخذناها الان وودينها كorderedITem
    becomes_ordered, created = OrderedProducts.objects.get_or_create(product=the_item)

    # creating an active order here, it will be so till is_ordered = True  which is until the transaction gets done
    # then we will create another one
    active_order_belongs_to_current_user, created = Orders.objects.get_or_create(who_orders=the_user, is_ordered=False)

    active_order_belongs_to_current_user.ordered_items.add(becomes_ordered)

    # this is true but when we make sure that the user has already purshased
    # and get completely the course or the item then we can add it to their
    # account to make sure that they just own it so we do not need it now
    # the_user.student_product.add(the_item)
    active_order_belongs_to_current_user.save()

    messages.info(request, 'item has been added to OrderedItem and السلة')
    return redirect('all_products')

# طبعا الطريقه المثلى للحذف يكون في صفحه اخرى وتكون فالسامري عشان الايدي حق العنصر لازم
# يكون هوا الايدي حق العنصر في ORDEREDProducts
def deleteItem(request, pk_):

    # هيا الفكره انها يتم حذفه من كونه اورديرد ايتم الى ان يرجع ايتم عايدي
    the_item_will_be_deleted = OrderedProducts.objects.get(id=pk_, is_ordered=False)

    # يتم استخدام فيلتر ايضا عشان بدون مايتم استخدام فورم يتم التاكد هل هوا موجود العنصر او لا باستخدام
    # exists() الي ماتجي في القيت ميثود لذلك يتم استخدام فيلتر او get_or_404

    the_item_will_be_deleted.delete()
    messages.info(request, 'has been removed')
    return redirect('the_cart')


def currentCart(request):
    current_user = get_object_or_404(Student, user=request.user)
    current_active_order = Orders.objects.filter(who_orders=current_user, is_ordered=False)
    if current_active_order.exists():
        return current_active_order[0]
    return 0

def viewCart(request):
    # rendering out all the orderedPro
    # all_ordered_items = OrderedProducts.objects.filter(is_ordered=False)
    exist_order = currentCart(request)

    # current_active_order.ordered_items.all() هذي هيا بالزبط بس انا سويت دااله كل انستانس اوردر يقدر يوصلها
    # is_order=False in Orders Model gives a lot ! بحيث تجعلني قادر ماسوي اوردر جديد واعرف انه فيه اوردر
    # فعال نشط لليوزر مايهم سوا فيه عناضر او لا بس اخليه شغال بحيث مايحتاج اسوي نيو انستانس اوردر لا فيه واحد شغال
    # ومن خلاله اقدر اوصل ومتطمن انه واصحد object اسوي فيه الي ابا مهمه جدا!

    exist_order.getAllItemsIn()

    context = {
        'order': exist_order
    }
    return render(request, 'AdvancedCart/cart_page.html', context)





# فيه بعض الخطوات الي لازم نكون متطلعين عليها قبل مايتم شراء الطلب راح نذكرها
def transactionProcess(request, pk_):
    # get the current order being purchased, تقدر ايضا تجيبه عن طريق is_ordered = False ! عادي
    # كلو يمشي
    order_to_purchase = Orders.objects.get(id=pk_)

    # and then we have to update the order to be is_ordered = True, cuz to let them finish
    # the opened still one and if its true close it and let them open another one
    # their order and have the ability to order again
    # updating the order to be shipped
    order_to_purchase.is_ordered = True
    order_to_purchase.save()

    # get all the current_order items, and update them,
    # current_active_order.ordered_items.all() هذي هيا بالزبط بس انا سويت دااله كل انستانس اوردر يقدر يوصلها
    all_order_items = order_to_purchase.getAllItemsIn()
    all_order_items.update(is_ordered=True)

    # convert the items into their general way which is Products to be sent the user courses so this fields just accept the original Object type course
    # not OrderedCourses
    current_product_in_the_current_order = [item.product for item in all_order_items]

    # grab the current user
    current_user = request.user.student
    # this is used when we wanna send lists of objects to the user
    # if many to many and you wanna send one instance such as Java only then ..add(instance)
    # but because many to many and wanna send lists of objects we use this * to send them
    current_user.student_product.add(*current_product_n_the_current_order)
    current_user.save()

    messages.info(request, 'thanks for buying theses courses ')
    return redirect('all_products')

def currentCustomerOrders(request):
    # filtering all current user order that is is_ordered = True
    all_ordered_orders = Orders.objects.filter(is_ordered=True)
    # for i in all_ordered_orders:
    #     for j in i.ordered_items.all():

    context = {
        'user_purchased_orders': all_ordered_orders
    }
    
    return render(request, 'AdvancedCart/user_orders.html', context)