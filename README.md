# FTwitter

FTwitter is a tool written in Python used to obtain urls to images posted in user Fleets. All information required to create this app was obtained with reverse engineering.

# Table of contents
* [How it works](#how-it-works)
  * [How to use](#how-to-use)
  * [What can go wrong](#what-can-go-wrong)
* [How to get oauth token with Mitmproxy](#how-to-get-oauth-token-with-mitmproxy)
  * [Installing Android emulator](#installing-android-emulator)
  * [Installing proxy certificate](#installing-proxy-certificate)
  * [Setting up Frida server](#setting-up-frida-server)
  * [Sniffing on the traffic](#sniffing-on-the-traffic)

# How it works?

FTwitter pretends to be an official Twitter for Android mobile app. Then it sends GET request to /fleets/v1/user_fleets endpoint and prints out urls in the response JSON.

For it to work I had to use [(un)official Consumer Keys](https://gist.github.com/shobotch/5160017) and sniff on the App's traffic to get the required headers.

## How to use

First you must clone this repository

```bash
git clone https://github.com/szymonorz/ftwitter.git
```

For it work you need Python 3.0+ and pip installed.

First install required packages.
```bash
pip install -r requirements.txt
```

Then run fleets.py
```bash
python3 ftwitter.py
```

You will be meet with this prompt
```bash
ftwitter>
```

Before any other action (except 'exit') you first must log in. Do it by typing 'login' or 'l'
```bash
ftwitter> l
Oauth token not present.
Oauth token not present
Initiating login....
Login: username
Password: password
```
If you put your credentials correctly, you should be met with
```bash
<Response [200]>
oauth_token_key: 123456-oauth-token
oauth_token_secret: IaMASecRet12356
Copy your oauth_token and secret and write them into the file
then you won't have to go through the login process again in the future
```
Now you can start using 'get' commands. For now there are only two options: 'fleets' (or 'f') and 'blockedby' (or 'bb').
'fleets' require you to put in user_id or @ handle.
```bash
ftwitter> get f 12
```
or
```bash
ftwitter> get f jack
```
If such user exists and everything went correctly you should be met with with url's to that user's Fleets.
``bash
<Response [200]>
[url's of Fleets]
```

After that save `oauth_token` and `oauth_token_secret` inside `ftwitter.py`.
```python
.
.
oauth_token_key="" #Put your oauth_token inside these brackets
oauth_token_secret="" #Put your oauth_token_secret inside these brackets
.
.
```
## What can go wrong?

During login you can get two kinds of wrong messages (except the one where you put incorrect login or password).

You may get
```
<Response [200]>
{'login_verification_request_id': 'y7r8vIJ6CdGYqEuIYoUcoXnmbp4XxfKh7lih0M', 
'login_verification_user_id': 1338078861486149632, 
'login_verification_request_url': 'https://twitter.com/account/login_challenge
?platform=mobile&user_id=1338078861486149632
&challenge_type=TemporaryPassword&
challenge_id=y7r8vIJ6CdGYqEuIYoUcoXnmbp4XxfKh7lih0M', 
'login_verification_request_type': 3,
 'login_verification_request_cause': 2}
```

That means Twitter thinks your account is suspicious. Simply logout and login into your account in your webrowser or mobile app. You will probably have to verify your account with a verification code. 
After you got that, you should be able to login normaly using `ftwitter.py`. If not, check [How to get oauth token with Mitmproxy]().

The second type of message would be
```
{'errors':[{'code':243,'message':'User is over the limit for
login attempts. Please try again in a n hour'}]}
```

That means your IP got blocked by Twitter because you've sent a lot of failed login requests :^). If you got this error, either wait for few days (I got my IP unblocked after 3 days) or check [How to get oauth token with Mitmproxy]().

# How to get oauth token with Mitmproxy

Considering you're there, you're probably IP blocked from the login endpoint. But fear not, I'm here to help you, poor creature.

For this to work you need [Frida](https://frida.re/docs/installation/) and [Mitmproxy](https://mitmproxy.org/) installed. You don't necessarily need to use Mitmproxy, you can also use either [Fiddler](https://www.telerik.com/download/fiddler) or [Burp proxy](https://portswigger.net/burp/communitydownload) but in this guide we'll be using mitmproxy.

You'll also need an Android emulator. The easiest way to get one is to install [Android Studio](https://developer.android.com/studio) and create one with AVD Manager.

Since I'm on Arch Linux (and have no idea how Windows works) I will be showing how to do this from Linux perspective, but here are some links to articles where they do the same thing but on Windows:
 * [Tutorial on bypass for SSL pinning](https://infosecwriteups.com/hail-frida-the-universal-ssl-pinning-bypass-for-android-e9e1d733d29)


First install required software
```bash
sudo pip install frida-tools
sudo pacman -S mitmproxy
```
## Installing Android emulator

I'm gonna assume you've already installed Android Studio.

### Step 1. Launch Android Studio
![Android Studio welcome screen](https://i.imgur.com/GViTtr8.png)
### Step 2. Open AVD Manager
Click on `Configure` in bottom-left corner and then choose `AVD Manager`
![Click on AVD Manager from the drop-down list](https://i.imgur.com/v7YC1Q8.png)
### Step 3. Create your Android emulator
Now create your android device. I don't think it really matter what kind of device you'll choose but I went with Pixel 4XL
![Pixel XL](https://i.imgur.com/3DtcIC8.png)

Then choose your preferred Android version. We'll go with Android Oreo. You will probably how to download it so it's going to take you some time.
![Choose Android Oreo](https://i.imgur.com/Cc0Vzp7.png)

### Step 4. Launch emulator
Just click on the green arrow next to your emulator (I highlighted the one we just created).
![Click on the green arrow](https://i.imgur.com/mzxCju8.png)

## Installing proxy certificate

### Step 1. Launch mitmproxy in terminal

We'll launch it on port 8080

```bash
mitmproxy -p 8080
```

### Step 2. Configure emulator to use our proxy
Click the 3 dots next to the emulator, then go `Settings->Proxy`.
Uncheck `Use Android Studio HTTPS proxy settings` and check `Manual proxy configuration`. Put `127.0.0.1` in `Host name` and `8080` in port number.

![](https://i.imgur.com/mmy78D9.png)

### Step 3. Download certificate

Open Google Chrome and then go to `mitm.it`. You can only access it if you have mitmproxy running and your emulator configured to be connected to it. 
![mitm.it](https://i.imgur.com/7GZWIww.png)

Then scroll down and choose `Get mitmproxy-ca-cert.cer` under Android logo.

![Choose the one next to Android logo](https://i.imgur.com/4W1Que1.png)

### Step 4. Install certificate

Installation is pretty simple, just follow with the steps. You'll have to setup a security PIN (don't choose `Fingerprint + PIN` option if you'll be asked to. Just choose `No fingerprint` and then `PIN`)

![name it cacert](https://i.imgur.com/RWDCfiD.png)

![click ok and setup security PIN](https://i.imgur.com/JjQTJyO.png)

Click ok and setup your PIN. Make it something simple like `0000`.
We don't really care about security of this emulator since we'll using it only for sniffing on traffic.

After it is installed you should get a popup at the bottom that reads `cacert is installed`.

![Toast with cacert is installed](https://i.imgur.com/3GFlDoa.png)

You should start seeing traffic in your mitmproxy. Visit any website in browser e.g. facebook

![traffic in mitmproxy](https://i.imgur.com/zGUhsHD.png?1)

![facebook endpoint](https://i.imgur.com/shocWRv.png)

## Setting up Frida server

Now here comes the big boy.
Make sure your PATH variable is correctly set up because you need access to `adb` from Android tools. You can install it independently
```bash
sudo pacman -S adb
```
or add it to yout PATH variable

(the path to adb directory is different on Windows, don't do this line if you're using [Windows](https://www.xda-developers.com/install-adb-windows-macos-linux/))
```bash
export PATH=~/Android/Sdk/platform-tools:$PATH
```
if you want to use `adb` on a daily basis you should add the line above to your `~/.bashrc` file.

Now you will input a set of commands
```bash
cd frida-tools/
adb root
adb shell cp /sdcard/Download/mitmproxy-ca-cert.cer /data/local/tmp/cert-der.crt

adb push frida-server /data/local/tmp
adb push frida-ssl-bypass.js /data/local/tmp
adb shell chmod 777 -R /data/local/tmp
adb shell /data/local/tmp/frida-server &
adb install twitter.apk
```
You need to aquire `twitter.apk` by yourself either from APKPure or APKMirror.
If at any point you've got `Permission denied` that means you've probably forgot to run `adb root` or you've set incorrect permissions on `/data/local/tmp`. 

Now wait for the apk to install and then launch it.

Then run
```bash
frida-ps -U
```
and you should notice `com.twitter.android` be listed.

![com.twitter.android](https://i.imgur.com/r5bABLe.png)

Now you are ready to launch the script.
```bash
frida -U -f com.twitter.android -l frida-ssl-bypass.js --no-paus
```

The result should look like this:
```bash
Spawned `com.twitter.android`. Resuming main thread!                    
[Android Emulator 5554::com.twitter.android]->
[.] Cert Pinning Bypass/Re-Pinning
[+] Loading our CA...
[o] Our CA Info: O=mitmproxy, CN=mitmproxy
[+] Creating a KeyStore for our CA...
[+] Creating a TrustManager that trusts the CA in our KeyStore...
[+] Our TrustManager is ready...
[+] Hijacking SSLContext methods now...
[-] Waiting for the app to invoke SSLContext.init()...
[o] App invoked javax.net.ssl.SSLContext.init...
[+] SSLContext initialized with our custom TrustManager!
[o] App invoked javax.net.ssl.SSLContext.init...
[+] SSLContext initialized with our custom TrustManager!
```

### Important!!!
If your script is stuck at
```bash
[-] Waiting for the app to invoke SSLContext.init()...
```

DO NOT attempt to login. Simpy restart shut down the emulator, activate it again, run
```bash
adb root
adb shell /data/local/tmp/frida-server &
```
and then launch the script again.
Repeat it untill you get
```bash
[o] App invoked javax.net.ssl.SSLContext.init...
[+] SSLContext initialized with our custom TrustManager!
```

Attempting to log in without the message above may result in your IP being blocked for few days.

Assuming everything went correctly you should start seeing traffic to appear in mitmproxy (Twitter's IP address is 104.244.42.66).

## Sniffing on the traffic

Now here you've got two options, depending on your situation.

If you've got IP banned you need to create new account and then look for POST request from endpoint /oauth/access_token.

You can also use a VPN and log in into already existing account but then you will be asked to verify your account with a code that  will be sent to you via email. After that you should also look for the same endpoint.

However if you logged in into already existing account and didn't have to verify your account you need to look for a POST request from /auth/1/xauth_password.json.

![xauth_password.json](https://imgur.com/pOLYUCg)

Click on the request and click on `Response`. You should see something like this
![JSON Response with all the headers and you oauth values at the bottom](https://i.imgur.com/E40qK9w.png)

Headers may differ based on what request you're looking at.
Now press `q` on your keyboard, then press `e` and something like this should pop-up

![List of all the available parts](https://i.imgur.com/PiXafsa.png)

Press `down arrow` key until you get to `raw` then press `Enter` and `export raw @focus` should appear in the bottom bar.
Input the name of the file to which you want to write the response and press `Enter`.
I named mine `my_resp.txt`.

![export raw @focus my_resp.txt](https://i.imgur.com/fspkgPW.png)

You can make sure that this file was created.
Now all you need to do is open it in text editor of your choice, scroll down to the very bottom of the file and there will be your
`oauth_token` and `oauth_token_secret`

![](https://i.imgur.com/nG66Jvn.png)

Copy those values and put them in `ftwitter.py`

```python
.
.
oauth_token_key="" #Put your oauth_token inside these brackets
oauth_token_secret="" #Put your oauth_token_secret inside these brackets
.
.
```
