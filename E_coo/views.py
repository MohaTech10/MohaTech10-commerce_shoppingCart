from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import *

from django.contrib import messages
# i will remove this view, and i will use class based-views specifically ListView that does pretty same thing about what
# this function does but a bit cleaner and shorter
class AllObjectsOfOneItemsList(ListView):
    # الان هذا الكلاس مسوؤل يروح للمودل الي اعطيته ويجيب كل الاوبجيكتس وثمن يرسل var context للتمبليت هذي
    model = Items  # Items.objects.all()   context { object_list: model } => to the template down as object_list
    template_name = 'all_prosucts.html'

# class SpecificInstanceToViewDetail(DetailView):
#     # هنا نفس الحكايه راح تجيب لك تفاصيل عن انستانس واحد وراح يكون من الانستانيس حقون المودل ايتمز وسوف يتم التعرف علليهم عن طريق السلق slug
#     model = Items
#     template_name = 'one_product.html'


    # and it returns  object as var context
    # ودايما في هذا الحاله لمن يتم طلب انستانس معين نحتاج فيلد في المودل اسمه slug + راح نستخدم get_absolute_url الي هوا راح يكون page_name
    # kwargs {'slug': slugField}
    # same thing that i used to do {% url 'name=page_name_leads_to_url' the instance chosen id/slug %}

    # طبعا تسويها في كل موديل فيلو انستانس الناس تبحث عنهم او تبا تشوف بياناتهم بشكل خاص في dynamic url rendering


# using view will solve the problem of many to many or one-to-many

def getObjectChosen(request, slug):
    # test
    all_ordered_items = OrderedItems.objects.all()



    the_item = Items.objects.get(slug=slug)
    
    # print(all_ordered_items)
    # for i in all_ordered_items:
    #     if the_item.id == i.items.id:
    #         print("True")

    all_item_tags = Tags.objects.filter(items=the_item)
    tags_list = []
    for tag in all_item_tags:
        tags_list.append(tag.tag_name)
    context = {
        'object': the_item,
        'the_tags': ','.join(tags_list),
        'ordered_items': all_ordered_items
    }
    return render(request, 'one_product.html', context)



def addToCart(request, slug):  # which item to add to cart !! we have to get which one and that's by their id or what ever !
    the_item = Items.objects.get(slug=slug)
    # for the last time this line to make sure all the OrderedItem instances will be something new i mean no duplicate instance if there is by clicking
    # on the button add to cart it will make sure and check if its already in the OrderedItems table if so then not created it will grab it and get it
    becomes_ordered_item, created = OrderedItems.objects.get_or_create(
        user_purchaser=request.user,
        items=the_item,
        clicked_the_item_or_ordered=False
        # to not create item has been already clicked and purchased into
        # the OrderItem model
    )

    # getting just the current active order
    user_orders_current_order = Orders.objects.all().filter(who_orders=request.user, is_ordered=False)

    # طبعا هذا البلوك كلو متعلق بالسله والمودل ORDER وكيفيه اضافه العناصر اليه وهنالك طريقتين بعد التحقق انه هل يوجد اوردر؟
    # وطبعا يكون الجواب ايوه بعد فتحه بالمرور على else في المرة الاولى ثم طريقة الاضافه تبدا
    # طبعا هنا الموضوع شويه مختلف هنا شرطين فقط هل فيه اكتيف اوردر ؟ ايه معناتو حلو اليوزر بدا يضيف شي في السله
    if user_orders_current_order.exists():
        current = user_orders_current_order[0]
        print(current)

        # ثم هنا الشرط الثاني بعد ماتم التاكد انه فيه اكتيف اوردر هل العنصر المراد اضافته موجود مسبقا فالاكتيف اوردر ؟ اذا ايوه لاتضيفه بس حدث الكميه حقته
        # هنا تبدا طريقه الاضافه وهيا كالتالي بالتحقق اولا هل العنصر المنتج موجود في السله ؟ اذا ايه
        # ستم فقط الزياده على كمية هذا العنصر الي موجود فالسله وحفظ التعديلا
        # check if the OrderedItem in the Order already to increase_it
        if current.items.filter(items__slug=slug).exists():
            becomes_ordered_item.quantity += 1
            becomes_ordered_item.save()
            messages.info(request, 'has been updated to your cart again')

        # HERE IT MEANS IF A NEW ITEM WILL BE PURCHASED
        # هنا الجزء الثاني الي هوا هذا العنصر ليس موجود في السله بعد يتم اضافته الى السله والحفط
        else:
            messages.info(request, 'has been added to your cart')
            current.items.add(becomes_ordered_item)


    # هنا يتم النظر الى هذا الشرط عندما لايكون هنالك طلب يعني فتح طلب جديد وتفعيله ويكون اكيد عن
    # طريق اضافة عنصر الفاتحه الي تم الضغط عليه  كأول عنصر يتم شراؤه ثم يبقى فعال الطلب يتم
    # اضافة اليه العناصر الاخرى بس مره واحده ينظر اليه ثم شغلنا كله فوق
    else:
        # creating a new order and put the first item in and then
        # all other items will be added to the order here created
        # until is_orderd = True => then we will open a new order
        messages.info(request, 'has been added')
        order = Orders.objects.create(who_orders=request.user)
        order.items.add(becomes_ordered_item)


    return redirect("product", slug)












def viewCart(request):
    all_purchased_items_in_one_order = OrderedItems.objects.all()

    context = {
        'all_items': all_purchased_items_in_one_order
    }
    return render(request, 'the_cart.html', context)


class viewAllPurchasedItems(ListView):
    model = OrderedItems
    template_name = 'the_cart.html'


def removeFromCart(request, slug):
    # grabbing the item that will be removed !
    the_item = Items.objects.get(slug=slug)
    # and then get all orders that belong to the
    # current user
    current_order = Orders.objects.filter(
        who_orders=request.user,
        is_ordered=False
    )
    if current_order.exists():
        # grab the active one that belongs to a user
        order = current_order[0]
        # check if Ordered item in the order model
        if order.items.filter(items__slug=slug).exists():
            inside_ordered_items = OrderedItems.objects.filter(
                user_purchaser=request.user,
                items=the_item,
                clicked_the_item_or_ordered=False
            )[0]
            print(OrderedItems.objects.filter(
                user_purchaser=request.user,
                items=the_item,
                clicked_the_item_or_ordered=False
            )[0])
            order.items.remove(inside_ordered_items)
            inside_ordered_items.delete()
            messages.info(request, 'has been removed completely from your cart')

        else:
            messages.info(request, 'item is no longer in your cart')
            return redirect('product', slug)
    else:
        messages.info(request, 'you did not even have any order yet')
        return redirect('product', slug)
    return redirect('product', slug)
