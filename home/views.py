from django.shortcuts import render
from .models import Usermsg
from .models import Typemsg
from .models import Article
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
def article(request,aid):
    thisarticle = list(Article.objects.filter(id=aid).values("id", "title", "author", "content"))[0]
    return render(request, "detail.html", {"thisarticle": thisarticle,})
def reg(request):
    if request.session.has_key("name617826782"):
        return HttpResponseRedirect("/")
    if request.method == "POST":
        name = request.POST["name"]
        passwd = request.POST["passwd"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        Usermsg.objects.create(name=name, passwd=passwd, email=email, phone=phone, isadmin=0)
        return HttpResponse("注册成功！")
    return render(request, "reg.html")
def login(request):
    if request.session.has_key("name617826782"):
        return HttpResponseRedirect("/")
    if request.method == "POST":
        name = request.POST["name"]
        passwd = request.POST["passwd"]
        islogin = Usermsg.objects.filter(name__exact=name, passwd__exact=passwd)
        if islogin:
            request.session["name617826782"] = name
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("登录失败！")
    return render(request, "login.html")
def logout(request):
    del request.session["name617826782"]
    return HttpResponseRedirect("/")
def index(request):
    if request.session.has_key("name617826782"):
        nav1 = request.session["name617826782"]
        nav2 = "/"
        nav3 = "退出"
        nav4 = "/logout"
    else:
        nav1 = "注册"
        nav2 = "/reg"
        nav3 = "登录"
        nav4 = "/login"
    typename = Typemsg.objects.values("id", "typename")
    article = Article.objects.values("id", "title", "author", "detail")[:20]
    return render(request, "index.html",{"article": article, "typename": typename, "nav1": nav1, "nav2": nav2, "nav3": nav3, "nav4": nav4})
def alist(request):
    if request.session.has_key("name617826782"):
        nav1 = request.session["name617826782"]
        nav2 = "/"
        nav3 = "退出"
        nav4 = "/logout"
    else:
        nav1 = "注册"
        nav2 = "/reg"
        nav3 = "登录"
        nav4 = "/login"
    typename = Typemsg.objects.values("id", "typename")
    article = Article.objects.values("id", "title", "author", "detail")
    return render(request, "list.html",{"article": article, "typename": typename, "nav1": nav1, "nav2": nav2, "nav3": nav3, "nav4": nav4})
def postarticles(request):
    if request.session.has_key('name617826782') == False:
        return HttpResponseRedirect('/login')
    else:
        nav1 = request.session['name617826782']
        nav2 = "/"
        nav3 = "退出"
        nav4 = "/logout"
    # 查询所有类别ID与名称
    typeall = Typemsg.objects.values("id", "typename")
    typeid = []
    typename = []
    for item in typeall:
        typeid.append(item["id"])
        typename.append(item["typename"])
    typeidandname = zip(typeid, typename)
    # 查询当前UID
    user = list(Usermsg.objects.filter(name=request.session['name617826782']).values())[0]
    uid = user["id"]
    uname = user["name"]
    isadmin = user["isadmin"]
    if (not isadmin):
        return HttpResponse("抱歉！只有管理员有权限发博文")
    if request.method == "POST":
        content = request.POST["content"]
        thistypeid = request.POST["typeid"]
        postname = request.POST["title"]
        detail = request.POST["detail"]
        Article.objects.create(title=postname, content=content, tid=thistypeid, uid=uid, author=uname, detail=detail)
        return HttpResponseRedirect('/')
    return render(request, 'postarticles.html',{"typeidandname": typeidandname, "nav1": nav1, "nav2": nav2, "nav3": nav3, "nav4": nav4})