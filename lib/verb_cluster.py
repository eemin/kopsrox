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
config = common.read_kopsrox_ini()
import proxmox_config as kprox

# variables from config
proxnode = (config['proxmox']['proxnode'])
proximgid = (config['proxmox']['proximgid'])
workers = (config['cluster']['workers'])

# this assignment will need to be in config in future
masterid = str(int(proximgid) + 1)

# info
if passed_verb == 'info':
  print('print info about cluster')
 
  # get runningvms
  vms = kprox.prox.nodes(proxnode).qemu.get()
  for vm in vms:
    vmid = vm.get('vmid')
    vmname = vm.get('name')
    vmstatus = vm.get('status')

    # print kopsrox info
    if ((int(vmid) >= int(proximgid)) and (int(vmid) < (int(proximgid) + 9))):
      print(vmid, '-', vmname, vmstatus, 'uptime:', vm.get('uptime'))

      # if vm is running run kubectl
      if ( vmstatus == 'running'):
        print('kubectl')
        kubectl = common.kubectl(vmid, 'get nodes')
        print(kubectl)

  #print(vms)
  exit(0)

# create new cluster
# check for existing install
# check files as well 
if passed_verb == 'create':
  print('creating new kopsrox cluster')

  # get list of runnning vms
  vmids = common.list_kopsrox_vm()

  # handle master install
  if (int(masterid) in vmids):
    print('found existing master vm', masterid)
  else:
    print('creating vmid', masterid)
    common.clone(masterid)

  # install k3s 
  common.k3s_init_master(masterid)

  # create new nodes per config
  print('build', workers, 'workers')
  exit(0)

# destroy
if passed_verb == 'destroy':
  print('destroying cluster')
  vmids = common.list_kopsrox_vm()
  for i in vmids:
      if ( int(i) != int(proximgid)):
        print('destroying vmid', i)
        common.destroy(i)
