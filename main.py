import cv2
import pytesseract
import numpy as np
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'

    # functions
def Text_Cleaner(raw_text):
    raw_text = raw_text.replace(',', "")

    lines = raw_text.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]

    text = ""
    for line in non_empty_lines:
        text += line
    return text

    #framework
def Tokenize(Tokens):
    smallest = 1000000
    for x in Tokens:
        if x < smallest:
            smallest = x
    return smallest

database = np.empty([10, 4], dtype=object)
Bounding_Box_Size = np.empty([500, 2], dtype=object) #(Box, String, len)
Tokens = []
Key = 'Reply'

users = 0
raw_text = ''
word_count = 0

    # load & read img
img = cv2.imread("Insta test pic edit.png")
#img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#print(pytesseract.image_to_boxes(img))

    #Visualize detected Characters
hImg, wImg,_ = img.shape
boxes = pytesseract.image_to_data(img)
#print(boxes)

    #create each word as a list
for x,b in enumerate(boxes.splitlines()):
      if x!=0:
            b = b.split()
            print(b)

            if len(b) == 12:
                  # x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                  raw_text += b[11] + ' '
                  Bounding_Box_Size[word_count][0] = b[9]
                  Bounding_Box_Size[word_count][1] = b[11]
                  word_count += 1

                    # push bounding box
                  if b[11] == Key:
                      Tokens.append(int(b[9]))

                    #Bounded Boxes for char visualization
                  # cv2.rectangle(img, (x, y), (w + x, y+ h), (0, 0, 255), 2)
                  # cv2.putText(img, b[11], (x, hImg-y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
            else:
                  raw_text += '\n'
#print(Tokens)
    #cleaning text
raw_text = raw_text.replace(',', "")
text = raw_text.split(' ')
print(text)

comment = ''
end_box = str(Tokenize(Tokens)) #end user size identification box
flag = True

for i in range(len(text)-1):
    if flag:
        database[users][0] = Text_Cleaner(text[i])  # UserName
        flag = False
        continue
    if Key in text[i] and str(end_box) in Bounding_Box_Size[i][0]:
        # print('found end')
        if "likes" not in text[i-1]:
            database[users][3] = 0  # likes
            database[users][2] = Text_Cleaner(text[i - 1])  # timestamp
            database[users][1] = Text_Cleaner(comment[:-1 * len(text[i - 1])])  # comment
        else:
            database[users][3] = text[i - 1]  # likes
            database[users][2] = Text_Cleaner(text[i - 2])  # timestamp
            comment = comment[:-1 * len(text[i - 1])]
            database[users][1] = Text_Cleaner(comment[:-1 * len(text[i - 2])])  # comment
        users += 1
        comment = ''
        flag = True
    else:
        comment += text[i] + ' '

#///////////////////////////////////////////////////////
    #print("Word_count list")
print()
print(Bounding_Box_Size)

    #Test finding new Users
print()
print("number of users ", users)
print(database)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # label for pandas  -> Numpy 2d array to excel
df = pd.DataFrame(data=database,columns=["User", "Comment", "Time", "Likes"])
df.to_csv("CommentTest.csv", index=False)

# cv2.imshow('Result', img)
# cv2.waitKey(0)

"""
/////////////////////////////////////////////////////////////////
# open text file
text_file = open("Output.txt", "w")

if "\n" in raw_text:
    data = raw_text.replace("\n", "")
else:
    data = raw_text.replace("\r", "\n")

text = raw_text.split('\n')


# write string to file
n = text_file.write(text)

# close file
text_file.close()

///////////////////////////////////////////////////////////////

#cleaning text
raw_text = raw_text.replace(',', "")

lines = raw_text.split("\n")
non_empty_lines = [line for line in lines if line.strip() != ""]

text = ""
for line in non_empty_lines:
      text += line + "\n"

print(lines)
"""


"""
#Sub-string indentification
new_user = '\n\n\n'
end = 'w_'  #(identify all possible timestamps)
comment = ''
end_box = str(Tokenize(Tokens)) #end user size identification box

for i in range(len(text)):
  #print(text[i])

  if end in text[i]:
        #print('found end')
        database[users][2] = Text_Cleaner(text[i]) #timestamp
        database[users][1] = Text_Cleaner(comment) #comment
        users += 1

  elif new_user in text[i]:
        #print("found new user in text list ", i)
        database[users][0] = Text_Cleaner(text[i]) #UserName
        comment = ''
  else:
        if Key in text[i] and str(end_box) not in Bounding_Box_Size[i][0]:
            comment += text[i] + ' '
        else:
            pass

"""



