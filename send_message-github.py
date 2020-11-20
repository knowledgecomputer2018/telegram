#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time
import asyncio
import nest_asyncio
nest_asyncio.apply()

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
SLEEP_TIME = 3

#import logging
#logging.basicConfig(level=logging.DEBUG)
class send_message_telegram():
    def __init__(self):
      self.sign_in_clients=[]
      self.num_lines_empty=0
      #........
      self.input_file="users3.csv"
      self.phone_file="phones.csv"
      #.........................

      self.Read_1000Phones=self.Read_idhash_phones(self.phone_file)
      print("Read phones.")
      print("len:{}".format(len(Read_1000Phones)))
      self.Read_send_user_phones=self.Read_send_user_phones(self.input_file)
      print("Read users.")
      print("len:{}".format(len(self.Read_send_user_phones)))
      #-------------
      try:
        loop=asyncio.get_event_loop()
        self.sign_in_clients=loop.run_until_complete(self.sign_in_PhoneNmbers(Read_1000Phones))
      except  Exception as e:
        pass
      finally:
        loop.stop()
      #..............
    def banner(self):
        message="ارسال پيام انبوه در تلگرام \ntele_id : ma_kh_kar\nphone: 09193577316"
    async def get_status_user(self,client,entity):
        return await client.get_entity(entity)
    async def create_client(self,phone, api_id, api_hash):
        """
        A coroutine to connect telegram.
        """
        client = TelegramClient(phone, api_id, api_hash)
      
        await client.connect()
        print(phone, api_id, api_hash)
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            os.system('clear')
            main.banner()
            await client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        print("test connect client.")
        test=asyncio.ensure_future(self.get_status_user(client,"98"+phone))
        #print(test)
        return client

    async def sign_in_PhoneNmbers(self,accounts):
        """
         Creates a group of coroutines and waits for them to finish
        """
        #sign_in_clients=[]
        #.........................
        corotunies=asyncio.as_completed([asyncio.create_task(self.create_client("98"+acc['phone'],int(acc['id']),acc['hash'])) for acc in accounts ])
        
        for f in corotunies:
          #print("98"+acc['phone'])
          #line1=phone=acc[0],api_id1=acc[1],api_hash1=acc[2]
          #client=await create_client("98"+acc[0],acc[1],acc[2])
          client=await f
          #....
          #write in csv file client 
          #....
          #if not client.is_user_authorized():
          #   client.send_code_request(acc[0])
            #  client.sign_in(acc[0], input('Enter the code: '))
          print()
          self.sign_in_clients.append(
              {
                #'phone':acc['phone'],
                'Full':False,
                'login':client
              }
              )

        return self.sign_in_clients

    #-----------------------------------------
    def Read_Phones(self,phone_file):#not work i do not know why
        lines=[]
        try:
            cpass = configparser.RawConfigParser()
            cpass.read(phone_file)
            #-------
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
            #-------
            lines.append([phone,api_id,api_hash])
                    
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)
        return lines
    def Read_idhash_phones(self,input_file):
        os.system('clear')
        main.banner()
        #input_file = sys.argv[1]
        phones = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:                
                phone = {}
                if (row[0]):
                    phone['id'] =int (row[0])
                else:
                    phone['id'] = ''
                if (row[1]):
                    phone['hash'] = (row[1])
                else:
                    phone['hash'] = ''
                if (row[2]):
                    phone['phone'] = (row[2])
                else:
                    phone['phone'] = ''
                phones.append(phone)
        return phones
            
    #------------------------------------------
    def Read_send_user_phones(self,input_file):
         
        
        os.system('clear')
        main.banner()
        #input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                
                user = {}
                if (row[0]):
                    user['username'] = row[0]
                else:
                    user['username'] = ''
                if (row[2]):
                    user['id'] = (row[2])
                else:
                    user['id'] = ''
                if (row[3]):
                    user['access_hash'] = (row[3])
                else:
                    user['access_hash'] = ''
                users.append(user)
        return users
                
    #------------------------------------------
    async def send_sms(self,client,users):
        print(gr+"[1] send sms by user ID\n[2] send sms by username ")
        mode = int(input(gr+"Input : "+re))
         
        message = input(gr+"[+] Enter Your Message : "+re)
 #       Num_Send_Message=0
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
                
            #------------------------------------------
                
            try:
               
                print(gr+"[+] Sending Message to:", user['username'])
                print("access_has:{}".format(user['access_hash']))

                #await client.send_message(receiver, message.format(user['username']))
                send_msg=aysncio.create_task(client.send_message(receiver,message.format(user['username'])))

                print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Trying to continue...")
                continue
            
        client.disconnect()
        print("Done. Message sent to all users.")
main=send_message_telegram()
#-------------
print(main.sign_in_clients)
print("sign in phones")
#------------- declare vars  -------------
print("start app.")
while(1):#always app is running

    #------------- change config  -------------
        #------------- add phone -------------
    add_phone = (input("Do you have add phone.Y/N\n"))
    if(add_phone=='Y'):
        mode = int(input("one phone (1)/ csv file phone(2\n)"))
        if(mode==1):
            new_client=main.create_client()
            signs_in.append(new_client)
        else:
            new_file = (input("please insert path of file)\n"))
            new_signs_in=main.sign_in_PhoneNmbers(new_file)
            for new_phone in new_signs_in:
                signs_in.append(new_phone)
    else:
        print("you enter No .")
    check_phone = (input("Do you have check phones.Y/N\n"))
        #------------- add sent users message -------------
    add_send_users = (input("Do you have add send user(csv file).Y/N\n"))
    if(add_send_users =='Y'):
        new_file = (input("please insert path of file)"))
        Read_send_user_phones=main.Read_send_user_phones(new_file)
        file_mode = int(input("do you have concate with previous file user_sent (1)/ this is a new file.(2)\n"))
        if(file_mode==1):
            print("start concate with previous files.\n sent message random.\n")
        else:
            print("send message to new your upload file.")
        
    num_lines_all=len(main.sign_in_clients)
    print("Num num_lines_all:{}".format(num_lines_all))
    #------------- sent message -------------
    mode = (input("Do you have send messsage.Y/N\n"))
    Num_Send_Message=30
    for line in range(len(main.sign_in_clients)):
      if(main.sign_in_clients[line]['Full']==False):
            main.num_lines_empty+=1
    num_message=30
    line=0
    #------------- calculate  -------------
    print("num_lines_empty:{}".format(main.num_lines_empty))
    print("valid Num send message:\n")
    Num_valid_send_message=main.num_lines_empty*Num_Send_Message
    print("today {} ".format(Num_valid_send_message))
      #-----------  -------------
    #Num_sent_messages=1000,num_lines=30,num_message=30,Num_valid_send_messags=900
    #24h=1*30*3=90*30=2700s/3600=1h
    #24=200*1000=200000*30=6m
    #-------------  -------------
    Num_sent_messages_to_users_for_customer = int(input("how many want send messsage to users(30,60,90.....900,990,...?\n"))
    #if(Num_valid_send_message<Num_sent_messages):
    #print("can not send message.valid send message is {}".format(Num_valid_send_message))
    #-------------  -------------
    Num_pop_user=0
    print("start send messag while...")
    
    while(mode=='Y'):
        #------------- client -------------
        client=main.sign_in_clients[line]['login']
        print(client)
        #------------- send message line -------------

        #start async func
        try:
        loop=asyncio.get_event_loop()
        loop.loop.run_until_complete(
        main.send_sms(client,Read_send_user_phones[Num_pop_user:Num_Send_Message]
        ))#0-30,30-60,60-90) )
        except  Exception as e:
          pass
        finally:
          loop.stop()
        
        
        #time.sleep(SLEEP_TIME)
        #------------- 30 later users -------------
        if(Num_Send_Message == Num_sent_messages_to_users_for_customer):#stop send message
            main.sign_in_clients[line]['Full']=True
            print("Num_send_message==Num_sent_messages_to_users_for_customer={}\n".format(Num_Send_Message))
            break
        elif(len(Read_send_user_phones)>Num_Send_Message):#sent user exsit or no
            main.sign_in_clients[line]['Full']=True
            Num_pop_user=Num_Send_Message
            Num_Send_Message+=30
            
            print("Num_send_message {}\n".format(Num_Send_Message))
        else:#users is end.
            break
            print("num sent users message is empty.\n")
        #------------- change line -------------
        #while(main.sign_in_clients[line]['Full']):
        #print("line {} is full.".format(main.sign_in_clients[line]['phone']))
        line+=1
        time.sleep(SLEEP_TIME)
        #.........UPDATE VARS
        #Num_valid_send_message-=Num_Send_Message
        
