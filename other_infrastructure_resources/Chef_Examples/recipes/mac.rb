# Cookbook Name:: suricata
# Recipe:: corpmac.rb
#

# Variable Definitions
suropts = node[:suricata]

raise 'No suricata interface defined for this host' if suropts[:interface].nil?
suricata_interface = suropts[:interface]

if suricata_interface.is_a? String
    suricata_interface = [ suricata_interface ]
end

raise 'No suricata rules defined for this host' if suropts[:rules].nil?
rules = suropts[:rules]


# Setup
group 'suricata' do
    gid 683
    action :create
end

user 'suricata' do
    comment 'suricata IDS user'
    gid 683
    shell '/sbin/nologin'
    system true
    action :create
end


# Install Suricata
package "libmagic" do
    action :install
    provider Chef::Provider::Package::Homebrew
end

homebrew_package "suricata" do
    homebrew_user 'user'
    action :install
end


directory '/etc/suricata/' do
    action :create
end


# Set Rules Up
directory '/etc/suricata/rules' do
    action :create
end

template '/etc/suricata/rules/local.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/local.rules.erb'
end

template '/etc/suricata/rules/shellcode.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/shellcode.rules.erb'
end

template '/etc/suricata/rules/osxmalware.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/osxmalware.rules.erb'
end

template '/etc/suricata/rules/nmap.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/nmap.rules.erb'
end

template '/etc/suricata/rules/mobilemalware.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/mobilemalware.rules.erb'
end

template '/etc/suricata/rules/emerging-exploit.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/emerging-exploit.rules.erb'
end

template '/etc/suricata/rules/emerging-shellcode.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/emerging-shellcode.rules.erb'
end

template '/etc/suricata/rules/dshield.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/dshield.rules.erb'
end

template '/etc/suricata/rules/compromised.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/compromised.rules.erb'
end

template '/etc/suricata/rules/tor.rules' do
    mode 0644
    owner 'root'
    group 'wheel'
    source 'mac_os_x/tor.rules.erb'
end


magic_file = '/usr/local/share/misc/magic.mgc'

include_recipe "logrotate::suricata_os_x"

service_name = 'com.host.suricata'

corpmacs = search(:node, 'roles:CorpMacDNS').map { |node| node['ipaddress'] }.sort!

template '/etc/suricata/suricata.yaml' do
    mode 0644
    source 'suricata.yaml.erb'
    variables({:pcapinterface => suricata_interface,
               :rules => rules,
               :magic_file => magic_file,
               :corpmacs => corpmacs})
    notifies :restart, "service[#{service_name}]", :delayed
end

%w[ classification.config reference.config threshold.config ].each do |configfile|
    cookbook_file "/etc/suricata/#{configfile}" do
        source configfile
        mode 0644
        owner 'root'
    end
end


# Setup logging
directory '/var/log/suricata/' do
    owner 'root'
    group 'suricata'
    mode 0775
    action :create
end

logfile_group = 'suricata'
if system('getent group splunk')
  logfile_group = 'splunk'
end


# Start Suricata
service 'com.host.suricata' do
    action [ :start ]
    restart_command "kill -USR2 `cat /var/run/suricata.pid`"
end
