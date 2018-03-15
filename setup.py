'''
setup.py by Sam Weiss (March 2018)

This is a utility to help with the setup and quick initialization of Emulab
experiments. It implements core functions for swapping in experiments, getting
files to them, and executing scripts. I've also included example code of how I
use this functionality
'''

import subprocess
from multiprocessing import Process
import os
import sys
try:
	import paramiko as PM
	from paramiko_helper import SSHSession
except Exception as e:
	print "Please install Paramiko for SSH functionality."
	print "install with: $> pip install paramiko"
	sys.exit(1)

'''
======================= Core functionality =======================
'''

class EmulabUtil:

	def __init__(self, username, ssh_key, emu_certificate, group, project):
		self.username = username
		self.ssh_key = ssh_key
		self.emu_certificate = emu_certificate
		self.group = group
		self.project = project

	# Swap Experiment In: Uses the provided emulab utility to swap an experiment
	# in. In order to make this work it launches a wrapper in a shell and prompts
	# the user for a password. This must be types in for the function to execute
	# successfully. Also please note that it is blocking and will wait until the
	# experiment completely swaps in before returning. This can take a LONG time.
	#
	# TODO: check if the experiment is already swapped in.
	# TODO: check to make sure it swaps in successfully.
	# TODO: use the real bindings instead of launching a shell lol.
	def swap_experiment_in(self):
		self.swap_experiment("in")

	def swap_experiment_out(self):
		self.swap_experiment("out")


	# actual implementation of in/out swapping, don't call this directly.
	def swap_experiment(self, in_out):
		wrapper = os.path.dirname(os.path.realpath(__file__)) + "/lib/script_wrapper.py"

		base_cmd = "{wrapper} --login={login} --cert={cert} swapexp -w -e {group},{project} {swap}"

		complete_cmd = base_cmd.format(wrapper = wrapper,
									   login = self.username,
									   cert = self.emu_certificate,
									   group = self.group,
									   project = self.project,
									   swap=in_out)
		print "Swapping experiment in with the following command: \n" + complete_cmd
		args = [complete_cmd]
		proc = subprocess.Popen(args, 
								stdin=subprocess.PIPE, 
								stdout=subprocess.PIPE, 
								stderr=subprocess.PIPE,
								shell=True)

		stdout, stderr = proc.communicate()
		print stdout
		print stderr



	# upload_with_sftp: upload a set of files from the local machine to an emulab
	# host. The parameters are as follows:
	# 	host: the host you want to upload a file to
	# 	source: the folder on your local machine you want to upload from
	# 	to_move: a list of files you want moved
	# 	destination: the folder on the emulab host you want the files places in
	# Please note that file names are preserved on uploading.
	def upload_with_sftp(self, host, source, to_move, destination):
		hostname = self.get_hostname(host)

		print "uploading to {}".format(hostname)
		
		sftp = SSHSession(hostname = hostname,
						  username = self.username,
						  key_file = open(self.ssh_key, 'r'))

		for file in to_move:
			sftp.put(source + file, destination + file)


	# upload_with_sftp_recursive: upload a folder from the local machine to an
	# emulab host. The parameters are as follows:
	# 	host: the host you want to upload a file to
	# 	source: the folder on your local machine you want to upload
	# 	destination: the folder on the emulab host you want the files placed
	# Please note that file names are preserved on uploading.
	def upload_with_sftp_recursive(self, host, source, destination):
		hostname = self.get_hostname(host)

		print "uploading to {}".format(hostname)
		
		sftp = SSHSession(hostname = hostname,
						  username = self.username,
						  key_file = open(self.ssh_key, 'r'))

		sftp.put_all(source, destination)


	# execute_script_on_server: a convenience function for running bash scripts
	# on an emulab host. This requires that the script already be on the host.
	# the parameters are as follows:
	# 	host: the host you want to upload a file to
	# 	script: fully qualified file name of the script on the host.
	def execute_script_on_server(self, host, script):
		hostname = self.get_hostname(host)
		print "executing {0} on host {1}".format(script, hostname)
		sftp = SSHSession(hostname = hostname,
						  username = self.username,
						  key_file = open(self.ssh_key, 'r'))
		# this helps for some reason, script execution is much less flaky with
		# these extra commands for an unknowable reason.
		sftp.command("pwd")
		sftp.command("ls")
		sftp.command("bash " + script)


	# execute_local_script_on_server: a convenience function for running a local
	# bash scripts on an emulab host.
	# the parameters are as follows:
	# 	host: the host you want to upload a file to
	# 	script: fully qualified file name of the script on the local machine.
	def execute_local_script_on_server(self, host, script):
		tmp_folder = "/tmp"
		# grab the file name
		script_name = script.split("/")[-1]
		source_folder = script.replace(script_name, "")
		# upload to the server
		self.upload_with_sftp(host, source_folder, script_name, tmp_folder)
		hostname = self.get_hostname(host)

		print "executing {0} on host {1}".format(script, hostname)
		sftp = SSHSession(hostname = hostname,
						  username = self.username,
						  key_file = open(self.ssh_key, 'r'))
		# this helps for some reason, script execution is much less flaky with
		# these extra commands for an unknowable reason.
		sftp.command("pwd")
		sftp.command("ls")
		sftp.command("bash " + tmp_folder + script_name)


	# execute_commands_on_server: a convenience function for running a couple
	# commands on an emulab host.
	# the parameters are as follows:
	# 	host: the host you want to upload a file to
	# 	commands: a list of commands to run on the host.
	def execute_commands_on_server(self, host, commands):
		hostname = self.get_hostname(host)
		print "executing {0} on host {1}".format(commands, hostname)
		sftp = SSHSession(hostname = hostname,
						  username = self.username,
						  key_file = open(self.ssh_key, 'r'))
		# this helps (?)
		sftp.command("pwd")
		sftp.command("ls")
		for command in commands:
			sftp.command(command)

	def get_hostname(self, host):
		return "{host}.{project}.{group}.emulab.net".format(host=host,
															project=self.project,
															group=self.group)

'''
======================= User Configuration =======================
'''

repo_location = "/home/musa/mongo"
repo_destination = "/var"

hosts = [
"Client"
"Config",
"Router",
"ShardR1",
"ShardR2",
"ShardR3"
]

cert_info = "/home/musa/.ssl/emulab.pem"
emu_group = "TuftsCC"
emu_project = "mongos"
private_key_location = "/home/musa/.ssh/id_rsa"
username = "sweiss07"
files_to_move = ["/mongod", "/mongos", "/mongo"]

remote_start_server = "/users/sweiss07/setup_server.sh"
setup_database_script = "/users/sweiss07/setup_database.sh"
run_test_scrupt = "/users/sweiss07/run_tests.sh"


'''
======================= Sample Code =======================
'''

# build my project locally so I can just upload the executables
def build_mongo_locally():
	print "building mongo"
	os.chdir(repo_location)
	cmd_base = "python {build} {targets}"
	build = "buildscripts/scons.py"
	targets = "mongod mongo mongos"
	subprocess.check_output(cmd_base.format(build = build,
											targets = targets),
						    shell=True)	

# deploy the executables to all the hosts in parallel
def server_setup(util):
	procs = []

	for host in hosts:
		p = Process(target=do_server_setup, args=(host,util,))
		procs.append(p)
		p.start()

	for proc in procs:
		p.join()

# perform necessary setup on a single host
def do_server_setup(host, util):
	own_cmds = ["sudo chmod 777 /var", "sudo chmod 777 /tmp" "rm -rf /var/mongo*"]
	util.execute_commands_on_server(host, own_cmds)
	util.upload_with_sftp(host, repo_location, files_to_move, repo_destination)
	util.execute_script_on_server(host, remote_start_server)

# initialize the sharded database from the client host
def setup_database(util):
	util.execute_script_on_server("Client", setup_database_script)

# run the necessary tests from the client host
def run_tests(util):
	util.execute_script_on_server("Client", run_test_script)

def main():

	# build before swapping in for niceness
	# build_mongo_locally()

	util = EmulabUtil(username,
					  private_key_location,
					  cert_info,
					  emu_group,
					  emu_project)

	util.swap_experiment_in()

	# server_setup(util)

	# setup_database(util)

	# run_tests(util)

if __name__ == '__main__':
	main()
