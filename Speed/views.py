from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .models import User, Likes, Comments
import datetime
import requests
import math
import json




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        labels = {'comment':'Add Comment'}

# Create your views here.
def index(request):
    return render(request, 'speed/index.html')

def docs(request):
    return render(request, 'speed/docs.html')

def contacts(request):
    return render(request, 'speed/contacts.html')

@login_required
def map_view(request):
    return render(request, 'speed/map.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, 'speed/login.html', {
                "message": "Invalid username and/or password."
            })
    else: 
        return render(request, 'speed/login.html')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'speed/register.html', {
                'message': 'Passwords must match.'
            })
        
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'speed/register.html', {
                'message': 'username already taken'
            }) 
        
        login(request, user)
        return HttpResponseRedirect(reverse(index))
    
    else:
        return render(request, 'speed/register.html')

@login_required
def analyze(request):
    if request.method == 'POST':
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        today = datetime.date.today()
        decade = datetime.timedelta(days=3650)
        past = today - decade
        today = today.isoformat()
        past = past.isoformat()

        url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={past}&end_date={today}&daily=windgusts_10m_max&windspeed_unit=ms&timezone=Africa%2FCairo'

        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            gusts_list = data['daily']['windgusts_10m_max']

            def handle_none(num):
                if num is None:
                    return float('-inf')
                return num

            
            max_gust = max(gusts_list, key=handle_none)

            p = 1/(len(gusts_list)+1)
            
            ten_minute_wind = max_gust/1.52 * 1.06
            ten_minute_wind = round(ten_minute_wind, 2)

            numerator = 1 - 0.2 * (math.log(-(math.log(1-0.02))))
            denominator = 1 - 0.2 * (math.log(-(math.log(0.98))))

            result1 = numerator/denominator
            final_result = result1 ** 0.5

            final_wind_value = ten_minute_wind * final_result

            user_comments = Comments.objects.all().order_by('-time')


            return render(request, 'speed/analyze.html', {
                'wind': final_wind_value, 'p': p, 'form': CommentForm(), 'comments':user_comments
            })
        else:
            return HttpResponse('Pick a valid location from the map')
        
    return HttpResponseRedirect(reverse(index))

@login_required
def comment(request):
    if request.method == 'POST':

        comment = CommentForm(request.POST)

        if comment.is_valid():
            entry = comment.cleaned_data['comment']
            user = request.user

            c = Comments(user_id=user, comment=entry)
            c.save()

            user_comments = Comments.objects.all().order_by('-time')

            return render(request, 'speed/analyze.html', {
                'comments': user_comments, 'form': CommentForm()
            })
    
    return HttpResponseRedirect(reverse(index))
    
@csrf_exempt
@login_required
def likes(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    if request.method =='POST':
        content = json.loads(request.body)
        if content is not None:
            change = content['likes']
            if change == 1:
                new_like = Likes(user_id=request.user, comment_id=comment)
                new_like.save()
            else:
                user_likes = Likes.objects.filter(user_id=request.user, comment_id=comment)
                user_likes.delete()
            
        return HttpResponse(404)
    
    comment_likes = Likes.objects.filter(comment_id=comment).count()
    current_user_likes = Likes.objects.filter(comment_id=comment).filter(user_id=request.user)

    return JsonResponse({'likes':comment_likes, 'user_liked': True if current_user_likes else False})
    

