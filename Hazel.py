import os,time,sys

#Main wallpaper path containing other wallapper folders
folder = f'...yourPath/{sys.argv[1]}'

#Script folder path to store the wallpaper value for persistence
dataFolder = f'...yourPath/{sys.argv[2]}.txt'

#Sorting the folder
walls = sorted(os.listdir(folder), key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)


#Read the index of current wallpaper from data file
with open(dataFolder, "r") as file:
    wallData = file.read().strip()
    
#Prevent empty data file
if not wallData:
    wallData = "1"

count = int(wallData)

while count>=0:
    #Writing current wallpaper index to data file
    with open(dataFolder, "w") as file:
        file.write(str(count))

    #Infinite Loop
    if (count == 0):
        count = len(walls)
    count -= 1

    #Wallpaper Change
    wallPath = os.path.join(folder,walls[count])
    os.system(f'swww img "{wallPath}" --transition-type none')

    #Change delay in seconds
    time.sleep(120)


