import random

from functools import reduce

DICE = {
    'G': {
        'NAME': 'Ability',
        'SIDES': {
            'BLANK': 'gblank',
            'A':     'ga',
            'A1':    'ga',
            'AA':    'gaa',
            'S':     'gs',
            'S1':    'gs',
            'SA':    'gsa',
            'SS':    'gss'
        }
    },
    'B': {
        'SIDES': {
            'BLANK':  'bblank',
            'BLANK2': 'bblank',
            'A':      'ba',
            'AA':     'baa',
            'S':      'bs',
            'SA':     'bsa'
        }
    },
    'R': {
        'SIDES': {
            'BLANK':   'rblank',
            'F':       'rf',
            'F2':      'rf',
            'FF':      'rff',
            'FF2':     'rff',
            'FT':      'rft',
            'FT2':     'rft',
            'T':       'rt',
            'T2':      'rt',
            'TT':      'rtt',
            'TT2':     'rtt',
            'DESPAIR': 'rdespair'
        }
    },
    'P': {
        'SIDES': {
            'BLANK': 'pblank',
            'F':     'pf',
            'FF':    'pff',
            'FT':    'pft',
            'T':     'pt',
            'T2':    'pt',
            'T3':    'pt',
            'TT':    'ptt'
        }
    },
    'W': {
        'SIDES': {
            'D':   'wd',
            'D2':  'wd',
            'D3':  'wd',
            'D4':  'wd',
            'D5':  'wd',
            'D6':  'wd',
            'DD':  'wdd',
            'L':   'wl',
            'L2':  'wl',
            'LL':  'wll',
            'LL2': 'wll',
            'LL3': 'wll'
        }
    },
    'Y': {
        'SIDES': {
            'BLANK':   'yblank',
            'S':       'ys',
            'S2':      'ys',
            'SA':      'ysa',
            'SA2':     'ysa',
            'SA3':     'ysa',
            'SS':      'yss',
            'SS2':     'yss',
            'A':       'ya',
            'AA':      'yaa',
            'AA2':     'yaa',
            'TRIUMPH': 'ytriumph'
        }
    },
    'K': {
        'SIDES': {
            'BLANK':  'kblank',
            'BLANK2': 'kblank',
            'F':      'kf',
            'F2':     'kf',
            'T':      'kt',
            'T2':     'kt'
        }
    },
}

animatedDiceMap = {
  'g': 'green',
  'y': 'yellow',
  'b': 'blue',
  'w': 'white',
  'p': 'purple',
  'r': 'red',
  'k': 'black'
}

summaryMap = {
  's': 'success',
  'a': 'advantage',
  'f': 'failure',
  't': 'threat',
  'despair': 'despair',
  'triumph': 'triumph',
  'l': 'lightpip',
  'd': 'darkpip'
}

roleMap = {
  'turtletech8': 946566378268282962,
  'hotshot798': 946569442727436339,
  'rainydamascus': 1063222057543942255,
  'mightysnez': 946568237368377406,
  "mad_snowboarder": 946569720059011082,
  't3mpe5t_1140': 967220857854361650,
  'scooterboy33': 987112842576658432,
  'theblainster': 990040246739681341,
  '.crusader1776': 967220857854361650
}

emojiMap = {}

def initializeEmojiMap(emojiList1, emojiList2):
    for emoji in emojiList1:
        emojiMap[emoji.name] = emoji.id
    
    for emoji in emojiList2:
        emojiMap[emoji.name] = emoji.id


def rollDie(dieSpec):
    obj_keys = list(dieSpec.keys())
    return dieSpec[obj_keys[random.randint(1, len(obj_keys))-1]]

def printSummary(summary):
  out = []
  for m in summary:
    if summary[m] > 0:
      out.append('(' + str(summary[m]) + ' ' + summaryMap[m] + ')')

  return out


def createEmojiString(tempResult):
  emojiString = []
  for temp in tempResult:
    item = temp.split('(')[1].split(')')[0]
    if len(item.split(' ')) > 1:
      count = item.split(' ')[0]
      em = item.split(' ')[1]
      emojiString.append(f'{count} <:{em}:{emojiMap[em]}>')
    else:
      emojiString.append(f'<:{item}:{emojiMap[item]}>')
    
  return emojiString

def createAniEmojiString(tempResult):
  emojiString = []
  for item in tempResult:
    emojiString.append(f'<a:{item}:{emojiMap[item]}>')
                     
  return emojiString

def filterSummary(summary):
  result = 0
  # Take the difference and only keep the one that had more
  result = summary['s'] - summary['f']
  if result > 0:
    summary['s'] = result
    summary['f'] = 0
  elif result < 0:
    summary['f'] = -result
    summary['s'] = 0
  else:
    summary['f'] = 0
    summary['s'] = 0
  
  result = summary['a'] - summary['t']
  if result > 0:
    summary['a'] = result
    summary['t'] = 0
  elif result < 0:
    summary['t'] = -result
    summary['a'] = 0
  else:
    summary['t'] = 0
    summary['a'] = 0

  return summary

async def roll(message, noText, rollCommand=None):
  rolls = rollCommand.split(' ')[1:] if rollCommand != None else message.content.split(' ')[1:]
  result = []
  summary = {
    's': 0,
    'a': 0,
    'triumph': 0,
    'l': 0,
    'f': 0,
    't': 0,
    'despair': 0,
    'd': 0
  }
  animated = []
  
  for item in rolls:
    repeat = int(item[0:1])
    die = item[1:2]
    
    for x in range(repeat):
      animated.append(animatedDiceMap[die])
      lot = rollDie(DICE[die.upper()]['SIDES'])
      result.append('(' + lot +')')
      # Multiple Success/Failure/Advantage/Threat
      if len(lot) == 3:
        # Same results
        if lot[1]==lot[2]:
          summary[lot[1]] += 2
        # Different results
        else:
          summary[lot[1]] += 1
          summary[lot[2]] += 1
      else:
        # Singular Success/Failure/Advantage/Threat
        if len(lot) == 2:
          summary[lot[1]] += 1
        # Triumph/Despair
        elif lot[1:] != 'blank':
          summary[lot[1:]] += 1
          # Also add to the appropriate success or failure
          summary['s' if lot[1:] == 'triumph' else 'f'] += 1
  
  
  # Filter the summary info
  summary = filterSummary(summary)
  
  aniEmojis = createAniEmojiString(animated)
  
  #context.params.name
  animatedMessage = await message.channel.send(content=' '.join(aniEmojis), reference=message)

  summaryMessage = printSummary(summary)
  
  
  summaryEmojis = createEmojiString(summaryMessage)
  emojiString = createEmojiString(result)
  
  
  me = message.author
  
  # Final Emoji Result
  await animatedMessage.edit(content=f"<:{me.nick.split(' ')[0].split('-')[0]}:{emojiMap[me.nick.split(' ')[0].split('-')[0]]}>" + ' '.join(emojiString))#[result.join(' '), summaryMessage.join(' ')].join('\n'),#result.join(' '),)

  # Final Summary Result
  if noText != 'Y':
    await message.channel.send(content=' '.join([f"<:{me.nick.split(' ')[0].split('-')[0]}:{emojiMap[me.nick.split(' ')[0].split('-')[0]]}> <@&{roleMap[me.name]}> ", ' '.join(summaryEmojis)]), reference=message)#result.join(' '),, reference=message.id)
  
  return ' '.join(summaryEmojis)

def createPolyResponse(arg):
  iter = int(arg[0:1])
  size = int(arg[2:])
  results = []
  resultsStr = []
  
  for i in range(iter):
    temp = random.randint(1, size)
    resultsStr.append(str(temp))
    results.append(temp)
  
  return '`' + arg + '` (' + ' + '.join(resultsStr) + ') = ' + str(reduce((lambda x, y: x + y), results)) + '.'

async def poly(message):
  dieList = []
  args = message.content.split(' ')[1:]
  
  for item in args:
    dieList.append(createPolyResponse(item))
  
  await message.channel.send(content='Rolled: ' + '  '.join(dieList), reference=message)