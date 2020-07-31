from django.db import models
from django.contrib.auth.admin import User

class Products(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.product_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # الفكره هنا لحفظ وجعل اليوزر يملك كورسات الان وهذا طبيعي جدا كل طالب لديه مواد وايضا، لمن يملك كورسات اقدر اسوي تشيك هل الكورس او الوجبه الي بيشتريها موجوده ضمن كورسات اذا ايه ! انت تملكها ببساطه !
    student_product = models.ManyToManyField(Products, null=True, blank=True)

    def __str__(self):
        return self.user.username

# هنا نضع العمليه التي تحدث في موقعنا الا وهيا شرا المنتجات / المواد
# الان هذا الاوجيكت اصبح تماما منتج واحد يمثل فقط منتج واحد لكن يكون منتج سوف يتم شرائه هذا هو الفرق الوحيد !
class OrderedProducts(models.Model):
    # فقط في هذي الحاله نستخدم 1T1 عشان احنا نبغا المنتج العام يتم ويتحول الي عنصر سوف يتم شرائه مره واحده بعد كذا نبغا نقوله لا ي بويا انت تملك هذا العنصر او اقوله هيا روح علي السله معد يمديك تشتريه مره ثانيه
    # وليس زي حالتنا القديمه الي هيا يقدر يشتري على كيفه !
    product = models.OneToOneField(Products, null=True, on_delete=models.SET_NULL)
    is_ordered = models.BooleanField(default=False)
    date_clicked = models.DateTimeField(auto_now_add=True)
    # to check if this basically has been ORDERED once before or no?!

    def __str__(self):
        return self.product.product_name

class Orders(models.Model):
    who_orders = models.ForeignKey(Student, on_delete=models.CASCADE)
    ordered_items = models.ManyToManyField(OrderedProducts)
    # هنا حتكون شكلها يعني فالسله كذا
    # كلهم حيكون تقدر تعلم عليهم لانهم م-٢-م فانا لمن اقول .all() راح اجيبهم كلهم في لسته ثم اسوي لوب عليهم في كل لوبه حوصل لواحد فيهم ثم هوا اساسا يمثل وان general product object الان خش جيب سعره وبس
    # 1- java
    # 2- Python
    # 3- C
    is_ordered = models.BooleanField(default=False)
    date_order = models.DateTimeField(auto_now_add=True)


    # must get the total price of the order itself which will be just getting the orderedItem.products price and show them !
    def getCartTotal(self):
        return sum([ordered_item.product.price for ordered_item in self.ordered_items.all()])
    def getAllItemsIn(self):
        # من خلالها راح اوصل لكل الطلبات حقون الي الاوردر انستانس الحالي واذا تم
        # شراء الاوردر قبل ماسوي عليه True وتم ارسلهم لليوزر بحيث حبقى عارف
        # اذا هذي العناصر فيه حساب المستخدم خلاص معناتو ياحببي انتا اشتريتهم
        # لاتضحك عليا !
        return self.ordered_items.all()
    def __str__(self):
        return str(self.id)