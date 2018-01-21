def getStoreApps():
  from subprocess import Popen, PIPE, STDOUT
  import re
  
  result = {}
  cmd = 'powershell Get-StartApps'
  p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
  output = p.stdout.read()
  for line in output.split("\n"):
    print line
    if line.strip() == "" or line.startswith("Name") or line.startswith("----"):
      print "in continue"
      continue
    for c in line:
      print [c]
    re.search('(\w+)', line)
    temp = line.split('  ')
    print temp
    name = temp[0]
    executable = temp[-1]
    print "exec" + executable
    winName = executable.split("_")[0]
    print "winName" + winName
    cmd = 'powershell Get-AppxPackage -Name "'+winName+'"'
    print cmd
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.stdout.read()
    packageName = ""
    installLocation = ""
    for entry in output.split("\n"):
      print entry
      if entry.strip() != "":
        temp = entry.split(": ")
        key = temp[0].strip()
        value = temp[1]
        if key == "PackageFullName":
          packageName = value
        if key == "InstallLocation":
          installLocation = value
    icon = ""
    if packageName != "":
      cmd = "powershell (Get-AppxPackageManifest -package \""+packageName+"\").package.applications.application.visualelements.Square150x150Logo"
      p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
      output = p.stdout.read()
      icon = installLocation + "\\" + output
    entry = {}
    entry["name"] = name
    entry["exec"] = "explorer shell:AppsFolder\\"+executable
    entry["icon"] = icon
    entry["type"] = "app"
    result[name] = entry
  return result