# blackrockstation
Code for Black Rock Station, honorarium art project for Burning Man 2021

Technical Questions
-------------------

-   How do we keep this powered 24/7?

-   How much power will it use? With the AC? Without the AC?

-   How often will we have to fuel a generator?

-   Since it is primarily an audio piece, can we get it placed in a location that it won't be overwhelmed by noise?

-   How do we keep the microcomputers free of dust?

-   Do we create lots of little autonomous systems (modularity) taking their signals from a master controller or one computer to control everything?

-   If there is a master controller, how will it signal everything else? MQTT w Ack? OSC? HTTP? (Note that there is nothing that the clients need to communicate back to the broker.)

-   If there is a light controller, how many channels does it need? Can everything flicker at the same time, or is it more disorienting if the lights are independent?

Technical Challenges to Overcome
--------------------------------

-   Recording quality multi-channel train sounds

-   Establishing a reliable power network

-   Establishing a reliable & robust data network

-   Creating a dependable signal network, i.e., broker and clients

-   Creating autonomous triggerable clients:

-   Crossing masts w lights and signal

-   Video controller

-   Interior and outdoor light controller

-   Audio controller

-   Train audio controller

-   Create a logging and error reporting system

-   Create an app controller/configuration utility

-   Making tech setup invisible, foolproof, and easy

Field Recording
---------------

-   Low-cost digital recorders are fine as long as they are matched and have XLR mic inputs

-   For the mic small diaphragm condenser microphones with a cardioid pattern are preferred, though others may work

-   Good wind protection is necessary

Data Network
------------

-   Wi-Fi should work well enough to connect a bunch of Raspi3b+'s if there is a router.

-   Network will remain unadvertised

Signal Network
--------------

-   OSC has worked well in the past

-   Apparently MQTT is a thing and requires a Broker

-   HTTP might be the simplest scheme simply because setting up a listener on the clients is well-trod territory. When needed, the Master makes request to clients. The response can return an success/error code. Client devices can register at the Master when they come up or periodically (though they must know who the master is)

-   We can hit port 80 of the Master to see the status, logs, reports, or upcoming events

-   Need controllers for the following:

-   Internal light controller

-   External light controller

-   Track sound controller 1

-   Track sound controller 2

-   Announcement controller

-   TV controller

-   Radio controller

-   Signal bridge controller

-   Waterproof Raspi Enclosure: Pinfox Waterproof Electronic ABS Plastic Junction Project Box Enclosure 200mm by 120mm by 75mm (Black), $11.99

Scheduling
----------

-   A schedule of events can be kept in a database coordinated with timestamps

-   "Random" events can be randomly seeded through the database. This ensures they don't collide with other events. It also allows us to know when the next event is.

-   The length of each event can be recorded in the database, so we can prevent collisions

-   We keep a database of the schedule of events

-   We also keep a database of the events themselves, including length, clients involved, and commands for clients, and any tricky timing (like a little asynchronous  recipe?)

-   How events work will require some thought because they have their own timing and desire to avoid collisions

-   If event scheduling can be simplified, scheduling will be easier. For instance, crossing bells and announcements happen before, during and after a train event every time. Maybe rules rather than explicit scheduling? Then we have to be more careful about collisions.

-   Care should be taken to choose a database that is least likely to be corrupted by sudden power interruptions

Light Controller
----------------

-   Relay boards JBtek 4 or 8 Channel DC 5V Relay Module for Arduino Raspberry Pi DSP AVR PIC ARM at 10A capacity

-   Can put in fully sealed box with external plugs for wiring simplicity

-   Control low wattage LED blubs and fluorescent lights

Wiring Diagram
--------------

![Black Rock Station Wiring Diagram](https://github.com/wmodes/blackrockstation/images/Black Rock Station Wiring Diagram.png)
