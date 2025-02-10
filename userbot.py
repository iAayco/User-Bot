#cute code
#cute imports
from datetime import datetime
from telethon import TelegramClient, events
from googletrans import Translator
import requests
#cute vars
now = datetime.now()
#replace the api id and api hash with yours sweetie
client = TelegramClient('aayco', api_id=1234, api_hash='7847ff302281cf49e398be0033b43c8c').start(phone='+201111111111')

#i will not explain this function as long it's so clear
@client.on(events.NewMessage(pattern='/test'))
async def ping_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
       return
    else:
       await event.reply(f"i'm still working bro...")
       
#this function will be to get your info
#the pattern when you send /me to any chat this function will work
@client.on(events.NewMessage(pattern='/me'))
async def me(event):
    #getting your info from client session
    me = await client.get_me()
    #check if you are who sent this command to make sure that only you will be who can use it
    if event.sender_id != me.id:
        #if not you then don't continue
        return
    #if you then start getting the info
    #your id
    me_id = me.id
    #your account first name
    first_name = me.first_name
    #your account username
    username = me.username if me.username else None
    #your account status (premium or not)
    premium = 'Premium User' if me.premium else 'Normal User'
    #the caption that contained all this info
    caption = (f'ID: {me_id}\nName: {first_name}\nUsername: {username}\nStatus: {premium}\nDate Now: {now}')
    #reply on your message with this caption
    await event.reply(caption)
    
#this function will be to get user info from message
#the pattern when you reply on message with /info in any chat this function will work
@client.on(events.NewMessage(pattern='/info'))
async def sender(event):
    #getting your info from client session
    me = await client.get_me()
    #check if you are who sent this command to make sure that only you will be who can use it
    if event.sender_id != me.id:
        #if not you then don't continue
        return
    #if you then start getting the info
    #getting message that you reolied on
    info = await event.get_reply_message()
    #gettin the message sender info
    sender = await info.get_sender()
    #sender id
    sender_id = sender.id
    #sender account first name
    first_name = sender.first_name
    #sender account username
    username = sender.username if sender.username else None
    #sender account status (premium or not)
    premium = 'Premium User' if sender.premium else 'Normal User'
    #the caption that contained all this info
    caption = (f'ID: {sender_id}\nName: {first_name}\nUsername: {username}\nStatus: {premium}\nDate Now: {now}')
    #reply on your message with this caption
    await event.reply(caption)
 
#this function will be to translate chat message
#the pattern when you reply on message with /translate + language in any chat this function will work    
@client.on(events.NewMessage(pattern='/translate (.+)'))
async def translate(event):
    #getting your info from client session
    me = await client.get_me()
    #check if you are who sent this command to make sure that only you will be who can use it
    if event.sender_id != me.id:
        #if not you then don't continue
        return
    #if you then start translating the message
    #getting the languge from user message (en: Engilsh, ar: Arabic, etc)
    language = event.pattern_match.group(1)
    #getting the message text
    message = event.message.message
    if message:
        #message found
        try:
            #Get Original Message Language
            detected_language = translator.detect(message).lang
            if detected_language:
                #Translate User Message From Original Language To User Input Language
                translated_text = translator.translate(message, src=detected_language, dest=language.lower())
                #Reply With Translated Message And Translate Info
                await event.reply(f'translated from {detected_language} to {language}\n{translated_text.text}')
        except Exception as e:
            #Reply With Error If Happend
            await event.reply(str(e))
 
#this function will be to get coin price in usdt from binance
#the pattern when you reply on message with /prc + coin in any chat this function will work              
@client.on(events.NewMessage(pattern='/prc (.+)'))
async def price(event):
    #getting your info from client session
    me = await client.get_me()
    #check if you are who sent this command to make sure that only you will be who can use it
    if event.sender_id != me.id:
        #if not you then don't continue
        return
    #get the coin name from user input message
    coin = event.pattern_match.group(1).upper()
    #send the request with coin name to binance api to get price in usdt
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin+'USDT'}"
    #send the request using requests
    response = requests.get(url)
    #if request sent successfully
    if response.status_code == 200:
        #convert response to json
        data = response.json()
        #the message that contain coin name and thier price in usdt
        text = f"price of {coin.upper()} is {data['price']}USDT"
        #reply with the message
        await event.reply(text)
    #if coin not on binance (not 200)
    else:
        #reply with this error message and status code
        await event.reply(f"Error : {response.status_code} This Coin Not In Binance")
    

with client:
    #Make Sure To Keep UserBot Running If Not Disconnected   
    client.run_until_disconnected()   
