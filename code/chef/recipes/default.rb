#
# Cookbook Name:: suricata
# Recipe:: default
#

suropts = node[:suricata]

raise 'No suricata interface defined for this host' if suropts[:interface].nil?
suricata_interface = suropts[:interface]

# Do we have multiple interfaces to listen on?
if suricata_interface.is_a? String
  suricata_interface = [ suricata_interface ]
end

# The list of rules to populate the yaml config with.
raise 'No suricata rules defined for this host' if suropts[:rules].nil?
rules = suropts[:rules]

case node[:platform]
when 'centos'
  include_recipe 'suricata::centos'
else
  include_recipe 'suricata::corpmac'
end
