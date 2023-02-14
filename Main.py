from music import *        # import music library
import random



instrument = 96
while instrument in range(96, 104) or instrument in [13, 31, 36, 45, 47, 49, 55, 86, 92, 93, 95]:            # preventing weird instruments from being chosen randomly
   instrument = random.randint(0, 111)
   chordPart = Part(instrument, 0)                                        # randomizing the intrument and setting the part to MIDI channel 0
print(instrument)

# getting the song criteria from the user

while 1:
   try:
      root  = input("Enter root note (e.g., C4), or leave blank for a random root: ")
      note = Note(root, QN)
      root = note.getPitch()                                    # converting the given note into a MIDI pitch value
      break
   except SyntaxError:
      root = random.randint(52, 64)                             # Setting a random root in appropriate ranges if nothing entered
      print("Assigned " + MIDI_PITCHES[root] + " as root")
      break
   except (NameError, TypeError):
      print("Invalid entry, please use the form \"C4\"")          # Error handling
      continue

while 1:
   try: 
      scale = list(input("Enter scale (e.g., MAJOR_SCALE), or leave blank for a random scale: "))
      break
   except SyntaxError:
      scale = random.choice([MAJOR_SCALE, MINOR_SCALE])                # Defaulting to major if nothing entered
      print("Assigned " + str(scale) + " as scale")
      break
   except (NameError, TypeError):
      print("Invalid entry, please use the form \"MAJOR_SCALE\"")          # Error handling
      continue

while 1:
   try:
      tempo = input("Enter tempo (bpm), or leave blank for a random tempo: ")
      break
   except SyntaxError:
      tempo = random.randint(90, 160)                    # Defaulting to 140 bpm if nothing entered
      print("Assigned " + str(tempo) + " as tempo")
      break
   except (NameError, TypeError):
      print("Invalid entry, please enter a number between 90 and 160")          # Error handling
      continue
   
score = Score("Random song", tempo)

# generating the chord progression

beats = 0
chords = Phrase()
durations = [4, 2]                                      # chord progression can only use whole or half notes
chordPart.setTempo(tempo)
for i in range(8):
   scale.append(scale[i] + 12)                         # creating a higher octave of the scale to allow for easier chord creation
scale = [note + root for note in scale]               # transposing the scale to the root note that was chosen

chordDict = {}                                        # adding a dictionary to keep track of the chords during each beat

while beats < 16:
   
   randIndex = random.randint(0, 6)                        # randomizing the root note of a chord to insert into the phrase
   
   if scale[randIndex + 2] - scale[randIndex] == 3 and scale[randIndex + 4] - scale[randIndex] == 6:                  # calculating if the random chord will be a diminished chord based on the semitone difference between chord tones
      noDims = range(8)
      del noDims[randIndex]                            # creating a temporary list with the index of the notes of the scale and removing the index position of the diminished root (major 7th/minor 2nd)
      randIndex = random.choice(noDims)                   # re-rolling random index in order for the note to not be a dimished chord
   
   if beats == 0:
      duration = random.choice(durations)
      chords.addChord([scale[0], scale[2], scale[4], scale[7]], duration) # adding chord tones on top of the random root
      
      chordDict[beats] = scale[0]     

      beats += duration

   elif beats % 4 == 2:                                  # making sure a half note chord is always followed by another half note chord
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], 2)
      
      chordDict[beats] = scale[randIndex]
      
      beats += 2     

   elif beats == 14: 
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], 2)
      
      chordDict[beats] = scale[randIndex]   
   
      beats += 2
      break
   
   else:
      duration = random.choice(durations)
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], duration)
      
      chordDict[beats] = scale[randIndex]      
   
      beats += duration

print(chordDict)


# generating the melody

instrument2 = 96

while instrument2 in range(96, 104) or instrument2 in [13, 31, 36, 37, 45, 47, 49, 55, 76, 86, 89, 92, 93, 95]:            # preventing weird instruments from being chosen randomly
   instrument2 = random.randint(0, 111)
   melodyPart = Part(instrument2, 1)                                                                   # randomizing the intrument and setting the part to MIDI channel 1
print(instrument2)

mDurations = [0.5, 1, 2]                                                         # creating a list of possible durations for melody notes


"""
diversity = input("How rhythmically diverse do you want your melody to be out (out of 5)?")
mDurationsChances = [diversity, 10, diversity, int(diversity/2)]   # Always want eighth notes to be the most likely note, and half notes/sixteenth notes to be the least likely
"""

mScale = list(scale)
mScale.append(REST)
adjChance = 100                                                                                    # setting the probability out of 10 that a random note in a melody will be adjacent to the previous note
# mChances = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
melody = Phrase()
mBeats = 0

melodyDict = {}                                                                                    # creating a dictionary to keep track of the melody notes (haven't implemented this yet)



while mBeats < 16:
   randAdj = random.randint(0, 10)                                                            # generating a random number to decide if the next note will be adjacent to current note
   randIndex = random.choice(range(len(mScale)))
   chordIndex = 0                
   mBeatsCount = mBeats
   mAdjacent = []
   
   currNote = 0                                                                             # variable to store the current note   

   mBeatsCount -= mBeats % 2                                                       # rounding down the beats of the melody to the nearest 2 beat increment, because this is the smallest possible increment for chords
   
   print mBeatsCount
   try:
      chordIndex = mScale.index(chordDict[mBeatsCount])                             # finding the index position in the melody scale of the current chord
   except KeyError:                                                            # dictionary of chords may not have a value for the current beat number if chord was a whole note, so if this was the case keep going back in the beats until we find a key match from the chords dictionary
      chordIndex = mScale.index(chordDict[mBeatsCount - 2])
         

   
   chordTones = [mScale[max(0, chordIndex - 7)], mScale[max(0, chordIndex - 5)], mScale[max(0, chordIndex - 3)], mScale[chordIndex], mScale[min(len(mScale)-2, chordIndex + 2)], mScale[min(len(mScale)-2, chordIndex + 4)], mScale[min(len(mScale)-2, chordIndex + 7)] ]

   
   chordTones = list(set(chordTones))                 # converting to a set then back to a list to remove duplicates
   
   if root + 12 not in chordTones:                    #  removing the scale root from the chord tones list if the root is not a chord tone in the current chord
      while root in chordTones:
         chordTones.remove(root)
      while root + 24 in chordTones:
         chordTones.remove(root + 24)
   

   chordTones = list(set(chordTones))
   

   
   
   """ sRepeat = random.randint(0, 10)
   

   if sRepeat > 0 and mBeats >= 2 and mBeats - 2 in melodyDict.keys() and duration != 2:
      print mBeats
      print melodyDict
      rBeats = mBeats - 2
      print rBeats     
      while rBeats < mBeats:
         keys = sorted(list(melodyDict.keys()))
         print(keys)
         print rBeats
         m = keys[keys.index(rBeats) + 1]
         melody.addNote(melodyDict[rBeats], keys[keys.index(rBeats) + 1] - rBeats)
         melodyDict[mBeats + rBeats] = melodyDict[rBeats]
         rBeats += keys[keys.index(rBeats) + 1] - rBeats
         
      mBeats += 2"""
      
   duration = random.choice(mDurations)   
   
   if randIndex == 0:               # creating a list of the two adjacent notes to the current one, accounting for if the current note is the first or last in the scale
      mAdjacent.append(mScale[randIndex + 1])
   elif randIndex == len(mScale) - 2:   
      mAdjacent.append(mScale[randIndex - 1])
   elif randIndex == len(mScale) - 1:   # if randindex picks a rest, there are no adjacent notes, so next note will just be a random note of the scale
      mAdjacent = list(mScale)
   else:
      mAdjacent.append(mScale[randIndex - 1])
      mAdjacent.append(mScale[randIndex + 1])
      
   print(mAdjacent)

   if duration >= 1:             # making sure that long notes are always chord tones
      if mBeats % 0.5 == 0.25:                  # making sure a sixteenth note is always followed by another one to prevent weird syncopation
         currNote = random.choice(chordTones)
         melody.addNote(currNote, 0.25)
            
         melodyDict[mBeats] = currNote       # storing the current note in the melody dictionary
         mBeats += 0.25
            
      elif mBeats >= 14: 
         currNote = random.choice(chordTones)
         melody.addNote(currNote, 16-mBeats) # ensuring that the melody never goes over 16 beats long
            
         melodyDict[mBeats] = currNote
         mBeats += 16-mBeats
         break
         
      else:
         currNote = random.choice(chordTones)
         melody.addNote(currNote, duration)
            
         melodyDict[mBeats] = currNote
         mBeats += duration
      
   else:
      if randAdj >= adjChance:  # if the next note will not be adjacent to the current one
         if mBeats % 0.5 == 0.25: # making sure a sixteenth note is always followed by another one to prevent weird syncopation
            currNote = mScale[randIndex]
            melody.addNote(currNote, 0.25)
            
            melodyDict[mBeats] = currNote
            mBeats += 0.25
            
         elif mBeats >= 14: 
            currNote = mScale[randIndex]
            melody.addNote(currNote, 16-mBeats) # ensuring that the melody never goes over 16 beats long
            
            melodyDict[mBeats] = currNote
            mBeats += 16-mBeats
            
            break
         
         else:
            currNote = mScale[randIndex]
            melody.addNote(currNote, duration)
            
            melodyDict[mBeats] = currNote
            mBeats += duration
      
      
      else:                         # if the next note will be adjacent to the current one
         if mBeats == 0:
            currNote = random.choice(mAdjacent)
            melody.addNote(currNote, duration)
            
            melodyDict[mBeats] = currNote
            mBeats += duration

         elif mBeats % 0.5 == 0.25: # making sure a sixteenth note is always followed by another one to prevent weird syncopation
            currNote = random.choice(mAdjacent)
            melody.addNote(currNote, 0.25)
            
            melodyDict[mBeats] = currNote
            mBeats += 0.25
            
         elif mBeats >= 14: 
            currNote = random.choice(mAdjacent)
            melody.addNote(currNote, 16-mBeats) # ensuring that the melody never goes over 16 beats long
            
            melodyDict[mBeats] = currNote
            mBeats += 16-mBeats
            
            break
            
         else:
            currNote = random.choice(mAdjacent)
            melody.addNote(currNote, duration)
            
            melodyDict[mBeats] = currNote
            mBeats += duration
            
      
      print(randAdj >= adjChance)
print(melodyDict)
   


# figure out how to make eighth notes more randomly inclined
""" potential options for user inputs:
repeat patterns (% chance of repeating last x beats)
syncopation
tension(prioritize chord tones less)

Things to add
-Don't play a long note of notes which are a tritone with any current chord tones
-"       "        "        notes which are a major 4ths , minor 6ths, minor 1sts of current chord
-Output a score of the song
-Add major 5th for minor key
-Weigh different durations differently
-Make a dictionary of the melody notes
-Add syncopation to chords
-Add % chance of repeating last 4 beats of melody
-Add higher notes in scale to chordTones
-Error-handling and list available scales in prompts
-Add a probability to the long notes being a chord tone (don't make it certain)
-Sort melody dictionary
-Make half-note chords less frequent than whole-note chords
-Change the UI
-Export score as an mp3 file
-Make the loop reset once one of the melody paths is taken, so it can take the same path on consecutive run-throughs
"""
# playing the song

chordPart.addPhrase(chords)
melodyPart.addPhrase(melody)
melodyPart.setDynamic(90)
chordPart.setDynamic(60)
score.addPart(chordPart)
score.addPart(melodyPart)
Mod.repeat(score, 2)
Play.midi(score)

# Write.midi(score, "song.mid")
