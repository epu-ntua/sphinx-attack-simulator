#!/bin/bash
D-ITG/bin/ITGRecv &> receiver.stdout &
D-ITG/bin/ITGSend -Q -l sender.log -x receiver.log &> sender.stdout
