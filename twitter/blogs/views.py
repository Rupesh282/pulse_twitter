from django.shortcuts import redirect, render
from .models import Posts, PostToTags
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
import datetime

def index(request) : 
    return render(request, 'index.html', {'name' : 'Rupesh'})

def createPostForm(request) : 
    return render(request, 'createPost.html')

def getPostsByForm(request)  :
    return render(request, 'getPostsByForm.html')

@csrf_exempt
def createPost(request) : 
    if request.method == "POST" : 
        text_data = request.POST.get("text_data")
        published_date = datetime.datetime.now().date()
        tags = request.POST.get("tags").strip().split(" ")
        
        print(f"data : {text_data}")
        print(f"date : {published_date}")
        print(f"tags : {tags}")
        
        blog_post = Posts(text_data=text_data, published_date=published_date)
        blog_post.save()
        
        # don't consider duplicate tags 
        repeated_tags = {}
        for tag in tags : 
            if len(tag) == 0 or (tag in repeated_tags) : 
                continue 
            else : 
                repeated_tags[tag] =  1
                
            post_tag = PostToTags(post=blog_post, tag_name=tag)
            post_tag.save()
        
        print("post, tags saved success !")
        
    
    return render(request, 'createPost.html')

@csrf_exempt
def deletePost(request, post_pk) : 
    if request.method == "DELETE" : 
        print(f"post pk : {post_pk}")
        
        try : 
            blog_post = Posts.objects.get(id = post_pk)
            blog_post.delete()
            print("deleted succussfully !!")
        except : 
            print("No record exists !")
        
    return HttpResponse("post deleted successfully !")



def _updateTags(old_tags, new_tags, old_post) :
    valid_map = {}
    for tag in new_tags : 
        if tag not in valid_map : 
            valid_map[tag] = 0
            
    for tag in old_tags : 
        if tag.tag_name in valid_map : 
            valid_map[tag.tag_name] = 1
        else : 
            # delete the current tag 
            tag.delete()
            
    for tag_name, added in valid_map.items() : 
        if added == 0 : 
            tag_entry = PostToTags(post = old_post, tag_name = tag_name)
            tag_entry.save()

@csrf_exempt
def updatePost(request, post_pk) : 
    if request.method == "POST" :
        try : 
            old_post = Posts.objects.get(id = post_pk)
            
            old_tags = PostToTags.objects.filter(post = old_post)
            
            print(f"current tags : {old_tags}")
            
            new_text_data = request.POST.get("text_data", None)
            new_tags = request.POST.get("tags", None)
            
            print(new_text_data)
            print(new_tags)
            
            if new_text_data != None : 
                old_post.text_data = new_text_data
                
            if new_tags != None : 
                new_tags = new_tags.strip().split(" ")
                _updateTags(old_tags, new_tags, old_post)
            
            old_post.save()
                
            print("post is updated !")
            
        except : 
            print("NO such post available")

        
    return HttpResponse("post updated successfully !")


@csrf_exempt
def getPostsFromTags(request) : 
    if request.method == "GET" : 
        tags = request.GET.get("tags", None)
        valid_posts = {}
        
        if tags == None : 
            return render(request, 'getPostsByTags.html')
        
        tags = tags.strip().split(" ")
        
        for tag in tags : 
            candidates = PostToTags.objects.filter(tag_name = tag)
            for candidate in candidates : 
                post_id = candidate.post.id
                if post_id not in valid_posts : 
                    valid_posts[post_id] = 1

        id_list = []  
        for key in valid_posts.keys() : 
            id_list.append(key)
            
        posts = Posts.objects.filter(id__in = id_list)
        
        context = {}
        context['posts'] = posts
            
        print(context)
        print(posts)
        return render(request, 'getPostsByForm.html', context)
            
    return HttpResponse("found some posts")


@csrf_exempt
def getPostsFromText(request) : 
    if request.method == "GET" : 
        text = request.GET.get("text_data").strip().split(" ")

        posts = Posts.objects.all()
        for field in text : 
            posts = posts.filter(text_data__icontains = field)

        return render(request, 'getPostsByForm.html', {'posts' : posts})
    
    else :
        return HttpResponse("not using GET for getPostsFromText")


@csrf_exempt
def getPostsFromDates(request) : 
    if request.method == "GET" : 
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date", datetime.datetime.now().date())
        
        posts = Posts.objects.all().exclude(
            published_date__gt = to_date
        ).filter(
            published_date__gte = from_date
        )
        
        print(posts)
        
        return render(request, 'getPostsByForm.html', {'posts' : posts})
    
    else :
        return HttpResponse("not using GET for getPostsFromDates")