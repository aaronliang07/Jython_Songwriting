from music import *        # import music library
import random

# getting the song criteria from the user

chordPart = Part("Chords", 0)
root  = input("Enter root note (e.g., C4): ")
note = Note(root, QN)
root = note.getPitch() # converting the given note into a MIDI pitch value
scale = list(input("Enter scale (e.g., MAJOR_SCALE): "))
tempo = input("Enter tempo (bpm): ")

score = Score("Random song", tempo)

# generating the chord progression

beats = 0
chords = Phrase()
durations = [4, 2]  # chord progression can only use whole or half notes
chordPart.setTempo(tempo)
for i in range(8):
   scale.append(scale[i] + 12) # creating a higher octave of the scale to allow for easier chord creation
scale = [note + root for note in scale] # transposing the scale to the root note that was chosen



while beats < 16:
   randIndex = random.choice(range(7)) # randomizing the root note of a chord to insert into the phrase
   
   if beats == 0:
      duration = random.choice(durations)
      chords.addChord([scale[0], scale[2], scale[4], scale[7]], duration) # adding chord tones on top of the random root
      beats += duration
      print(duration)
   elif beats % 4 == 2: # making sure a half note chord is always followed by another half note chord
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], 2)
      beats += 2
      print(2)
   elif beats == 14: 
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], 2)
      beats += 2
      print(2)
      break
   else:
      duration = random.choice(durations)
      chords.addChord([scale[randIndex], scale[randIndex + 2], scale[randIndex + 4], scale[randIndex + 7]], duration)
      beats += duration
      print(duration)

# generating the melody

melodyPart = Part("Melody", 1)
mDurations = [0.25, 0.5, 1, 2]
mScale = list(scale)
mScale.append(REST)
melody = Phrase()
mBeats = 0
while mBeats < 16:
   randIndex = random.choice(range(len(mScale)))
   
   if mBeats == 0:
      duration = random.choice(mDurations)
      melody.addNote(mScale[randIndex], duration)
      mBeats += duration
      print(duration)
   elif mBeats % 0.5 == 0.25: # making sure a sixteenth note is always followed by another one to prevent weird syncopation
      melody.addNote(mScale[randIndex], 0.25)
      print(0.25)
      mBeats += 0.25
   elif mBeats >= 14: 
      melody.addNote(mScale[randIndex], 16-mBeats) # ensuring that the melody never goes over 16 beats long
      print(16-mBeats)
      mBeats += 16-mBeats
      break
   else:
      duration = random.choice(mDurations)
      melody.addNote(mScale[randIndex], duration)
      mBeats += duration
      print(duration)
      
# figure out how to prioritize the chord tones from chord part
# figure out how to make shorter notes more randomly inclined
# potential options for user inputs: repeat patterns, syncopation, tension(prioritize chord tones less)

# playing the song

print(beats)
print(mBeats)
chordPart.addPhrase(chords)
melodyPart.addPhrase(melody)
score.addPart(chordPart)
score.addPart(melodyPart)
Mod.repeat(score, 2)
Play.midi(score)
