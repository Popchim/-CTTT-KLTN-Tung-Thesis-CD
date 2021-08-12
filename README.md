**Thesis full title	: A secure, scalable, FOTA-capable, home automation IoT system to control fan and air-conditioner electronics**

Contact Info

	Full name	: Nguyen thanh Tung
	Mobile phone	: 07.07.07.6350
	Email		: gooooogle1503@gmail.com

Directory Guide

	o root
		|-> o A_secure_scalable_FOTA_capable_IoT_system_to_control_fan_and_AC
		|	||-> I.   APP 
		|	||-> II.  SOURCE
		|	||-> III. LIB
		|-> IV. THESIS
		|-> V.  REF

**I. APP**			

	Contains the applications we used in our thesis
		|-> 1. raspbian	
		|-> 2. upython
		|-> 3. nodered
		|-> 4. mosquitto
		|-> 5. network
		|-> 6. openssl
		
**1. raspbian**		: Contains the tool to install Raspbian OS on a Raspberry Pi 4 hardware, where the other tools will run on

**2. upython**		: Contains the tool to flash the MicroPython runtime on a ESP32 hardware, plus tools to communicate with the ESP32 hardware serially

**3. nodered**		: Contains the Node-red flow-based visual programming tool

**4. mosquitto**	: Contains the mosquitto MQTT broker Linux utility

**5. network**		: Contains the LAN configuration Linux utilities

**6. openssl**		: Contains the tool to generate and verify TLS cryptographic keys and certificates

****

**II. SOURCE**

	Contains the source code, scripts, configuration files we composed and used with the applications in APP
		|-> 1. upython
		|-> 2. nodered
		|-> 3. mosquitto
		|-> 4. network
		|-> 5. openssl
		
**1. upython**		: Contains the MicroPython source code

**2. nodered**		: Contains the Node-red main flow, user modules and setting file

**3. mosquitto**	: Contains the setting files for the mosquitto utility

**4. network**		: Contains the setting files for Linux network utilities

**5. openssl**		: Contains the generated TLS private keys and public certificates of local CA and machine

****

**III. LIB**

	Contains the imported libraries to be used with the applications in APP
			|-> 1. nodered
			
**1. nodered**		: additional library dependencies to be imported in Node-red

****

**IV. THESIS**

	Contains the thesis paper and presentation slides
			|-> 1. DOC
			|-> 2. PDF
			|-> 3. SLIDES
			
**1. DOC**		: Contains the thesis in DOCX format

**2. PDF**		: Contains the thesis in PDF format

**3. SLIDES**		: Contains the presentation slides

****

**V. REF**

	Contains the papers and books we referenced in our thesis
			|-> o  [1-45].pdf
			|-> 1. INDEX.pdf
			
****
			
**1. INDEX.pdf**		: Please use this file to look up the numbered references
