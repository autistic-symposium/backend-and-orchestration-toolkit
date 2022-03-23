# Cookbook Name:: suricata
# Recipe:: centos
#

# Variable Definitions
suropts = node[:suricata]

suricata_interface = suropts[:interface]

# Do we have multiple interfaces to listen on?
if suricata_interface.is_a? String
	suricata_interface = [ suricata_interface ]
end

raise 'No suricata rules defined for this host' if suropts[:rules].nil?
rules = suropts[:rules]


# Setup
yum_package 'libcap-ng'

yum_package 'libhtp'

%w[ libmnl libnetfilter_queue ].each do |pkg|
    yum_package pkg
end


# Install Suricata
yum_package 'suricata' do
    notifies :restart, 'service[suricata]', :delayed
end

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

if node[:platform_version][0] == '6'
    template '/etc/init.d/suricata' do
      mode 0555
      owner 'root'
      group 'root'
      source 'suricata.init.erb'
      variables({:interface => suricata_interface})
    end
else
    template '/etc/systemd/system/suricata.service' do
      mode 0444
      owner 'root'
      group 'root'
      source 'suricata.service.erb'
      variables({:interface => suricata_interface})
    end
end

cookbook_file '/etc/logrotate.d/suricata' do
      source 'suricata_logrotate'
      owner 'root'
      group 'root'
      mode 0644
end

# Set Rules Up
directory '/etc/suricata/rules' do
    action :create
end

# Need to create these rules when time comes.
#template '/etc/suricata/rules/local.rules' do
#    mode 0644
#    owner 'root'
#    group 'wheel'
#    source 'centos/local.rules.erb'
#end


# Set and configurate Suricata for centos
magic_file = '/usr/share/file/magic'

service_name = 'suricata'

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

%w[ fast.log  outputs.log  suricata.log tls.log eve.json ].each do |logfile|
      file "/var/log/suricata/#{logfile}" do
          mode 0640
          owner 'suricata'
          group logfile_group
      end
end


# Start Suricata
service 'suricata' do
      supports :status => true, :restart => true, :reload => true
      action [ :enable, :start ]
end
