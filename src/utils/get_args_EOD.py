import sys

project_url = sys.argv[1]
output = project_url.split("/-/")[0]
folders = []
file_paths = sys.argv[2:len(sys.argv)]
for f in file_paths:
    folder = f.split("/")[0]
    if folder not in folders:
        folders.append(folder)
        output = output + " " + folder
print(output)