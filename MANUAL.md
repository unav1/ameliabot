Introduction
============

Ameliabot is implemented on top of untwisted framework. It uses some of the untwisted tools in its plugin architecture. The fact of untwisted
being such a modular and objective event driven framework makes ameliabot core be so small. The plugin api is neat and powerful.
There is a variety of plugins that perform different tasks such as calculating integrals or executing python code on the fly.

The standard irc commands follow the following format although it is possible to implement irc commands that follow a different pattern.

@command arg1 arg2 ... arg_n 'argument with spaces' "argument with spaces"

or

@command arg1 arg2 ... arg_n argument with spaces with no '' 

The latter one uses regex for the command template.

User Plugins
============

User plugins should be in the ~/.amelia/ folder, such a folder is appended to sys.path then the plugins should be
loaded from ~/.amelia/ameliarc with a simple import.

Consider a file named ~/.amelia/my.py in order to make the bot load the plugin named my.py one would put
in the ~/.amelia/ameliarc file the following sequence of code.

~~~python
# plugin imports.

import my

# irc network handle, such a handle installs the plugins.
def irc_network(server)
    # plugin installations.
    my.install(server)
~~~

Plugin Template
===============

The standard plugin template is as follows.

~~~python
from untwisted.plugins.irc import send_msg
from untwisted.network import xmap
from ameliabot.cmd import command

def install(server):
    xmap(server, 'CMSG', send)
    xmap(server, 'PMSG', send)

@command('@tell person note')
def send(server, nick, user, host, target, msg, person, note):
        send_msg(server, person, note)
~~~

The xmap function binds the event 'CMSG' to the handle named send. The event 'CMSG' means
that someone has sent a msg to one of the channels that the bot is in.

The decorator named command means that the handle named send will be executed only if it is 
an user msg that matches the pattern starting with:

~~~
'@tell person tell'.
~~~

Example

~~~
@tell hafydd "you're a nice buddy."
~~~

Whenever an user that is in a channel that you're in issues that command
the bot will send a private msg to the person whose nick is hafydd.

The event named 'PMSG' means that the bot will reply to private messages as well. So, if an user
sends a private message to the bot and such a private message matches the command pattern then
the bot will send a msg to an user whose nick was specified.

The events 'CMSG' and 'PMSG' are implemented in untwisted as a facility to distinguish between 
prvate messages and channel messages.

It is possible yet to use the irc event named 'PRIVMSG' which matches both private messages and channel messages.

In the command template shown above the arguments 'person' and 'note' that are passed to the command '@tell'
turn into variables that are in the handle scope.

It is possible to implement command templates using regex as follows.

~~~python
from ameliabot.cmd import regcmd

def install(server):
    xmap(server, 'CMSG', send)

@regcmd('@test (?P<arg1>[^ ]+) (?P<arg2>.+)')
def handle(server, nick, user, host, target, msg, arg1, arg2):
        send_msg(server, target, 'The command issued:@%s %s' % (arg1, arg2))
~~~

The name of the groups so defined turn into variables that are in the scope.
In the example above the command wouldn't require '' or "" to enclose arguments that demand spaces. 

Example:

~~~
@test alpha this is cool
~~~

The function named handle would receive arg1 and arg2 as follows.

~~~
arg1:'alpha'
arg2:'this is cool'
~~~

Irc Events
==========

Irc messages that are based abstracted into commands with arguments. Untwisted irc plugin parsers irc messages
then turn them into events that can be binded to functions. The commands are neatly parsed and their arguments
are given to the handles.

There is below a list of common irc events and an example of the arguments that the handles receive.

~~~
from untwisted.plugins.irc import send_msg
from untwisted.network import xmap

def install(server):
    # When an user joins a channel that the bot is in.
    xmap(server, 'JOIN', send_welcome)
    
    # When the server issues ping.
    xmap(con, 'PING', on_ping)

    # When an user leaves a channel that the bot is in.
    xmap(con, 'PART', on_part)

    # When the server sends the motd.
    xmap(con, '376', on_376)

    # When there is a NOTICE command coming from the irc network.
    xmap(con, 'NOTICE', on_notice)

    # When an user has sent a private or a channel msg.
    xmap(con, 'PRIVMSG, on_privmsg)

def on_join(server, nick, user, host, channel):
    pass

def on_ping(con, prefix, servaddr):
    pass

def on_part(con, nick, user, host, chan):
    pass

def on_376(con, prefix, nick, msg):
    pass

def on_notice(con, prefix, nick, msg, *args):
    pass

def on_privmsg(con, nick, user, host, target, msg):
    pass
~~~

The irc events above are the basic ones, for a better description see irc rfc.

Plugin Help System Scheme
=========================









