# wi-fi-positioning-app
Application that attempts to approximate user device location on a map of Westminster College campus by scanning nearby Wi-Fi hotspots. Developed to test the possibility of implementing such a system at Westminster College campus given only the existing network infrastructure. 

Utilizes hotspot signal strength data acquired via the Windows WLAN API to calculate relative distances using the free space path loss (FSPL) formula. Then employs a technique called Wi-Fi trilateration, the same underlying technique behind GPS, to approximate user location given these distances.

Unfortunately this project did not yield the desired results, as phone GPS was not accurate enough to record hotspot locations. The FSPL formula also probably needed to be refined a bit to be more accurate, perhaps with the aid of fingerprinting. Given a technology like a dedicated GPS device to log hotspot positions more accurately and the time to implement fingerprinting, I believe this system has a higher liklihood of sucess.

For discussion of results and implementation, please see analysis_and_discussion.pdf
