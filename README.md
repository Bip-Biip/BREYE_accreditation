# BREYE_accreditation

Ce dépôt répertorie tous les tests à passer pour certifier qu'un prototype de Br'Eye est fonctionnel.

## Préparer l'environnement de Br'eye

Considérons une Raspberry PI 4 avec un environnement Raspbian nouvellement installé.

Commençons par installer le text to speech ainsi que les principales bibliothèques Python.

Pour cela, exécutons dans le terminal les commandes suivantes :

```
sudo apt-get install python3-rpi.gpio
sudo pip3 install adafruit-circuitpython-fingerprint
sudo pip3 install adafruit-circuitpython-max9744
sudo pip3 install adafruit-circuitpython-pn532
sudo pip3 install pygame
sudo pip3 install getmac
```

Une fois ceci fait, il faut configurer correctement la Raspberry.
Entrons pour cela dans le menu de configuration : `sudo raspi-config`

Sélectionnons **Interfacing Options** puis **I2C** et **Yes**

Sélectionnons **Interfacing Options** puis **Serial** et **No** puis **Yes**

Vérifions maintenant si l'UART est désactivé, si oui, nous devrons le réactiver.
Ouvrons le fichier */boot/config.txt* et vérifions la ligne *enable_uart*.
Si nous avons `enable_uart=0` remplaçons-là par `enable_uart=1`

Enfin, redémarrons la Raspberry.

PS : ne pas oublier d'autoriser VNC pour la connexion à distance.
