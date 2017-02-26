from PIL import Image
from io import BytesIO
from app import tabletop_entity, config
import json, glob, os, requests, base64

class TableTopGenerator:

    @staticmethod
    def getWeissImages(cards):
        baseurl = 'http://ws-tcg.com/en/cardlist/cardimages/'
        for card in cards:
            isGif = False
            isPng = False
            baseImageName = card.number.replace('/EN', 'EN').replace('/', '_')
            imagenamelwr = baseImageName.lower()
            imagenameupr = imagenamelwr.upper()
            if imagenamelwr[-1] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
                imagenameupr = imagenameupr[:-1] + imagenamelwr[-1]
            imagenames = [baseImageName, 'ws_' + baseImageName, 'WS_' + baseImageName,
                          imagenamelwr, 'ws_' + imagenamelwr, imagenameupr, 'WS_' + imagenameupr,
                          imagenamelwr + '_td', 'ws_' + imagenamelwr + '_td', imagenameupr + '_TD', 'WS_' + imagenameupr + '_TD',
                          imagenamelwr + 'td', 'ws_' + imagenamelwr + 'td', imagenameupr + 'TD', 'WS_' + imagenameupr + 'TD',
                          imagenamelwr + 'u', 'ws_' + imagenamelwr + 'u', imagenameupr + 'U', 'WS_' + imagenameupr + 'U',
                          imagenamelwr + 'r', 'ws_' + imagenamelwr + 'r', imagenameupr + 'R', 'WS_' + imagenameupr + 'R',
                          imagenamelwr + 'cc', 'ws_' + imagenamelwr + 'cc', imagenameupr + 'CC', 'WS_' + imagenameupr + 'CC',
                          imagenamelwr + 'c', 'ws_' + imagenamelwr + 'c', imagenameupr + 'C', 'WS_' + imagenameupr + 'C',
                          imagenamelwr + 'cr', 'ws_' + imagenamelwr + 'cr', imagenameupr + 'CR', 'WS_' + imagenameupr + 'CR',
                          imagenamelwr + 'rr', 'ws_' + imagenamelwr + 'rr', imagenameupr + 'RR', 'WS_' + imagenameupr + 'RR',
                          imagenamelwr + 'rrplus', 'ws_' + imagenamelwr + 'rrplus', imagenameupr + 'RRPlus', 'WS_' + imagenameupr + 'RRPlus',
                          imagenamelwr + 'rrr', 'ws_' + imagenamelwr + 'rrr', imagenameupr + 'RRR', 'WS_' + imagenameupr + 'RRR',
                          imagenamelwr + 'pr', 'ws_' + imagenamelwr + 'pr', imagenameupr + 'PR', 'WS_' + imagenameupr + 'PR']
            otherNames = [x.replace('-', '_') for x in imagenames]
            imagenames += otherNames
            imagenames = [baseurl + x for x in imagenames]

            imgResponse = requests.get(baseurl + imagenamelwr + '.jpg')

            #PNG
            for imagename in imagenames:
                if imgResponse.status_code != 404:
                    break
                imgResponse = requests.get(imagename + '.png')
                isPng = True
                isGif = False

            # JPEG
            for imagename in imagenames:
                if imgResponse.status_code != 404:
                    break
                imgResponse = requests.get(imagename + '.jpg')
                isPng = False
                isGif = False

            #GIF
            for imagename in imagenames:
                if imgResponse.status_code != 404:
                    break
                imgResponse = requests.get(imagename + '.gif')
                isGif = True
                isPng = False

            if imgResponse.status_code != 404:
                img = Image.open(BytesIO(imgResponse.content))
                imgSaveName = 'app/images/' + imagenamelwr + '.jpg'
                if isGif:
                    bg = Image.new("RGB", img.size, (255,255,255))
                    bg.paste(img, (0, 0))
                    bg.save(imgSaveName, 'JPEG')
                elif isPng:
                    bg = Image.new('RGBA',img.size,(255,255,255,255))
                    bg.paste(img, (0, 0))
                    bg.save(imgSaveName, 'JPEG')
                else:
                    img.save(imgSaveName, 'JPEG')
                card.imageurl = imgSaveName
                card.save(card.id)
                print(imgSaveName + ' retrieved')

    @staticmethod
    def generateTableTopJson(name, description, cards, cardBackKey='magic', local=False):
        cardSets = [cards[x:x+69] for x in range(0, len(cards), 69)]
        tableTopObject = tabletop_entity.TableTopObjectState(name, description)

        for cardset in cardSets:
            size = (409, 585)
            images = []
            tableCards = []
            for card in cardset:
                img = None
                if not local:
                    imgResponse = requests.get(card["imageurl"])
                    img = Image.open(BytesIO(imgResponse.content))
                else:
                    img = Image.open(card['imageurl'])
                for i in range(card["count"]):
                    images.append(img.resize(size, Image.ANTIALIAS))
                    tableCards.append(card)

            dimensions = (size[0]*10, size[1]*7)
            #creates a new empty image, RGB mode, and size 4096 by 4096.
            newImg = Image.new('RGB', dimensions)

            cur = 0
            for i in range(0,dimensions[1],size[1]):
                if(cur >= len(images)):
                    break
                for j in range(0,dimensions[0],size[0]):
                    if (cur >= len(images)):
                        break
                    #paste the image at location j,i:
                    newImg.paste(images[cur], (j,i))
                    cur += 1

            #newImg.save("grid"+str(curIndex+1)+".jpg", "JPEG")
            temp = BytesIO()
            newImg.save(temp, 'JPEG')
            temp.seek(0)

            b64image = base64.b64encode(temp.read())

            # data to send with the POST request
            payload = {
                'image': b64image,
                'title': 'apiTest'
            }
            imgUrl = requests.post(
                "https://api.imgur.com/3/image",
                headers={
                    'Authorization': 'Client-ID ' + config.IMGUR_CLIENT_ID
                },
                data=payload
            )
            response = imgUrl.json()
            if not response['success']:
                raise Exception("Image upload failed")
            tableTopObject.addDeck(response['data']['link'], tableCards, cardBackKey)
        return tabletop_entity.TableTopSave([tableTopObject]).getJson()
