from flask import Flask, request, make_response
import requests
from json import loads, dumps
from urllib.parse import urlparse, parse_qs
from os.path import join
import asyncio
from urllib import request as ro

my_app = Flask(__name__)


def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        if query.path[:9] == '/playlist': return parse_qs(query.query)['list'][0]


loop = asyncio.get_event_loop()


async def save_file(filepath, data):
    ro.urlretrieve(data, filepath)
    async with ro.urlretrieve(data, filepath):
        print("data saved in ", filepath)


@my_app.route("/", methods=['GET'])
def home():
    return "video = /vid?url=\naudio = /aud?url=\ninfo = /info?url="


@my_app.route("/vid", methods=["GET"])
def ytt():
    url = request.args.get("url")
    vid = extract_video_id(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://y2matemp3.online',
        'Alt-Used': 'y2matemp3.online',
        'Connection': 'keep-alive',
        'Referer': 'https://y2matemp3.online/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    json_data = {
        'q': url,
    }

    if url:
        response = requests.post('https://y2matemp3.online/api/analyze', headers=headers, json=json_data).text
        lod = loads(response)
        return_dict = dumps(
            {
                "by": "@me_dhurgham",
                "result": {
                    "title": lod["videos"]["text"],
                    "duration": lod["videos"]["durationText"],
                    "server": f"http://.../tmp/{vid}.mp4",
                }})

        output = make_response(return_dict)
        output.headers['Content-Type'] = 'application/json; charset=utf-8'
        url = lod["videos"]["mp4s"][1]["url"]
        filepath = join("/var/www/html/tmp", f'{vid}.mp4')
        tasks = [loop.create_task(save_file(filepath, url))]
        loop.run_until_complete(asyncio.wait(tasks))

        return output
    else:
        return "uwu"


@my_app.route("/aud", methods=["GET"])
def ytt():
    url = request.args.get("url")
    vid = extract_video_id(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://y2matemp3.online',
        'Alt-Used': 'y2matemp3.online',
        'Connection': 'keep-alive',
        'Referer': 'https://y2matemp3.online/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    json_data = {
        'q': url,
    }

    if url:
        response = requests.post('https://y2matemp3.online/api/analyze', headers=headers, json=json_data).text
        lod = loads(response)
        return_dict = dumps(
            {
                "by": "@me_dhurgham",
                "result": {
                    "title": lod["videos"]["text"],
                    "duration": lod["videos"]["durationText"],
                    "server": f"http://.../tmp/{vid}.mp4",
                }})

        output = make_response(return_dict)
        output.headers['Content-Type'] = 'application/json; charset=utf-8'
        url = lod["videos"]["audios"][0]["url"]
        filepath = join("/var/www/html/tmp2", f'{vid}.mp3')
        tasks = [loop.create_task(save_file(filepath, url))]
        loop.run_until_complete(asyncio.wait(tasks))
        return output
    else:
        return "uwu"


@my_app.route("/info", methods=["GET"])
def info():
    url = request.args.get("url")
    vid = extract_video_id(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://y2matemp3.online',
        'Alt-Used': 'y2matemp3.online',
        'Connection': 'keep-alive',
        'Referer': 'https://y2matemp3.online/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    json_data = {
        'q': url,
    }

    if url:
        response = requests.post('https://y2matemp3.online/api/analyze', headers=headers, json=json_data).text
        lod = loads(response)
        return_dict = dumps(
            {
                "by": "@me_dhurgham",
                "result": {
                    "title": lod["videos"]["text"],
                    "duration": lod["videos"]["durationText"],
                    "img": f"http://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                }})

        output = make_response(return_dict)
        output.headers['Content-Type'] = 'application/json; charset=utf-8'
        return output
    else:
        return "uwu"


my_app.run(host='0.0.0.0', port=5000)
