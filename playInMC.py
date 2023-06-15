import mido
from mido import MidiFile
import socket
import sys

inPort = mido.open_input('Digital Piano:Digital Piano MIDI 1')
mcHost = "localhost"
mcPort = 18589

def midiNoteToCreatePitch(note):
    pitch = (note - 6) % 12
    if note >= 78 and pitch == 0: return 12
    return pitch

def midiNoteToCreateOctave(note):
    return int((note - 42) / 12) + 1

def clamp(val, minVal, maxVal):
    if val < minVal: return minVal
    if val > maxVal: return maxVal
    return val

def midiNoteToCreateNote(note):
    return (clamp(midiNoteToCreateOctave(note), 1, 3), midiNoteToCreatePitch(note))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((mcHost, mcPort))
    if len(sys.argv) > 1:
        messages = MidiFile(sys.argv[1]).play()
    else:
        messages = inPort
    for message in messages:
        print(message)
        if (message.type != 'note_on' and message.type != 'note_off'): continue
        octave, note = midiNoteToCreateNote(message.note)
        pressed = message.type == 'note_on'
        mcMessage = 0x8 if pressed else 0x0
        mcMessage = mcMessage + (octave - 1)
        mcMessage = (mcMessage << 4) + note
        sock.send(bytes([mcMessage]))