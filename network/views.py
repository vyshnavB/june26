from django.contrib.auth import authenticate, login,  logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from itertools import chain
from django.contrib import messages
import itertools
from .models import *
from django.db.models import Q
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q, Count
import datetime
from django.db.models import F
from django.contrib.auth.hashers import make_password
from django.db.models import Avg

import datetime

from datetime import datetime, timedelta
import requests


from decimal import Decimal




@csrf_exempt
@login_required(login_url='login')
def intrest_page(request):
    intr=intrest.objects.all()

    followig_user=request.user.id
    a="#Article"
    b="#Book"
    c="#Case Study"
    d="#Education"
    e="#Interviews"
    f="#Market Research"
    g="#Observation"
    h="#Poem"
    i="#Survey"
    j="#Work & Business"
    
 
    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=a).first():
         button_texta = 'Unfollow'
    else:  
        button_texta = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=b).first():
         button_textb = 'Unfollow'
    else:  
        button_textb = 'Follow'	  
    
     
    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=c).first():
         button_textc = 'Unfollow'
    else:  
        button_textc = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=d).first():
         button_textd = 'Unfollow'
    else:  
         button_textd = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=e).first():
         button_texte = 'Unfollow'
    else:  
        button_texte = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=f).first():
         button_textf = 'Unfollow'
    else:  
        button_textf = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=g).first():
         button_textg = 'Unfollow'
    else:  
        button_textg = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=h).first():
         button_texth = 'Unfollow'
    else:  
        button_texth = 'Follow'	      


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=i).first():
         button_texti = 'Unfollow'
    else:  
        button_texti = 'Follow'	 


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=j).first():
         button_textj = 'Unfollow'
    else:  
        button_textj = 'Follow'	                   



    return render(request,"intrest.html",{"intr":intr,"button_texta":button_texta,"button_textb":button_textb,"button_textc":button_textc,
                                          "button_textd":button_textd,"button_texte":button_texte,"button_textf":button_textf,
                                          "button_textg":button_textg,"button_texth":button_texth,"button_texti":button_texti,"button_textj":button_textj})



@csrf_exempt
def intrest_create(request):
    if request.method == 'POST':
        intr = request.POST['intr']
        int=intrest(
            intr=intr
        )
        int.save()
        return redirect("index")
         
        
       

@csrf_exempt
@login_required(login_url='login')
def index(request):
    
    
    if request.method == 'POST':
        selected_value = request.POST.get('dropdown')

        
        
        if selected_value == "best" :
            
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            usr=User.objects.all()
            choose=intrest_followers.objects.all()
            intr_following_list = []
            feed = []

            # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        
            us=request.user

            
            user_following = intrest_followers.objects.filter(following_user=request.user)


            for users in user_following:
                intr_following_list.append(users.topic)

                    

           


            posts = Post.objects.filter(intr_id__in=intr_following_list,date_created__gte=last_24_hours).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')
        

        
            frd=friend.objects.all()
            pending=friend_request.objects.all()


            
            suggestions = []
            if request.user.is_authenticated:
                followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


            intrests = []
            if request.user.is_authenticated:
                followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
            
            intr = intrest.objects.all()
            followig_user = request.user.id


            
            interest_list = []
            for interest in intr:
                is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                interest_data = {
                    'id' : interest.id,
                    'name': interest.intrest_name,
                    'is_following': is_following
                }
                interest_list.append(interest_data)






            context = {
                'index_posts': 1,
                "posts": posts,
                'pending':pending,
                "suggestions": suggestions,      
                "page": "all_posts",
                "intrests":intrests,
                'profile': False,
                "frd":frd,
                "usr":usr.count(),  
                "intr":intr,"choose":choose,
                "interest_list":interest_list
            
            }    
        

            return render(request, "network/index.html",context)
        
        if selected_value == "new" : 
            usr=User.objects.all()
            choose=intrest_followers.objects.all()
            intr_following_list = []
            feed = []

            # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        
            us=request.user

            user_following = intrest_followers.objects.filter(following_user=request.user)


            for users in user_following:
                intr_following_list.append(users.topic)

                    

           


            posts = Post.objects.filter(intr_id__in=intr_following_list).order_by('-date_created')
        

        
            frd=friend.objects.all()

            pending=friend_request.objects.all()


            
            suggestions = []
            if request.user.is_authenticated:
                followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


            intrests = []
            if request.user.is_authenticated:
                followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
            
            intr = intrest.objects.all()
            followig_user = request.user.id


            
            interest_list = []
            for interest in intr:
                is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                interest_data = {
                    'id' : interest.id,
                    'name': interest.intrest_name,
                    'is_following': is_following
                }
                interest_list.append(interest_data)






            context = {
                'index_posts': 1,
                "posts": posts,
                'pending':pending,
                "suggestions": suggestions,      
                "page": "all_posts",
                "intrests":intrests,
                'profile': False,
                "frd":frd,
                "usr":usr.count(),  
                "intr":intr,"choose":choose,
                "interest_list":interest_list
            
            }    
        

            return render(request, "network/index.html",context) 
        
        if selected_value == "top" :
            
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            usr=User.objects.all()
            choose=intrest_followers.objects.all()
            intr_following_list = []
            feed = []

            # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        
            us=request.user

            user_following = intrest_followers.objects.filter(following_user=request.user)


            for users in user_following:
                intr_following_list.append(users.topic)

                    

           


           
            posts = Post.objects.filter(intr_id__in=intr_following_list).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')
        

        
            frd=friend.objects.all()
            pending=friend_request.objects.all()


            
            suggestions = []
            if request.user.is_authenticated:
                followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


            intrests = []
            if request.user.is_authenticated:
                followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
            
            intr = intrest.objects.all()
            followig_user = request.user.id


            
            interest_list = []
            for interest in intr:
                is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                interest_data = {
                    'id' : interest.id,
                    'name': interest.intrest_name,
                    'is_following': is_following
                }
                interest_list.append(interest_data)






            context = {
                'index_posts': 1,
                "posts": posts,
                'pending':pending,
                "suggestions": suggestions,      
                "page": "all_posts",
                "intrests":intrests,
                'profile': False,
                "frd":frd,
                "usr":usr.count(),  
                "intr":intr,"choose":choose,
                "interest_list":interest_list
            
            }    
        

            return render(request, "network/index.html",context)
        

    
    one_week_ago = datetime.now() - timedelta(weeks=1)
    usr=User.objects.all()
    choose=intrest_followers.objects.all()
    intr_following_list = []
    feed = []

    # last_24_hours = timezone.now() - timezone.timedelta(hours=24)

    us=request.user

    user_following = intrest_followers.objects.filter(following_user=request.user)


    for users in user_following:
        intr_following_list.append(users.topic)

        
    posts = Post.objects.filter(intr_id__in=intr_following_list,date_created__gte=one_week_ago).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')



    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    intr = intrest.objects.all()
    followig_user = request.user.id


    
    interest_list = []
    for interest in intr:
        is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
        interest_data = {
            'id' : interest.id,
            'name': interest.intrest_name,
            'is_following': is_following
        }
        interest_list.append(interest_data)






    context = {
        'index_posts': 1,
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
        "frd":frd,
        "usr":usr.count(),  
        "intr":intr,"choose":choose,
        "interest_list":interest_list
    
    }    


    return render(request, "network/index.html",context)




@csrf_exempt
def article_list_by_tag(request, tag):
    post = Post.objects.filter(tages_n=tag)

    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    context = {
        'posts': post,
        'tag': tag,
        "suggestions": suggestions,
        "intrests":intrests,
    }
    return render(request, 'article_list.html', context)



# class postDetailView(HitCountDetailView):
#     model = Post
#     template_name = "network/index.html"
#     slug_field = "slug"
#     count_hit = True


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Redirect staff users to admin panel
            if user.is_staff:
                return redirect('admin:index')
            else:
                return redirect('index')
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]

        user_type=request.POST["user_type"]
        if fname == None:
            fname = "none"

        lname = request.POST["lastname"]
        if lname == None:
            lname = "none"

       


        profile = request.FILES.get("profile")
   
       
        cover = request.FILES.get('cover')
        
       


       

        # Ensure password matches confirmation
        password = request.POST["password"]
        # confirmation = request.POST["confirmation"]
        # if password != confirmation:
        #     return render(request, "network/register.html", {
        #         "message": "Passwords must match."
        #     })

        # Attempt to create new user
        try: 
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.user_type= user_type
            
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "../static/propic.jpg"
            user.cover = cover           
            user.save()
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("account_details"))
    else:
        return render(request, "network/register.html")

def account_details(request):
    return render(request,"account_details.html")

def register2(request):
    if request.method == "POST":
        user = request.user  # Assuming the user is already authenticated
        user.genter = request.POST.get("genter")
        user.bio = request.POST.get("bio")
        user.category = request.POST.get("category")
        user.twitter_link = request.POST.get("twitter_link")
        user.linkedin_link = request.POST.get("linkedin_link")
        user.website_link = request.POST.get("website_link")
        user.facebook_link = request.POST.get("facebook_link")
        user.youtube_link = request.POST.get("youtube_link")
        user.education = request.POST.get("education")
        user.state = request.POST.get("state")
        user.address = request.POST.get("address")
        user.city = request.POST.get("city")
        user.mobile = request.POST.get("mobile")
        user.save()


        
        return redirect("intrest_page")

@csrf_exempt
@login_required(login_url='login')
def profile(request, username):
    user = User.objects.get(id=username)
    all_posts = Post.objects.filter(creater=user).annotate(num_wishlist=Count('postz')).order_by('-date_created')
    frd = friend.objects.filter()
    rqst=friend_request.objects.filter()
    topic_foll=intrest_followers.objects.all()
    orders=Order_Itemz.objects.all()

    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()

    dd=inv + noti

    downloads=download.objects.all()

   
        
    page_foll=pagefollow.objects.all()
    choose=intrest_followers.objects.all()
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    us = request.user
    pge = User.objects.get(id=username)

    to_us = pge
    
    join ='Join'

    if invite_request.objects.filter(from_user=us,to_user=pge):

        inv = invite_request.objects.filter(from_user=us,to_user=pge)

        for i in inv:

            if i.status == "User_Pending":

                join = 'Pending'
            elif i.status == "Joined": 
                join = 'Joined'   


    elif    invite_request.objects.filter(to_user=us,from_user=pge):
        inv = invite_request.objects.filter(to_user=us,from_user=pge)

        for i in inv:

            if i.status == "User_Pending":

                join = 'Pending'
            elif i.status == "Joined": 
                join = 'Joined'   




    
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)

    post_count = len(posts)
    
    

    to=request.user.id
    fr=username

    if friend_request.objects.filter(from_user__id=to, to_user__id=fr,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'


        

    user_followers = len(friend_request.objects.filter(to_user=username))
    user_following = len(friend_request.objects.filter(from_user=username))   
    intrests=intrest.objects.all().order_by("?")[:5]


     
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6] 



    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")

  

    car=Cart.objects.filter(product__creater=username,status="Accept")

    car_status_counts = (
        Cart.objects
        .filter(product__creater=username)
        .values('status')
        .annotate(count=Count('status'))
    )

    

    categories = ["Article", "Book", "Case Study", "Education", "Interviews", "Market Research", "Observation", "Poem", "Survey", "Work & Business"]                
    context = {
        "username": user,
        "posts": posts,
        'button_text': button_text,
        "posts_count": all_posts.count(),
        "rqst":rqst,
        "page": "profile",
        "suggestions": suggestions,      
        "intrests":intrests,
        "frd":frd,
        'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
        "post_count":post_count,
        "choose":choose,
        'user_followers': user_followers,
        'user_following': user_following,
        "topic_foll":topic_foll,
        "page_foll":page_foll,
        "dd":dd,
        "orders":orders,
        "downloads":downloads,
        "notifi_count":notifi_count,
        'join':join,
        'categories': categories,
        "car":car,
        "car_status_counts": car_status_counts,  # Add car_status_counts to context
       
        
    }
   
    return render(request,'network/profile.html',context)





@csrf_exempt
@login_required(login_url='login')
def buyprofile(request, username):
    user = User.objects.get(id=username)
    wishlist_items = wishlist.objects.filter(usr=request.user)
    book_sell = Post.objects.filter(creater=user).annotate(num_wishlist=Count('postz')).order_by('-date_created')

   


    wishlis=wishlist.objects.all()

    orders=Order_Itemz.objects.all()
    post_cnt=Post.objects.filter(creater=username).count()

    downloads=download.objects.all()


    user_following_list = []
    feed = []

    # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
   
    us=request.user

    user_following = friend_request.objects.filter(from_user__id=username)


    for users in user_following:
        user_following_list.append(users.to_user)

    for usernames in user_following_list:
        feeds = Post.objects.filter(creater=usernames)  
        
        feed.append(feeds,)

        all_posts = list(chain(*feed))

    posts = list(chain(*feed))
    frd = friend.objects.filter()
    rqst=friend_request.objects.filter()
    topic_foll=intrest_followers.objects.all()

    
        
    page_foll=pagefollow.objects.all()
    choose=intrest_followers.objects.all()
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    
   
    

    post_count = len(posts)

    


    to=request.user.id
    fr=username

    if friend_request.objects.filter(from_user__id=to, to_user__id=fr,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'

    user_followers = len(friend_request.objects.filter(to_user=username))
    user_following = len(friend_request.objects.filter(from_user=username))   
    intrests=intrest.objects.all().order_by("?")[:5]


     
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6] 
   


    car=Cart.objects.filter(user=username,status="Accept")

    

    return render(request, 'buyprofile.html', {
        "username": user,
        "posts": posts,
        'button_text': button_text,
        "rqst":rqst,
        "page": "profile",
        "suggestions": suggestions,      
        "intrests":intrests,
        "frd":frd,
        'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
        "post_count":post_count,
       "choose":choose,
        'user_followers': user_followers,
        'user_following': user_following,
        "topic_foll":topic_foll,
        "page_foll":page_foll,
        "orders":orders,
        'wishlist_items': wishlist_items,
        "post_cnt":post_cnt,
        "downloads":downloads,
        "car":car,
        
      
    })

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@csrf_exempt
def saved(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(savers=request.user).order_by('-date_created')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "network/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "saved"
        })
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt        
def intrest_create_post(request,pk):
    intr = intrest.objects.get(id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        categories=request.POST.get('categories')
        title=request.POST.get('title')

        status=request.POST.get('status')
       
        if status == None:
            status = "nsale" 
        Product_Price=request.POST.get('Product_Price')
        if Product_Price=="":
            Product_Price=None
        # offer_price=request.POST.get('offer_price')
        # if offer_price=="":
        #     offer_price=None

        offer_toggle = request.POST.get('offer_toggle')

        if offer_toggle == None :
            offer_toggle = "Normal"

        
        post = Post(
                    creater=request.user,
                    content_text=text,
                    title=title,
                    content_image=pic,
                    categories=categories,
                    intr_id=intr,
                 
                    # content_image=pic,
                    status=status,
                    Product_Price=Product_Price,
                    posts_type="intrest_post",
                    Offer_toggle = offer_toggle,
                  
                    )
        
        
        post.save()

        p=Post.objects.get(id=post.id)

        if len(request.FILES) != 0:
            p.content_image=request.FILES['picture']

        if p.Offer_toggle != "Normal" :

            p.Offer_price = request.POST['offer_price']  
            p.Offer_Start_Date = request.POST['offer_price_start']  
            p.Offer_End_Date =  request.POST['offer_price_end']  

        p.save() 
        return redirect("topicpage",pk)    
    

@csrf_exempt        
def sub_intrest_create_post(request,pk):
    lev2_id = level2.objects.get(id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        categories=request.POST.get('categories')
        title=request.POST.get('title')
     
        
        status=request.POST.get('status')
        tages_n=request.POST.get('tages_n')
        if tages_n == "":
            tages_n = "True"
        if status == None:
            status = "nsale"
        Product_Price=request.POST.get('Product_Price')
        
        if Product_Price=="":
            Product_Price=None

        post = Post(creater=request.user,lev2_id=lev2_id, content_text=text,title=title,categories=categories,tages_n=tages_n, content_image=pic,status=status,Product_Price=Product_Price,posts_type="lev_2_intrest_post",)
        post.save()
        return redirect("subtopicpage",pk)    


@csrf_exempt
def user_create_post(request,pk):
    if request.method == 'POST':


                # if len(request.FILES) != 0:
        #     post.creater = request.FILES.get('file')

        



        text = request.POST.get('text')
        
        categories=request.POST.get('categories')
        title=request.POST.get('title')

        status=request.POST.get('status')
        
        if status == None:
            status = "nsale"
        Product_Price=request.POST.get('Product_Price')
        if Product_Price=="":
            Product_Price=None
        # offer_price=request.POST.get('offer_price')
        # if offer_price=="":
        #     offer_price=None

        offer_toggle = request.POST.get('offer_toggle')

        if offer_toggle == None :
            offer_toggle = "Normal"


        
        
        post = Post(
                    creater=request.user,
                    content_text=text,
                    title=title,
                    
                    categories=categories,
                  
                    # content_image=pic,
                    status=status,
                    Product_Price=Product_Price,
                    posts_type="user_post",
                    Offer_toggle = offer_toggle,
                  
                    )
        
        
        post.save()

        p=Post.objects.get(id=post.id)

        if len(request.FILES) != 0:
            p.content_image=request.FILES['picture']

        if p.Offer_toggle != "Normal" :

            p.Offer_price = request.POST['offer_price']  
            p.Offer_Start_Date = request.POST['offer_price_start']  
            p.Offer_End_Date =  request.POST['offer_price_end']  

        p.save()    

   
        return redirect("index")
    


def normal_createpost(request,pk):
    choose=intrest_followers.objects.all()
    intu=intrest.objects.all()
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user) 
    context = {
       "choose":choose,
        'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),
       "intu" : intu
    }
    return render(request,"normal_createpost.html",context)
    


@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        try:
            post.content_text = text
            if img_chg != 'false':
                post.content_image = pic
            post.save()
            
            if(post.content_text):
                post_text = post.content_text
            else:
                post_text = False
            if(post.content_image):
                post_image = post.img_url()
            else:
                post_image = False
            
            return JsonResponse({
                "success": True,
                "text": post_text,
                "picture": post_image
            })
        except Exception as e:
    
            return JsonResponse({
                "success": False
            })
    else:
            return HttpResponse("Method must be 'POST'")

@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
          
            try:
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
          
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            try:
                post.savers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))
 
@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            try:
                post.savers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
          
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
        
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))



@csrf_exempt
def pageindex(request):
    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')

    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    if page_number == None:
        page_number = 1
    pagepost = paginator.get_page(page_number)
    followings = []
    suggestions = []  
    suggestions = []
    search = request.GET.get('search')
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")
        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:5]
    return render(request, "pageindex.html", {
        "posts": pagepost,
        "suggestions": suggestions, 
        "page": "all_posts",
        'profile': False,
        "search": search,
        'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),
    })

@csrf_exempt
def pag(request,pk):

    pag=page.objects.filter(creater=pk)
    # pge=pagefollow.objects.all()
    all_pages=User.objects.order_by("?")[:6]
    intrests=intrest.objects.all().order_by("?")[:5]

    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")
   
    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joinedd = invite_request.objects.all()

    

    to_user=request.user


    friends_list=""
    if invite_request.objects.filter(from_user=to_user,status="page_Joined"):
        friends_list = invite_request.objects.filter(from_user=to_user,status="page_Joined")

    elif invite_request.objects.filter(to_user=to_user,status="page_Joined"):
        friends_list = invite_request.objects.filter(to_user=to_user,status="page_Joined")


    # for i in noti_notifi_count:
    #     if i.to_user.id == request.user.id:
    #         if i.type == "Page_Invitions_To_User":
    #             notifi_count=notifi_count +1

    #         if i.type == "Page_Accept_User_Invitions":
    #             notifi_count=notifi_count +1

    #         if i.type == "User_Fllowing":
    #             notifi_count=notifi_count +1
                
    #         if i.type == "Page_Post_Reviwes_Replay":
    #             notifi_count=notifi_count +1 

    #         if i.type == "User_Post_Reviwes":
    #             notifi_count=notifi_count +1

    #         if i.type == "User_Post_Reviwes_Replay":
    #             notifi_count=notifi_count +1

    #         if i.type == "Intrest_Post_Reviwes":
    #             notifi_count=notifi_count +1
                
    #         if i.type == "Intrest_Post_Reviwes_Replay":
    #             notifi_count=notifi_count +1

    #         if i.type == "Intrest_level_2_Post_Reviwes":
    #             notifi_count=notifi_count +1
                
    #         if i.type == "Intrest_level_2_Post_Reviwes_Replay":
    #             notifi_count=notifi_count +1    

    #     if i.type == "Page_New_Post":
    #         for j in page_joined :

    #             if i.pages == j.pages:
    #                 notifi_count=notifi_count +1

    context={
        "pag":pag,
        # "pge":pge,
        "all_pages":all_pages,
        "intrests":intrests,
        'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),
        'page_joinedd':page_joinedd,
        'notifi_count':notifi_count,
        "friends_list":friends_list,
       }
   
    
    
    return render(request,"page.html",context) 


@csrf_exempt
def mypage(request,pk):
    
    
    pag=User.objects.all()
    return render(request,"mypage.html",{"pag":pag,})  




def page_registration(request,pk):
    rgs=User.objects.get(id=pk)
    suggestions = []
    follower=False
   
    return render(request,"page_registration.html",{"rgs":rgs,
    })

    
        

@csrf_exempt
def page_creation(request,pk):
    if request.method == 'POST':
        
        creater=request.user
        pagename = request.POST.get('pagename')
        website = request.FILES.get('website')
        username=request.POST.get('username')
        category= request.POST.get('category')
        emial=request.POST.get('emial')
        image=request.FILES.get('image')

        
        pag = page(creater=creater, pagename=pagename, website=website,emial=emial,category=category,image=image,username=username)
           
        pag.save()
        return redirect("pag",pk)
    


@login_required(login_url='login')
def pageprofile(request,pageid):
    pro=User.objects.get(id=pageid)
    posts = Post.objects.filter(creater=pageid).order_by('-date_created')
    choose=intrest_followers.objects.all()
    
    followings = []
   
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    follower=False


    to=request.user.id
    frm=pageid

    if pagefollow.objects.filter(from_user__id=to, to_page__id=frm,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow' 

    user_followers = len(pagefollow.objects.filter(to_page=pageid))

    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = []
    search = request.GET.get('search')
    

    follower_count = Follower.objects.get(user=pro).followers.all().count()
    following_count = Follower.objects.filter(followers=pro).count()        
    # suggestions = User.objects.all()
    # req=invite_request.objects.all
    
    us = request.user
    pge = User.objects.get(id=frm)

    to_us = pge
    
    join ='Join'

    if invite_request.objects.filter(to_user=us):

        inv = invite_request.objects.filter(to_user=us)

        for i in inv:

            if i.status == "Pending":

                join = 'Pending'
            elif i.status == "Joined": 
                join = 'Joined'

    elif invite_request.objects.filter(from_user=us): 
        inv = invite_request.objects.filter(from_user=us)

        for i in inv:

            if i.status == "Pending":

                join = 'Pending'
            elif i.status == "Joined": 
                join = 'Joined'              
  
        

    friends_list=[]
    if invite_request.objects.filter(to_user=to_us,status="Joined"):
        friends_list = invite_request.objects.filter(to_user=to_us,status="Joined")
        
        

    if request.user.is_authenticated:
        # followings = friend_request.objects.filter(from_user=request.user)

        if invite_request.objects.filter(to_user=to_us, status__in=["Joined","User_Pending"]):
            frnd_list = invite_request.objects.filter(to_user=to_us, status__in=["Joined","User_Pending"])

        
            join_friends=[]
           
            for i in frnd_list :

                join_friends.append(User.objects.filter(id=i.from_user.id))

            if join_friends:
                combined_queryset = join_friends[0]
                for queryset in join_friends[1:]:
                      combined_queryset |= queryset

                suggestions = User.objects.exclude(pk__in=combined_queryset).exclude(username=request.user.username).order_by("?")
            else:
               suggestions = User.objects.exclude(username=request.user.username).order_by("?")
        else:
             suggestions = User.objects.exclude(username=request.user.username).order_by("?")

            
       

        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:9]

        if request.user in Follower.objects.get(user=pro).followers.all():
            follower = True    
    page_joined=[]
    if  invite_request.objects.filter(from_user=request.user,status="Joined"):
        page_joined = invite_request.objects.filter(from_user=request.user, status="Joined").first()

    
    
    categories = ["Article", "Book", "Case Study", "Education", "Interviews", "Market Research", "Observation", "Poem", "Survey", "Work & Business"]                
   
    
    context = {
        "categories" :categories,
        "pro":pro,
        "posts":posts,
        "pag":pag,
        "posts_count": posts.count(),
        "suggestions":suggestions,
        "search" : search,
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count,
         "button_text":button_text,
        "user_followers":user_followers,
         'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
        "choose":choose,
        'join':join,
        'fncount':len(friends_list),
        'friends_list':friends_list,
        'page_joined':page_joined,
    }


    return render(request,"pageprofile.html",context)




def pageprofile2(request,pageid):
    pro=page.objects.get(id=pageid)
    posts = Post.objects.filter(page_id=pageid).order_by('-date_created')
    choose=intrest_followers.objects.all()
    followings = []
   
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    follower=False


    to=request.user.id
    frm=pageid

    if pagefollow.objects.filter(from_user_id=to, to_page_id=frm,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'

    user_followers = len(pagefollow.objects.filter(to_page=pageid))

    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = []
    search = request.GET.get('search')


    if request.user.is_authenticated:
        joined_users = invite_request.objects.filter(pages=pro, status="page_Joined").values_list("to_user", flat=True)
        pending_users = invite_request.objects.filter(pages=pro, status="Pending").values_list("to_user", flat=True)
        suggestions = User.objects.exclude(username=request.user.username).exclude(pk__in=joined_users).exclude(pk__in=pending_users).order_by("?")





    follower_count = Follower.objects.get(user=pro.creater).followers.all().count()
    following_count = Follower.objects.filter(followers=pro.creater).count()        
    # suggestions = User.objects.all()
    # req=invite_request.objects.all
    
    us = request.user
    pge = page.objects.get(id=frm)

  


    
    
    
    join ='Join'

    if invite_request.objects.filter(from_user=us,pages=pge):

        inv = invite_request.objects.filter(from_user=us,pages=pge)

        for i in inv:

            if i.status == "Pending":

                join = 'Pending'
            elif i.status == "page_Joined": 
                join = 'page_Joined'
                
    elif   invite_request.objects.filter(to_user=us,pages=pge):
                inv = invite_request.objects.filter(to_user=us,pages=pge)

                for i in inv:

                    if i.status == "Pending":

                        join = 'Pending'
                    elif i.status == "page_Joined": 
                        join = 'page_Joined'

    
                   

  


        
    friends_list=""
    if invite_request.objects.filter(pages=pge,status="page_Joined"):
        friends_list = invite_request.objects.filter(pages=pge,status="page_Joined")

    
    context = {
        "pro":pro,
        "posts":posts,
        "pag":pag,
        "posts_count": posts.count(),
        "suggestions":suggestions,
        "search" : search,
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count,
         "button_text":button_text,
        "user_followers":user_followers,
         'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
        "choose":choose,
        'join':join,
        'fncount':len(friends_list)
        
    }


    return render(request,"pageprofile2.html",context)



def buy_pageprofile(request,pageid):
    pro=User.objects.get(id=pageid)
    posts = Post.objects.filter(creater=pageid).order_by('-date_created')
    choose=intrest_followers.objects.all()
    
    followings = []
   
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    follower=False


    to=request.user.id
    frm=pageid

    if pagefollow.objects.filter(from_user__id=to, to_page__id=frm,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow' 

    user_followers = len(pagefollow.objects.filter(to_page=pageid))

    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = []
    search = request.GET.get('search')
    

    follower_count = Follower.objects.get(user=pro).followers.all().count()
    following_count = Follower.objects.filter(followers=pro).count()        
    # suggestions = User.objects.all()
    # req=invite_request.objects.all
    
    us = request.user
    pge = User.objects.get(id=frm)

    to_us = pge
    
    join ='Join'

    if invite_request.objects.filter(from_user=us,to_user=to_us):

        inv = invite_request.objects.filter(from_user=us,to_user=to_us)

        for i in inv:

            if i.status == "Pending":

                join = 'Pending'
            elif i.status == "Joined": 
                join = 'Joined'   
  
        

    friends_list=[]
    if invite_request.objects.filter(to_user=to_us,status="Joined"):
        friends_list = invite_request.objects.filter(to_user=to_us,status="Joined")
        
        

    if request.user.is_authenticated:
        # followings = friend_request.objects.filter(from_user=request.user)

        if invite_request.objects.filter(to_user=to_us, status__in=["Joined","User_Pending"]):
            frnd_list = invite_request.objects.filter(to_user=to_us, status__in=["Joined","User_Pending"])


            join_friends=[]
           
            for i in frnd_list :

                join_friends.append(User.objects.filter(id=i.from_user.id))

            for i in frnd_list:

                join_friends.append(User.objects.filter(id=i.from_user.id))

            if join_friends:
                combined_queryset = join_friends[0]
                for queryset in join_friends[1:]:
                      combined_queryset |= queryset

                suggestions = User.objects.exclude(pk__in=combined_queryset).exclude(username=request.user.username).order_by("?")
            else:
               suggestions = User.objects.exclude(username=request.user.username).order_by("?")
        else:
             suggestions = User.objects.exclude(username=request.user.username).order_by("?")

            
       

        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:9]

        if request.user in Follower.objects.get(user=pro).followers.all():
            follower = True    
    page_joined=[]
    if  invite_request.objects.filter(from_user=request.user,status="Joined"):
        page_joined = invite_request.objects.get(from_user=request.user,status="Joined")

    
    
    context = {
        "pro":pro,
        "posts":posts,
        "pag":pag,
        "posts_count": posts.count(),
        "suggestions":suggestions,
        "search" : search,
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count,
         "button_text":button_text,
        "user_followers":user_followers,
         'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
        "choose":choose,
        'join':join,
        'fncount':len(friends_list),
        'friends_list':friends_list,
        'page_joined':page_joined,
    }


    return render(request,"buy_pageprofile.html",context)

def pagepost(request,pk):
    pg = page.objects.get(id=pk)
    return render(request,"pagepost.html",{"pg":pg})   

@login_required(login_url='login')
@csrf_exempt
def create_pagepost(request,pk):
    if request.method == 'POST':


        text = request.POST.get('text')
        
        categories=request.POST.get('categories')
        title=request.POST.get('title')

        status=request.POST.get('status')
        
        if status == None:
            status = "nsale"
        Product_Price=request.POST.get('Product_Price')
        if Product_Price=="":
            Product_Price=None
     

        offer_toggle = request.POST.get('offer_toggle')

        if offer_toggle == None :
            offer_toggle = "Normal"

        
        
        post = Post(
                    creater=request.user,
                    content_text=text,
                    title=title,
                    
                    categories=categories,
                  
                    #content_image=pic,
                    status=status,
                    Product_Price=Product_Price,
                    posts_type="page_post",
                    Offer_toggle = offer_toggle,
                  
                    )
        
        
        post.save()

        p=Post.objects.get(id=post.id)

        if len(request.FILES) != 0:
            p.content_image=request.FILES['picture']

        if p.Offer_toggle != "Normal" :

            p.Offer_price = request.POST['offer_price']  
            p.Offer_Start_Date = request.POST['offer_price_start']  
            p.Offer_End_Date =  request.POST['offer_price_end']  

        p.save()    

   
        return redirect("index")




        
@csrf_exempt
def cart(request):
    return render(request,"cart.html")


@csrf_exempt
def checkout(request):
    return render(request,"checkout.html")


@csrf_exempt
@login_required(login_url='signin')
def category(request,id):
    category = Category.objects.get(id=id)
    product = Product.objects.filter(Category_Name=category)

    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
 
    category = Category.objects.all()
    context = {
        'pro'  : product, 
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'category' : category,       
        
    }
    return render(request,'shop-full.html',context)


@csrf_exempt
@login_required(login_url='signin')
def show_all(request):
   
    product = Product.objects.all()
    category = Category.objects.all()
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
 

    context = {
        'pro'  : product, 
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'category' : category,
               
    }
    return render(request,'shop-full.html',context)


def get_days_left(start_date, end_date):
    """
    Returns the number of days left between start_date and end_date
    """
    days_left = (end_date - datetime.now().date()).days
    if days_left < 0:
        return "Sale has ended"
    elif days_left == 0:
        return "Sale ends today"
    elif days_left == 1:
        return "Sale ends in 1 day"
    else:
        return f"Sale ends in {days_left} days"


@login_required(login_url='login')
def product_detail(request,id,userid):
    product=Post.objects.filter(id=id)
    rew=review.objects.filter(post__id=id)
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
 

    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()


    dd=inv + noti

    to=request.user.id


    rew_1=review.objects.filter(post__id=id,rating=1).count()
    rew_2=review.objects.filter(post__id=id,rating=2).count()
    rew_3=review.objects.filter(post__id=id,rating=3).count()
    rew_4=review.objects.filter(post__id=id,rating=4).count()
    rew_5=review.objects.filter(post__id=id,rating=5).count()


   
    avg = 5*rew_5 + 4*rew_4 + 3*rew_3 + 2*rew_2 + 1*rew_1

    average = rew_5 + rew_4 + rew_3 + rew_2 + rew_1


    avav = avav = avg / average if average != 0 else 0


    post = Post.objects.get(id=id)
    post.average_rating = avav
    post.save()


    # pos = Post.objects.get(id=id)
    # view = request.user

    # post_view = post_viewers.objects.get(post=pos, viewer=view)
    # post_view.save()




    post_view=Post.objects.get(id=id)
    if post_view.views_count is None:
         post_view.views_count = 1
    else:
         post_view.views_count += 1
    post_view.save()


    
    


    if friend_request.objects.filter(from_user_id=to,to_user_id=userid,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'

    product1=Post.objects.get(id=id)

    Offer_toggle = product1.Offer_toggle
    offer_price = ""
    days_left=""
    if Offer_toggle != "Normal":

        start_d = product1.Offer_Start_Date

        end_d = product1.Offer_End_Date

        today = datetime.now().date()

       
        start_date = start_d 
        end_date = end_d 
        
        if today >= start_date and today <= end_date:

            offer_price = product1.Offer_price
            days_left = get_days_left(start_date, end_date)



    # viwers 

    

    if post.creater != request.user:

        viewer, created = PostViewer.objects.get_or_create(post=post, user=request.user)      
         
    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")

    for i in noti_notifi_count:
        if i.from_user.id == request.user.id:
            if i.type == "Page_Invitions_To_User":
                notifi_count=notifi_count +1

            if i.type == "Page_Accept_User_Invitions":
                notifi_count=notifi_count +1

            if i.type == "User_Fllowing":
                notifi_count=notifi_count +1
                
            if i.type == "Page_Post_Reviwes_Replay":
                notifi_count=notifi_count +1 

            if i.type == "User_Post_Reviwes":
                notifi_count=notifi_count +1

            if i.type == "User_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_level_2_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_level_2_Post_Reviwes_Replay":
                notifi_count=notifi_count +1    

        if i.type == "Page_New_Post":
            for j in page_joined :

                if i.pages == j.pages:
                    notifi_count=notifi_count +1

    context = {
        'pro'  : product, 
        'crt' : crt,
       
        'crt_count' : crt_count,
        
        "rew":rew,
        "rew_1":rew_1,
        "rew_2":rew_2,
        "rew_3":rew_3,
        "rew_4":rew_4,
        "rew_5":rew_5,
        "avav":avav,

        "rew_count":rew.count(),
        "button_text":button_text,
        'offer_price':offer_price,
        'days_left':days_left,
        "dd":dd,
        "notifi_count":notifi_count,
        
        

    }

    return render(request,'product-detail.html',context)


@csrf_exempt
def reviews(request,userid,id):
    post=Post.objects.get(id=userid)
    reviewer=request.user
    reviewz= request.POST.get('reviewz')
    mail = request.POST.get('mail')
    rating =request.POST.get('rating')
    rev = review (post=post,reviewer=reviewer,reviewz=reviewz,mail=mail,rating=rating)
    rev.save()

    revw = review.objects.get(id=rev.id)

    

    if post.posts_type == "page_post":
        notification = Notifications()
        notification.from_user = request.user
        notification.to_user = post.creater
        notification.pages = post.page_id
        notification.post = post
        notification.review = revw


        notification.type = "Page_Post_Reviwes"

        notification.save()

    elif post.posts_type == "user_post":
        notification = Notifications()
        notification.from_user = post.creater
        notification.to_user = request.user
        notification.post = post
        notification.review = revw
        notification.type = "User_Post_Reviwes"
        notification.save()

    elif post.posts_type == "intrest_post":
        notification = Notifications()
        notification.from_user = post.creater
        notification.to_user = request.user
        notification.post = post
        notification.review = revw
        notification.type = "Intrest_Post_Reviwes"
        notification.save()  


    elif post.posts_type == "lev_2_intrest_post":
        notification = Notifications()
        notification.from_user = post.creater
        notification.to_user = request.user
        notification.post = post
        notification.review = revw
        notification.type = "Intrest_level_2_Post_Reviwes"
        notification.save()     

    

    return redirect("product_detail",userid,id)


@csrf_exempt
def add_cart(request,id,pk):
    if request.method=='POST':
        fr_user=request.user
        user=User.objects.get(id=pk)
        product=Post.objects.get(id=id)
       
        
        ct=Cart(user=fr_user,to_user=user,product=product,product_qty="1",status="Pending")
        ct.save()
        return redirect('cart')

@csrf_exempt
@login_required(login_url='signin')
def cart(request):
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()
   
    sub_total=0 
    grand_total = 0
    shipping =50
    
    grand_total =  sub_total + shipping

    context = {
        'crt' : crt,
        
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        
        
    }


    return render(request,'cart.html',context)    


def zip(request):
    if request.method=='POST':
        zipcode=request.POST['zip']
        if Zip.objects.filter(zip_code=zipcode).exists():
            messages.info(request, 'Delery avilable')
            return redirect('cart') 
        else:
            messages.info(request, 'Delery is not avilable')
            return redirect('cart')


def remove_cart(request,id):
    crt=Cart.objects.get(id=id)
    crt.delete()
    return redirect('cart')

def remove_cart_all(request):
    crt=Cart.objects.filter(user=request.user)
    crt.delete()
    return redirect('cart')
    
@csrf_exempt
@login_required(login_url='signin')
def checkout(request):
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    ship = Orderz.objects.filter(user=request.user)

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
 
    
    shipadd = ""
    for i in ship:
        shipadd = str(i.Full_name)+" , " + str(i.House)+" , "  + str(i.Area)+" , "+ str(i.Landmark)+" , " + str(i.Town)+" , " + str(i.State)+" , " + str(i.Zip)+" , " + str(i.Phone)



    context = {
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'ship'    :   ship,
        'shipadd'  : shipadd,
    }

    return render(request,'checkout.html',context)   

@csrf_exempt
@login_required(login_url='signin')


def order_item(request, product_id,uid):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)
        if Orderz.objects.filter(user=request.user).exists():
            ship1 =Orderz.objects.get(user=request.user)
            ship1.user=user
            ship1.Full_name = request.POST['fullname']
            ship1.Phone = request.POST['phone']
            ship1.House = request.POST['house']
            ship1.Area = request.POST['area']
            ship1.Landmark = request.POST['landmark']
            ship1.Town = request.POST['town']
            ship1.State = request.POST['state']
            ship1.Zip = request.POST['zip']
            ship1.save()
            return redirect('order_manage',product_id,uid)
        else:
            ship=Orderz()
            ship.user=user

            ship.Area = request.POST['area']
            ship.Landmark = request.POST['landmark']
            ship.Town = request.POST['town']
            ship.State = request.POST['state']
            ship.Zip = request.POST['zip']
            ship.save()
       
        
       
        return redirect('order_manage',product_id,uid)
    
    # If the request method is not POST, render the order form template
    return render(request, 'order_item.html', {'product': product})





@csrf_exempt
@login_required(login_url='signin')
def Orderss(request,pk):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)
        if Orderz.objects.filter(user=request.user).exists():
            ship1 =Orderz.objects.get(user=request.user)
            ship1.user=user
            ship1.Full_name = request.POST['fullname']
            ship1.Phone = request.POST['phone']
            ship1.House = request.POST['house']
            ship1.Area = request.POST['area']
            ship1.Landmark = request.POST['landmark']
            ship1.Town = request.POST['town']
            ship1.State = request.POST['state']
            ship1.Zip = request.POST['zip']
            ship1.save()
            return redirect('order_manage',pk)
        else:
            ship=Orderz()
            ship.user=user
            ship.Full_name = request.POST['fullname']
            ship.Phone = request.POST['phone']
            ship.House = request.POST['house']
            ship.Area = request.POST['area']
            ship.Landmark = request.POST['landmark']
            ship.Town = request.POST['town']
            ship.State = request.POST['state']
            ship.Zip = request.POST['zip']
            ship.save()
            return redirect('order_manage',pk)        
        

@csrf_exempt
def place_order(request,id):
   
        return redirect ('my_order')
               
    
@csrf_exempt
@login_required(login_url='signin')
def dashboard(request):
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    ship = Orderz.objects.filter(user=request.user)

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
 
    orderitem = Order_Itemz.objects.filter(user=request.user)
    order_count = orderitem.count()
    shipadd = ""
    for i in ship:
        shipadd = str(i.Full_name)+" , " + str(i.House)+" , "  + str(i.Area)+" , "+ str(i.Landmark)+" , " + str(i.Town)+" , " + str(i.State)+" , " + str(i.Zip)+" , " + str(i.Phone)



    context = {
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'ship'    :   ship,
        'orderitem'  : orderitem,
        'shipadd'  : shipadd,
        'order_count' : order_count,
    }
    return render(request,'dashboard.html',context)

@csrf_exempt
@login_required(login_url='signin')
def dashboard_profile(request): 
    phone=Member.objects.get(user=request.user) 
    ph=phone.phone
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
    orderitem = Order_Itemz.objects.filter(user=request.user)
    order_count = orderitem.count()
    category = Category.objects.all()
    context = {
        'pro'  : product, 
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'category' : category,
        'phone':ph,
        'order_count':order_count,
    }

    return render(request,'dash-my-profile.html',context)


@csrf_exempt
@login_required(login_url='signin')
def dash_edit_profile(request):
    
    phone=Member.objects.get(user=request.user) 
    ph=phone.phone
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
    orderitem = Order_Itemz.objects.filter(user=request.user)
    order_count = orderitem.count()
    category = Category.objects.all()
    context = {
        'pro'  : product, 
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'category' : category,
        'phone':ph,
        'order_count':order_count,
    }


    return render(request,'dash-edit-profile.html',context)


@csrf_exempt
@login_required(login_url='signin')
def edit(request):
    if request.method=='POST':
        user=User.objects.get(id=request.user.id)
        user.first_name=request.POST['fname']
        user.last_name=request.POST['lname']
        user.email=request.POST['email']
        pho=Member.objects.get(user=request.user)
        pho.phone=request.POST['phone']
        user.save()
        pho.save()
        return redirect('dash_edit_profile')     

@login_required(login_url='signin')
def dash_address_book(request):
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    phone=Member.objects.get(user=request.user) 
    ph=phone.phone
    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 

    ship = Orderz.objects.filter(user=request.user)
    address = ""
    reg = ""
    for i in ship:
        address = str(i.House)+" , "  + str(i.Area)+" , "+ str(i.Landmark)+" , " + str(i.Town)+" , " + str(i.State) +" , " + str(i.Zip)
        reg = str(i.Town)+" , " + str(i.State) 

    grand_total =  sub_total + shipping
    orderitem = Order_Itemz.objects.filter(user=request.user)
    order_count = orderitem.count()
    category = Category.objects.all()
    context = {
        'pro'  : product, 
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'category' : category,
        'address':address,
        'reg':reg,
        'ph' :ph,

       
        'order_count':order_count,
    }
    return render(request,'dash-address-book.html',context)

@csrf_exempt

def track_order(request):

    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
    orderitem = Order_Itemz.objects.filter(user=request.user)
    order_count = orderitem.count()


    context = {
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'order_count' :order_count,
        
    }
    return render(request,'dash-track-order.html',context)


@csrf_exempt
def my_order(request,pk):


    return render('my_order.html') 



@csrf_exempt
def order_manage(request,id,uid):  
    crt=Cart.objects.filter()
    pos=Post.objects.get(id=id)
    crt_count = crt.count()
    ship=Orderz.objects.filter(user=request.user)
    ord=Order_Itemz.objects.all()



    sub_total=0 
    grand_total = 0
    shipping =50
    for i in crt:
      sub_total =  sub_total + i.product_qty * i.product.Product_Price 


    grand_total =  sub_total + shipping
 
    shipadd = ""
    for i in ship:
        shipadd = str(i.user.username)+" , " + str(i.House)+" , "  + str(i.Area)+" , "+ str(i.Landmark)+" , " + str(i.Town)+" , " + str(i.State)+" , " + str(i.Zip)+" , " + str(i.Phone)



    context = {
        'crt' : crt,
        'crt_count' : crt_count,
        'sub_total' : sub_total,
        'shipping'  : shipping,
        'grand_total' : grand_total,
        'ship'    :   ship,
       "shipadd":shipadd,
        "pos":pos,
        "ord":ord
        
    }
    return render(request,'dash-manage-order.html',context) 


@csrf_exempt
@login_required(login_url='signin')
def admin_dash(request):
    if not request.user.is_staff:
        return redirect('signin')
    return render(request,'administrator/index.html') 

@csrf_exempt
@login_required(login_url='signin')
def dash_category(request):
    category=Category.objects.all()
    context={
        'category':category,

    }
    return render(request,'administrator/category.html',context)

@csrf_exempt
@login_required(login_url='signin')
def add_category(request):
    if request.method=='POST':
        cat=Category()
        cat.Category_Name = request.POST['category']
        cat.save()
        return redirect('dash_category')

@csrf_exempt
@login_required(login_url='signin')
def del_category(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('dash_category')



@csrf_exempt
@login_required(login_url='signin')
def dash_product(request):
    cat=Category.objects.all()
    context ={
        'cat' :cat,

         }

    return render(request,'administrator/products.html',context)




@csrf_exempt
def edit_product(request,id):
    
    cat=Category.objects.all()
    product=Product.objects.get(id=id)
    context ={
        'cat' :cat,
        'product' :product,
         }
        
    return render(request,'administrator/edit_product.html',context)


@csrf_exempt
def edit_pro(request,id):

    if request.method=='POST':
        c = request.POST['cat']
        cat=Category.objects.get(id=c)
        pro=Product.objects.get(id=id)
       
        pro.Category_Name = cat
        
        pro.Product_Name = request.POST['pname']
        pro.Product_Description = request.POST['desp']
        pro.Product_Price = request.POST['price']
        pro.Product_Delprice = request.POST['delprice']
        if len(request.FILES) != 0:
            if len(pro.Product_Image) > 0  :
                os.remove(pro.Product_Image.path)
            pro.Product_Image = request.FILES['file']
            
        pro.save()
        return redirect('show_product')



@login_required(login_url='signin')
def show_product(request):

    product=Product.objects.all()
    context= {
        'product' : product,

    }

    return render(request,'administrator/show_product.html',context)

@login_required(login_url='signin')
def show_order(request):
    order = Orderz.objects.all()
    context = {
        'order' :order,
    }
    return render(request,'administrator/show_order.html',context)

@login_required(login_url='signin')
def status(request,id):
    if request.method=='POST':
        order = Orderz.objects.get(id=id)
        
        order.status = request.POST['st']
        order.save()
        return redirect('show_order')
          



@login_required(login_url='signin')
def show_order_product(request,id):
    items=Order_Itemz.objects.filter(order=id)
    order =Orderz.objects.get(id=id)
    context={
       'items' : items,
       'order' :order,
    }
    return render(request,'administrator/show_order_product.html',context)   



# def show_user(request):

#     users = User.objects.all()
#     return render(request,'administrator/show_users.html',{'users':users})   


def user_carts(request,id):
    us = User.objects.get(id=id)
    
    carts=Cart.objects.filter(user=us)
    context = {
        'carts' : carts,
    }
    

    return render(request,'administrator/view_carts.html',context)  


# def logout(request):
#     request.session["uid"] = ""
#     auth.logout(request)
#     return redirect('index')


# def add_product(request):
#      if request.method == 'POST':
#         Product_Name = request.POST.get('Product_Name')
#         Product_Image = request.FILES.get('Product_Image')
#         Product_Price= request.POST.get('Product_Price')
#         Product_Description=request.POST.get('Product_Description')
#         date_created=request.POST.get('date_created')
#         try:
#             sel = Product.objects.create(creater=request.user, Product_Name=Product_Name, Product_Image=Product_Image,Product_Price=Product_Price,Product_Description=Product_Description,
#             date_created=date_created)
#             return HttpResponseRedirect(reverse('index'))
#         except Exception as e:
#             return HttpResponse(e)
#      else:
#         return HttpResponse("Method must be 'POST'")


# def dash(request):
#     return render(request,"")    


@csrf_exempt
def edit_profile(request,pk):
    profile=User.objects.get(id=pk)
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    return render(request,"edit_profile.html",{"profile":profile, 'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  })




@csrf_exempt
def edit_pr(request,pk):
    if request.method=='POST':
        profile=User.objects.get(id=pk)


        profile.first_name=request.POST['first_name']
        profile.last_name=request.POST['last_name']
        profile.username=request.POST['username']
        if request.POST.get('password'):
            # Hash the new password using Django's password hasher
            hashed_password = make_password(request.POST['password'])
            profile.password = hashed_password
        profile.email=request.POST['email']
        
        profile.genter=request.POST['genter']
        profile.category=request.POST['category']
        profile.website_link=request.POST['website_link']
        profile.linkedin_link=request.POST['linkedin_link']
        profile.twitter_link=request.POST['twitter_link']
        profile.facebook_link=request.POST['facebook_link']
        profile.education=request.POST['education']
        profile.you_link=request.POST['you_link']
        profile.state=request.POST['state']
       
        profile.city=request.POST['city']
        profile.mobile=request.POST['mobile']
        profile.bio=request.POST['bio']
        # Update the profile picture if a new file is uploaded
        if 'profile' in request.FILES:
            profile.profile_pic = request.FILES['profile']

        # Update the cover image if a new file is uploaded
        if 'cover' in request.FILES:
            profile.cover = request.FILES['cover']

        profile.save()
        return redirect('profile', pk)

    return render(request, 'edit_profile.html', {'profile': profile})

# def edit_profilr_pic(request,pk):
#     if request.method=='POST':
#         profile=User.objects.get(id=pk)

        



#         profile.save()
#         return redirect('profile',pk)


@csrf_exempt
def edit_page(request,pk):
    profile=User.objects.get(id=pk)
    return render(request,"edit_page.html",{"profile":profile})      


@csrf_exempt
def edit_pages(request,pk):
    if request.method=='POST':
        profile=User.objects.get(id=pk)
        profile.pagename=request.POST['pagename']
        profile.category=request.POST['category']
        profile.emial=request.POST['emial']
        profile.cover=request.FILES.get("cover")
        profile.image=request.FILES.get("image")
        profile.website_link=request.POST['website_link']
        profile.linkedin_link=request.POST['linkedin_link']
        profile.twitter_link=request.POST['twitter_link']
        profile.facebook_link=request.POST['facebook_link']
        profile.education=request.POST['education']
        profile.you_link=request.POST['you_link']
        profile.state=request.POST['state']
       
        profile.city=request.POST['city']
        profile.mobile=request.POST['mobile']
        profile.save()
        return redirect('pageprofile',pk)     

@csrf_exempt
def search(request):
    template = 'search.html'
    query = request.GET.get('q')

    # Search for pages
    pages = page.objects.filter(Q(pagename__icontains=query))
    page_count = pages.count()

    # Search for interests
    interests = intrest.objects.filter(Q(intrest_name__icontains=query))
    interest_count = interests.count()

    # Search for users
    users = User.objects.filter(Q(username__icontains=query))
    user_count = users.count()

    # Search for posts
    posts = Post.objects.filter(Q(creater__username__icontains=query))
    post_count = posts.count()

    # Combine search results and remove duplicates
    results = list(chain(users, pages, interests, posts))
    results = list(set(results))

    # Display a message if no results were found
    if not results:
        message = "No results found for '{}'.".format(query)
    else:
        message = "Showing results for '{}'.".format(query)

    # Hide username field if no matching users found
    hide_username = user_count == 0

    context = {
        'query': query,
        'users': users,
        'user_count': user_count,
        'posts': posts,
        'post_count': post_count,
        'pages': pages,
        'page_count': page_count,
        'interests': interests,
        'interest_count': interest_count,
        'message': message,
        'results': results,
        'hide_username': hide_username,
    }
    return render(request, template, context)




@csrf_exempt
def intrest_follow(request,pk):
    followig_user=request.user 
    topic=intrest.objects.get(id=pk)
    intr_follow=intrest_followers(following_user=followig_user,topic=topic)
    intr_follow.save()
    return redirect("intrest_page")


@csrf_exempt
def intrest_unfollow(request,pk):
    followig_user=request.user
    topic=pk
    s=intrest_followers.objects.filter(following_user=followig_user,topic=topic)
    s.delete()
    return redirect("intrest_page")

@csrf_exempt
def filter_intrest_follow(request,pk):
    followig_user=request.user
    topic=intrest.objects.get(id=pk)
    intr_follow=intrest_followers(following_user=followig_user,topic=topic)
    intr_follow.save()
    return redirect("index")


@csrf_exempt
def filter_intrest_unfollow(request,pk):
    followig_user=request.user
    topic=pk
    s=intrest_followers.objects.filter(following_user=followig_user,topic=topic)
    s.delete()
    return redirect("index")

@csrf_exempt
def intrest_follow_topicpage(request,pk):
    followig_user=request.user
    topic=intrest.objects.get(id=pk)
    intr_follow=intrest_followers(following_user=followig_user,topic=topic)
    intr_follow.save()
    return redirect("topicpage",pk)


@csrf_exempt
def intrest_unfollow_topicpage(request,pk):
    followig_user=request.user
    topic=pk
    s=intrest_followers.objects.filter(following_user=followig_user,topic=topic)
    s.delete()
    return redirect("topicpage",pk)
    

@csrf_exempt
def sent_friend_request(request,userid):
    from_user=request.user
    to_user=User.objects.get(id=userid)
    frequest =friend_request(from_user=from_user,to_user=to_user,stat="following")
    frequest.save()


    friend_request_id = friend_request.objects.get(id=frequest.id)

    follow_Notification = Notifications()

    follow_Notification.from_user = to_user
    follow_Notification.to_user = request.user
    follow_Notification.friend_request = friend_request_id
    follow_Notification.type = "User_Fllowing"

    follow_Notification.save()

    return redirect("profile",userid)
    
    

@csrf_exempt
def accept_friend_request(request,requestid):
    request=friend_request.objects.get(id=requestid)

    to=request.to_user
    fr=request.from_user
    gg=friend(
        to=to,
        fr=fr,
    )
    gg.save()
   
    # request.to_user.frdz.add(request.from_user)
    # request.from_user.frdz.add(request.to_user)
    request.delete()
    return HttpResponse("/")
    
    

  

@csrf_exempt
def userfriends(request,id):
    frd = friend.objects.filter()
    return render(request,"userfriends.html",{"frd":frd})    

@csrf_exempt
def following(request,id):
    frd = friend_request.objects.filter(from_user=id)

    return render(request,"following.html",{"frd":frd}) 

@csrf_exempt
def followers(request,id):
    frd = friend_request.objects.filter(to_user=id)
    return render(request,"followers.html",{"frd":frd}) 

#invite


@csrf_exempt
def intrst_followers(request,id):
    frd = intrest_followers.objects.filter()
    intrs=intrest.objects.get(id=id)
    return render(request,"intrest_followers.html",{"frd":frd,"intrs":intrs}) 

@csrf_exempt
def sent_invite_request(request,userid,id):
    from_user=request.user
    pages=page.objects.get(id=id)
    to_user=User.objects.get(id=userid)

    frequest =invite_request()
    frequest.pages=pages
    frequest.from_user=from_user
    frequest.to_user=to_user
    frequest.save()

    user_page_noti = Notifications()

    inv_id = invite_request.objects.get(id=frequest.id)

    user_page_noti.pages = pages
    user_page_noti.to_user = to_user
    user_page_noti.from_user = from_user

    user_page_noti.invite_request = inv_id
    
    user_page_noti.type = "user_page_to_user"

    user_page_noti.save()

    messages.info(request, 'Invitation Request Sent Successfully..')
    
    return redirect("pageprofile2",id)

@csrf_exempt
def accept_invite_request(request,requestid,):
    request=invite_request.objects.get(id=requestid)

    to_user=request.to_user
    fr_user=request.from_user
    fr_pages=request.pages
    gg=invited(
       to_user=to_user,
       fr_user=fr_user,
       fr_pages=fr_pages 
    )
    gg.save()
      
    # request.to_user.frdz.add(request.from_user)
    # request.from_user.frdz.add(request.to_user)
    request.delete()

    return redirect("/")
    
@csrf_exempt    
def page_follow(request,userid):
    from_user=request.user
    to_page=page.objects.get(id=userid)
    frequest =pagefollow(from_user=from_user,to_page=to_page,stat="following")
    frequest.save()
    return redirect("pageprofile",userid) 


@csrf_exempt
def page_unfollow(request,pk):
    to=request.user.id
    fr=pk

    s=pagefollow.objects.filter(from_user=to,to_page=fr,stat="following")
    s.delete()
   
    return redirect('pageprofile',pk)


@csrf_exempt
def notification(request):

    intrests=intrest.objects.all().order_by("?")[:5]
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]



    # fr=friend_request.objects.all()
    # inv=invite_request.objects.all()
    # pag=page.objects.all()
    # foll=Follower.objects.all()

    foll_noti=friend_request.objects.filter(to_user=request.user).order_by("date_created")


    # crt=Cart.objects.filter(user=request.user)
    # crt_count = crt.count()

    Notification = Notifications.objects.filter(to_user=request.user)

    Notification2 = Notifications.objects.filter(from_user=request.user)

    


    context={
            #  'fr':fr,
            #  "inv":inv,
            #  'crt' : crt,
            #  'crt_count' : crt_count,
            #  'pag':pag,
            #  "foll":foll,
             "suggestions":suggestions,
             "intrests":intrests,
            #  "foll_noti":foll_noti,
            #  "foll_noti_c":foll_noti.count()
            'Notification':Notification,
            "Notification2":Notification2,
        }
   
    return render(request,"notification.html",context)  


@csrf_exempt
def userinviters(request,id):
    frd = invited.objects.filter()
    return render(request,"userfriends.html",{"frd":frd})     


@csrf_exempt
def delete_inv(request,pk):
    delete=invite_request.objects.get(id=pk)
    delete.delete()
    messages.info(request, 'Invitation Request Deleted Successfully..')
    return redirect('/')


@csrf_exempt
def delete_frd(request,pk):
    to=request.user.id
    fr=pk

    s=friend_request.objects.filter(from_user__id=to, to_user__id=fr,stat='following')
    s.delete()
   
    return redirect('profile',pk)


@csrf_exempt
def delete_post(request,pk) :
    delete=Post.objects.get(id=pk)
    delete.delete()
    return redirect('/')   

@csrf_exempt
def pages_accept_invites(request,pk):
    pge=invited.objects.all()
    return render(request,'pages_accept_invites.html',{'pge':pge})

def post_comment(request,pk):
    post=Post.objects.filter(id=pk)
    comment=Comment.objects.filter(post_id=pk)
    intrests=intrest.objects.all().order_by("?")[:5]
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
    
      
    context = {
        'posts'  : post, 
        'comment':comment,
        "suggestions":suggestions,
        "intrests":intrests
       
    }

    return render(request,'post_comment.html',context)


@csrf_exempt
def commentz(request,userid):
    post=Post.objects.get(id=userid)
    commenter=request.user
    comment_content= request.POST.get('comment_content')
    cmd =Comment(post=post,commenter=commenter,comment_content=comment_content)
    cmd.save()
    return redirect("post_comment",userid)


def reply(request,userid):
    reviews=review.objects.get(id=userid)
    replier=request.user
    reply_text= request.POST.get('reply_text')
    cmd =ReviewReply(reviews=reviews,replier=replier,reply_text=reply_text)
    cmd.save()


    RevieReply = ReviewReply.objects.get(id=cmd.id)

    

    post_type = reviews.post.posts_type

    if post_type == "page_post":
        notification = Notifications()

        notification.from_user = reviews.reviewer
        notification.to_user = request.user
        notification.pages = reviews.post.page_id
        notification.post = reviews.post
        notification.review = reviews
        notification.ReviewReply = RevieReply

        notification.type = "Page_Post_Reviwes_Replay"
        notification.save()

    elif post_type == "user_post":
        notification = Notifications()
        notification.from_user = reviews.reviewer
        notification.to_user = request.user
        
        notification.post = reviews.post
        notification.review = reviews
        notification.ReviewReply = RevieReply

        notification.type = "User_Post_Reviwes_Replay" 
        notification.save()

    elif post_type == "intrest_post":
        notification = Notifications()
        notification.from_user = reviews.reviewer
        notification.to_user = request.user
        
        notification.post = reviews.post
        notification.review = reviews
        notification.ReviewReply = RevieReply

        notification.type = "Intrest_Post_Reviwes_Replay" 
        notification.save()

    elif post_type == "lev_2_intrest_post":
        notification = Notifications()
        notification.from_user = reviews.reviewer
        notification.to_user = request.user
        
        notification.post = reviews.post
        notification.review = reviews
        notification.ReviewReply = RevieReply

        notification.type = "Intrest_Post_Reviwes_Replay" 
        notification.save()        



    return redirect("review_reply",userid)


        
@csrf_exempt
@login_required(login_url='login')
def nsale_post_share(request,pk):
    post=Post.objects.filter(id=pk)
   

    context = {
        'post'  : post, 
     
    }

    return render(request,'nsale_post_share.html',context)       

@csrf_exempt
@login_required(login_url='login')
def sale_post_share(request,pk):
    post=Post.objects.filter(id=pk)
   

    
    context = {
        'post'  : post, 
       
    }

    return render(request,'sale_post_share.html',context)          


@csrf_exempt
def add_to_wish(requset,pk):
    usr=requset.user
    post=Post.objects.get(id=pk)
    wish=wishlist(usr=usr,post=post)
    wish.save()
    return redirect("index")



@csrf_exempt
def wishlis(request,pk):
    wsh=wishlist.objects.all()
    intrests=intrest.objects.all().order_by("?")[:5]
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    suggestions = []
    choose=intrest.objects.all()
    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()

    dd=inv + noti
    search = request.GET.get('search')
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")
        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:5]


        
    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")

    for i in noti_notifi_count:
        if i.from_user.id == request.user.id:
            if i.type == "Page_Invitions_To_User":
                notifi_count=notifi_count +1

            if i.type == "Page_Accept_User_Invitions":
                notifi_count=notifi_count +1

            if i.type == "User_Fllowing":
                notifi_count=notifi_count +1
                
            if i.type == "Page_Post_Reviwes_Replay":
                notifi_count=notifi_count +1 

            if i.type == "User_Post_Reviwes":
                notifi_count=notifi_count +1

            if i.type == "User_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_level_2_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_level_2_Post_Reviwes_Replay":
                notifi_count=notifi_count +1    

        if i.type == "Page_New_Post":
            for j in page_joined :

                if i.pages == j.pages:
                    notifi_count=notifi_count +1

    context = {'wsh':wsh,
               "suggestions":suggestions,
               "intrests":intrests,
               "dd":dd,
               'crt' : crt,

               'crt_count' : crt_count,
               'search': search,
               'notifi_count':notifi_count,
                "choose":choose
          }   

    return render(request,'wishlist.html',context)

@csrf_exempt
def delete_wishlist(request,pk):
    delete=wishlist.objects.get(id=pk)
    delete.delete()
    return redirect('wishlis',pk)  

@csrf_exempt
def pdf_view(request):
    with open('E:\mypdf.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
        return response
    

@csrf_exempt
def topicpage(request,pk):
    posts = Post.objects.filter(intr_id=pk).order_by('-date_created')
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    choose=intrest_followers.objects.all()

    lev2=level2.objects.all()
    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()

    dd=inv + noti

    user_followers = len(intrest_followers.objects.filter(topic=pk))

    post_count = len(posts)
    to=request.user.id
    fr=pk

    if intrest_followers.objects.filter(following_user=to, topic=fr).first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'


    suggestions = []
    search = request.GET.get('search')
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")
        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:5]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
        
    
    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")

    for i in noti_notifi_count:
        if i.from_user.id == request.user.id:
            if i.type == "Page_Invitions_To_User":
                notifi_count=notifi_count +1

            if i.type == "Page_Accept_User_Invitions":
                notifi_count=notifi_count +1

            if i.type == "User_Fllowing":
                notifi_count=notifi_count +1
                
            if i.type == "Page_Post_Reviwes_Replay":
                notifi_count=notifi_count +1 

            if i.type == "User_Post_Reviwes":
                notifi_count=notifi_count +1

            if i.type == "User_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_level_2_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_level_2_Post_Reviwes_Replay":
                notifi_count=notifi_count +1    

        if i.type == "Page_New_Post":
            for j in page_joined :

                if i.pages == j.pages:
                    notifi_count=notifi_count +1

    
    intr = intrest.objects.get(id=pk)
    
    intrest_path = intr.tooltip 
    
    my_list_intrest_path = []
    if intrest_path != None:
       my_list_intrest_path = [int(x) for x in intrest_path.split("/")]
       
       

  
    class_intersts = [] 
    for i in my_list_intrest_path:
        class_intersts.append(intrest.objects.get(id=i))

       


       
    context = {
        'intr':intr,
        'crt' : crt,
        'crt_count' : crt_count,
        "posts": posts,
        "post_count":post_count,
        "dd":dd,
        "search":search,
        "lev2":lev2,
        "button_text":button_text,
        "user_followers":user_followers,
        "intrests":intrests,
        "suggestions": suggestions, 
        "notifi_count":notifi_count,
        "my_list_intrest_path":my_list_intrest_path,
        "class_intersts":class_intersts,
        "choose":choose
                }
   
    return render(request,'topicpage.html',context)

@csrf_exempt
def subtopicpage(request,pk):
    intr = level2.objects.get(id=pk)
    posts = Post.objects.filter(lev2_id=pk).order_by('-date_created')
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)

    lev2=level2.objects.all()

    user_followers = len(intrest_followers.objects.filter(topic=pk))

    post_count = len(posts)
    to=request.user.id
    fr=pk

    # if intrest_followers.objects.filter(following_user=to, topic=fr).first():
    #      button_text = 'Unfollow'
    # else:  
    #     button_text = 'Follow'


    suggestions = []
    search = request.GET.get('search')
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")
        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:5]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
        
    
    notifi_count = 0
    noti_notifi_count = Notifications.objects.filter(is_read=False)

    page_joined = invite_request.objects.filter(from_user=request.user,status="Joined")

    for i in noti_notifi_count:
        if i.from_user.id == request.user.id:
            if i.type == "Page_Invitions_To_User":
                notifi_count=notifi_count +1

            if i.type == "Page_Accept_User_Invitions":
                notifi_count=notifi_count +1

            if i.type == "User_Fllowing":
                notifi_count=notifi_count +1
                
            if i.type == "Page_Post_Reviwes_Replay":
                notifi_count=notifi_count +1 

            if i.type == "User_Post_Reviwes":
                notifi_count=notifi_count +1

            if i.type == "User_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_Post_Reviwes_Replay":
                notifi_count=notifi_count +1

            if i.type == "Intrest_level_2_Post_Reviwes":
                notifi_count=notifi_count +1
                
            if i.type == "Intrest_level_2_Post_Reviwes_Replay":
                notifi_count=notifi_count +1    

        if i.type == "Page_New_Post":
            for j in page_joined :

                if i.pages == j.pages:
                    notifi_count=notifi_count +1

    context ={
        'intr':intr,
        'crt' : crt,
        'crt_count' : crt_count,
        "posts": posts,
        "post_count":post_count,
        "search":search,
        "lev2":lev2,
        "user_followers":user_followers,
        "intrests":intrests,
        "suggestions": suggestions,
        "notifi_count":notifi_count,
        } 
    return render(request,'subtopicpage.html',context)

@csrf_exempt
def new_post(request):
    usr=User.objects.all()
   
   

    user_following_list = []
    feed = []

   

    user_following = friend_request.objects.filter(from_user__username=request.user.username)


    for users in user_following:
        user_following_list.append(users.to_user)

    for usernames in user_following_list:
        feed_lists=Post.objects.filter(creater=usernames).order_by('-date_created') 
        
        feed.append(feed_lists,)



    posts = list(chain(*feed))
    
 

   
    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    
    intr=intrest.objects.all()


    followig_user=request.user.id
    a="#Article"
    b="#Book"
    c="#Case Study"
    d="#Education"
    e="#Interviews"
    f="#Market Research"
    g="#Observation"
    h="#Poem"
    i="#Survey"
    j="#Work & Business"
    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=a).first():
         button_texta = 'Unfollow'
    else:  
         button_texta = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=b).first():
         button_textb = 'Unfollow'
    else:  
         button_textb = 'Follow'	  
    
     
    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=c).first():
         button_textc = 'Unfollow'
    else:  
         button_textc = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=d).first():
         button_textd = 'Unfollow'
    else:  
         button_textd = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=e).first():
         button_texte = 'Unfollow'
    else:  
         button_texte = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=f).first():
         button_textf = 'Unfollow'
    else:  
         button_textf = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=g).first():
         button_textg = 'Unfollow'
    else:  
         button_textg = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=h).first():
         button_texth = 'Unfollow'
    else:  
        button_texth = 'Follow'	      


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=i).first():
         button_texti = 'Unfollow'
    else:  
        button_texti = 'Follow'	 


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=j).first():
         button_textj = 'Unfollow'
    else:  
        button_textj = 'Follow'	     

    return render(request, "new_post.html",{
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
         "frd":frd,
         "usr":usr.count(),  
         "intr":intr,"button_texta":button_texta,"button_textb":button_textb,"button_textc":button_textc,
                                          "button_textd":button_textd,"button_texte":button_texte,"button_textf":button_textf,
                                          "button_textg":button_textg,"button_texth":button_texth,"button_texti":button_texti,"button_textj":button_textj
       
    })

@csrf_exempt
def user_posts(request):

    if request.method == 'POST':
        selected_value = request.POST.get('dropdown')

        
        
        if selected_value == "best" :
            
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            usr=User.objects.all()
            choose=intrest_followers.objects.all()
            user_following_list = []
            feed = []

            # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        
            us=request.user

            user_following = friend_request.objects.filter(from_user__username=request.user.username)


            for users in user_following:
                if users.from_user == request.user:
                    user_following_list.append(users.to_user)

                    

           


            posts = Post.objects.filter(creater__in=user_following_list,date_created__gte=last_24_hours).exclude(intr_id__isnull=False).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')
        

        
            frd=friend.objects.all()
            pending=friend_request.objects.all()


            
            suggestions = []
            if request.user.is_authenticated:
                followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


            intrests = []
            if request.user.is_authenticated:
                followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
            
            intr = intrest.objects.all()
            followig_user = request.user.id


            
            interest_list = []
            for interest in intr:
                is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                interest_data = {
                    'id' : interest.id,
                    'name': interest.intrest_name,
                    'is_following': is_following
                }
                interest_list.append(interest_data)






            context = {
                'user_posts': 1,
                "posts": posts,
                'pending':pending,
                "suggestions": suggestions,      
                "page": "all_posts",
                "intrests":intrests,
                'profile': False,
                "frd":frd,
                "usr":usr.count(),  
                "intr":intr,"choose":choose,
                "interest_list":interest_list
            
            }    
        

            return render(request, "user_posts.html",context)
        
        if selected_value == "new" :
                last_24_hours = timezone.now() - timezone.timedelta(hours=24)
                usr=User.objects.all()
                choose=intrest_followers.objects.all()
                user_following_list = []
                feed = []

                # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            
                us=request.user

                user_following = friend_request.objects.filter(from_user__username=request.user.username)


                for users in user_following:
                    if users.from_user == request.user:
                        user_following_list.append(users.to_user)

                        

            


                posts = Post.objects.filter(creater__in=user_following_list).exclude(intr_id__isnull=False).order_by('-date_created')
            

            
                frd=friend.objects.all()
                pending=friend_request.objects.all()


                
                suggestions = []
                if request.user.is_authenticated:
                    followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                    suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


                intrests = []
                if request.user.is_authenticated:
                    followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                    intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
                
                intr = intrest.objects.all()
                followig_user = request.user.id


                
                interest_list = []
                for interest in intr:
                    is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                    interest_data = {
                        'id' : interest.id,
                        'name': interest.intrest_name,
                        'is_following': is_following
                    }
                    interest_list.append(interest_data)






                context = {
                    'user_posts': 1,
                    "posts": posts,
                    'pending':pending,
                    "suggestions": suggestions,      
                    "page": "all_posts",
                    "intrests":intrests,
                    'profile': False,
                    "frd":frd,
                    "usr":usr.count(),  
                    "intr":intr,"choose":choose,
                    "interest_list":interest_list
                
                }    
            

                return render(request, "user_posts.html",context)  
        
        if selected_value == "top" :
            
            last_24_hours = timezone.now() - timezone.timedelta(hours=24)
            usr=User.objects.all()
            choose=intrest_followers.objects.all()
            user_following_list = []
            feed = []

            # last_24_hours = timezone.now() - timezone.timedelta(hours=24)
        
            us=request.user

            user_following = friend_request.objects.filter(from_user__username=request.user.username)


            for users in user_following:
                if users.from_user == request.user:
                    user_following_list.append(users.to_user)

                    

           


            posts = Post.objects.filter(creater__in=user_following_list).exclude(intr_id__isnull=False).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')
        

        
            frd=friend.objects.all()
            pending=friend_request.objects.all()


            
            suggestions = []
            if request.user.is_authenticated:
                followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
                suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


            intrests = []
            if request.user.is_authenticated:
                followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
                intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
            
            intr = intrest.objects.all()
            followig_user = request.user.id


            
            interest_list = []
            for interest in intr:
                is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
                interest_data = {
                    'id' : interest.id,
                    'name': interest.intrest_name,
                    'is_following': is_following
                }
                interest_list.append(interest_data)






            context = {
                'user_posts': 1,
                "posts": posts,
                'pending':pending,
                "suggestions": suggestions,      
                "page": "all_posts",
                "intrests":intrests,
                'profile': False,
                "frd":frd,
                "usr":usr.count(),  
                "intr":intr,"choose":choose,
                "interest_list":interest_list
            
            }    
        

            return render(request, "user_posts.html",context)
        
    
            
    one_week_ago = datetime.now() - timedelta(weeks=1)
    usr=User.objects.all()
    choose=intrest_followers.objects.all()
    user_following_list = []
    feed = []

    # last_24_hours = timezone.now() - timezone.timedelta(hours=24)

    us=request.user

    user_following = friend_request.objects.filter(from_user__username=request.user.username)


    for users in user_following:
        if users.from_user == request.user:
            user_following_list.append(users.to_user)

            

    


    posts = Post.objects.filter(creater__in=user_following_list,date_created__gte=one_week_ago).exclude(intr_id__isnull=False).annotate(num_likes=Count('likers')).order_by('-num_likes','-date_created')



    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    intr = intrest.objects.all()
    followig_user = request.user.id


    
    interest_list = []
    for interest in intr:
        is_following = intrest_followers.objects.filter(following_user=followig_user, topic=interest).exists()
        interest_data = {
            'id' : interest.id,
            'name': interest.intrest_name,
            'is_following': is_following
        }
        interest_list.append(interest_data)






    context = {
        'user_posts': 1,
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
        "frd":frd,
        "usr":usr.count(),  
        "intr":intr,"choose":choose,
        "interest_list":interest_list
    
    }    


    return render(request, "user_posts.html",context)

            
@csrf_exempt
def best_post(request):
    usr=User.objects.all()
   
   
    last_24_hours = timezone.now() - timezone.timedelta(hours=24)


    intr_following_list=[]
    intr=[]

    us=request.user

    now = timezone.now()
    one_day_ago = now - timezone.timedelta(hours=24)

    user_following = intrest_followers.objects.filter(following_user=request.user)


    for users in user_following:
        intr_following_list.append(users.topic)

    for usernames in intr_following_list:
        feed_lists = Post.objects.annotate(nlikes=Count('likers', )).filter(intr_id=usernames,nlikes__gt=1,date_created__gte=last_24_hours).order_by('date_created')
        intr.append(feed_lists,)
 
    

    posts = list(chain(*intr))
 

   
    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    


    intr=intrest.objects.all()


    followig_user=request.user.id
    a="#Article"
    b="#Book"
    c="#Case Study"
    d="#Education"
    e="#Interviews"
    f="#Market Research"
    g="#Observation"
    h="#Poem"
    i="#Survey"
    j="#Work & Business"
    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=a).first():
         button_texta = 'Unfollow'
    else:  
        button_texta = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=b).first():
         button_textb = 'Unfollow'
    else:  
        button_textb = 'Follow'	  
    
     
    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=c).first():
         button_textc = 'Unfollow'
    else:  
        button_textc = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=d).first():
         button_textd = 'Unfollow'
    else:  
         button_textd = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=e).first():
         button_texte = 'Unfollow'
    else:  
        button_texte = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=f).first():
         button_textf = 'Unfollow'
    else:  
        button_textf = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=g).first():
         button_textg = 'Unfollow'
    else:  
        button_textg = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=h).first():
         button_texth = 'Unfollow'
    else:  
        button_texth = 'Follow'	      


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=i).first():
         button_texti = 'Unfollow'
    else:  
        button_texti = 'Follow'	 


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=j).first():
         button_textj = 'Unfollow'
    else:  
        button_textj = 'Follow'	     

    return render(request, "best_post.html",{
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
         "frd":frd,
         "usr":usr.count(),  
         "intr":intr,"button_texta":button_texta,"button_textb":button_textb,"button_textc":button_textc,
                                          "button_textd":button_textd,"button_texte":button_texte,"button_textf":button_textf,
                                          "button_textg":button_textg,"button_texth":button_texth,"button_texti":button_texti,"button_textj":button_textj
       
    })


@csrf_exempt
def top_post(request):
    usr=User.objects.all()
   
   
   
    last_24_hours = timezone.now() - timezone.timedelta(hours=24)


    intr_following_list=[]
    intr=[]


    sub_intr_following_list=[]
    sub_intr=[]

    us=request.user

    now = timezone.now()
    one_day_ago = now - timezone.timedelta(hours=24)

    user_following = intrest_followers.objects.filter(following_user=request.user)


    for users in user_following:
        intr_following_list.append(users.topic)

    for usernames in intr_following_list:
        feed_lists = Post.objects.annotate(nlikes=Count('likers', )).filter(intr_id=usernames,nlikes__gt=1).order_by('-nlikes')
        intr.append(feed_lists,)
 


    user_following = intrest_followers.objects.filter(following_user=request.user)


    for users in user_following:
        intr_following_list.append(users.topic)

    for usernames in intr_following_list:
        feed_lists = Post.objects.annotate(nlikes=Count('likers', )).filter(lev2_id__parent_name=usernames,nlikes__gt=1).order_by('-nlikes')

        sub_intr.append(feed_lists,)

        

    posts = list(chain(*intr,*sub_intr))
 

   
    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    


    intr=intrest.objects.all()


    followig_user=request.user.id
    a="#Article"
    b="#Book"
    c="#Case Study"
    d="#Education"
    e="#Interviews"
    f="#Market Research"
    g="#Observation"
    h="#Poem"
    i="#Survey"
    j="#Work & Business"
    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=a).first():
         button_texta = 'Unfollow'
    else:  
        button_texta = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=b).first():
         button_textb = 'Unfollow'
    else:  
        button_textb = 'Follow'	  
    
     
    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=c).first():
         button_textc = 'Unfollow'
    else:  
        button_textc = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=d).first():
         button_textd = 'Unfollow'
    else:  
         button_textd = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=e).first():
         button_texte = 'Unfollow'
    else:  
        button_texte = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=f).first():
         button_textf = 'Unfollow'
    else:  
        button_textf = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=g).first():
         button_textg = 'Unfollow'
    else:  
        button_textg = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=h).first():
         button_texth = 'Unfollow'
    else:  
        button_texth = 'Follow'	      


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=i).first():
         button_texti = 'Unfollow'
    else:  
        button_texti = 'Follow'	 


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=j).first():
         button_textj = 'Unfollow'
    else:  
        button_textj = 'Follow'	     

    return render(request, "top_post.html",{
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
         "frd":frd,
         "usr":usr.count(),  
         "intr":intr,"button_texta":button_texta,"button_textb":button_textb,"button_textc":button_textc,
                                          "button_textd":button_textd,"button_texte":button_texte,"button_textf":button_textf,
                                          "button_textg":button_textg,"button_texth":button_texth,"button_texti":button_texti,"button_textj":button_textj
       
    })



@csrf_exempt
def sales_post(request):
    usr=User.objects.all()
    choose=intrest_followers.objects.all()
    user_following_list = []
    feed = []

    intr_following_list=[]
    intr=[]

    
    user_following = intrest_followers.objects.filter(following_user=request.user)


    for users in user_following:
        intr_following_list.append(users.topic)

    for usernames in intr_following_list:
        feed_lists = Post.objects.filter(intr_id=usernames,status="sale")
        intr.append(feed_lists,)
    

    user_following = friend_request.objects.filter(from_user__username=request.user.username)


    for users in user_following:
        user_following_list.append(users.to_user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(creater=usernames,status="sale")  
        
        feed.append(feed_lists,)



    posts = list(chain(*feed,*intr))
 

   
    frd=friend.objects.all()
    pending=friend_request.objects.all()


    
    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]


    intrests = []
    if request.user.is_authenticated:
        followings = intrest_followers.objects.filter(following_user=request.user).values_list('topic', flat=True)
        intrests = intrest.objects.exclude(pk__in=followings).exclude().order_by("?")[:6]
    
    intr=intrest.objects.all()


    followig_user=request.user.id
    a="#Article"
    b="#Book"
    c="#Case Study"
    d="#Education"
    e="#Interviews"
    f="#Market Research"
    g="#Observation"
    h="#Poem"
    i="#Survey"
    j="#Work & Business"
    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=a).first():
         button_texta = 'Unfollow'
    else:  
        button_texta = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=b).first():
         button_textb = 'Unfollow'
    else:  
        button_textb = 'Follow'	  
    
     
    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=c).first():
         button_textc = 'Unfollow'
    else:  
        button_textc = 'Follow'	


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=d).first():
         button_textd = 'Unfollow'
    else:  
         button_textd = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=e).first():
         button_texte = 'Unfollow'
    else:  
        button_texte = 'Follow'	   


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=f).first():
         button_textf = 'Unfollow'
    else:  
        button_textf = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=g).first():
         button_textg = 'Unfollow'
    else:  
        button_textg = 'Follow'	    


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=h).first():
         button_texth = 'Unfollow'
    else:  
        button_texth = 'Follow'	      


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=i).first():
         button_texti = 'Unfollow'
    else:  
        button_texti = 'Follow'	 


    if intrest_followers.objects.filter(following_user=followig_user, topic__intrest_name=j).first():
         button_textj = 'Unfollow'
    else:  
        button_textj = 'Follow'	     

    return render(request, "sales_post.html",{
        "posts": posts,
        'pending':pending,
        "suggestions": suggestions,      
        "page": "all_posts",
        "intrests":intrests,
        'profile': False,
         "frd":frd,
         "usr":usr.count(),  
          "intr":intr,"button_texta":button_texta,"button_textb":button_textb,"button_textc":button_textc,
                                          "button_textd":button_textd,"button_texte":button_texte,"button_textf":button_textf,
                                          "button_textg":button_textg,"button_texth":button_texth,"button_texti":button_texti,"button_textj":button_textj,"choose":choose,
       
    })


@csrf_exempt
def download_item(request, pk,userid):
    # Retrieve the product
    product = Post.objects.filter(id=pk)
    rew = review.objects.filter(post__id=pk)
    to=request.user.id
    
    
    
    
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)


    if friend_request.objects.filter(from_user_id=to,to_user_id=userid,stat='following').first():
         button_text = 'Unfollow'
    else:  
        button_text = 'Follow'

    context = {
        'pro'  : product, 
        "rew":rew,
        "button_text":button_text,
         'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),  
    }

    return render(request,'download_item.html',context)

@csrf_exempt
def sent_friend_request_download(request,pk,userid):
    product = Post.objects.filter(id=pk)
    from_user=request.user
    to_user=User.objects.get(id=userid)
    frequest =friend_request(from_user=from_user,to_user=to_user,stat="following")
    frequest.save()
    return redirect("product_detail",pk,userid)
    


@csrf_exempt
def delete_frd_download(request,pid,pk):
    product = Post.objects.filter(id=pk)
    to=request.user.id
    fr=pk

    s=friend_request.objects.filter(from_user_id=to, to_user_id=fr,stat='following')
    s.delete()
   
    return redirect('product_detail',pid,pk)

@csrf_exempt
def page_createpost(request,pk):
    choose=intrest_followers.objects.all()
    pro=User.objects.get(id=pk)
    intu=intrest.objects.all()
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)


    def get_interest_path(interest, path=[]):
        if interest.parent:
            path.insert(0, interest.parent.id)
            get_interest_path(interest.parent, path)
        return path

    def get_sublevel_interests(parent):
        sublevels = parent.intrest_set.all()
        sublevel_interests = []
        for sublevel in sublevels:
            sublevel_interests.append(sublevel.id)
            sublevel_interests.extend(get_sublevel_interests(sublevel))
        return sublevel_interests

    parent_interest = intu.first()  # Selecting the first interest for demonstration purposes
    parent_path = get_interest_path(parent_interest)

    parent_path_2 = []
    for i in parent_path:
        parent_path_2.append(intrest.objects.get(id=i))

    sublevels = get_sublevel_interests(parent_interest)

    sublevels_2 = []
    for i in sublevels:
        sublevels_2.append(intrest.objects.get(id=i))


    print(sublevels_2)  


    intrest_following = intrest_followers.objects.all()   


    context = {
       "choose":choose,
       "pro":pro,
       'crt' : crt,
        'crt_count' : crt_count,
        "invc":inv.count(),
       "intu" : intu,
        "intrest_following": intrest_following,
    }
    return render(request,"page_createpost.html",context)

@csrf_exempt
def topic_createpost(request, pk):
    parent_interest = intrest.objects.get(id=pk)

    def get_interest_path(interest, path=[]):
        if interest.parent:
            path.insert(0, interest.parent.id)
            get_interest_path(interest.parent, path)
        return path

    def get_sublevel_interests(parent):
        sublevels = parent.intrest_set.all()
        sublevel_interests = []
        for sublevel in sublevels:
            sublevel_interests.append(sublevel.id)
            sublevel_interests.extend(get_sublevel_interests(sublevel))
        return sublevel_interests

    parent_path = get_interest_path(parent_interest)

    parent_path_2 = []
    for i in parent_path:
        
        parent_path_2.append(intrest.objects.get(id=i))


    
    
    sublevels = get_sublevel_interests(parent_interest)

    sublevels_2 = []
    for i in sublevels:
        
        sublevels_2.append(intrest.objects.get(id=i))


    intr = intrest.objects.get(id=pk)
    crt = Cart.objects.filter(user=request.user)
    lev2 = level2.objects.all()
    crt_count = crt.count()
    inv = invite_request.objects.filter(to_user=request.user)
    choose = intrest_followers.objects.all()
    intu = intrest.objects.all()

    intrest_path = intr.tooltip

    if intrest_path:
        my_list_intrest_path = [int(x) for x in intrest_path.split("/")]
    else:
        my_list_intrest_path = []

    class_intersts = []
    for i in my_list_intrest_path:
        class_intersts.append(intrest.objects.get(id=i))


    intrest_following=intrest_followers.objects.all()    

    context = {
        "choose": choose,
        "intr": intr,
        'crt': crt,
        'crt_count': crt_count,
        "invc": inv.count(),
        "intu": intu,
        "lev2": lev2,
        "class_intersts": class_intersts,
        'sublevels': sublevels,
        "parent_path":parent_path,
        'parent_path_2':parent_path_2,
        'sublevels_2':sublevels_2,
        'intrest_following':intrest_following,
    }

    return render(request, "topic_createpost.html", context)

@csrf_exempt
def create_post(request,pk):
    choose = intrest_followers.objects.all()
    intu = intrest.objects.all()
    crt = Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv = invite_request.objects.filter(to_user=request.user)

    def get_interest_path(interest, path=[]):
        if interest.parent:
            path.insert(0, interest.parent.id)
            get_interest_path(interest.parent, path)
        return path

    def get_sublevel_interests(parent):
        sublevels = parent.intrest_set.all()
        sublevel_interests = []
        for sublevel in sublevels:
            sublevel_interests.append(sublevel.id)
            sublevel_interests.extend(get_sublevel_interests(sublevel))
        return sublevel_interests

    parent_interest = intu.first()  # Selecting the first interest for demonstration purposes
    parent_path = get_interest_path(parent_interest)

    parent_path_2 = []
    for i in parent_path:
        parent_path_2.append(intrest.objects.get(id=i))

    sublevels = get_sublevel_interests(parent_interest)

    sublevels_2 = []
    for i in sublevels:
        sublevels_2.append(intrest.objects.get(id=i))



    intrest_following = intrest_followers.objects.all()
    context = {
        "choose": choose,
        "crt": crt,
        "crt_count": crt_count,
        "invc": inv.count(),
        "intu": intu,
        "parent_path": parent_path,
        "parent_path_2": parent_path_2,
        "sublevels": sublevels,
        "sublevels_2": sublevels_2,
        "intrest_following": intrest_following,
    }
    return render(request, "createpost.html", context)


@csrf_exempt
def invitation_request(request,nid):
    fr=friend_request.objects.all()
    inv=invite_request.objects.all()
    pag=page.objects.all()
    foll=Follower.objects.all()
    foll_noti=friend_request.objects.all().order_by("date_created")
    intrests=intrest.objects.all().order_by("?")[:5]

    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()

    suggestions = []
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
   
    return render(request,"invitation_request.html",{'fr':fr,"inv":inv, 'crt' : crt,
        'crt_count' : crt_count,'pag':pag,"foll":foll,"suggestions":suggestions,"intrests":intrests,"foll_noti":foll_noti,"foll_noti_c":foll_noti.count()})  



@csrf_exempt
def subtopic_createpost(request,pk):
    choose=intrest_followers.objects.all()
    intr = level2.objects.get(id=pk)

    context = {
       "choose":choose,
       "intr":intr
      
    }
    return render(request,"subtopic_createpost.html",context)


# /Ananthakrishnan
@csrf_exempt
def Invite_Page(request,pk):
    user = request.user

    pge = User.objects.get(id=pk)

    to_user = pge


    add_invite = invite_request()

    add_invite.from_user = user
    add_invite.to_user = to_user


   
    add_invite.status = "Pending"

    add_invite.save()

    inv_id = invite_request.objects.get(id=add_invite.id)


    Notifi =Notifications()

    Notifi.from_user = user
    Notifi.to_user = to_user
    
    Notifi.type = "User_Page_Join_Request"
    Notifi.invite_request = inv_id

    Notifi.save()
    return redirect('pageprofile',pk)



def Invite_user_Page(request,pk,kk):
    user = request.user

    pge = page.objects.get(id=pk)
    to_ur=pge.creater
    usr = User.objects.get(id=kk)



    add_invite = invite_request()

    add_invite.from_user = user
    add_invite.pages = pge
    add_invite.to_user = to_ur

    add_invite.status = "Pending"

    add_invite.save()

    inv_id = invite_request.objects.get(id=add_invite.id)


    Notifi =Notifications()

    Notifi.from_user = user
    Notifi.pages = pge
    Notifi.to_user = to_ur
    
    Notifi.type = "User_userpage_Join_Request"
    Notifi.invite_request = inv_id

    Notifi.save()
    return redirect('pageprofile2',pk)


def Leave_Join(request,pk):
    user = request.user

    pge = User.objects.get(id=pk)

    to_user = pge
    


    del_join = invite_request.objects.get(from_user=user,to_user=to_user)

    
    del_join.delete()

    return redirect('pageprofile',pk)


def Leave_userpage_Join(request,pk):
    user = request.user

    pge = page.objects.get(id=pk)

    to_user = pge.creater


    if invite_request.objects.get(to_user=to_user,from_user=user,pages=pge):
         
         del_join=invite_request.objects.get(to_user=to_user,from_user=user,pages=pge)
        
         del_join.delete()

    return redirect('pageprofile2',pk)


def Invite_Joined(request,pk,id):
    

    inv = invite_request.objects.get(id=pk)

    inv.status = "Joined"

    inv.save()

    noti = Notifications.objects.get(id=id)

    noti.type="User_Accept_Page_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()   


    return redirect(notification)


def userpage_Invite_Joined(request,pk,id):
    

    inv = invite_request.objects.get(id=pk)

    inv.status = "Joined"

    inv.save()

    noti = Notifications.objects.get(id=id)

    noti.type="User_Accept_Page_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()


    return redirect(notification)


def page_invite_accept(request,pk):
    

    inv = invite_request.objects.get(id=pk)

    inv.status = "Joined"

    inv.save()

    noti = Notifications.objects.get(id=pk)

    noti.type="user_Accept_userPage_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()


    return redirect(notification)

def Invite_Removed(request,pk,id):
    

    inv = invite_request.objects.get(id=pk)

    inv.delete()

    

    return redirect('profile',id)



def Join_friends(request,id):

    pge = page.objects.get(id=id)


    to_us = pge.creater.id


    friends_list=""
    if invite_request.objects.filter(pages=pge,status="page_Joined"):
        friends_list = invite_request.objects.filter(pages=pge,status="page_Joined")


  
    context = {
        'friends_list':friends_list,
        'pro':pge,
    
    }

    
    
    return render(request,'join_friends.html',context)


def Join_friends_organization(request,id):

    pge = request.user
  


    friends_list=""
    if invite_request.objects.filter(to_user=pge,status="Joined"):
        friends_list = invite_request.objects.filter(to_user=pge,status="Joined")


    context = {
        'friends_list':friends_list,
        'pro':pge,
    }

    
    
    return render(request,'join_friends.html',context)


def Join_friends_reqest(request,id):

    pge = User.objects.get(id=id)

    to_us = pge


    join_list=""
    if invite_request.objects.filter(to_user=to_us,status="Pending"):
        join_list = invite_request.objects.filter(to_user=to_us,status="Pending")

    
    context = {
        'join_list':join_list,
        'pro':pge,
    }

    
    
    return render(request,'join_request_friends.html',context)


def User_page_invitation(request,pk,id):

    from_user = request.user


    user_id = User.objects.get(id=id)

    add_invite = invite_request()

    add_invite.from_user = from_user
    add_invite.to_user = user_id
   

    add_invite.status = "User_Pending"
    add_invite.save()

    inv_id=invite_request.objects.get(id=add_invite.id)
    

    Notifi =Notifications()

    Notifi.from_user = from_user
    Notifi.to_user =  user_id
    
    Notifi.type = "Page_Invitions_To_User"
    Notifi.invite_request = inv_id

    Notifi.save()

    
    return redirect('pageprofile',pk)


def User_page_invitation2(request,pk):


    user_id = request.user
    pge = User.objects.get(id=pk)
    add_invite = invite_request()

    add_invite.from_user = pge
    add_invite.to_user =  user_id
    # add_invite.pages = pge

    add_invite.status = "User_Pending"
    add_invite.save()

    inv_id=invite_request.objects.get(id=add_invite.id)
    

    Notifi =Notifications()

    Notifi.from_user = user_id
    Notifi.to_user = pge
    # Notifi.pages = pge
    Notifi.type = "Page_Invitions_To_User"
    Notifi.invite_request = inv_id

    Notifi.save()


    return redirect('profile',pk)



def User_Invite_Joined(request,pk):
    

    inv = invite_request.objects.get(id=pk)

    inv.status = "Joined"
 
    inv.save()

    nid=request.user

    return redirect('invitation_request',nid.id)



def Page_notifications(request,id):

    # pag_noti = invite_request.objects.filter()

    Notification =  Notifications.objects.filter(to_user=request.user)


    context = {
        'Notification':Notification,
        'page_id':id,
    }

    return render(request,'Mypage_notifications.html',context)



def Accept_notifiction_User(request,id,pk):

    inv = invite_request.objects.get(id=id)

    inv.status = "Joined"

    inv.save()


    noti = Notifications.objects.get(id=pk)

    noti.type="User_Accept_Page_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()


    return redirect(notification)



def user_Accept_userpage_notifiction(request,id,pk):

    inv = invite_request.objects.get(id=id)

    inv.status = "page_Joined"

    inv.save()


    noti = Notifications.objects.get(id=pk)

    noti.type="User_Accept_userpage_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()


    return redirect(notification)



def Delete_Notification_Invitations(request,id):

    inv = invite_request.objects.get(id=id)

    inv.delete()

    return redirect(notification)


def Page_Accept_Notification(request,id,pk):

    inv = invite_request.objects.get(id=id)

    inv.status = "page_Joined"

    inv.save()

    noti = Notifications.objects.get(id=pk)

    noti.type="Page_Accept_User_Invitions"
    

    noti.date_created=timezone.now()


    noti.save()

    return redirect(Page_notifications,noti.pages.id)


def Page_Reject_user_join_Notification(request,id,pk):

    inv = invite_request.objects.get(id=id)

    inv.delete()

    return redirect(Page_notifications,pk)


# Ananthakrishnan/


def review_reply(request,pk):
    rev=review.objects.get(id=pk)
    reply=ReviewReply.objects.all()
    
    return render(request,"review_reply.html",{"rev":rev,"reply":reply})



def reply_delete(request,pk,id):
    rep=ReviewReply.objects.get(id=pk)
    rep.delete() 
    return redirect('review_reply',id)



def review_delete(request,nj,pk,id):
    rep=review.objects.get(id=nj)
    rep.delete()
    return redirect('product_detail',pk,id)


def confirm_order(request,id,pk):

    ordr=Orderz.objects.get(user=request.user)
    post=Post.objects.get(id=id)

    item=Order_Itemz(order=ordr,product=post)
    item.save()


    return redirect('order_manage',id,pk)



def download_histoy(request,id,pk):

        product=Post.objects.get(id=id)
        free_download_user=User.objects.get(id=request.user.id)

        dow=download(post=product,user=free_download_user)
        dow.save()
        return redirect("product_detail",id,pk)




def buy_profile_bookmark(request,pk):
    user = User.objects.get(id=pk)
    wsh= Post.objects.filter(creater=user).annotate(num_wishlist=Count('postz')).order_by('-date_created')
    intrests=intrest.objects.all().order_by("?")[:5]
    crt=Cart.objects.filter(user=request.user)
    crt_count = crt.count()
    inv=invite_request.objects.filter(to_user=request.user)
    suggestions = []
    inv=invite_request.objects.filter(to_user=request.user).count()
    noti=friend_request.objects.filter(to_user=request.user).count()

    dd=inv + noti
    search = request.GET.get('search')
    if request.user.is_authenticated:
        followings = friend_request.objects.filter(from_user=request.user).values_list('to_user',flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")
        if search:
            suggestions = suggestions.filter(username__icontains=search)
        suggestions = suggestions[:5]

    return render(request,'buy_profile_bookmark.html',{'wsh':wsh,"suggestions":suggestions,"intrests":intrests,"dd":dd, 'crt' : crt,
        'crt_count' : crt_count, 'search': search,
          })



def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.viewers += 1
    post.save()
    # rest of the view code


# Ananthakrishnan

# /Ananthakrishnan



def viewerz(request,post_id):
    view = PostViewer.objects.filter(post=post_id)
    
    return render(request,"viewerz.html",{"view":view})


@csrf_exempt
def wishlist_users(request):

    intrests = intrest.objects.all()

    context = {
        'intrests':intrests
    }

    return render(request,"wishlist_users.html",context)



def intrest_create(request):
    if request.method == 'POST':
        intrest_name = request.POST.get("intrest_name")
        parent = request.POST.get("pran")



        if intrest.objects.filter(intrest_name=intrest_name).exists():
            messages.error(request, "An intrest with that name already exists.")
            return redirect("wishlist_users")
        

        if parent != "":

 

            

            intrest1 = intrest.objects.get(id=intrest_create.id)

            temp=[]
            temp2=[]

            
           
            parent1 = intrest1.parent.id


            temp.append(intrest1.parent.id)
            temp2.append(intrest1.parent)
            while parent1 is not None:
                intrest3 = intrest.objects.get(id=parent1)
                if intrest3.parent is not None:  
                    temp.append(intrest3.parent.id)
                    temp2.append(intrest3.parent)
                    parent1 = intrest3.parent.id
                else:
                    parent1 = None

            formatted_str = "/".join(str(i) for i in (reversed(temp)))  
            formatted_str2 = "/".join(str(i) for i in (reversed(temp2)))          
            tooltip =  formatted_str
            tooltip2 =  formatted_str2

            level = len(temp)
            

            intrest2 = intrest.objects.get(id=intrest_create.id)
            intrest2.tooltip = tooltip
            intrest2.level = level  
            intrest2.tooltip2 = tooltip2  
            

            intrest2.save()


            return redirect("wishlist_users")
        else:                
            intrest_create = intrest()
            intrest_create.intrest_name = intrest_name
            intrest_create.save()

            return redirect("wishlist_users")

    return redirect("wishlist_users")


wishlist_users
        # if parent == "#Book":
        #     tooltip = f"{parent} - {intrest_name}"

        # intrest.objects.create(
        #     intrest_name=intrest_name,
        #     parent=parent,
        #     tooltip=tooltip
        # )

        # 

    
    # If the request method is not POST, render the form
   


def messagess(request):

    crt=Cart.objects.filter(to_user=request.user)

    return render(request,'messages.html',{"crt":crt})



def cart_request_delete(request,pk):

    crt_req=Cart.objects.get(id=pk)

    crt_req.status= "Reject"

    crt_req.save()

    return redirect(messagess)


def cart_request_Accept(request,pk):

    crt_req=Cart.objects.get(id=pk)

    crt_req.status= "Accept"

    crt_req.save()

    return redirect(messagess)


def admin_user(request,pk):
    users=User.objects.all()
    return render(request,'admin_user.html')


from django.conf import settings

import os
@csrf_exempt
@login_required(login_url='login')

def edit_post(request, post_id, ik):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        # Check if the delete_image checkbox is selected
        if 'delete_image' in request.POST:
            # Delete the existing image if it exists
            if post.content_image:
                # Delete the file from the file system
                os.remove(os.path.join(settings.MEDIA_ROOT, str(post.content_image)))
                # Clear the content_image field in the model
                post.content_image = None
        else:
            # Update the content_text field
            post.content_text = request.POST.get('content_text', '')

            # Check if a new image file is uploaded
            if 'content_image' in request.FILES:
                # Delete the existing image if it exists
                if post.content_image:
                    # Delete the file from the file system
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(post.content_image)))

                # Save the uploaded image file to the appropriate location
                post.content_image = request.FILES['content_image']

        # Save the post model instance
        post.save()

        return redirect('profile',ik)

    return render(request, 'edit_post.html', {'post': post})


from django.shortcuts import render, redirect, get_object_or_404
def edit_giz_post(request, post_id, ik):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Delete the post and redirect to the desired page
            post.delete()
            return redirect('profile', ik)
        
    if request.method == 'POST':
        post.title = request.POST.get('title', '')
        post.categories = request.POST.get('categories', '')
        post.Product_Price = request.POST.get('product_price', '')
        post.content_text = request.POST.get('content_text', '')

        # Check if a new image file is uploaded
        if 'content_image' in request.FILES:
            # Delete the existing image if it exists
            if post.content_image:
                post.content_image.delete()

            # Update the content_image field with the newly uploaded image
            post.content_image = request.FILES['content_image']

        # Save the updated post
        post.save()

        return redirect('profile', ik)

    return render(request, 'edit_giz_post.html', {'post': post})


from django.shortcuts import render, redirect, get_object_or_404

def edit_org_giz_post(request, post_id, ik):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Delete the post and redirect to the organization profile
            post.delete()
            return redirect('pageprofile')

        post.title = request.POST.get('title', '')
        post.categories = request.POST.get('categories', '')
        post.Product_Price = request.POST.get('product_price', '')
        post.content_text = request.POST.get('content_text', '')

        # Check if a new image file is uploaded
        if 'content_image' in request.FILES:
            # Delete the existing image if it exists
            if post.content_image:
                post.content_image.delete()

            # Update the content_image field with the newly uploaded image
            post.content_image = request.FILES['content_image']

        # Save the updated post
        post.save()

        return redirect('pageprofile', ik)

    return render(request, 'edit_org_giz_post.html', {'post': post})