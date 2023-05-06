import common_config as common, sys, os, wget, re, time, urllib.parse
verb = 'cluster'
verbs = common.verbs_cluster

# check for arguments
try:
  if (sys.argv[2]):
    passed_verb = str(sys.argv[2])
except:
  print('ERROR: pass a command')
  print('kopsrox', verb, '', end='')
  common.verbs_help(verbs)
  exit(0)

# unsupported verb
if not passed_verb in verbs:
  print('ERROR: \''+ passed_verb + '\'- command not found')
  print('kopsrox', verb, '', end='')
  common.verbs_help(verbs)
  exit(0)

# import config
config = common.read_kopsrox_ini2()
import proxmox_config as kprox
#print(config)

# variables from config
proxnode = (config['proxmox']['proxnode'])
proximgid = (config['proxmox']['proximgid'])
workers = (config['cluster']['workers'])

# this assignment will need to be in config in future
masterid = str(int(proximgid) + 1)

# info
if passed_verb == 'info':
    print('print info about cluster')
    
    vms = kprox.prox.nodes(proxnode).qemu.get()
    #common.task_status(kprox.prox, vms, proxnode)
    for vm in vms:
        vmid = vm.get('vmid')
        vmname = vm.get('name')

        # print kopsrox info
        if ((int(vmid) >= int(proximgid)) and (int(vmid) < (int(proximgid) + 9))):
          #print(vm)
          print(vmid, '-', vmname, vm.get('status'), 'uptime:', vm.get('uptime'))

    #print(vms)
    exit(0)

# create
if passed_verb == 'create':
    print('create')

    # lets assume masters will always be 1 for now
    # check for masterid
    if kprox.prox.nodes(proxnode).qemu(masterid).status.get():
        print('ERROR: existing master node found id', masterid)
 #      common.qaexec(masterid, 'ls')
        exit(0)


    print(masterid, 'not found')
    common.clone(masterid)
   
    # create new nodes per config
    print('build', workers, 'workers')
    exit(0)
