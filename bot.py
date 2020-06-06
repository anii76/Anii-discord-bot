import discord
import datetime
import random
import requests as req
from bs4 import BeautifulSoup as bs
import re

class Bot(discord.Client):
 
  def _init_(self):
    super()._init_()
   
  def random_color(self):
    hexa = "0123456789abcd"
    random_hex = "0x"
    for i in range(6):
      random_hex += random.choice(hexa)
    return discord.Colour(int(random_hex,16))

  def create_embed(self,title,desc,colour,image=""):
    embed = discord.Embed()
    embed.title = title
    embed.description = desc
    embed.colour = colour
    if (image !=""):
      embed.set_image(url=image)
    return embed
	
  async def on_ready(self):
    print("Logged in a")
    print(self.user.name)
    print(self.user.id)
    print("........")

  async def on_member_join(self, member):
    embed = discord.Embed(colour=0x95efcc, description=f"Welcome to my discord server! You are the {len(list(member.guild.members))}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.timestamp = datetime.datetime.utcnow()

    #channel = discord.utils.get(server.channels, name="bot_commands", type="ChannelType.text")
    channel = bot.get_channel(id=YourChannelIDHere)
    await channel.send(embed=embed)

  async def on_message(self, message):
   
    if (message.author == self.user):
      return
    
    if (message.content.startswith("ping")):
      await message.channel.send("pong 🙄")
     
    if (message.content.startswith("pong")):
      await message.channel.send("ping 😴")

    if (message.content.startswith("!corona")):
      await message.channel.send("https://ncov2019.live/")

    if (message.content.startswith("!greet")):
      embed = discord.Embed(colour=0xffa500, title="Hello "+message.content.split(' ')[1]+" 👋")
      await message.channel.send(embed = embed)

    if (message.content.startswith("!book")):
      
      try:
         s = ' '.join(message.content.split(' ')[1:])
         doc = req.get("https://www.goodreads.com/search?q=" + s.replace(' ','+') + "&search%5Bsource%5D=goodreads&search_type=books&tab=books")
         soup = bs(doc.text, features="html.parser")
         dd = soup.find_all("div",{"class":"mainContent"})[0].find_all("table",{"cellspacing":"0"})[0].find_all("tr")[0].find_all("a",{"class":"bookTitle"})[0]
         link = ''.join(re.findall('href="(.+)" i',str(dd)))
         print("https://www.goodreads.com"+link)
         doc = req.get("https://www.goodreads.com"+link)
         soup = bs(doc.text, features="html.parser")
         dd = soup.find_all("div",{"class":"mainContent"})[0].find_all("div",{"id":"topcol"})[0]
      except:
         print('cannot find input')
         embed = discord.Embed(colour=0xff0000, description="Error: cannot find book")
         await message.channel.send(embed = embed)
         return
      
      try:
         title = dd.find_all("div",{"class":"last col"})[0].find_all("h1",{"id":"bookTitle"})[0].text.replace('\n','')
         print("Title :"+title)
      except:
         title = ' '.join(message.content.split(' ')[1:])
         print('cannot find title')

      try:
         cover = dd.find_all("a")[0].find_all("img",{"id":"coverImage"})[0]
         coverUrl = ''.join(re.findall('src="(.+)"',str(cover)))
         print("coverUrl :"+coverUrl)
      except:
         coverUrl = ''
         print('cannot find coverUrl')
     
      try:
         serie = dd.find_all("div",{"class":"last col"})[0].find_all("h2")[0].find_all("a")[0].text.replace('\n','')
         print("Book Series :"+serie)
      except:
         serie = 'N\A'
         print('cannot find serie')

      try:
         desc = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"description"})[0].find_all("span")[0].text
         print("Book Description :"+desc)
      except:
         desc = 'N\A'
         print('cannot find desc')

      try:
         author = dd.find_all("div",{"class":"last col"})[0].find_all("a",{"class":"authorName"})[0].find_all("span",{"itemprop":"name"})[0].text
         print("Book Author :"+author)
      except:
         author = 'N\A'
         print('cannot find author')

      try:
         rating = dd.find_all("div",{"class":"last col"})[0].find_all("span",{"itemprop":"ratingValue"})[0].text.replace('\n','')
         print("Rating :"+rating)
      except:
         rating = 'N\A'
         print('cannot find rating')


      try:
         num = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("span",{"itemprop":"numberOfPages"})[0].text
         print("Number of Pages :"+num)
      except:
         num = 'N\A'
         print('cannot find num')


      try:
         pub = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("div",{"class":"row"})[1].text.replace('\n','')
         print("Publication :"+pub)
      except:
         pub = 'N\A'
         print('cannot find pub')
    
      try:
         b = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("div",{"class":"buttons"})[0].find_all("div",{"class":"infoBoxRowTitle"})
         p = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("div",{"class":"buttons"})[0].find_all("div",{"class":"infoBoxRowItem"})
         f =[[b[i].text,p[i].text.replace('\n','')] for i in range(len(b)) if b[i].text !='']
         f = f[:len(f)-1]
         details = ''
         for i in f:
            details +="**"+i[0]+" :** "+i[1]+"\n" 
            print(i[0]+" :"+i[1])
      except:
         details = ''
         print('cannot find details')
      
      
      color = self.random_color()
      description ="**Title :** "+title+"\n"+"**Author :** "+author+"\n"+"**Book Series :** "+serie+"\n"+"**Rating :** "+rating+"\n"+"**Published :** "+pub+"\n"+"**Number Of Pages :** "+num+"\n"+details+"**Book Description :** "+desc+"\n"+"https://www.goodreads.com"+link
      embed = self.create_embed(title,description,color,coverUrl)
      
      await message.channel.send(embed = embed)
            


    if (message.content.startswith("!good night")):
      
      doc = req.get("https://www.luvze.com/good-night-quotes/")
      soup = bs(doc.text, features="html.parser")
      dd = soup.find_all("div",{"class":"content-sidebar-wrap"})[0].find_all("div",{"class":"entry-content"})[0].find_all("p")
      txt = [i.text for i in dd[2:]]
      txt.remove('')
      txt = [re.sub('[0-9]+. ','',i) for i in txt ]
      dd.reverse()
      img = [''.join(re.findall('href="(.+)" rel',str(i))) for i in dd if i.text == '']
      case = random.choice(['text','img'])
      description = image = ''
      if case == 'text' :
        description = random.choice(txt)
      else :
         image = random.choice(img) 

      #member = discord.utils.get(message.guild.members, name=message.author.display_name)
      embed = self.create_embed("Good night "+message.author.display_name+" 👋😴",description,0x800080,image)
      await message.channel.send(embed = embed)

    if (message.content.startswith("!help")):
      embed = discord.Embed(colour=0x6e6fad, title= "Anii Help", description="❕ Type ***!dm*** : So I can send you a private message ! \n❕ Type ***!greet*** : To recieve Anii76's greetings ! \n❕ Type ***!book*** : So I can find your favourite book 📚 !\n❕ Type ***!movie*** : So I can find your favourite movie/serie 🎬 ! \n❕ Type ***!anime*** : So I can find your favourite anime !\n❕ Type ***!corona*** : To display corona news ! \n❕ Type ***!good night*** : To recieve nighty quotes ! \n❕ Type ***!help*** : To display this message ! ☺️ \n")
      await message.channel.send(embed = embed)

    if (message.content.startswith("!dm")):

      name = message.content.split(' ')[1]
      
      if (name == 'all'):
        for member in message.guild.members:
         if member != self.user :
            try:
              embed = discord.Embed(colour=0x95efcc, title="Azul "+str(member)+" 👋")
              await member.send(embed = embed)
            except discord.Forbidden:
              embed = discord.Embed(colour=0xff0000, description="**Error: user "+ name +" dosen't accept private messages**")
              await message.channel.send(embed = embed)
      else:
        member = discord.utils.get(message.guild.members, name=name)
        try:
           embed = discord.Embed(colour=0x95efcc, title="Azul "+name+" 👋")
           await member.send(embed = embed)
        except discord.Forbidden:
           embed = discord.Embed(colour=0xff0000, description="**Error: user "+ name +" dosen't accept private messages**")
           await message.channel.send(embed = embed)
        except AttributeError:
           embed = discord.Embed(colour=0xff0000, description="**Error: member "+name+" not found**")
           await message.channel.send(embed = embed)

    if (message.content.startswith("!movie") or message.content.startswith("!anime")):

      try:
         s = ' '.join(message.content.split(' ')[1:]) #movie name
         doc = req.get("https://www.imdb.com/find?s=tt&q=" + s.replace(' ','+') + "&ref_=nv_sr_sm") 
         soup = bs(doc.text, features= "html.parser")
         dd = soup.find_all("div",{"id":"main"})[0].find_all("table",{"class":"findList"})[0].find_all("td",{"class":"result_text"})[0].find_all("a")[0]
         link = re.findall('".+"',str(dd))[0].replace('"','')
         print("https://www.imdb.com"+link)
         if 'title' in link:
            doc = req.get("https://www.imdb.com"+link)
            soup = bs(doc.text, features="html.parser")
         else:
            embed = discord.Embed(colour=0xff0000, description="**Error: cannot find movie**")
            await message.channel.send(embed = embed)
            return
      except:
         print('cannot find input')
         embed = discord.Embed(colour=0xff0000, description="**Error: cannot find movie**")
         await message.channel.send(embed = embed)
         return

      try:
         title = soup.find_all("div",{"class":"title_block"})[0].find_all("div",{"class":"title_wrapper"})[0].find_all("h1")[0].text.replace('\xa0','')#.replace(' ','')
         print("Title :"+title)
      except:
         title = ' '.join(message.content.split(' ')[1:])
         print('cannot find title')
         #await message.channel.send('Error: cannot find movie')
         #return

      try:
         rating = soup.find_all("div",{"class":"title_block"})[0].find_all("div",{"class":"ratings_wrapper"})[0].find_all("span",{"itemprop":"ratingValue"})[0].text
         rating +="/10"
         print("Rating :"+rating)
      except:
         rating = 'N\A'
         print('cannot find rating')

      try:
         img = soup.find_all("div",{"class":"slate_wrapper"})[0].find_all("div",{"class":"poster"})[0].find_all("img")[0]
         img = ''.join(re.findall('src="(.+)?" t', str(img)))
         print("img : "+img)
      except:
         img = ''
         print('cannot find img')

      try:
         duration = soup.find_all("div",{"class":"title_block"})[0].find_all("div",{"class":"title_wrapper"})[0].find_all("time")[0].text.replace('\n','').replace(' ','')
         print("Duration :"+duration)
      except:
         duration ='N\A'
         print('cannot find duration')
     
      try:
         Geners = soup.find_all("div",{"class":"title_block"})[0].find_all("div",{"class":"title_wrapper"})[0].find_all("a")
         geners = ', '.join([i.text for i in Geners[:len(Geners)-1] ])
         print("Geners :"+geners)
         release = Geners[len(Geners)-1].text.replace('\n','')
         print("Release :"+release)
      except:
         geners = 'N\A'
         print('cannot find geners')
         release = 'N\A'
         print('cannot find release')

      try:
         ep = soup.find_all("div",{"id":"main_top"})[0].find_all("div",{"class":"button_panel navigation_panel"})[0].find_all("span",{"class":"bp_sub_heading"})[0].text
         print("Episode Guide :"+ep)
      except: 
         print('cannot find ep')
         ep ='N\A'
  
      try:
         plot = soup.find_all("div",{"class":"plot_summary"})[0].find_all("div",{"class":"summary_text"})[0].text.replace('\n','')
         print("Plot :"+plot)
      except:
         plot ='N\A'
         print('cannot find plot')
      
      color = self.random_color()
      description ="**Title :** "+title+"\n"+"**Rating :** "+rating+"\n"+"**Duration :** "+duration+"\n"+"**Geners :** "+geners+"\n"+"**Release :** "+release+"\n"+"**Episode Guide :** "+ep+"\n"+"**Plot :** "+plot+"\n"+"https://www.imdb.com"+link
      embed = self.create_embed(title,description,color,img)
      
      await message.channel.send(embed = embed)      



if __name__ == "__main__":
  bot = Bot()
  bot.run("YourTokenHere")
