""" Init views """

IMAGE_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'])
AUDIO_EXTENSIONS = set(['m4a', 'wav', 'mp3', 'ogg', '3gpp', 'mp4'])
EXCEL_EXTENSIONS = set(['xls', 'xlsx'])
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | AUDIO_EXTENSIONS | EXCEL_EXTENSIONS
