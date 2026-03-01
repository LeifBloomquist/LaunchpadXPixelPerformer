# name=Launchpad X Pure Performance
"""
# Launchpad X Pure Performance

An FL Studio script for Focused Performance Mode on the Launchpad X
"""
import device
import playlist
import transport
import midi
import time
from themes import CurrentTheme, NextTheme

MSG_HEADER = [0xF0, 0x00, 0x20, 0x29, 0x02,0x0C]
INIT_MSG   = [0x0E, 0x01, 0xF7]
DEINIT_MSG = [0x0E, 0x00, 0xF7]

NOVATION_LOGO = 0x63
RIGHT_ARROWS  = [0x59, 0x4F, 0x45, 0x3B, 0x31, 0x27, 0x1D, 0x13]
TOP_BUTTONS   = [0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62]

SESSION       = TOP_BUTTONS[4]
CUSTOM        = TOP_BUTTONS[6]
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

# Timer for clearing all clips
session_pressed = False
session_pressed_time = 0
HOLD_THRESHOLD = 1.5  # Seconds


def OnInit():
    device.midiOutSysex(bytes(MSG_HEADER + INIT_MSG))
    PaintTopRow()
    PaintAllButtons()


def OnDeInit():
    device.midiOutSysex(bytes(MSG_HEADER + DEINIT_MSG))


def PaintCell(cell_id, color):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x0, cell_id, color)
    
    
def FlashCell(cell_id, color1, color2):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x0, cell_id, color1)
    device.midiOutMsg(midi.MIDI_NOTEON, 0x1, cell_id, color2)


def PulseCell(cell_id, color):
    device.midiOutMsg(midi.MIDI_NOTEON, 0x2, cell_id, color)


def ClearAllClips():
    for track, row in enumerate(CLIP_GRID):                 # For all tracks
        playlist.triggerLiveClip(track+1,-1,midi.TLC_Fill)  # Stop the clips on this track


def PaintTopRow():
    # Paint the top row of buttons     
    PaintCell(TOP_BUTTONS[0], CurrentTheme().arrow_colors)    # Arrows
    PaintCell(TOP_BUTTONS[1], CurrentTheme().arrow_colors)
    PaintCell(TOP_BUTTONS[2], CurrentTheme().arrow_colors)
    PaintCell(TOP_BUTTONS[3], CurrentTheme().arrow_colors)
    PaintCell(SESSION,        CurrentTheme().session_default) # Session
    PaintCell(TOP_BUTTONS[5], CurrentTheme().OFF)             # Note
    PaintCell(CUSTOM,         CurrentTheme().logo_color)      # Custom
    PaintCell(CAPTURE_MIDI,   CurrentTheme().idle_color)      # Capture MIDI
    
    # Paint Logo
    PaintCell(NOVATION_LOGO, CurrentTheme().logo_color)
    
    
def PaintAllButtons():    
    # Paint the clip grid    
    for i, row in enumerate(CLIP_GRID):
        
        loop_mode = playlist.getLiveLoopMode(i+1)   # Tracks indexed from 1
        
        for j, cell in enumerate(row):
            
            block_status = playlist.getLiveBlockStatus(i+1, j, midi.LB_Status_Simple)   # Tracks indexed from 1
            
            match block_status:
                case 0:   # Empty
                    PaintCell(cell, CurrentTheme().OFF)
                    
                case 1:   # Filled                    
                    if loop_mode == 1:  # LiveLoop_OneShot
                        PaintCell(cell, CurrentTheme().oneshot_color)
                    else:
                        PaintCell(cell, CurrentTheme().filled_color)
                
                case 2:   # Playing
                    FlashCell(cell, CurrentTheme().playing_color, CurrentTheme().filled_color)
                    
                case 3:   # Cued, not playing
                    PulseCell(cell, CurrentTheme().cued_color)
                    
                case _:   # Unknown??
                     PaintCell(cell, CurrentTheme().COLOR_ERROR)            
    
    # Paint the side arrows    
    for i, cell in enumerate(RIGHT_ARROWS):
        
        track_status = playlist.getLiveStatus(i+1, midi.LB_Status_Simple)   # Tracks indexed from 1
        loop_mode = playlist.getLiveLoopMode(i+1)   # Tracks indexed from 1
        
        # Playing
        match track_status:
            case 0:   # Empty
                PaintCell(cell, CurrentTheme().OFF)
                
            case 2:   # None Playing (swapped with 1?)
                if loop_mode == 1:  # LiveLoop_OneShot                 
                    PaintCell(cell, CurrentTheme().oneshot_color)
                else:
                    PaintCell(cell, CurrentTheme().filled_color)
            
            case 1:   # Any Playing  (swapped with 2?)
                FlashCell(cell, CurrentTheme().playing_color, CurrentTheme().filled_color)
                
            case 3:   # None cued, not playing - !!!! For some reason this never seems to be true?
                PulseCell(cell, CurrentTheme().filled_color)
                
            case _:   # Unknown??
                PaintCell(cell, CurrentTheme().COLOR_ERROR)


def OnMidiIn(event):
    global session_pressed
    global session_pressed_time
    
    event.handled=True
    
    if playlist.getPerformanceModeState() == 0:   # Not in Performance Mode
        return
    
    # Filter out aftertouch    
    if event.status == midi.MIDI_KEYAFTERTOUCH:
        return
        
    # Filter out releases    
    if event.data2 == 0:        
        # Handle release of Session
        if event.data1 == SESSION:
            session_pressed = False
            PaintCell(SESSION, CurrentTheme().session_default)
        return
        
    # Handle press of Session
    if event.data1 == SESSION:
        session_pressed = True
        session_pressed_time = time.time()
        PaintCell(SESSION, CurrentTheme().session_pressed)
        return
    
    # Handle side arrow buttons    
    if event.data1 in RIGHT_ARROWS:
        track = RIGHT_ARROWS.index(event.data1)
        
        # Stop the clips on this track
        playlist.triggerLiveClip(track+1,-1,midi.TLC_Fill)
        PaintAllButtons()
        return
        
    # Handle clip grid    
    for i, row in enumerate(CLIP_GRID):
        if event.data1 in row:
            block = row.index(event.data1)
            playlist.triggerLiveClip(i+1, block, midi.TLC_MuteOthers | midi.TLC_Fill)

    # Control playback with Capture MIDI button
    if event.data1 == CAPTURE_MIDI:
        if transport.isPlaying():
            transport.stop()
            PaintCell(CAPTURE_MIDI, CurrentTheme().idle_color)            
        else:
            transport.start()
            
    # Switch Themes with Custom button
    if event.data1 == CUSTOM:
        NextTheme()
        PaintTopRow()
    
    # Refresh
    PaintAllButtons()


def OnRefresh(flags):    
    if playlist.getPerformanceModeState() == 0:   # Not in Performance Mode
        PulseCell(CAPTURE_MIDI, CurrentTheme().idle_color)        
        PulseCell(NOVATION_LOGO, CurrentTheme().idle_color)
        return
       
    if transport.isPlaying() == 0:                # In Performance Mode, but not Playing 
        PaintCell(CAPTURE_MIDI, CurrentTheme().idle_color)        
        return     
    

def OnIdle():
    global session_pressed
    global session_pressed_time    
                
    # If Session held down, clear all clips    
    if (session_pressed):
        delta = time.time() - session_pressed_time
            
        if delta > HOLD_THRESHOLD:
            ClearAllClips()
            PaintCell(SESSION, CurrentTheme().session_cleared)
            session_pressed = False


# Show status, playback and beat through Capture MIDI and Novation Logo
# Mimic the Akai Fire Colors, mostly
def OnUpdateBeatIndicator(value):    
    #Indicate the beat
    match value:
        case 0:   # Off
            PaintCell(CAPTURE_MIDI, CurrentTheme().OFF)
            PaintCell(NOVATION_LOGO, CurrentTheme().OFF)
            
        case 1:   # Bar
            PaintCell(CAPTURE_MIDI, CurrentTheme().bar_color)
            PaintCell(NOVATION_LOGO, CurrentTheme().logo_color)
        
        case 2:   # Beat
            PaintCell(CAPTURE_MIDI, CurrentTheme().beat_color)
            PaintCell(NOVATION_LOGO, CurrentTheme().logo_color)

        case _:   # Unknown??
            PaintCell(CAPTURE_MIDI, CurrentTheme().COLOR_ERROR)
            PaintCell(NOVATION_LOGO, CurrentTheme().COLOR_ERROR)
            
    PaintAllButtons()
