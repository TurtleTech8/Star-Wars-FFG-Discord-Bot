import roll

destinyPoints = {
  'destinyLight': 0,
  'destinyDark': 0
}


def saveDestinyPoints(arg):
  value = int(arg.split(' ')[0])
  if 'lightpip' in arg:
    destinyPoints['destinyLight'] += value
  else:
    destinyPoints['destinyDark'] += value


def getDestinyPoints():
  light = destinyPoints['destinyLight']
  dark = destinyPoints['destinyDark']
  
  command = []
  if light != 0:
    for i in range(light):
      command.append('(lightside)')

  if dark != 0:
    for i in range(dark):
      command.append('(darkside)')

  return roll.createEmojiString(command)


def resetDestinyPoints():
  destinyPoints['destinyLight'] = 0
  destinyPoints['destinyDark'] = 0


async def printDestinyPoints(message):
  await message.channel.send(content='Destiny Points:')
  
  destiny = getDestinyPoints()

  if(len(destiny) != 0):
    await message.channel.send(content=' '.join(destiny))

def flipDestinyPoint(arg):
  other = 'destinyDark' if arg == 'destinyLight' else 'destinyLight'
  
  if destinyPoints[arg] == 0:
    return
  
  destinyPoints[arg] -= 1
  
  destinyPoints[other] += 1

async def parseDestiny(message):
  
  if len(message.content.split(' ')) > 1:
    command = message.content.split(' ')[1]
    if command.lower() == 'roll':
      rollResults = await roll.roll(message, 'Y', '$roll 1w')
      
      saveDestinyPoints(rollResults)
      
      await message.channel.send(content='Destiny roll results: ' + rollResults, reference=message)
    elif command.lower() == 'l':
      flipDestinyPoint('destinyLight')
    elif command.lower() == 'd':
      flipDestinyPoint('destinyDark')
    elif command.lower() == 'reset':
      resetDestinyPoints()
    elif command.lower() == 'set':
      destinyPoints['destinyLight'] = int(message.content.split(' ')[2])
      destinyPoints['destinyDark'] = int(message.content.split(' ')[3])
  
  await printDestinyPoints(message)
