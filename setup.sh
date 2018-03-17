#!/usr/bin/env bash

gem install terminal-notifier
cp  ./toolkit.plist ~/Library/LaunchAgents/toolkit.plist
touch /tmp/toolkit.out
touch /tmp/toolkit.err
chown $USER /tmp/toolkit.out
chown $USER /tmp/toolkit.err
launchctl load ~/Library/LaunchAgents/toolkit.plist