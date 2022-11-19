import os.path
import uuid
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
import base64
from django.views.decorators.csrf import csrf_exempt
from app.models import Goods, User, Cart, Sort
import hashlib
from django.conf import settings


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


def index(request):
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
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
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        # 对用户输入的用户名和密码进行检查
        username_db = User.objects.all()
        if username and password:
            privkeystr = request.session.get('privkey').encode()
            privkey = RSA.importKey(privkeystr)
            cipher = PKCS1_v1_5.new(privkey)
            # 将base64编码格式password进行解码，后解密
            password = cipher.decrypt(base64.b64decode(password.encode()), 'error').decode()
            for user in username_db:
                if username in user.username:
                    user_current = User.objects.get(username=username)
                    password_md5 = hash_md5(password)
                    if password_md5 == user_current.password:
                        request.session['user_name'] = user_current.username
                        request.session['user_id'] = user_current.id
                        return HttpResponseRedirect('/index/')
                    else:
                        error = "用户名或密码错误"
                        return render(request, 'login.html', locals())
                else:
                    error = "用户名或密码错误"
                    return render(request, 'login.html', locals())
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
    return render(request, 'user_center.html', locals())


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
