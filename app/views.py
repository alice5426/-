import os.path
import uuid
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
import base64
from django.views.decorators.csrf import csrf_exempt
from app.models import Goods, User, Cart, Sort, Buy
import hashlib
from django.conf import settings
import json

# hash加密存储与验证
def hash_md5(ciphertext):
    m = hashlib.md5()
    # 对待加密的明文进行update方法处理，输入的形式为字符串
    m.update(ciphertext.encode())
    # 以十六进制存储
    return m.hexdigest()


# 上传图片保存名字
def do_file_name(file_name):
    return str(uuid.uuid1()) + os.path.splitext(file_name)[1]


# 主界面
def index(request):
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(id=user_id)
        goods_list = Goods.objects.filter().exclude(user_id=user_id).order_by('create_time')
    else:
        goods_list = Goods.objects.filter().order_by('create_time')
    return render(request, 'index.html', locals())


# 登录
def login(request):
    if request.method == "GET":
        # username = request.session.get('username', None)
        # if username is None:
        # 伪随机数生成RSA公私钥对
        random_generator = Random.new().read
        rsa = RSA.generate(1024, random_generator)
        rsa_private_key = rsa.export_key()
        rsa_public_key = rsa.public_key().export_key()
        # 用session方式存储公私钥，PKCS1格式
        request.session['privkey'] = rsa_private_key.decode()
        request.session['pubkey'] = rsa_private_key.decode()
        pub_key = request.session.get('pubkey')
        return render(request, 'login.html', {'pub_key': pub_key})
    # else:
    # return HttpResponseRedirect(reversed('index'))

    if request.method == "POST":
        pub_key = request.session.get('pubkey')
        user_name = request.POST.get('username')
        password = request.POST.get('passwd')
        # 对用户输入的用户名和密码进行检查
        username_db = User.objects.values('username')
        if user_name and password:
            privkeystr = request.session.get('privkey').encode()
            privkey = RSA.importKey(privkeystr)
            cipher = PKCS1_v1_5.new(privkey)
            # 将base64编码格式password进行解码，后解密
            password = cipher.decrypt(base64.b64decode(password.encode()), 'error').decode()
            for user in username_db:
                if user_name == user['username']:
                    user_current = User.objects.get(username=user_name)
                    password_md5 = hash_md5(password)
                    if password_md5 == user_current.password:
                        request.session['user_name'] = user_current.username
                        request.session['user_id'] = user_current.id
                        return HttpResponseRedirect('/index/')
                    else:
                        error = "用户名或密码错误"
                else:
                    error = "用户名或密码错误"
            else:
                error = "用户名或密码错误"
            return render(request, 'login.html', locals())
    else:
        error = "用户名或密码不能为空"
        return render(request, 'login.html', locals())


# 注册
def register(request):
    if request.method == "GET":
        random_generator = Random.new().read
        rsa = RSA.generate(1024, random_generator)
        rsa_private_key = rsa.export_key()
        rsa_public_key = rsa.public_key().export_key()
        # 用session方式存储公私钥，PKCS1格式
        request.session['privkey'] = rsa_private_key.decode()
        request.session['pubkey'] = rsa_public_key.decode()
        pub_key = request.session['pubkey']
        return render(request, 'register.html', locals())

    if request.method == "POST":
        # 获取注册传入的参数
        sex = request.POST.get("sex")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        username = request.POST.get("username")
        pub_key = request.session['pubkey']
        if not username:
            username_error = "请输入正确的用户名"
            return render(request.GET, 'register.html', locals())
        # password_1 和 password_2加密
        password_1 = request.POST.get("passwd1")
        password_2 = request.POST.get("passwd2")
        if password_1 and password_1:
            # 利用存储在session中的密钥进行解密
            private_str = request.session.get('privkey').encode()
            private = RSA.importKey(private_str)
            cipher = PKCS1_v1_5.new(private)
            # 解密
            password_1 = cipher.decrypt(base64.b64decode(password_1.encode()), 'error').decode()
            password_2 = cipher.decrypt(base64.b64decode(password_2.encode()), 'error').decode()
        else:
            password_1_error = "密码不能为空"
            return render(request, 'register.html', locals())
        # 利用hash函数对password_1密码进行加密处理
        password_m1 = hash_md5(password_1)
        # 对password_2密码进行hash加密处理
        password_m2 = hash_md5(password_2)
        if password_m1 != password_m2:
            password_2_error = "两次输入密码不一致"
            return render(request, 'register.html', locals())
        # 查询用户是否注册
        try:
            old_user = User.objects.get(username=username)
            username_error = "当前用户已被注册"
            return render(request, 'register.html', locals())
        # 若当前用户没有找到，则会报错，说明当前用户名可以使用
        except Exception as e:
            try:
                user = User.objects.create(username=username, password=password_m1, sex=sex, email=email,
                                           phone_number=phone)
                # 注册成功
                success = "注册成功！请前往登录"
                # request.session['username'] = username
                return render(request, 'register.html', locals())
            except Exception as e:
                # 若创建不成功，报错
                username_error = "用户名已被占用"
                return render(request, 'register.html', locals())


# 退出
def login_out(request):
    del request.session['user_name']
    del request.session['user_id']
    del request.session['privkey']
    del request.session['pubkey']
    return HttpResponseRedirect("/index/")


# 用户中心
def user_center(request):
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
    if request.method == "GET":
        # 该用户发布的商品
        issue_list = Goods.objects.filter(user_id=user_id)
        # 该用户购物车中商品
        goods_list = Cart.objects.filter(cart_user_id=user_id)
        # 用户购物记录
        user_buy = Buy.objects.filter(user_id= user_id)

        cart_list = [] #存储用户购物车的商品
        for goods in goods_list:
            cart_id_dict = {}
            cart_id_dict['cart_id'] = goods.id
            cart_id_dict['cart_create'] = goods.cart_create_time
            cart_id_dict['good'] = Goods.objects.get(id=goods.goods_id)
            cart_list.append(cart_id_dict)

        buy_list = []  # 存储用户购物记录
        for buy in user_buy:
            user_buy_dict = {}
            user_buy_dict['buy_id'] = buy.id
            user_buy_dict['buy_create'] = buy.create_time
            user_buy_dict['good'] = Goods.objects.get(id = buy.good_id )
            buy_list.append(user_buy_dict )

        user = User.objects.get(id=user_id)
        if user.birthday != None:
            user_birthday = user.birthday.strftime('%Y-%m-%d')
        else:
            user_birthday = user.birthday
        return render(request, 'user_center.html', locals())


# 接受用户数据的修改
@csrf_exempt
def users_information(request):
    result = 0
    user_id = request.session.get('user_id')
    if request.method == "POST":
        username = request.POST.get("user_nicheng")
        print(username)
        user_information = request.POST.get("user_information")
        print(user_information )
        user_sex = request.POST.get("user_sex")
        print(user_sex)
        user_birthday = request.POST.get("user_birthday")
        print(user_birthday)
        user_address = request.POST.get("user_address")
        user_img = request.FILES.get("head_img")
        print(user_img )
        if user_img == None:
            try:
                User.objects.filter(id=user_id).update(username=username, information=user_information, sex=user_sex,
                                                    birthday=user_birthday, address=user_address)
                result = 1
            except Exception as e:
                print(e)
        else:
            user_img_chunks = user_img.chunks()
            # 文件保存路径
            user_img_name = os.path.join("image", do_file_name(user_img.name)).replace('\\', '/')
            # 文件完整的保存路径
            user_img_path = os.path.join(settings.MEDIA_ROOT, user_img_name).replace('\\', '/')
            with open(user_img_path, "wb") as file:
                for chunk in user_img_chunks:
                    file.write(chunk)
            try:
                User.objects.filter(id=user_id).update(username=username, information=user_information, sex=user_sex,
                                                       img=user_img_name, birthday=user_birthday, address=user_address)
                result = 1
            except Exception as e:
                print(e)
    return HttpResponse(result)



# 商品发布页面
def issue_page(request):
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')

    if request.method == "GET":
        return render(request, 'issue_page.html', locals())


@csrf_exempt
def issue_form(request):
    flag = 0
    if request.method == "POST":
        goods_name = request.POST.get('goods_name')
        print(goods_name)
        goods_detal = request.POST.get('goods_detal')
        print(goods_detal)
        goods_price = request.POST.get('goods_price')
        print(goods_price)
        categorys = request.POST.get('categorys')
        print(categorys)
        address = request.POST.get('address')
        print(address)
        pho_num = request.POST.get('pho_num')
        print(pho_num)
        file_img = request.FILES.get('file_img')  # 获取文件
        print(file_img.name)
        print(file_img.size)
        file_chunks = file_img.chunks()
        # 文件保存路径
        file_name = os.path.join("image", do_file_name(file_img.name)).replace('\\', '/')
        # 文件完整的保存路径
        file_path = os.path.join(settings.MEDIA_ROOT, file_name).replace('\\', '/')
        with open(file_path, "wb") as file:
            for chunk in file_chunks:
                file.write(chunk)
        new_issue = Goods()
        new_issue.name = goods_name
        new_issue.detal = goods_detal
        new_issue.price = goods_price
        new_issue.master_pho = pho_num
        userid = request.session.get('user_id')
        new_issue.user_id = userid
        sort = Sort.objects.get(id=categorys)
        new_issue.sort_id = sort.id
        new_issue.img = file_name
        try:
            new_issue.save()
            flag = 1
        except Exception as e:
            print(e)
    return HttpResponse(flag)


# 商品详情页面
def good_detail_page(request):
    user_name = request.session.get('user_name')
    id = request.GET.get('id')
    print("id:" + id)
    goods_detail = Goods.objects.get(id=id)
    return render(request, "good_detail_page.html", {"goods_detail": goods_detail, "user_name": user_name})


# 测试
def test(request):
    user_id = request.session.get("user_id")
    cart = Cart()
    cart.user_id = User.objects.get(id=user_id)
    return HttpResponse(cart.user_id.id)


# 加入购物车
def join_cart(request):
    result = 1
    good_id = request.GET.get("id")
    print(good_id)
    user_id = request.session.get("user_id")
    cart = Cart()
    cart.cart_user_id = user_id
    cart.goods_id = good_id
    try:
        cart.save()
    except Exception:
        print(Exception)
        result = 0
    return HttpResponse(json.dumps(result))


# 发布商品的删除
def  del_goods(request):
    result = 1
    good_id = request.GET.get("id")
    print("id"+good_id)
    try:
        Goods.objects.filter(id=good_id).delete()
    except Exception:
        result = 0
    return HttpResponse(json.dumps(result))


# 购物车商品删除
def del_carts(request):
    result = 1
    user_id = request.session.get("user_id")
    good_cart_id = request.GET.get("id")
    del_cart_dict = {}
    try:
        del_cart_dict["cart_user_id"] = user_id
        del_cart_dict ["id"] =good_cart_id
        Cart.objects.filter(**del_cart_dict).delete()
    except Exception as e :
        result = 0
        print(e)
    return HttpResponse(json.dumps(result))


# 购买商品
def buy_goods(request):
    result = 1
    user_id = request.session.get("user_id")
    good_id = request.GET.get("id")
    buy = Buy()
    buy.user_id = user_id
    buy.good_id = good_id
    try:
        buy.save()
    except Exception:
        result = 0
    return HttpResponse(json.dumps(result))
