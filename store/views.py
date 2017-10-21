from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from store.models import Item


def add_to_bucket(request):
    # item_id = request.GET['id']
    # print(item_id)
    # return HttpResponse(1, content_type="text/html")
    item_id = request.GET.get('id', None)
    data = {
        'is_added': "success"
    }
    return JsonResponse(data)


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


def sign_out(request):
    logout(request)
    return redirect('store:login')


def sign_up(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    email = request.POST.get('email', False)
    if username_present(username):
        return redirect('store:login')

    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    pw = new_user.check_password(password)

    return redirect('store:login')


def sign_in(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    if not username_present(username):
        return redirect('store:login')
    user = User.objects.get(username=username)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('store:store')
    else:
        return redirect('store:login')


def login_manager(request):
    print("login manager")
    # logout(request)
    if request.user is None:
        return redirect('store:login')
    return redirect('store:store')
    # return redirect('store:login')


@login_required
def store_main(request):
    items_list = Item.objects.all().order_by("price")
    paginator = Paginator(items_list, 9)  # Show 25 contacts per page

    page_request_var = "page"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "items_list": queryset,
        "title": "Store",
        "page_request_var": page_request_var,
    }
    return render(request, "store_list.html", context)


def goto_login(request):
    context = {}
    return render(request, "login.html", context)
