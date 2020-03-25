# ipx800
Package Homeassistant pour contrôler le module IPX800v4 de GCE-Electronics 

## Utilisation

Dans le fichier configuration.yaml :

```yaml
	ipx800:
		host: 192.168.1.106
		port: 80
		api_key: apikey
```

Dans le fichier sensor.yaml :
```yaml
	- platform: ipx800
	  enabled_counters:
	  - 1 # comment
	  - 2 
	  enabled_analogs:
	  - 1 
	  enabled_virtualanalogs: 
	  - 17 
```
Dans le fichier light.yaml :
```yaml
	- platform: ipx800
	  enabled_virtualanalogs: 
	  - 17
```
Dans le fichier switch.yaml :
```yaml
	- platform: ipx800
	  enabled_relays: 
	  - 1
	  - 2
	  enabled_virtualinputs: 
	  - 1
	  - 2
	  enabled_virtualoutputs: 
	  - 1
```

## Information de licence

[Lire la licence](LICENSE)

