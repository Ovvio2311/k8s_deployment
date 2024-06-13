# Setup jump host

## Add local windows user for jump host

Run powershell as Administrators

```pwoershell
$Password = Read-Host -AsSecureString
New-LocalUser "autotolladmin1" -Password $Password -AccountNeverExpires -PasswordNeverExpires
New-LocalUser "autotolladmin2" -Password $Password -AccountNeverExpires -PasswordNeverExpires
Add-LocalGroupMember -Group "Administrators" -Member autotolladmin1, autotolladmin2

mkdir C:\autotoll_workspace
mkdir C:\autotoll_workspace\tools
mkdir C:\autotoll_workspace\browser_url
```

## Edit group policy

\Administrative Templates\Windows Components\Remote Desktop Services\Remote Desktop Session Host\Session Time Limits\set timelimit for active but idle remote desktop service sessions = 8 hour
\Administrative Templates\Windows Components\Remote Desktop Services\Remote Desktop Session Host\Security\Always prompt for password upon connection = Disabled

## Upload tools

7zip
chrome
git
heidiSQL
mongodb-compass
mongodb-database-tools
notepad++
putty
superputty
WinSCP
