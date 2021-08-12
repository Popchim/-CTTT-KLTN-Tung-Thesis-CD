Contact Info
	Full name	: Nguyen thanh Tung
	Mobile phone	: 07.07.07.6350
	Email		: gooooogle1503@gmail.com

Directory Guide
	o root
		|-> o A_secure_scalable_FOTA_capable_IoT_system_to_control_fan_and_AC
		|	||-> o APP 
		|	||-> o SOURCE
		|	||-> o LIB
		|	||-> o DATASET
		|-> o THESIS
		|	||-> o DOC
		|	||-> o PDF
		|	||-> o SLIDE
		|-> o REF
		|-> o SOFT

Thesis full title	: A secure, scalable, FOTA-capable, home automation IoT system to control fan and air-conditioner electronics
------------------------------------------------------------------------------------------------------------------------------------------------------------
*/APP			: Contains the applications we used in our thesis
			|-> o raspbian	
			|-> o upython
			|-> o nodered
			|-> o mosquitto
			|-> o network
			|-> o openssl
*/APP/raspbian		: Contains the tool to install Raspbian OS on a Raspberry Pi 4 hardware, where the other tools will run on
*/APP/upython		: Contains the tool to flash the MicroPython runtime on a ESP32 hardware, plus tools to communicate with the ESP32 hardware serially  
*/APP/nodered		: Contains the Node-red flow-based visual programming tool 
*/APP/mosquitto	: Contains the mosquitto MQTT broker Linux utility
*/APP/network		: Contains the LAN configuration Linux utilities
*/APP/openssl		: Contains the tool to generate and verify TLS cryptographic keys and certificates
------------------------------------------------------------------------------------------------------------------------------------------------------------
*/SOURCE		: Contains the source code, scripts, configuration files we composed and used with the applications in APP
			|-> o upython
			|-> o nodered
			|-> o mosquitto
			|-> o network
			|-> o openssl
*/SOURCE/upython	: Contains the MicroPython source code
*/SOURCE/nodered	: Contains the Node-red main flow, user modules and setting file
*/SOURCE/mosquitto	: Contains the setting files for the mosquitto utility
*/SOURCE/network	: Contains the setting files for Linux network utilities
*/SOURCE/openssl	: Contains the generated TLS private keys and public certificates of local CA and machine
------------------------------------------------------------------------------------------------------------------------------------------------------------
*/LIB			: Contains the imported libraries to be used with the applications in APP
			|-> o nodered
*/LIB/nodered		: additional library dependencies to be imported in Node-red
------------------------------------------------------------------------------------------------------------------------------------------------------------
*/DATASET		: BLANK (not in use)
------------------------------------------------------------------------------------------------------------------------------------------------------------
root/THESIS/DOC	: Contains the thesis in DOCX format
root/THESIS/PDF	: Contains the thesis in PDF format
root/THESIS/SLIDES	: Contains the presentation slides
------------------------------------------------------------------------------------------------------------------------------------------------------------
root/REF		: Contains the papers and books we referenced in our thesis
			|-> o 1.pdf
			|-> ..
			|-> o 45.pdf
			|-> o INDEX.pdf
INDEX.pdf		: Please use this file to look up the numbered references
------------------------------------------------------------------------------------------------------------------------------------------------------------
root/SOFT		: Has the same content as APP
