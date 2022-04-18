from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .serializers import MessageSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.user.is_authenticated:
        curr_user = request.user.id
        post = Post.objects.all().order_by('-post_time')
        dp_ = profile.objects.get(user = curr_user)
        dp = dp_.dp
        context={'post':post, 'dp': dp}
        return render(request, 'home.html', context)
    else:
        return redirect("/signin")

def postdetails(request, id):
    post = Post.objects.all().filter(id = id)
    user = request.user
    post_ = Post.objects.get(id=id)
    comments = Comment.objects.all().filter(post = post_).order_by('-date')
    p_comnt = post_.comnt
    if request.method == 'POST':
        try:
            comm = request.POST.get('comm')
            Obj = Comment(post = post_,user = user,body = comm)
            p_comnt = p_comnt + 1
            post_.comnt = p_comnt
            post_.save()
            Obj.save()
        except:
            pass

    comm_count = Comment.objects.all().filter(post = post_).count()
    dp_ = profile.objects.get(user = user)
    dp = dp_.dp
    context = {'post': post,'comments': comments, 'dp':dp, 'count': comm_count}
    return render(request, 'postdetails.html', context)

def about(request):
    return render(request, 'about.html')

def signin(request):
    if request.method == 'POST':
        try :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        except:
            return redirect("signin")
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(username=username, email=email, password=password)
        if user is None:
            context = {'message': 'Fill again!'}
            return render(request,'signup.html', context)
        else:
            if User.objects.filter(username=username).count():
                context = {'message': 'User already registered'}
                return render(request,'signup.html', context)
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                bio_ = "Hi there"
                Profile = profile(bio=bio_,user=user)
                Profile.save()
                context = {'message': 'User registered'}
                return render(request, 'signup.html', context)
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

def Profile(request):
    curr_user=request.user.id
    pro_ = profile.objects.get(user = curr_user)
    pro = pro_.dp
    bio_ = profile.objects.filter(user=curr_user).values('bio')
    bio = bio_[0]['bio']
    p_no = Post.objects.filter(user_name = curr_user).count()
    post = Post.objects.all().filter(user_name = curr_user)

    context = {'bio':bio, 'pro':pro, 'p_no':p_no, 'post': post}
    return render(request, 'profile.html',context)

def edit(request):
    curr_user = request.user.id
    pro = profile.objects.get(user = curr_user)
    p_no = Post.objects.filter(user_name = curr_user).count()
    obj = Post.objects.all().filter(user_name = curr_user)
    print(obj)
    if request.method == 'POST':
        bio = request.POST.get('bio')
        email = request.POST.get('email', False)
        dp_ = request.FILES.get('dp', False)

        if dp_ is not False:
            try:
                dp_del = pro.dp
                dp_del.delete()
                pro.dp = request.FILES['dp']
                pro.save()
                for o in obj:
                    p_del = o.p_dp
                    p_del.delete()
                    o.p_dp = request.FILES['dp']
                    o.save()
                
            except:
                pro.dp = request.FILES['dp']
                pro.save()
                for o in obj:
                    p_del = o.p_dp
                    p_del.delete()
                    o.p_dp = request.FILES['dp']
                    o.save()
        
        if len(email) != 0:
            try:
                User.objects.filter(id = curr_user).update(email=email)
            except:
                print("Exception")

        if len(bio) != 0 :
            try:
                profile.objects.filter(user=curr_user).update(bio=bio)
            except:
                print("Exception")

        return redirect('/profile')
    curr_user=request.user.id
    pro_ = profile.objects.get(user = curr_user)
    pro = pro_.dp
    context = {'pro':pro, 'p_no':p_no}
    return render(request, 'edit.html',context)

def post(request):
    curr_user=request.user.id
    if request.method == 'POST':
        
        posts = Post()
        posts.description = request.POST.get('desc')
        posts.file = request.FILES['file']
        posts.user_name = request.user
        posts.tags = request.POST.get('tags')
        dp_ = profile.objects.get(user = curr_user)
        posts.p_dp = dp_.dp
        posts.likes = 0
        posts.save()

    pro_ = profile.objects.get(user = curr_user)
    pro = pro_.dp
    context = {'pro':pro}
    return render(request, 'post.html', context)
    
def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post).count()
    user_ = Likes.objects.filter(user = user, post = post)

    if not liked and user_ != user:
        like = Likes.objects.create(user=user,post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes -1

    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('postdetails',args=[id]))
    

def comment(request, id):
    return HttpResponseRedirect(reverse('postdetails',args=[id]))


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')

@csrf_exempt
def message_list(request, sender=None, receiver=None):
   
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('/signin')
    if request.method == "GET":
        dp_ = profile.objects.get(id = request.user.id)
        dp = dp_.dp
        return render(request, 'direct.html',{'users': User.objects.exclude(username=request.user.username), 'dp':dp})

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('/signin')
    if request.method == "GET":
        pro_ = profile.objects.get(user = receiver)
        pro = pro_.dp
        dp_ = profile.objects.get(id = request.user.id)
        dp = dp_.dp
        context = {'users': User.objects.exclude(username=request.user),
        'receiver': User.objects.get(id=receiver),
        'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver)
         | Message.objects.filter(sender_id=receiver, receiver_id=sender),'person': User.objects.filter(id=receiver),
         'pro':pro,
         'dp':dp
        }
        return render(request, "messages.html", context)

