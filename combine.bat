setlocal enabledelayedexpansion
set myfiles=
for %%f in (*.pcap) do set myfiles=!myfiles! %%f
Cmd /V:on /c "C:\Program Files\Wireshark\mergecap.exe" -w temp.pcap %myfiles%