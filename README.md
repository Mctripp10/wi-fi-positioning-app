# Wi-Fi Positioning App
Wi-Fi positioning system that approximates user device location on a map using signal strength from nearby Wi-Fi access points.

# Motivation
I had always wondered if there was a way to determine how close you were in relation to Wi-Fi access points based solely on signal strength. The stronger the signal, the closer you should be, right? Well, while there is a relationship between signal strength and distance, it is not perfectly linear (more details on that below). Taking this idea, I wanted to test the possibility of implementing my very own Wi-Fi positioning system at my college campus given only the existing network infrastructure. 

# Method
There are many ways to implement a Wi-Fi positioning system. As I was required to use only the technologies available to me already on campus, my approach relied heavily on access point signal strength:
1. Utilizes hotspot signal strength data acquired via the Windows WLAN API to calculate relative distances using the free space path loss (FSPL) formula
2. Employs a technique called Wi-Fi trilateration, the same underlying technique behind GPS, to approximate user location given these distances

# Results

Unfortunately, this project did not yield the desired results, as phone GPS was not accurate enough to record hotspot locations. The FSPL formula also probably needed to be refined a bit to be more accurate, perhaps with the aid of fingerprinting. Given a technology like a dedicated GPS device to log hotspot positions more accurately and the time to implement fingerprinting, however, I believe this system has a high liklihood of success.

For discussion of results and implementation, please see analysis_and_discussion.pdf
