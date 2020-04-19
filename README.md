# NotifyIPChange
A python script that notifies the change of server local IP address via email.
For Windows users, you can find the executable in [release](https://github.com/BlackNight95/NotifyIPChange/releases).

# Usage
Change filename `config_template.yaml` to `config.yaml` and make sure that it is in the same directory as the python script. Set up your own configurations and run the script.

# Configuration
* `computer_name`: define the name of your computer here (optional)
* `server`: SMTP sever of your email servive
* `port`: SMTP port of your email servicve
* `password`: password for your email account
* `from`: your email adress
* `to`: destination of the message

Some email service providers:
|Mail|SMTP Server|Port|Password|
|:----:|:----:|:----:|:----:|
|QQ|smtp.qq.com|587|authentication code|
|163|smtp.163.com|25|authentication code|
|126|smtp.126.com|25|authentication code|
|Gmail|smtp.gmail.com|587|user password|
|Tsinghua|mails.tsinghua.edu.cn <br> mail.tsinghua.edu.cn|25|user password|

* For security and privacy reasons, the `passcode`, `from` and `to` configs are able to use environment variables. 
* For authentication code, you need to get it from your email service provider (normally can be found in your personal account settings).
* For gmail, you may need to turn on [this](https://www.google.com/settings/security/lesssecureapps) safety feature.

