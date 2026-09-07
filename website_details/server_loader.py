import os
from pathlib import Path
from livereload import Server

file_dir = Path(__file__).resolve().parent
os.chdir(file_dir)

server = Server()

# Watch files in the root folder AND subdirectories
server.watch('*.html')
server.watch('*.css')
server.watch('*/*.html')
server.watch('*/*.css')

# Point directly to your root directory and set default page
server.serve(port=5500, root=file_dir, default_filename='index.html')