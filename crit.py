import random
from math import floor
import roll
import re

CRIT = {
    0:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Minor Nick:** The target suffers 1 strain.'},
    1:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Slowed Down:** The target can only act during the last allied Initiative slot on his next turn.'},
    2:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Sudden Jolt:** The target drops whatever is in hand.'},
    3:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Distracted:** The target cannot perform a free maneuver during his next turn.'},
    4:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Off-Balance:** Add <:kblank:> to his next skill check.'},
    5:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Discouraging Wound:** Flip one light side Destiny point to a dark side Destiny Point (reverse if NPC).'},
    6:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Stunned:** The target is staggared until the end of his turn.'},
    7:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Stinger:** Increase difficulty of next check by one.'},
    8:  {'severity': 2, 'severityMessage': 'Average',  'result': '**Bowled over:** The target is knocked prone and suffers 1 strain.'},
    9:  {'severity': 2, 'severityMessage': 'Average',  'result': '**Head Ringer:** The target increases the difficulty of all Intellect and Cunning checks by one until the end of the encounter.'},
    10: {'severity': 2, 'severityMessage': 'Average',  'result': '**Fearsome Wound:** The target increase the difficulty of all Presence and Willpower checks by one until the end of the encounter.'},
    11: {'severity': 2, 'severityMessage': 'Average',  'result': '**Agonizing Wound:** The target increases the difficulty of all Brawn and Agility checks by one until the end of the encounter.'},
    12: {'severity': 2, 'severityMessage': 'Average',  'result': '**Slightly Dazed:** The target is disoriented until the end of the encounter.'},
    13: {'severity': 2, 'severityMessage': 'Average',  'result': '**Scattered Senses:** The target removes all <:bblank:> from skill checks until the end of the encounter.'},
    14: {'severity': 2, 'severityMessage': 'Average',  'result': '**Hamstrung:** The target loses his free maneuver until the end of the encounter.'},
    15: {'severity': 2, 'severityMessage': 'Average',  'result': '**Overpowered:** The target leaves himself open, and the attacker may immediately attempt another free atack against him, using the same pool as the original attack.'},
    16: {'severity': 2, 'severityMessage': 'Average',  'result': '**Winded:** Until the end of the encounter, the target cannot voluntarily suffere strain to activate any abilities or gain additional maneuvers.'},
    17: {'severity': 2, 'severityMessage': 'Average',  'result': '**Compromised:** Increase difficulty of all skill checks by one until the end of the encounter.'},
    18: {'severity': 3, 'severityMessage': 'Hard',     'result': '**At the Brink:** The target suffers 1 strain each time he performs an action.'},
    19: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Crippled:** One of the target\'s limbs (selected by the GM) is crippled until healed or replaced. Increase difficulty of all checks that required use of that limb by one.'},
    20: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Maimed:** One of the target\'s limbs (selected by the GM) is permanently lost. Unless the target has a cybernetic replacement, the target cannot perform actions that would require the use of that limb. All other actions gain <:kblank:>.'},
    21: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Horrific Injury:** Randomly roll 1d10 to determine one of the target\'s characteristics--1-3 for Brawn, 4-6 for Agility, 7 for Intellect, 8 for Cunning, 9 for Presence, 10 for Willpower. Until this Critical Injury is healed, treat that characteristic as one point lower.'},
    22: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Temporarily Lame:** Until this Critical Injury is healed, the target cannot perform more than one manuever during his turn.'},
    23: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Blinded:** The target can no longer see. Upgrade the difficulty of all checks twice. Upgrade the difficulty of Perception and Vigilance checks three times.'},
    24: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Knocked Sensless:** The target is staggared for the remainder of the encounter.'},
    25: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Gruesome Injury:** Randomly roll 1d10 to determine the target\'s characteristics--1-3 for Brawn, 4-6 for Agility, 7 for Intellect, 8 for Cunning, 9 for Presence, 10 for Willpower. That characteristic is permanently reduced by one, to a minimum of one.'},
    26: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Bleeding out:** Every round, the target suffers 1 wound and 1 strain at the beginning of his turn. For every five wounds he suffers beyond his wound threshold, he suffers one additional Critical Injury. Roll on the chart, suffereing injury (if he suffers this result a second time due to this, roll again).'},
    27: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**The End is Nigh:** The target will die after the last Initiative slot during the next round.'},
    28: {'severity': 0, 'severityMessage': '-',        'result': '**Dead:** Complete, obliterated death.'}
}

SHIP_CRIT = {
    0:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Mechanical Stress:** The ship or vehicle suffers one point of system strain.'},
    1:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Jostled:** A small explosion or impact rocks the vehicle. All crew members suffer one strain and are disoriented.'},
    2:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Losing Power to Shields:** Decrease defense in affected defense zone by one until the Critical Hit is repaired. If the ship or vehicle has no defense, suffer one point of system strain.'},
    3:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Knocked Off Course:** A particularly strong blast or impact sends the ship or vehicle careening off in a new direction. On his next turn, the pilot cannot execute any maneuvers and must make a Piloting check to regain control. The difficulty of this check depends on his current speed.'},
    4:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Tailspin:** All firing from the ship or vehicle suffers <:kblank:> <:kblank:> dice until the end of the pilot\'s next turn. All crew members are immobilized until the end of the pilot\'s next turn.'},
    5:  {'severity': 1, 'severityMessage': 'Easy',     'result': '**Component Hit:** One component of the attacker\'s choice is knocked offline, and is rendered inoperable until the end of the following round. For a list of ship components, see Cheat-Sheets chat.'},
    6:  {'severity': 2, 'severityMessage': 'Average',  'result': '**Shields Failing:** Reduce defense in all defense zones by one point until the Critical Hit is repaired. If the ship or vehicle has no defense, suffer two points of system strain.'},
    7:  {'severity': 2, 'severityMessage': 'Average',  'result': '**Navicomputer Failure:** The navicomputer (or in the case of a ship without a navicomputer, its R2 Unit) fails and the ship cannot make the jump to hyperspace until the Critical Hit is repaired. If the ship or vehicle is without a hyperdrive, the vehicle or ship\'s navigation systems fail, leaving it flying or driving blind, unable to tell where it is or where it\'s going.'},
    8:  {'severity': 2, 'severityMessage': 'Average',  'result': '**Power Fluctuations:** The ship or vehicle is beset by random power surges and outages. The pilot cannot voluntarily inflict system strain on the ship (to gain an extra starship maneuver, for example, until this Critical hit is repaired.'},
    9:  {'severity': 3, 'severityMessage': 'Hard',     'result': '**Shields Down:** Decrease defense in affected defense zone to zero, and decrease defense in all other defense zones by one until this Critical Hit is repaired. While the defense of the affected defense zone cannot be restored until the Critical Hit is repaired, defense can be assigned to protect that defense zone from other zones as usual. If the ship or vehicle is without defense, suffer four points of system strain.'},
    10: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Engine Damaged:** The ship or vehicle\'s maximum speed is reduced by one point, to a minimum of one, until the Critical Hit is repaired.'},
    11: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Shield Overload:** The ship\'s shields completely fail. Decrease the defense of all defense zones to zero. This Critical hit cannot be repaired until the end of the encounter, and the ship suffers two points of system strain. If the ship or vehicle is without defense, reduce armor by 1 until the Critical Hit is repaired.'},
    12: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Engines Down:** The ship or vehicle\'s maximum speed is reduced to zero until the Critical Hit is repaired, although it continues on its present course thanks to momentum. In addition, the ship cannot execute any maneuvers until the Critical Hit is repaired.'},
    13: {'severity': 3, 'severityMessage': 'Hard',     'result': '**Major System Failure:** One component of the attacker\'s choice is heavily damaged, and is inoperable until the Critical Hit is repaired. For a list of ship components, see the Cheat-Sheets chat.'},
    14: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Major Hull Breach:** A huge, gaping tear is torn in the ship\'s hull and it depressurizes. For ships and vehicles of silhouette 4 and smaller, the entire ship depressurizes in a number of rounds equal to the ship\'s sillhouette. Ships and vehicles of silhouette 5 and larger tend to be highly compartmentalized and have many safeguards against depressurization. These ships don\'t completely depressurize, but parts do (the specifics of which parts depressurize is up to the GM; however each section fo the ship or vehicles that does lose aird does so in a number of round equal to the vehicle\'s silhouette. Vehicles and ships operating in an atmosphere can better handle this Critical Hit. However, the huge tear still inflicts penalties, causing the vehicle to suffere the Destabilized Critical Hit instead.'},
    15: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Destabilized:** The ship or vehicle\'s structural integrity is seriously damaged. Reduce the ship or vehicle\'s hull trauma threshold and system strain threshold to half their original values until repaired.'},
    16: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Fire!:** Fire rages through the ship. The ship or vehicle immediately takes two points of system strain, and anyone caught in the fire takes damage as discussed on page 214. A fire can be put on with some quick thinking and appropriate skill. Vigilance and/or Coll checks at the GM\'s discretion. Once going, a fire takes one round per two of the ship\'s silhouette points to put out.'},
    17: {'severity': 4, 'severityMessage': 'Daunting', 'result': '**Breaking Up:** The vehicle or ship has suffered so much damage that it begins to come apart at its seams, breaking up and disintegrating around the crew. At the end of the following round, the ship is completely destroyed and the surrounding environment is littered with debris. Anyone aboard the ship or vehicle has one round to get to an escape pod, bail out, or dive for the nearest hatch before they are lost.'},
    18: {'severity': 0, 'severityMessage': '-',        'result': '**Vaporized:** The ship or vehicle is completely destroyed, consumed in a particularly large and dramatic fireball. Nothing survives.'},
}

personCritMap = [1, 6, 11, 16, 21, 26, 31, 26, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101, 106, 111, 116, 121, 126, 131, 141, 151]

shipCritMap = [1, 10, 19, 16, 28, 37, 46, 55, 64, 73, 82, 91, 100, 109, 118, 127, 134, 139, 145, 154];

def findMapping(x, critMap):
  start = 0
  end = len(critMap)-1
  mid = 0
  choice = 0

  # Iterate while start not meets end
  while (start<=end):
    # Find the mid index
    mid=floor((start + end)/2)

    # If element is present at mid, return True
    if critMap[mid]==x:
      return mid
    # Else look in left or right half accordingly
    elif critMap[mid] < x:
      start = mid + 1
      choice = mid
    else:
      choice = mid -1
      end = mid - 1
  
    
  return choice

async def rollCrit(message):
  randRoll = random.randint(1, 100)
  final = randRoll
  message1 = f'Rolled a d100: {str(final)}'
  
  if '+' in message.content:
    final += int(message.content.split('+')[1])
    message1 += f" + {str(int(message.content.split('+')[1]))} for a total of {str(final)}"
  
  elif '-' in message.content:
    final -= int(message.content.split('-')[1])
    message1 += f" - {str(int(message.content.split('-')[1]))} for a total of {str(final)}"
  
  await message.channel.send(content=message1, reference=message)
  
  if final > 0:
    value = findMapping(final, personCritMap)
    critObj = CRIT[value]

    message2 = f"Crit {str(final)}: {critObj['severityMessage']} "

    for i in range(critObj['severity']):
      message2 += f"<:pd:{roll.emojiMap['pd']}> "
    

    if '<' in critObj['result']:
      emojiR = critObj['result'].split(':')[2].split(':')[0]
      critObj['result'].replace(f':{emojiR}:`, `:{emojiR}:{roll.emojiMap[emojiR]}')

    message2 += critObj['result']

    await message.channel.send(content=message2)


async def rollShipCrit(message):
  randRoll = random.randint(1, 100)
  final = randRoll
  message1 = f'Rolled a d100: {str(final)}'
  
  if '+' in message.content:
    final += int(message.content.split('+')[1])
    message1 += f" + {str(int(message.content.split('+')[1]))} for a total of {str(final)}"
  
  elif '-' in message.content:
    final -= int(message.content.split('-')[1])
    message1 += f" - {str(int(message.content.split('-')[1]))} for a total of {str(final)}"
  
  await message.channel.send(content=message1, reference=message)
  
  if final > 0:
    value = findMapping(final, shipCritMap)
    critObj = SHIP_CRIT[value]

    message2 = f"Crit {str(final)}: {critObj['severityMessage']} "

    for i in range(critObj['severity']):
      message2 += f"<:pd:{roll.emojiMap['pd']}> "
    

    if '<' in critObj['result']:
      emojiR = critObj['result'].split(':')[2].split(':')[0]
      critObj['result'].replace(f':{emojiR}:`, `:{emojiR}:{roll.emojiMap[emojiR]}')

    message2 += critObj['result']

    await message.channel.send(content=message2)