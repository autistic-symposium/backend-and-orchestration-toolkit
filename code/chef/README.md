# resources on chef 

<br>

## Suricata Chef Cookbook 

This cookbook installs and configures Suricata.

## Usage

### suricata::default

*  include `suricata` in your node's `run_list`:

```json
{
  "name":"my_node",
  "run_list": [
    "recipe[suricata]"
  ]
}
```

