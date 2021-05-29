import json
import os
import os.path
import mysql.connector
from requests import get

mail_from = 'sender@gmail.com'
mail_passwd = 'SMTPPassword'
mail_subject = 'L\'IP du NAS a changée'
mail_rcpts = ['email@gmail.com', 'email@outlook.com']

db_host = '127.0.0.1'
db_user = 'dbuser'
db_passwd = 'password'
db_db = 'database'

wordpress_url_name = '/url'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)

# Recuperation de l'adresse IP
response = get('https://ipinfo.io').text
data = json.loads(response)
ip = data['ip']

def write_ip(new_ip):
    f = open(__location__ + '/current.ip', 'w')
    f.write(new_ip)
    f.close()

def send_mail(new_ip):
    f = open(__location__ + '/email.txt', 'w')
    email = "to: "
    cmd = "curl --ssl-reqd --url 'smtps://smtp.gmail.com:465' --user '" + mail_from + ":" + mail_passwd + "' --mail-from '" + mail_from + "' "
    for rcpt in mail_rcpts:
        email += rcpt + ';'
        cmd += "--mail-rcpt '" + rcpt + "' "
    email += "\nfrom: gmail.com\nsubject: L'IP a changee\n\nLa nouvelle adresse IP est: " + new_ip
    f.write(email)
    f.close()
    cmd += "--upload-file " + __location__ + "/email.txt"
    os.system(cmd)

def set_ip_in_wp_config(new_ip):
    print('Modification de la base de donnees de Wordpress')

    # Execution de la requete de modification de l'adresse IP dans Wordpress
    try:
        cnx = mysql.connector.connect(user=db_user, password=db_passwd, host=db_host, database=db_db)
        cursor = cnx.cursor()
        cursor.execute("UPDATE `wp_options` SET `option_value` = 'https://" + new_ip + wordpress_url_name + " WHERE `option_name` IN ('siteurl', 'home')")
        cnx.commit()
    except mysql.connector.Error as err:
        print("Erreur dans la modification de la base de donnees de Wordpress: {}".format(err))
    cnx.close()

# Verification de l'ancienne adresse
# Si la nouvelle adresse est differente, envoi d'un mail pour prevenir du changement d'IP
if os.path.isfile(__location__ + '/current.ip'):
    f = open(__location__ + '/current.ip', 'r')
    current_ip = f.read()
    f.close()
    if ip != current_ip:
        print('L\'IP a changee, Envoi d\'un mail')
        send_mail(ip)
        write_ip(ip)
        set_ip_in_wp_config(ip)
else:
    print('Le fichier d\'IP n\'existe pas. Creation du fichier...')
    write_ip(ip)

