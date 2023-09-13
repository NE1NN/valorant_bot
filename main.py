import requests
import bs4
import discord
import os
from keep_alive import keep_alive

client = discord.Client()

#gets the player stats
def player_stats(user_id):
  #searches the player stats
  splitted = user_id.split('!stats')[1]      #removes and replaces the space with %20 if there's any
  replaced = splitted.replace(' ', '%20')   
  name, hashtag = replaced.split('#')
  res = requests.get(f'https://tracker.gg/valorant/profile/riot/{name}%23{hashtag}/overview?playlist=competitive&season=all')
  soup = bs4.BeautifulSoup(res.content, 'html.parser')
  
  #gets the image
  img_list = []
  imgs = soup.find_all('img')
  for img in imgs:
    imglink = img.attrs.get('src')
    img_list.append(imglink)

  #gets the specific stats
  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__username')
  username = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__discriminator')
  hashtag = elems[0].text
  
  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.highlighted.highlighted--giants > div.highlighted__content > div > div.valorant-highlighted-content__stats > div:nth-child(2) > span.valorant-highlighted-stat__value')
  rank = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(2) > div > div.numbers > span.value')
  kd = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(3) > div > div.numbers > span.value')
  hs = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(4) > div > div.numbers > span.value')
  win = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(1) > div > div.numbers > span.value')
  damage_round = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.main > div:nth-child(10) > div > div.numbers > span.value')
  most_kills = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.top-agents.area-top-agents > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > span')
  fav_agent = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.title > div > div > span.playtime')
  playtime = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.main > div:nth-child(8) > div > div.numbers > span.value')
  clutch = elems[0].text

  elems = soup.select('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.title > div > div > span.matches')
  matches = elems[0].text

  #stores the stats in a list
  stats = [username, hashtag, rank, kd, win, hs, damage_round, most_kills, fav_agent, img_list[0], playtime, clutch, matches]
  return stats

agent_banner = {
'jett' : 'https://i.pinimg.com/originals/85/5a/08/855a0837a156f5d081698d2b0ee70799.jpg', 
'cypher': 'https://i.pinimg.com/originals/59/81/5b/59815b28683f251af4806821dceb7c9e.jpg',
'omen' : 'https://i.pinimg.com/originals/a5/58/7e/a5587ef0805bcabc92982a31255c120d.jpg',
'sage' : 'https://i.pinimg.com/originals/bb/e9/f3/bbe9f30c8b31948e3282fba93aa43ddd.jpg',
'brimstone' : 'https://i.pinimg.com/originals/d7/13/3f/d7133f5fc52f53f240d568d0d563e5d3.jpg',
'astra' : 'https://images7.alphacoders.com/113/thumb-1920-1134343.png',
'viper' : 'https://i.pinimg.com/originals/46/3f/cb/463fcb7864e67c1e4d1294c6aa7bc9c4.jpg',
'yoru' : 'https://wallpaperaccess.com/full/5784768.jpg',
'phoenix' : 'https://i.pinimg.com/736x/b9/9d/f4/b99df4c32294a24dbbdc9fe5a772b11e.jpg',
'reyna' : 'https://wallpaperaccess.com/full/7471446.jpg',
'sova' : 'https://i.pinimg.com/originals/3f/84/8e/3f848e7b4f9ac44c53ff21be41048e92.jpg',
'killjoy' : 'https://i.pinimg.com/originals/45/3c/d6/453cd69032714a79e59d76c860fe588a.jpg',
'breach' : 'https://i.pinimg.com/originals/85/5a/59/855a59a97913db5dcd67d06835c5b9ab.jpg',
'raze' : 'https://i.pinimg.com/originals/ff/55/12/ff5512f837d2e75be004986e3e5cd924.jpg',
'skye' : 'https://i.pinimg.com/originals/99/11/5f/99115fdab7cf2d16bfc780a2e09896b6.jpg',
'kayo' : 'https://images6.alphacoders.com/115/1152788.png',
'chamber' : 'https://images.alphacoders.com/118/1186637.png'
}

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return

    if message.content.startswith('!p'):
      await message.channel.send('Main woyyy')

    if message.content.startswith('!stats'):
      stats = player_stats(message.content)
      embed = discord.Embed(
        title = f'{stats[0]}{stats[1]}',
        description = f"{stats[-3]} {stats[-1]}",
        colour = discord.Color.blue()
        
      )

      embed.add_field(name='Rank', value=stats[2], inline=False)
      embed.add_field(name='K/D', value=stats[3], inline=True)
      embed.add_field(name='Win%', value=stats[4], inline=True)
      embed.add_field(name='HS%', value=stats[5], inline=True)
      embed.add_field(name='DMG/Round', value=stats[6], inline=True)
      embed.add_field(name='Most Kills', value=stats[7], inline=True)
      embed.add_field(name='Clutches', value=stats[-2], inline=True)
      embed.add_field(name='Fav Agent', value=stats[8], inline=False)
      embed.set_thumbnail(url=stats[9])
      embed.set_image(url=agent_banner[stats[8].lower()])
      embed.set_footer(text='made by Nein#4083 | stats taken from https://tracker.gg/valorant')
      await message.channel.send(embed=embed)
    
  except:
    await message.channel.send('Cannot find the user id, you need to sign in with your Riot ID to https://tracker.gg/valorant')
      
keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

