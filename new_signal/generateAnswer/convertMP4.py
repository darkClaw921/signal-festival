from moviepy.editor import *



def convertMP4toMP3(path):
    # Load the mp4 file
    video = VideoFileClip(path)
    path = path.split('.')[0]
    # Extract audio from video
    video.audio.write_audiofile(f"{path}.mp3")
    return f"{path}.mp3"

# # Load the mp4 file
# video = VideoFileClip("example.mp4")

# # Extract audio from video
# video.audio.write_audiofile("example.mp3")
if __name__ == '__main__':
    convertMP4toMP3('audio.mp4')