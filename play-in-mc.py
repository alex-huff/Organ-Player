import mido
from mido import MidiFile
import socket
import sys

in_port = mido.open_input('Digital Piano:Digital Piano MIDI 1')
mc_host = "localhost"
mc_port = 18589

def midi_note_to_create_pitch(note):
    pitch = (note - 6) % 12
    if note >= 78 and pitch == 0: return 12
    return pitch

def midi_note_to_create_octave(note):
    return int((note - 42) / 12)

def clamp(val, min_val, max_val):
    if val < min_val: return min_val
    if val > max_val: return max_val
    return val

def midi_note_to_create_note(note):
    return (clamp(midi_note_to_create_octave(note), 0, 2), midi_note_to_create_pitch(note))

def send_update(is_pressed, octave, note, socket):
    if (is_pressed == note_state[octave][note]): return
    mc_message = 0x8 if is_pressed else 0x0
    mc_message = mc_message + octave
    mc_message = (mc_message << 4) + note
    socket.send(bytes([mc_message]))
    note_state[octave][note] = is_pressed

pedal_down = False
queued_releases = set()
note_state = [[False for n in range(13)] for o in range(3)]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((mc_host, mc_port))
    if len(sys.argv) > 1:
        messages = MidiFile(sys.argv[1]).play()
    else:
        messages = in_port
    for message in messages:
        print(message)
        if (message.type != 'note_on' and message.type != 'note_off' and (message.type != 'control_change' or message.control != 64)): continue
        if (message.type == 'control_change'):
            if (message.value == 127):
                pedal_down = True
            elif (message.value == 0):
                pedal_down = False
                for octave, note in queued_releases:
                    send_update(False, octave, note, sock)
                queued_releases.clear()
            continue
        octave, note = midi_note_to_create_note(message.note)
        pressed = message.type == 'note_on' or message.velocity == 0
        if (pedal_down and not pressed):
            queued_releases.add((octave, note))
            continue
        send_update(pressed, octave, note, sock)
