Param
(
   [Switch]$Start,
   [Switch]$Stop,
   [Switch]$Status,
   [Switch]$SkipBuild
)


########################################
##         Utility Functions          ##
########################################
function Print-Usage
{
   Write-Host "`nUSAGE:" -ForegroundColor Yellow
   Write-Host "   .\docker <OPTIONS> [SERVER]" 
   Write-Host "   e.g. '.\docker -Start -SkipBuild apache'" -ForegroundColor DarkGray

   Write-Host "`nARGS:" -ForegroundColor Yellow
   Write-Host "   SERVER" -ForegroundColor Green
   Write-Host "      This argument is optional"
   Write-Host "      Possible values: nginx, apache"

   Write-Host "`nOPTIONS:" -ForegroundColor Yellow
   Write-Host "   -Start" -ForegroundColor Green
   Write-Host "      Start the specifed SERVER running on the Docker Container(s)."
   Write-Host "      If SERVER isn't specifed, both servers will be started.`n"
   Write-Host "   -Stop" -ForegroundColor Green
   Write-Host "      Stop the specifed SERVER running on the Docker Container(s)."
   Write-Host "      If SERVER isn't specifed, both servers will be stopped.`n"
   Write-Host "   -Status" -ForegroundColor Green
   Write-Host "      Display the status of the specifed SERVER running on the Docker Container(s)."
   Write-Host "      If SERVER isn't specifed, both servers status will be be displayed.`n"
   Write-Host "   -SkipBuild" -ForegroundColor Green
   Write-Host "      Skip the container build process.`n"
}

function Systemd-Start {
   Param(
      [Parameter(Mandatory=$true)]
      [ValidateSet("nginx", "apache")]
      [string]$compose_service,
      [Parameter(Mandatory=$true)]
      [string[]]$systemd_services
   )
   $s = [system.String]::Join(" ", $systemd_services)
   iex "docker-compose exec $compose_service systemctl enable $s"
   iex "docker-compose exec $compose_service systemctl start $s"
}

function Systemd-Stop {
   Param(
      [Parameter(Mandatory=$true)]
      [ValidateSet("nginx", "apache")]
      [string]$compose_service,
      [Parameter(Mandatory=$true)]
      [string[]]$systemd_services
   )
   $s = [system.String]::Join(" ", $systemd_services)
   iex "docker-compose exec $compose_service systemctl stop $s"
}

function Systemd-Status {
   Param(
      [Parameter(Mandatory=$true)]
      [ValidateSet("nginx", "apache")]
      [string]$compose_service,
      [Parameter(Mandatory=$true)]
      [string[]]$systemd_services
   )
   $s = [system.String]::Join(" ", $systemd_services)
   iex "docker-compose exec $compose_service systemctl status $s" | Write-Host
}


########################################
##            Main Process            ##
########################################

# validate arguments
if (
      ($Start.IsPresent + $Stop.IsPresent + $Status.IsPresent -ne 1) -or
      ($args.Count -gt 1) -or
      ($args[0] -and ($args[0] -ne "nginx") -and ($args[0] -ne "apache"))
   ) {
   Print-Usage
   exit 1
}

# build containers
if (!$SkipBuild -and $Start) {
   Write-Host "`nSCRIPT: Building Docker Containers" -ForegroundColor DarkGreen
   try {
      iex "docker-compose up -d --build"
   } catch {
      Write-Host "ERROR: Failed to build Docker containers" -ForegroundColor Red
      exit 1
   }
}

[string[]] $ComposeService= if ($args[0]) {@($args[0])} else {@("apache", "nginx")}

# systemd operations
if ($Start.IsPresent) {
   $ComposeService.ForEach({
      try {
         Write-Host "`nSCRIPT: Starting $_ server..." -ForegroundColor DarkGreen
         $ServerName = if ($_ -eq "nginx") {"nginx"} else {"apache2"}
         Systemd-Start -compose_service $_ -systemd_service @("supervisor", $ServerName)
      } catch {
         Write-Host "ERROR: $_" -ForegroundColor Red
         exit 1
      }
   })
}

if ($Status.IsPresent) {
   $ComposeService.ForEach({
      try {
         Write-Host "`nSCRIPT: Retrieving $_ server status..." -ForegroundColor DarkGreen
         $ServerName = if ($_ -eq "nginx") {"nginx"} else {"apache2"}
         Systemd-Status -compose_service $_ -systemd_service @($ServerName, "supervisor")
      } catch {
         Write-Host "ERROR: $_" -ForegroundColor Red
         exit 1
      }
   })
}

if ($Stop.IsPresent) {
   $ComposeService.ForEach({
      try {
         Write-Host "`nSCRIPT: Stopping $_ server..." -ForegroundColor DarkGreen
         $ServerName = if ($_ -eq "nginx") {"nginx"} else {"apache2"}
         Systemd-Stop -compose_service $_ -systemd_service @($ServerName, "supervisor")
      } catch {
         Write-Host "ERROR: $_" -ForegroundColor Red
         exit 1
      }
   })

   Write-Host "`nSCRIPT: Servers have been stopped.`n`tRun 'docker-compose stop' to stop the containers." -ForegroundColor Blue
} 

