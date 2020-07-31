from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.contrib.auth.admin import User
class Tags(models.Model):
    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_name

# so here is just a way of explaining what is a pro/item
# اكتشفت انه لازم يكون حلقه وصل بين الايتم اوبجكيت والسله الا وهي العمليه الي تحدث 'OrderedItem' وهيا مودي يحمل فقط ويسوي انشا new instance عندما
# تضيف ايتم معين الى السله بحيث الاوردر يسوي rendering من المودل المنتجات المطلوبه فهمت ؟
class Items(models.Model):
    name = models.CharField(max_length=100, null=True)
    tag = models.ManyToManyField(Tags)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        # if slug does not exist yet not created
        if not self.slug:
            self.slug = slugify(self.name)  # it takes the name and convert it into slug field
        super(Items, self).save(args, kwargs)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


# هنا تحدث العمليه بحيث ون يوزر يقدر يشتري الكثير من الايتمز وهيا تكون العلاقه بين الايتم والسله
# يعني بمجرد انك تروح لكل الاتيمز الي فوق وتقول بشتري تصبح هذي الايتم مسجله ويتم انشائها ك انستانسيس في المودل هذا وتصبح منتجات تم طلبها
# ثم نروح فالسله نقوم نعرض في الصفحه الصفوف الي هنا وثمن نسوي للاوردر تاكيد الي راح يكون يحمل اسطر من المشتريات المنتجيه وهكذا
class OrderedItems(models.Model):
    # and takes the item that will be purchased !
    # and who will buy these items before even who will create the order
    user_purchaser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    clicked_the_item_or_ordered = models.BooleanField(default=False)
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.items.name


# طبعا بعد ماصار عندنا مكان للمنجات الي تم شرايها الان نقدر نسوي create instance يكون فقط زي الخزان اضيف فيه الطلبات الي تم طلبها ولن يتم فتح اوردر الا
# معناتو فيه instances of the OrderItems !
class Orders(models.Model):
    # should take the user who has placed that orders , and on order should just hold the PurchasedItems not all the items
    # objects !
    who_orders = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItems)
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # super important cuz it will tell us to keep the order holds new items if its false تعني انه هوا لسا نفس الاوردر خليه يعبي
    # طلبات فيلو لمن تصير True معناتو خلاص تم معالجة الطلب والان يقدر يسوي اوردر جديد ! بنيو ايتمز
    is_ordered = models.BooleanField(default=False)
    order_date_create = models.DateTimeField(auto_now_add=True, null=True)
    order_date_purchased = models.DateTimeField(null=True)


    # user here but i am not gonna mentioned
    def __str__(self):
        return 'order\'s ' + str(self.order_id)
