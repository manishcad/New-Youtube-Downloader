from msilib.schema import Error
from django.shortcuts import render
import youtube_dl
from django.contrib import messages
# Create your views here.


def home(request):
    audio_video_streams = []
    if request.method == "POST":
        global url
        url = request.POST.get("url")
        try:
            with youtube_dl.YoutubeDL() as yt:
                video_data = yt.extract_info(url, download=False)

                for i in video_data['formats']:

                    file_size = i['filesize']
                    if file_size is not None:
                        file_size = str(round(int(file_size)/1000000))+" MB"

                    res = "AUDIO"
                    if i['height'] is not None:
                        res = str(i['height']) + "P"

                    audio_video_streams.append({
                        'url': i['url'],
                        'ext': i['ext'],
                        'file_size': file_size,
                        'res': res,
                    })
                context = {'title': video_data.get(
                    "title"), 'views': video_data.get("view_count"), 'duration': str(video_data.get("duration")//60)+" Min", 'dislikes': video_data.get("dislike_count"), 'likes': video_data.get("like_count"), 'thumb': video_data.get('thumbnails')[3]['url'], 'steams': audio_video_streams}
                return render(request, 'home.html', context)
        except Exception as e:
            print(e)
            messages.warning(request, "Enter a Valid Youtube Url ")

    context = {}
    return render(request, 'home.html', context)
