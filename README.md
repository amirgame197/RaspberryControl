# RaspberryControl
Control your RaspberryPi from anywhere --- Cute interface included!<br>
...<br>
<br>
<br>
Or maybe not?<br>
Anyway. Beauty is subjective, take a good look at the interface yourself!<br>


![phito](https://github.com/user-attachments/assets/53ca911a-ad15-4df5-a9ab-19e2d5fb0354)
<br>
This control panel is created and tested using `Raspberry Pi Zero W` running `Raspberry Pi OS`. Other versions and micro controllers will work too, but NanoPi or OrangePi (or any other micro controller) might need some tweaks because of the compatibility issues.<br>
<br>
# Installation & Setup
* Step 1: Downloading the project
  * In your Raspberry + Server
    * Option 1: Paste `git clone https://github.com/amirgame197/RaspberryControl` to automatically download the files. you may need to install `git`.
    * Option 2: Manually download the project files anywhere you want.
    * At the end, keep the `Server` folder in your server and the `Client` folder in your raspberry: These two will speak with each other once configured.
  <br>
* Step 2: Install the required packages
  * Server Packages: `pip install Flask Flask-SocketIO eventlet`
  * Client Packages: `pip install python-socketio psutil`
  <br>
* Step 3: Configuration
  * In your server, run `python server.py` and wait for it to start listening. The default port is 12667, but you can change it in the `server.py` code.
  * In your client, open `config.py`. Change the server_url to your server's listening address. For example, If your server's IP is `45.625.437.859` listening to `12667`, The `config.py` should look like this: `server_url = "http://45.125.237.159:12667"`
  <br>
* Step 4: Testing
  * Now in your client, run `python RaspberryClient.py` and wait for it to connect. After that, If you open a webpage and go to the `server_url` you set earlier, You should see the green indicator pointing that the micro controller is operational!
  <br>
* Step 5: Running as a Service
  * If you dont want the code to get killed whenever you close your terminal, Follow these easy steps. We use systemctl as our service container (because its easy).
    * Server Instructions:
      * `nano /etc/systemd/system/raspberrycontrol.service`
      * Paste these in that new file (make sure of line breaks not getting messed up)
      * ```
        [Unit]
        Description=RaspberryPi Control Service
        After=network.target
        
        [Service]
        Type=simple
        Restart=on-failure
        RestartSec=5s
        WorkingDirectory=/root/RaspberryControl/Server #Change this line if you need to
        ExecStart=python3 server.py
        
        [Install]
        WantedBy=multi-user.target
        ```
      * Save the file using Ctrl+X >> Y >> Enter
      * `systemctl daemon reload`
      * `systemctl enable raspberrycontrol`
      * `systemctl restart raspberrycontrol`
      * Before any of these please make sure there are not any other instances of the script since it would mess up and they get in a fight of who can take the server port.
      * Also, to check whats going on you can do either:
        * Option 1: `systemctl status raspberrycontrol`
        * Option 2: `journalctl -u raspberrycontrol -f`
    * Client Instructions:
      * Technically doing the same thing, just in your micro controller
      * Plus, this service content can be used as client template:
      * ```
        [Unit]
        Description=RaspberryPi Client Control Service
        After=network.target
        
        [Service]
        Type=simple
        Restart=on-failure
        RestartSec=5s
        WorkingDirectory=/root/RaspberryControl/Client #Change this line if you need to
        ExecStart=python3 RaspberryClient.py
        
        [Install]
        WantedBy=multi-user.target
        ```
  <br>
  <br>
# The Story
Time for the second story. This one is not dumb. not painful. not something that makes you think about your life decisions.<br>
You know, have you ever got that weird feeling<br>
That makes you think about everything, all at once, for seconds, minutes, maybe even hours.<br>
<br>
It was fall. Years ago, three or four. I was not feeling anything. The most real thing i felt was just silence of me lying down in street while rain drops are touching my face and nothing ever happening.<br>
Of course, It was all dreams and my mind desperately seeking for a comfort, impossible for my current situation.<br>
The life routine was simple: get up morning, go to work, get back home, try to do something that values your potential. I was all alone and silent since there was no need to use my voice at all.<br>
Days past by like that and ive been trying to find a way to escape my unsettling reality. You know, the reality that you couldnt enjoy is not a reality - since you are not living in it. You live in your own imaginations instead.<br>
<br>
I remember the afternoon i was with my friends talking about stuff. One of them had a real bad depression problem and i thought its a good time to bring that up, not as a mental problem but something that everyone have felt atleast once in their life, but they can never even imagine yours as it is entirely subjective. I came up with a line: My idea of fixing such problem is that what if its just a stage of your life, so you can get past through it by just trying new things that makes you not think about anything else?<br>
He said: How was your stage of depression?<br>
I responded: There is no was.<br>
I thought about my own words for a second, What if it really was the solution of my reality?<br>
He then said: Have you ever tried to try something new, something you could never try in the past but you can now?<br>
Later that night, I did think a lot. I did think about everything - all at once, until i fell asleep.<br>
The next day i woke up i knew what i could do. I had a lot of free time, and i was hungry to learn something new - something different than the other things i already knew.<br>
I thought about micro controllers. They looked so cool, can you imagine you can have a whole computer in palm of your hands? Wait, oh well. I guess those are called phones anyway.<br>
But you could program those. Make them work entirely how you like, no phone works like that. I started with some basics and since i already knew wiring and basic stuff ive gone with a headstart.<br>
After some time i came up with a raspberry pi. My mission was to create a LTE Drone.<br>
Since the raspberry pi should have been LTE (no WiFi, no Radio), i couldnt just connect ssh to it since the ports are all closed. The fix? use your public server as a relay! Then i thought about creating a whole control panel so i can easily control my raspberry pi's stuff through web. The control panel you see right now.<br>
After that, the idea looked possible enough, I did have the blueprints and the only thing remaining to be done was getting the parts and assembling them, which after many attepmts and headaches i finally did everything.<br>
The only little problem was something that caused the whole project to go down: Little Raspberry Pi's CPU could not handle four motors all going PWM (the thing that makes them change rotation speed) for some reason, causing a really really bad and unstable behaviour like they were tripping and stuff. I later found out that there is a reason "Flight Controller"s exist and you cant simluate that on a normal micro controller which is also light.<br>
Project got wrapped up, but my mind did not.<br>
<br>
For months i was thinking about other projects i had in my mind until some extremely weird stuff happened (which i may include some small parts in the next episodes) and i couldnt continue anymore.<br>
But just so you know, drone was a failure and it will be. Flight controller is expensive and maybe even unreachable in my current state, The parts ive used in the drone are in a different project which i will talk about -<br>
Later.
