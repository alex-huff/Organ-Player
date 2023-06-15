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

def sendMessage(message, socket):
    sendUpdate(message.type == 'note_on', message.note, socket)

def sendUpdate(isPressed, midiNote, socket):
    octave, note = midiNoteToCreateNote(midiNote)
    mcMessage = 0x8 if isPressed else 0x0
    mcMessage = mcMessage + (octave - 1)
    mcMessage = (mcMessage << 4) + note
    socket.send(bytes([mcMessage]))

pedalDown = False
queuedReleases = set()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((mcHost, mcPort))
    if len(sys.argv) > 1:
        messages = MidiFile(sys.argv[1]).play()
    else:
        messages = inPort
    for message in messages:
        print(message)
        if (message.type != 'note_on' and message.type != 'note_off' and (message.type != 'control_change' or message.control != 64)): continue
        if (message.type == 'control_change'):
            if (message.value == 127):
                pedalDown = True
            elif (message.value == 0):
                pedalDown = False
                for note in queuedReleases:
                    sendUpdate(False, note, sock)
                queuedReleases.clear()
            continue
        if (pedalDown and message.type == 'note_off'):
            queuedReleases.add(message.note)
            continue
        sendMessage(message, sock)