import json

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from store.models import Item, Bucket, Order


@login_required
def add_to_bucket(request):
    # TODO Changing number in card onSuccess of ajax query
    item_id = request.GET.get('id', None)
    bucket = Bucket.objects.get(user=request.user)
    json_list = json.loads(bucket.items)
    json_list.append(item_id)
    bucket.items = json.dumps(json_list)
    bucket.save()
    data = {
        'is_added': "success"
    }
    return JsonResponse(data)


@login_required
def user_bucket(request):
    bucket = Bucket.objects.get(user=request.user)
    ids_list = json.loads(bucket.items)
    items_list = list()
    for id in ids_list:
        items_list.append(Item.objects.get(id=id))
    context = {
        "items_list": items_list,
        "title": "Bucket of " + request.user.username,
        "user_bucket_size": len(items_list),
    }
    return render(request, "bucket.html", context)


@login_required
def delete_from_bucket(request):
    user = request.user
    bucket = Bucket.objects.get(user=user)
    items_list = json.loads(bucket.items)
    items_list.remove(request.GET.get('id', None))
    bucket.items = json.dumps(items_list)
    bucket.save()
    data = {
        'is_deleted': "success"
    }
    return JsonResponse(data)


@login_required
def user_orders(request):
    user = request.user
    orders = Order.objects.all().filter(user=user)
    # TODO number of items in order
    # TODO price of an order
    context = {
        "title": user.username + " orders",
        "order_list": orders
    }
    return render(request, "orders.html", context)


@login_required
def manager_orders(request):
    user = request.user
    if not user.is_staff and user.is_superuser:
        return redirect('store:store')
    orders = Order.objects.all()
    context = {
        "title": "Orders",
        "order_list": orders
    }
    return render(request, "orders_manager.html", context)


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
    is_super = request.POST.get('is_super', False) == 'on'
    email = request.POST.get('email', False)
    if username_present(username):
        return redirect('store:login')

    new_user = User.objects.create_user(username, email, password)
    new_user.is_staff = True
    new_user.is_superuser = True
    new_user.save()
    bucket = Bucket.objects.create()
    bucket.user = new_user
    bucket.items = json.dumps(list())
    bucket.save()
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
def clean_bucket(request):
    user = request.user
    bucket = Bucket.objects.get(user=user)
    bucket.items = "[]"
    bucket.save()
    data = {
        'is_cleaned': "success"
    }
    return JsonResponse(data)


@login_required
def make_order(request):
    user = request.user
    bucket = Bucket.objects.get(user=user)
    if bucket.items == "[]":
        data = {
            'is_ordered': "empty_bucket"
        }
        return JsonResponse(data)
    items_dict = dict()
    for item_id in json.loads(bucket.items):
        item = Item.objects.get(id=item_id)
        if item in items_dict:
            items_dict[item] += 1
        else:
            items_dict[item] = 1

    price = 0
    for k, v in items_dict.items():
        price += k.price * v
        if k.number < v:
            data = {
                'is_ordered': "not_enough_items"
            }
            return JsonResponse(data)

    new_order = Order.objects.create()
    new_order.user = user
    new_order.items = bucket.items
    new_order.price = price
    new_order.save()
    bucket.items = "[]"
    bucket.save()
    for k, v in items_dict.items():
        k.number -= v
        k.save()
    data = {
        'is_ordered': "success"
    }
    return JsonResponse(data)


@login_required
def store_main(request):
    if request.method == "GET":
        items_list = Item.objects.all().order_by("price").filter(number__gt=0,
                                                                 title__contains=request.GET.get('title', ""))
    else:
        items_list = Item.objects.all().order_by("price").filter(number__gt=0)
    paginator = Paginator(items_list, 6)  # Show 25 contacts per page
    user = request.user
    user_bckt = Bucket.objects.get(user=user)
    bucket_size = len(json.loads(user_bckt.items))
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
        "user_bucket_size": bucket_size,
        "page_request_var": page_request_var,
    }
    return render(request, "store_list.html", context)


def goto_login(request):
    context = {}
    return render(request, "login.html", context)
