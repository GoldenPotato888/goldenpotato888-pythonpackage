from googleapiclient.discovery import build

key = "AIzaSyAEUENGu1DU-HTTS-AZ22vNXvH8s-Y1VIw"
yt = build("youtube", "v3", developerKey=key)

def get_channel_id(name: str) -> str:
    request = yt.search().list(
        part="snippet",
        q=name,
        type="channel"
    )
    response = request.execute()

    return response['items'][0]['snippet']['channelId']

def get_channel_stats(channel_id: str) -> str:
    request = yt.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()

    return response['items'][0]['statistics']

def get_videos_from_channel(channel_id: str) -> str:
    import isodate
    response = yt.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while True:
        playlist_response = yt.playlistItems().list(
            part="contentDetails",
            playlistId=uploads,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = [item["contentDetails"]["videoId"] for item in playlist_response["items"]]

        video_response = yt.videos().list(
            part="snippet,contentDetails",
            id=",".join(video_ids)
        ).execute()

        for item in video_response["items"]:
            video_id = item["id"]
            title = item["snippet"]["title"]
            duration = item["contentDetails"]["duration"]
            duration = isodate.parse_duration(duration)
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                content_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                content_duration = f"{minutes:02}:{seconds:02}"
            videos.append((video_id, title, content_duration))

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    thing_to_return = ""
    for vid in videos:
        thing_to_return += f"ID: {vid[0]} | Name: {vid[1]} | Duration: {vid[2]}\n"
    return thing_to_return

def get_video_stats(video_id: str) -> str:
    response = yt.videos().list(
        part="statistics",
        id=video_id
    ).execute()
    return f"Views: {response['items'][0]['statistics']['viewCount']}\nLikes: {response['items'][0]['statistics']['likeCount']}\nComments: {response['items'][0]['statistics']['commentCount']}"

print(get_channel_stats(get_channel_id('GoldenPotato888')))