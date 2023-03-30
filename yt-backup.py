import os
import git
import ghapi
from yt_dlp import YoutubeDL

# Clone the repository using ghapi library
gh = ghapi.GitHub()
owner, repo = 'prolifick1', 'audio-spoken-short'
repo_info = gh.repos.get(owner=owner, repo=repo)
clone_url = repo_info['clone_url']
git.Repo.clone_from(clone_url, repo)

# Change to the cloned directory
os.chdir(repo)

# Download the playlist using yt-dlp library
with YoutubeDL({'flat_playlist': True, 'print_json': False, 'extract_flat': True}) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=PL7AAPmGX5Gsaj3F_Wsy9XjeRhLGtGuqDN'])
    
# Sort the tracks
with open('audio-spoken-short-updated.txt', 'r') as f:
    tracks = f.readlines()
tracks.sort()
with open('audio-spoken-short-updated.txt', 'w') as f:
    f.writelines(tracks)

# Perform the Git merge using GitPython library
repo = git.Repo('.')
empty_file_path = 'empty-file.txt'
with open(empty_file_path, 'w') as f:
    f.write('')
repo.index.merge_file('audio-spoken-short.txt', 'audio-spoken-short.txt', empty_file_path, 'audio-spoken-short-updated.txt', 'theirs')
os.remove(empty_file_path)

# Show the Git diff
diff = repo.git.diff('audio-spoken-short.txt')
print(diff)

# Commit and push the changes
repo.git.add('audio-spoken-short.txt')
repo.index.commit('message')
origin = repo.remote(name='origin')
origin.push()