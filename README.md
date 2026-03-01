## Launchpad X Pure Performance
A minimalist FL Studio script for focused Performance Mode on the Launchpad X!

## Installation
1. Download the ZIP and extract it to the following folder:

> ...\Documents\Image-Line\FL Studio\Settings\Hardware\

2. Under MIDI settings, set *both* LPX MIDI Devices to "Launchpad X Pure Performance", assign each a MIDI Port Number, and enable "Send master sync".

![MIDI Settings](https://raw.githubusercontent.com/LeifBloomquist/LaunchpadXPurePerformance/refs/heads/main/Screenshots/MIDISettings.png)


## Usage
Note: The script is only active when the FL Project is in Performance Mode.

* Use the **Capture MIDI** button to start/stop playback.
* Use the **8x8 grid** to trigger and cue clips.
* Use the **>** buttons on the right side to end playback on that particular row.
* Press and hold the **Session** button for 1.5 seconds to "clear" the playback state of all cells.
* Use the **Session** button for 1.5 seconds to "clear" the playback state of all cells.
* Use the **Custom** button to change themes (see below) 
* TODO: use the **Arrow Buttons** to move the Performance Grid.


## Status Indicators
The **Novation Logo** will change color based on the script state:
* Pulsing Orange: Not in Performance Mode
* Solid Red: In Performance Mode, but not playing
* Flashing Red: Performance Mode Active (flashes in time with the beat)

The **Capture MIDI** button will change color based on the playback state:
* Pulsing Orange: Not in Performance Mode
* Solid Orange: In Performance Mode, but not playing
* Flashing Yellow/Green/Green/Green: Performance Mode Active (Mimics Akai FL Studio Fire Playback colors in time with the beat)

## Themes
By pressing the **Custom** button, the Launchpad X will cycle through various color schemes.  Themes can be easily added and modified though the `themes.py` script.


## Known Issues
The built-in "Flashing Colour" mode on the Launchpad X has wonky timing.  See [Issue #1](https://github.com/LeifBloomquist/LaunchpadXPurePerformance/issues/1) for workaround.


## Acknowledgements
The following repositories were really helpful references in understanding how to program the LaunchPad X.  Thanks!

* [Launchpong-X](https://github.com/MaddyGuthridge/Launchpong-X) by Maddy Guthridge
* [Novation-Launchpad-X-MK3](https://github.com/MetallicAsylum/Novation-Launchpad-X-MK3) by Metallic Asylum / Maxwell Zentolight
