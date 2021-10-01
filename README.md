# Black Rock Station
Code for Black Rock Station, honorarium art project for Burning Man 2021.

Various subsystems (lights, audio, video, etc) rely on a network of semi-autonomous controller modules receiving orders from a central scheduling controller.

## Authors

* Author: Black Rock Transportation Company <info@blackrocktrainstation.com>
* Date: Apr 2021
* License: MIT

## Dependencies

You must have the following software installed before you attempt to install the python modules:

* Sox
* VLC
* Sip
* PyQt5

If you are developing on MacOS, use `brew install`. If you are installing on the Raspberry Pi, use `apt-get install`.

## Installation

Because python 3.7 is the latest pre-built version for the Raspberry Pi, we use version 3.7. You should too for this project if you don't want to have to make subtle adjustments. We suggest you use `pyenv` to manage your python versions. Confirm you have 3.7 with:

`% python --version`

It should report python 3.7.x

Create a virtual environment in your envs folder with:

`% python3 -m venv blackrockstation`

Activate the venv with:

`% source ~/dev/envs/blackrockstation/bin/activate`

Clone the repo from Github, then `cd blackrockstation` into the new repoI’m  folder.

Install the python module requirements with:

`% pip install -r requirements.txt`

You'll probably need the media files for testing. Download the mediafiles to the root:

[media-files.tar.gz](https://drive.google.com/file/d/1_eMsQjETB9L_u6GMdJ2qZpQZf2TpKboU/view?usp=sharing)

And unpack with:

`% tar xvf media-files.tar.gz`

## Raspberry Pi

To prep your Raspberry Pi, see my guide [Raspberry Pi Standard Install for Development or Projects](https://github.com/wmodes/raspi-install).

There are all sorts of tricky things about installing on the Raspberry Pi. On one hand, it is a pretty standard Debian variant. On the other hand, some packages are not yet available for the Pi and require extra work.

Here's the list of installation requirements:

```
sudo apt-get install -y sox vlc python3-vlc
sudo apt-get install -y qt5-default pyqt5-dev pyqt5-dev-tools python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qsci python3-pyqt5.qtmultimedia
```

## Executing

### Testing on the command line

Use `start.py` to start each subsystem. For example, to start the announce subsystem:

`% python start.py announce`

`start.py` without arguments lists available controllers.

### Running from systemd during production

After testing, you probably want the Rpi to run the controller on boot. We'll add a unit file to `systemd`. A sample unit file is included in the repo.

First copy this file out of the repo (lest your modified version be overwritten by a `git pull`) to your home directory:

  `cp brs.service ~`

Edit your copied unit file `brs.service`. Find the line:

  `ExecStart=/usr/bin/python3 -u start.py scheduler`

Change `scheduler` to whichever of the controllers you want your Rpi to take on the identity. Available controllers are `announce`, `crossing`, `lights`, `radio`, `scheduler`, `signal`, `train`, and `television`. (Note that the radio, television, announce, and train controllers will each need their media files in their respective data directories.)

From your home directory, using the modified unit file, enable `brs.service`:

```
sudo systemctl enable brs.service
sudo systemctl start brs.service
```

Later, if you want to turn off the service:

  `sudo systemctl stop brs.service`

## General and Network-wide

Considerations for shared resources among the entire network.

### General Technical Questions

-   How do we keep this powered 24/7?
-   How much power will it use? With the AC? Without the AC?
-   How often will we have to fuel a generator?
-   Since it is primarily an audio piece, can we get it placed in a location that it won't be overwhelmed by noise?
-   How do we keep the microcomputers free of dust?
-   Do we create lots of little autonomous systems (modularity) taking their signals from a master controller or one computer to control everything?
-   If there is a master controller, how will it signal everything else? MQTT w Ack? OSC? HTTP? (Note that there is nothing that the clients need to communicate back to the broker, except maybe a simple .)
-   If there is a light controller, how many channels does it need? Can everything flicker at the same time, or is it more disorienting if the lights are independent?

### General Technical Challenges to Consider

-   Recording quality multi-channel train sounds
-   Establishing a reliable power network
-   Establishing a reliable & robust data network
-   Creating a dependable signal network, i.e., broker and clients
-   Creating autonomous triggerable clients.
-   Create a logging and error reporting system
-   Create an app controller/configuration utility
-   Making tech setup invisible, foolproof, and easy

### Wiring Diagram

![Black Rock Station Wiring Diagram](https://raw.githubusercontent.com/wmodes/blackrockstation/main/images/wiring-diagram.png)

Note that data "wires" may be WiFi, though for more remote systems (Crossing Mast and Signal Bridge) should be prepared to run ethernet.

### Controllers

Each discrete system has an semi-independent subservient controller. We need the following controllers:

  1. Internal light controller
  2. Crossing mast controller
  3. Track sound controller
  4. Announcement controller
  5. television controller
  6. Radio controller
  7. Signal bridge controller

### Data Network

-   Wi-Fi should work well enough to connect a bunch of Raspi3b+'s if there is a router.
-   Network will remain unadvertised

### Signal Network

The signal network will allow the various controllers to talk with each other and coordinate events.

- Looking for dead simplicity, and robustness under harsh conditions
-   OSC has worked well in the past
-   Apparently MQTT is a thing and requires a Broker
- Brandon tells us that gRPI is good
-   HTTP might be the simplest scheme simply because setting up a listener on the clients is well-trod territory. When needed, the Master makes request to clients. The response can return an success/error code. Client devices can register at the Master when they come up or periodically (though they must know who the master is)
-   We can hit port 80 of any of the controllers to see status, logs, reports, or upcoming events
-   Waterproof Raspi Enclosure: Pinfox Waterproof Electronic ABS Plastic Junction Project Box Enclosure 200mm by 120mm by 75mm (Black), $11.99

## Scheduler Controller

The central controller controls the scheduling of both trains and time-slips. It sends signals to each of the other subservient controllers.

### Scheduling

-   A schedule of events can be kept in a database coordinated with timestamps
-   "Random" events can be randomly seeded through the database. This ensures they don't collide with other events. It also allows us to know when the next event is.
-   The length of each event can be recorded in the database, so we can prevent collisions. Though the controllers themselves can be the final arbiter.
-   We keep a database of the schedule of events
-   We also keep a database of the events themselves, including length, clients involved, and orders for clients, and any tricky timing (like a little asynchronous  recipe?)
-   How events work will require some thought because they have their own timing and desire to avoid collisions
-   If event scheduling can be simplified, scheduling will be easier. For instance, crossing bells and announcements happen before, during and after a train event every time. Maybe rules rather than explicit scheduling? Then we have to be more careful about collisions.
-   Care should be taken to choose a database that is least likely to be corrupted by sudden power interruptions

### Orders

Here are the Orders the scheduler controller responds to:

- order *controller* *command*
- reqTrains [num_events]
- reqStatus
- reqLog [num_events]

This is passed as an JSON string:

```
{
  "cmd" :   "reqTrains",
  "qty" :     10
}
```

## Train Audio Controller

The train audio controller handles the sounds of trains. It needs to be given scheduled events from the central controller describing the audio and type of train passing. Additional considerations are:

- Has to send line audio to the two stereo speakers mounted trackside and the subwoofer mounted to the station.
- The distance to the trackside powered speakers is considerable and might require a pre-amp.
- Must be located in the station because the separation of the speakers and the subwoofer.
- Must be coordinated with the crossing mast controllers
- It cannot be interrupted by time-slips

### Field Recording

-   Low-cost digital recorders are fine as long as they are matched and have XLR mic inputs
-   For the mic small diaphragm condenser microphones with a cardioid pattern are preferred, though others may work
-   Good wind protection is necessary

### Orders

Here are the orders the train controller responds to:

- set off
- set on
- set train *direction* *type* *year*
- request status
- request log [num_events]
- request report

## Announce Controller

The announce controller handles announcements. It needs to be given scheduled events from the scheduler controller describing which announcement to play. Additional considerations are:

- Has to send line audio to a small amp and out to the speaker horns inside and outside the station.
- Must be coordinated with scheduled trains
- It will not be interrupted by time-slips (or will it?)

### Orders

Here are the orders the train controller responds to:

- set off
- set on
- set glitch
- set announce *id* *year*
- request status
- request log [num_events]
- request report

## Crossing Mast Controller

The crossing mast controller handles turning the crossing lights and bell on and off. It operates on scheduled train events from the central controller. Additional considerations:

- Where to place the controller? Is there space or a housing on the crossing masts themselves?
- Has to be weatherproof since it is outside
- Is the distance too great for WiFi? Prepare to run ethernet.
- Since these lights/bells are either on or off, it could be possible to locate the controller in the station and run only switched power to the masts. However, the masts need steady power anyway to power a safety flood light.
- The masts themselves are a distance apart. I suspect it is simpler to have one controller turn them on and off, with power wiring from the least distant to the most distant.
- Timing-wise, the lights/bell begin some number of seconds before a train "arrives" and turns off as soon as a train passes the station.

### Orders

Here are the orders the crossing controller responds to:

- set on
- set off
- request status
- request log [num_events]
- request report

## Signal Bridge Controller

The signal bridge controller handles turning the lights on the signal bridge. Unlike the crossing mast controller, the signal lights are more complicated. It responds to timed events from the central controller. The light is always on in one of two settings, highball/go (green/upper light) or stop (red/lower light). Considerations include:

- Where to place the controller? Need a housing on the signla bridge.
- Has to be weatherproof since it is outside
- Is the distance too great for WiFi?
- The default setting of the signal bridge lights when no train is passing or present is stop.
- 5-10 minutes before a train passes, the signal would go to highball.
- Timing-wise, the lights go from highball to stop after the train passes the station.

### Orders

Here are the orders the signal controller responds to:

- set go *direction*
- set stop
- request status
- request log [num_events]
- request report

## Internal Light Controller

The light controller controls the internal lighting. It has recipes for glitch effects during time-slips as well as recipes for what lighting it provides during different eras. Additional notes:

-   Relay boards JBtek 4 or 8 Channel DC 5V Relay Module for Arduino Raspberry Pi DSP AVR PIC ARM at 10A capacity
-   Can put in fully sealed box with external plugs for wiring simplicity
-   Control low wattage LED blubs and fluorescent lights

### Orders

Here are the orders the light controller responds to:

- set off [num]
- set on [num]
- set glitch
- set year *year*
- request status
- request log [num_events]
- request report

## Radio Controller

The radio controller handles audio coming from the radio. It only needs to know what era it is operating in to play period-appropriate music, announcements, and news. Additional considerations are:

- Glitch/static sounds during time-slips
- Possibly keeping track of announcements, news, and music to mix them up as necessary.

### Orders

Here are the orders the radio controller responds to:

- set off
- set on
- set glitch
- set year *year*
- request status
- request log [num_events]
- request report

## Television Controller

The television controller handles audio/video coming from the television. Like the radio, it only needs to know what era it is operating in. It has the same considerations as the radio controller.

### Orders

Here are the orders the television controller responds to:

- set off
- set on
- set glitch
- set year *year*
- request status
- request log [num_events]
- request report
