from django.shortcuts import render
import requests
from isodate import parse_duration
from django.conf import settings
# Create your views here.
def index(request):
    videos=[]
    if request.method=="POST":
        search_url='https://www.googleapis.com/youtube/v3/search'
        video_url='https://www.googleapis.com/youtube/v3/videos'
        s_params={
            'part':'snippet',
            'q':request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type':'video'
        }
        video_ids=[]
        r=requests.get(search_url,params=s_params)
        result=r.json()['items']
        for result in result:
            video_ids.append((result['id']['videoId']))
        v_params={
            'part':'snippet,contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id':','.join(video_ids),
            'maxResults': 9,

        }
        r=requests.get(video_url,params=v_params)
        results=r.json()['items']
        
        for result in results:
            video_data={
                'title':result['snippet']['title'],
                'id':result['id'],
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbmail':result['snippet']['thumbnails']['high']['url'],
                'url':f'https://www.youtube.com/watch?v={ result["id"] }'
            }
            videos.append(video_data)

    context={
        'videos':videos
    }

    return render(request,'index.html',context)