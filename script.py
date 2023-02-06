import os
import pytube
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def upload_video_to_youtube(video_file, title, description, tags):
    # First, let's build the credentials object
    credentials, project = google.auth.default()

    youtube = build('youtube', 'v3', credentials=credentials)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": 22
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            media_body=video_file
        )
        response = request.execute()
        print(f"Video was uploaded successfully with id: {response['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None
    return response

def download_video_by_link(link, path):
    try:
        video = pytube.YouTube(link)
        video.streams.first().download(output_path=path)
        print(f"Video was downloaded successfully to: {path}")
        return os.path.join(path, video.streams.first().default_filename)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    link = input("Enter the video link: ")
    path = input("Enter the path to download the video: ")
    video_file = download_video_by_link(link, path)
    if video_file:
        title = input("Enter the video title: ")
        description = input("Enter the video description: ")
        tags = input("Enter the video tags (comma-separated): ").split(',')
        upload_video_to_youtube(video_file, title, description, tags)
    else:
        print("Video download failed")
