from PIL import Image
from io import BytesIO
from app import tabletop_entity, config
import json, glob, os, requests, base64

class TableTopGenerator:

    @staticmethod
    def generateTableTopJson(name, description, cards):
        cardSets = [cards[x:x+69] for x in range(0, len(cards), 69)]
        tableTopObject = tabletop_entity.TableTopObjectState(name, description)

        for cardset in cardSets:
            size = (409, 585)
            images = []
            tableCards = []
            for card in cardset:
                imgResponse = requests.get(card["imageurl"])
                img = Image.open(BytesIO(imgResponse.content))
                for i in range(card["count"]):
                    images.append(img.resize(size, Image.ANTIALIAS))
                    tableCards.append(card["name"])

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
            tableTopObject.addDeck(response['data']['link'], tableCards)
        return tabletop_entity.TableTopSave([tableTopObject]).getJson()
