# name=Launchpad X PiXel Performer
"""
# Launchpad X PiXel Performer

An FL Studio script for Focused Performance Mode on the Launchpad X
"""
import device
import playlist
import transport
import midi


MSG_HEADER = [0xF0, 0x00, 0x20, 0x29, 0x02,0x0C]
INIT_MSG   = [0x0E, 0x01, 0xF7]
DEINIT_MSG = [0x0E, 0x00, 0xF7]

NOVATION_LOGO = 0x63
RIGHT_ARROWS  = [0x59, 0x4F, 0x45, 0x3B, 0x31, 0x27, 0x1D, 0x13]
TOP_BUTTONS   = [0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62]
CAPTURE_MIDI  = TOP_BUTTONS[7]

CLIP_GRID = [
    list(range(0x51, 0x59)),
    list(range(0x47, 0x4F)),
    list(range(0x3D, 0x45)),
    list(range(0x33, 0x3B)),
    list(range(0x29, 0x31)),
    list(range(0x1F, 0x27)),
    list(range(0x15, 0x1D)),
    list(range(0x0B, 0x13)),
]

COLOR_BLACK    = 0x00
COLOR_BLUE     = 0x29
COLOR_DARKBLUE = 0x2D
COLOR_WHITE    = 0x03
COLOR_GREEN    = 0x15
COLOR_RED      = 0x48
COLOR_DARKRED  = 0x79
COLOR_YELLOW   = 0x0D
COLOR_IDLE     = 0x7E  # Dullish orange


def OnInit():
    device.midiOutSysex(bytes(MSG_HEADER + INIT_MSG))
    
    # Paint the top row of buttons     
    PaintCell(TOP_BUTTONS[0], COLOR_DARKBLUE)  # Arrows
    PaintCell(TOP_BUTTONS[1], COLOR_DARKBLUE)
    PaintCell(TOP_BUTTONS[2], COLOR_DARKBLUE)
    PaintCell(TOP_BUTTONS[3], COLOR_DARKBLUE)
    PaintCell(TOP_BUTTONS[4], COLOR_WHITE)     # Session
    PaintCell(TOP_BUTTONS[5], COLOR_BLACK)     # Note
    PaintCell(TOP_BUTTONS[6], COLOR_BLACK)     # Custom
    PaintCell(CAPTURE_MIDI,   COLOR_BLACK)     # Capture MIDI


def OnDeInit():
    device.midiOutSysex(bytes(MSG_HEADER + DEINIT_MSG))


def PaintCell(cell_id, color):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x0, cell_id, color)
    
    
def FlashCell(cell_id, color1, color2):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x0, cell_id, color1)
    device.midiOutMsg(midi.MIDI_NOTEON, 0x1, cell_id, color2)


def PulseCell(cell_id, color):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x2, cell_id, color)


def OnMidiIn(event):
    
    event.handled=True
    
    # Filter out aftertouch    
    if event.status == midi.MIDI_KEYAFTERTOUCH:
        return
        
    # Filter out releases    
    if event.data2 == 0:
        return
    
    # Handle side arrow buttons
    
    if event.data1 in RIGHT_ARROWS:
        track = RIGHT_ARROWS.index(event.data1)
        
        # Stop the clips on this track
        playlist.triggerLiveClip(track+1,-1,midi.TLC_Fill)
        
    # Handle clip grid
    
    for i, row in enumerate(CLIP_GRID):
        if event.data1 in row:
            block = row.index(event.data1)
            playlist.triggerLiveClip(i+1, block, midi.TLC_MuteOthers | midi.TLC_Fill) 

    # Control playback with Capture MIDI.  Mimic the Akai Fire Colors
    
    if event.data1 == TOP_BUTTONS[7]:
        if transport.isPlaying():
            transport.stop()
            PaintCell(CAPTURE_MIDI, COLOR_IDLE)
            
        else:            
            FlashCell(CAPTURE_MIDI, COLOR_GREEN, COLOR_BLACK);
            transport.start()

def OnIdle():

    # Indicate status through the logo
    
    if playlist.getPerformanceModeState() == 0:   # Not even in Performance Mode
        PulseCell(NOVATION_LOGO, COLOR_IDLE)
        return
    elif transport.isPlaying() == 0:              # In Performance Mode, but not playing 
        PulseCell(NOVATION_LOGO, COLOR_IDLE)
    else:                                         # Performing!
        FlashCell(NOVATION_LOGO, COLOR_RED, COLOR_BLACK)
    
    # Paint the clip grid
    
    for i, row in enumerate(CLIP_GRID):
        for j, cell in enumerate(row):
            
            block_status = playlist.getLiveBlockStatus(i+1, j, midi.LB_Status_Simple)   # Tracks indexed from 1
            
            match block_status:
                case 0:   # Empty
                    PaintCell(cell, COLOR_BLACK)
                    
                case 1:   # Filled
                    PaintCell(cell, COLOR_GREEN)
                
                case 2:   # Playing
                    FlashCell(cell, COLOR_RED, COLOR_BLACK)
                    
                case 3:   # Scheduled, not playing
                    PulseCell(cell, COLOR_RED)
                    
                case _:   # Unknown??
                    PaintCell(cell, COLOR_IDLE)            
    
    # Paint the side arrows
    
    for i, cell in enumerate(RIGHT_ARROWS):
        
        if transport.isPlaying() == 0:     # Not playing 
            PaintCell(cell, COLOR_DARKRED)
            continue
        
        track_status = playlist.getLiveStatus(i+1, midi.LB_Status_Simple)   # Tracks indexed from 1
        
        match track_status:
            case 0:   # Empty
                PaintCell(cell, COLOR_BLACK)
                
            case 2:   # None Playing  (swapped with 1?)
                PaintCell(cell, COLOR_DARKRED)
            
            case 1:   # Any Playing  (swapped with 2?)
                FlashCell(cell, COLOR_RED, COLOR_DARKRED)
                
            case 3:   # None scheduled, not playing
                PulseCell(cell, COLOR_DARKRED)                
                
            case _:   # Unknown??
                PaintCell(cell, COLOR_IDLE)

