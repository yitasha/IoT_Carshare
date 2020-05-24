from os import listdir
from os.path import isfile, join
import cv2

# Set the relative path of image folder
# All the pictures get stored in images folder 
# "folder name/ap/image/"
path = "github copy/ap/image/"

# List all the files from image folder
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for x in range(len(onlyfiles)):
    print(str(x) + ":" + onlyfiles[x])

# User can select a image based on index
print("Choose a image or type in 'Quit'")
selection = input("Select an option: ")
while(True):
    if selection == "Quit":
        print("Good Bye!")
        break
    elif selection is not None:
        print(onlyfiles[int(selection)])
        img = cv2.imread(path + onlyfiles[int(selection)],1)
        # img is the picture code need to send to MP using database function
        # def checkFaceImage(self, img, carid, date)
        print(img)
        break
    else:
        print("Invalid input - please try again.")

