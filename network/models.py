from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from distutils.command.upload import upload
from itertools import product
from django.shortcuts import reverse
from pyexpat import model
from autoslug import AutoSlugField
from unicodedata import category
from venv import create
from django.db import models
from django.contrib.auth.models import User
from .validators import file_size
from django.contrib.contenttypes.fields import GenericRelation



# class search_item(models.Model):
#     username = models.CharField(max_length=50)
#     pagename=models.CharField(max_length=255,null=True)
#     intrest_name=models.CharField(max_length=255,blank=True)
class intrest(models.Model):
    intrest_name=models.CharField(max_length=255,blank=True)  
    parent=models.ForeignKey("self", on_delete=models.CASCADE,blank=True,null=True)  
    tooltip=models.CharField(max_length=255,blank=True,null=True)
    tooltip2=models.CharField(max_length=255,blank=True,null=True)
    level=models.IntegerField(blank=True,null=True)
    

    def __str__(self):
        return self.intrest_name



class level2(models.Model):
    intrest_name=models.CharField(max_length=255,blank=True)    
    parent_name=models.ForeignKey(intrest, on_delete=models.CASCADE,null=True)



class level3(models.Model):
    intrest_name=models.CharField(max_length=255,blank=True)    
    parent_1=models.ForeignKey(intrest, on_delete=models.CASCADE,null=True)
    parent_2=models.ForeignKey(level2, on_delete=models.CASCADE,null=True)



class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='posts/',default='static/std.jpg')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='posts', default="card2.webp")
    friends=models.ManyToManyField("User",blank=True,related_name="frnd")
    address=models.CharField(max_length=255, blank=True, null=True)
    genter=models.CharField(max_length=255, blank=True, null=True)
    category=models.CharField(max_length=255,blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    website_link= models.URLField(blank=True, null=True)
    facebook_link= models.URLField(blank=True, null=True)
    you_link= models.URLField(blank=True, null=True)
    education= models.URLField(blank=True, null=True)
    state=models.CharField(max_length=255,null=True,blank=True)
    city=models.CharField(max_length=255,null=True,blank=True)
    mobile=models.IntegerField(max_length=255,null=True,blank=True)
    user_type=models.CharField(max_length=255,null=True,blank=True)

    USER_TYPE_CHOICES = (
            ('Admin', 'Admin'),
            ('individual', 'individual'),
            ('organization', 'organization'),
        )
    
    

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
        
        }
    

class page(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=255,null=True)
    pagename=models.CharField(max_length=255,null=True)  
    website=models.CharField(max_length=255,null=True)
    category=models.CharField(max_length=255,null=True)
    emial=models.CharField(max_length=255,null=True)
    cover = models.ImageField(upload_to='posts', default="card2.webp")
    image=models.ImageField(upload_to='posts/', blank=True)   
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    website_link= models.URLField(blank=True, null=True)
    facebook_link= models.URLField(blank=True, null=True)
    you_link= models.URLField(blank=True, null=True)
    education= models.URLField(blank=True, null=True)
    state=models.CharField(max_length=255,null=True,blank=True)
    city=models.CharField(max_length=255,null=True,blank=True)
    mobile=models.IntegerField(max_length=255,null=True,blank=True)


    def __str__(self):
        return self.pagename
    
    def serialize(self):
        return {
            'id': self.id,
            "pagename": self.pagename,
            "image": self.image.url,
        }



class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    page_name=models.CharField(max_length=255,null=True)
    page_id=models.ForeignKey(page, on_delete=models.CASCADE,null=True)
    intr_id=models.ForeignKey(intrest, on_delete=models.CASCADE,null=True)
    lev2_id=models.ForeignKey(level2, on_delete=models.CASCADE,null=True)
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    status=models.CharField(max_length=255,null=True)
    average_rating = models.IntegerField( default=0,null=True)

    
    content_image = models.FileField(upload_to='posts/', blank=True,null=True,validators=[file_size])
    likers = models.ManyToManyField(User,blank=True , related_name='likes')
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    comment_count = models.IntegerField(default=0)
    posts_type = models.CharField(max_length=255,null=True)
    
   
    title=models.CharField(max_length=255,default=True)
    categories=models.CharField(max_length=255,default=True)
    Product_Price = models.IntegerField(null=True,blank=True)

    Offer_toggle = models.CharField(max_length=100,default='Normal')
    
    views_count =models.IntegerField(null=True,blank=True,default=0)


    Offer_price=models.IntegerField(null=True,blank=True)
    Offer_Start_Date = models.DateField(null=True,blank=True)
    Offer_End_Date = models.DateField(null=True,blank=True)
    


    def __str__(self):
        return self.posts_type



    def post_link(self):
        return reverse("post", kwargs={
            'slug': self.slug
        })



    def _str_(self):
        return f"Post ID: {self.id} (creater: {self.creater})" 

    def img_url(self):
        return self.content_image.url



class post_viewers(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_viewed')
    viewer=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_viewed')



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
        


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class sell(models.Model):
    creater=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    picture=models.ImageField(upload_to='posts/',blank=True)
    Title=models.CharField(max_length=255,null=True)
 



class pageposts(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pageposts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User,blank=True , related_name='pagelikes')
    savers = models.ManyToManyField(User,blank=True , related_name='pagesaved')
    comment_count = models.IntegerField(default=0)



# Create your models here.


class Category(models.Model):
    Category_Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Category_Name




class Product(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    Product_Name = models.CharField(max_length=150)
    Product_Image = models.ImageField(upload_to='posts',null=True)
    Product_Description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    Product_Price = models.IntegerField()
   

    def __str__(self):
        return self.Product_Name 


class Zip(models.Model):
    zip_code = models.IntegerField()

    def __str__(self):
        return self.zip_code


    
class Cart(models.Model):
    user=models.ForeignKey(User,related_name='from_user_cart',on_delete=models.CASCADE,null=True,blank=True)
    to_user=models.ForeignKey(User,related_name='to_user_cart',on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Post,related_name='select_post',on_delete=models.CASCADE,null=True,blank=True)   
    product_qty = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    cart_status = ( 

    ('Accept','Accept'),
    ('Pending','Pending'),
    ('Reject','Reject'),

)
    status=models.CharField(max_length=255,choices=cart_status,blank=True,null=True)


    def __str__(self):
        return self.user.first_name


    def __str__(self):
        return self.user.first_name
    


class Orderz(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    Full_name = models.CharField(max_length=255,null=True)
    Phone = models.CharField(max_length=12,null=True)
    House  = models.CharField(max_length=255,null=True)
    Area = models.CharField(max_length=60,null=True)
    Landmark = models.CharField(max_length=60,null=True)
    Town =  models.CharField(max_length=60,null=True)
    State =  models.CharField(max_length=60,null=True)
    Zip = models.IntegerField(null=True)
    date_created=models.DateTimeField(default=timezone.now)
    

    
class Order_Itemz(models.Model):
    order = models.ForeignKey(Orderz,on_delete=models.CASCADE,null=True,blank=True) 
    product = models.ForeignKey(Post,on_delete=models.CASCADE)
    free_download_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    date_created=models.DateTimeField(default=timezone.now)
    
    

class friend_request(models.Model):
    from_user=models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)
    stat=models.TextField(max_length=255,blank=True)
    date_created = models.DateTimeField(default=timezone.now)



class invited(models.Model):
    to_user=models.ForeignKey(User,related_name='toinvit',on_delete=models.CASCADE,blank=True,default=True) 
    fr_user=models.ForeignKey(User,related_name='frinvit',on_delete=models.CASCADE,blank=True,default=True)
    fr_pages=models.ForeignKey(page,related_name='pagez',on_delete=models.CASCADE,blank=True,default=True)


class commentz(models.Model):
    fr_user=models.ForeignKey(User,related_name='comm',on_delete=models.CASCADE,blank=True,default=True)    
    user_post=models.ForeignKey(Post,related_name='pos',on_delete=models.CASCADE,blank=True,default=True)
    comment=models.TextField(max_length=255,blank=True)



class friend(models.Model):
    to=models.ForeignKey(User,related_name='toreq',on_delete=models.CASCADE,blank=True,default=True) 
    fr=models.ForeignKey(User,related_name='freq',on_delete=models.CASCADE,blank=True,default=True)


class wishlist(models.Model):
    usr=models.ForeignKey(User,related_name='whs',on_delete=models.CASCADE,blank=True,default=True)
    post=models.ForeignKey(Post,related_name='postz',on_delete=models.CASCADE,blank=True,default=True)


class intrest_followers(models.Model):
    following_user=models.ForeignKey(User,related_name='intr',on_delete=models.CASCADE,blank= True,default=True)
    topic=models.ForeignKey(intrest,on_delete=models.CASCADE,default=True,related_name='top',blank=True)

class review(models.Model):
    reviewz=models.CharField(max_length=255,blank=True,null=True) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='reviewposst',default=True,blank=True,null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer',default=True,blank=True,null=True)
    mail=models.EmailField(max_length=255,blank=True,null=True)
    rating=models.IntegerField(max_length=255,blank=True,null=True)
    review_time = models.DateTimeField(default=timezone.now)



class ReviewReply(models.Model):
    reviews = models.ForeignKey(review, on_delete=models.CASCADE, related_name='replies')
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=255)
    reply_time = models.DateTimeField(auto_now_add=True)

    
class pagefollow(models.Model):
    from_user=models.ForeignKey(User,related_name='from_users',on_delete=models.CASCADE)
    to_page=models.ForeignKey(page,related_name='to_page',on_delete=models.CASCADE)
    stat=models.TextField(max_length=255,blank=True)  


# /Ananthakrishnan
class invite_request(models.Model):
    from_user=models.ForeignKey(User,related_name='fr_inv',on_delete=models.CASCADE)
    to_user=models.ForeignKey(User,related_name='to_inv',on_delete=models.CASCADE)
    pages=models.ForeignKey(page,related_name='pagz',on_delete=models.CASCADE,null=True)
   

    inv_statuses = (
       
        ('Pending','Pending'),
        ('User_Pending','User_Pending'),
        ('Joined','Joined'),
        ('Rejected','Rejected'),

    )
    
    status =models.CharField(max_length=150,choices=inv_statuses,default='Pending')
    date_created = models.DateTimeField(default=timezone.now)

    
class Notifications(models.Model):
    from_user=models.ForeignKey(User,related_name='fr_noti',on_delete=models.CASCADE,null=True,blank=True)
    to_user=models.ForeignKey(User,related_name='to_noti',on_delete=models.CASCADE,null=True,blank=True)

    pages=models.ForeignKey(page,related_name='pagz_noti',on_delete=models.CASCADE,null=True,blank=True)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='post_noti',null=True,blank=True)

    invite_request =models.ForeignKey(invite_request,on_delete=models.CASCADE,related_name='invite_request',null=True,blank=True)

    friend_request = models.ForeignKey(friend_request,on_delete=models.CASCADE,related_name='friend_request',null=True,blank=True)

    review = models.ForeignKey(review,on_delete=models.CASCADE,related_name='review',null=True,blank=True)

    ReviewReply = models.ForeignKey(ReviewReply,on_delete=models.CASCADE,related_name='ReviewReply',null=True,blank=True)

    choice =(
        ('Default','Default'),
        ('User_Fllow','User_Fllow'),
        ('User_Fllowing','User_Fllowing'),
        ('User_Post_like','User_Post_like'),
        ('User_New_Post','User_New_Post'),
        ('User_Post_Reviwes','User_Post_Reviwes'),
        ('User_Post_Reviwes_Replay','User_Post_Reviwes_Replay'),
        ('Page_Invitions_To_User','Page_Invitions_To_User'),

        ('User_Accept_userpage_Invitions','User_Accept_userpage_Invitions'),
        
        ('User_Accept_Page_Invitions','User_Accept_Page_Invitions'),
        ('User_Page_Join_Request','User_Page_Join_Request'),
        ('Page_Accept_User_Invitions','Page_Accept_User_Invitions'),
        ('Page_New_Post','Page_New_Post'), 
 

        ('Intrest_Post_Reviwes','Intrest_Post_Reviwes'),
        ('Intrest_Post_Reviwes_Replay','Intrest_Post_Reviwes_Replay'),

        ('Intrest_level_2_Post_Reviwes','Intrest_level_2_Post_Reviwes'),
        ('Intrest_level_2_Post_Reviwes_Replay','Intrest_level_2_Post_Reviwes_Replay'),   
    )



    type = models.CharField(max_length=150,choices=choice,default='Default')

    date_created = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']


class PostViewer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True)



# Ananthakrishnan/

class download(models.Model):
    post=models.ForeignKey(Post,related_name='downloading_post',on_delete=models.CASCADE)    
    user=models.ForeignKey(User,related_name='downloading_user',on_delete=models.CASCADE)
    download_date=models.DateTimeField(default=timezone.now)



class viewers(models.Model):
    post=models.ForeignKey(Post,related_name='viewed_post',on_delete=models.CASCADE)   
    user=models.ForeignKey(User,related_name='viewed_user',on_delete=models.CASCADE)


