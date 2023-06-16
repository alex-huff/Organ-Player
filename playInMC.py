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
    return int((note - 42) / 12)

def clamp(val, minVal, maxVal):
    if val < minVal: return minVal
    if val > maxVal: return maxVal
    return val

def midiNoteToCreateNote(note):
    return (clamp(midiNoteToCreateOctave(note), 0, 2), midiNoteToCreatePitch(note))

def sendUpdate(isPressed, octave, note, socket):
    if (isPressed == noteState[octave][note]): return
    mcMessage = 0x8 if isPressed else 0x0
    mcMessage = mcMessage + octave
    mcMessage = (mcMessage << 4) + note
    socket.send(bytes([mcMessage]))
    noteState[octave][note] = isPressed

pedalDown = False
queuedReleases = set()
noteState = [[False for n in range(13)] for o in range(3)]
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
                for octave, note in queuedReleases:
                    sendUpdate(False, octave, note, sock)
                queuedReleases.clear()
            continue
        octave, note = midiNoteToCreateNote(message.note)
        pressed = message.type == 'note_on'
        if (pedalDown and not pressed):
            queuedReleases.add((octave, note))
            continue
        sendUpdate(message.type == 'note_on', octave, note, sock)