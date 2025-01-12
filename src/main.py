from PIL import Image, ImageDraw
from pathlib import Path


# open image with white background and black text
IMAGEPATH = "tests\\images\\1backup.png"

im = Image.open(IMAGEPATH)
#im = im_crop.resize((500, 500))
w, h = im.size
print(im.format, im.size, im.mode)
initExp2 = 1


rgb_im = im.convert('RGB')
# resize the image to size variable
# check if image already of the size of the letter

# get square coord around the letter
def getBlackPixelCoord(img, reductor=1):
    print(img.size)
    blackCoord = []
    threshold = 240
    width, height = img.size
    for x in range(width // reductor):
        for y in range(height // reductor):
            if img.getpixel((x * reductor, y * reductor))[0] < threshold and img.getpixel((x * reductor, y * reductor))[1] < threshold and img.getpixel((x * reductor, y * reductor))[2] < threshold:
                blackCoord.append((x * reductor, y * reductor)) 
    return blackCoord

def createBlackPixelRender(blackPixelCoord, im):
    print(blackPixelCoord)
    minHeight, maxHeight = blackPixelCoord[0][0], blackPixelCoord[-1][0]
    minWidth, maxWidth = blackPixelCoord[0][1], blackPixelCoord[-1][1]
    im.show()
    im = im.crop((minHeight, minWidth, maxHeight, maxWidth+5))
    im.show()
    for co in blackPixelCoord:
        if minWidth > co[1]:
            minWidth = co[1]
        if maxWidth < co[1]:
            maxWidth = co[1]

    letterHeight = maxHeight - minHeight + 10
    letterWidth = maxWidth - minWidth + 10
    print(f"LetterWidth = {letterWidth}")
    print(f"LetterHeight = {letterHeight}")
    letterHeight = 20
    letterWidth = 20
    newIm = Image.new("RGB", (letterWidth, letterHeight), color="white")
    ctx = ImageDraw.Draw(newIm)
    for coord in blackPixelCoord:
        ctx.rectangle([(coord[0] - minHeight, coord[1] - minWidth), (coord[0] - minHeight, coord[1] - minWidth)], fill="black")
        
    #newIm.show()
    return newIm

def getCaseScore(im):
    divideBy = 4
    dividedCases = []
    nbCases = 0
    mult = 0
    activeRow = 0
    caseScore = {}
    firstCaseScore = 10
    for i in range(divideBy ** 2):
        if ((im.size[0] / divideBy) * mult) == im.size[0]:
            mult = 0
            activeRow += 1
        topLeftCornerCoord = (((im.size[0] / divideBy) * mult), ((im.size[1] / divideBy) * activeRow))
        bottomRightCornerCoord = ((((im.size[0] / divideBy) * mult) + im.size[0] / divideBy), (((im.size[1] / divideBy) * activeRow)  + im.size[1] / divideBy))
        mult += 1
        nbCases += 1
        dividedCases.append([topLeftCornerCoord, bottomRightCornerCoord])
        #caseScore[f"{topLeftCornerCoord} {bottomRightCornerCoord}"] = firstCaseScore * nbCases * caseScoreMultiplicator
        caseScore[topLeftCornerCoord, bottomRightCornerCoord] = firstCaseScore ** nbCases
    
    return caseScore

def getLetterScore(im):
    letterScore = 0
    caseScore = getCaseScore(im)
    blackPixelCoord = getBlackPixelCoord(im)
    
    for coord in blackPixelCoord:
        for key, value in caseScore.items():
            if (coord[0] >= key[0][0] and coord[0] <= key[1][0]) and (coord[1] >= key[0][1] and coord[1] <= key[1][1]):
                letterScore += value
    
    return letterScore
    


blackPixelCoord = getBlackPixelCoord(im, reductor=1)
newIm = createBlackPixelRender(blackPixelCoord, im)
letterScore = getLetterScore(newIm)
print(f"\n[/] Image path = {IMAGEPATH}\n[#] LetterScore = {letterScore}")