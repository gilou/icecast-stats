Quick and dirty script to grab all information from the default icecast status.xsl page, and sum up all the listeners given a common mountname structure (i.e. radio-mp3 radio-aac radio-blah...)

Output is done in JSON for now, just to try a few possibilities

It is written in Python3, and requires dnspython (dnspython3 in pip) joblib and libxml (lxml). six is needed as well for...
It should work in Python2 (dnspython joblib lxml) using the six module.

Usage: ./netradio.py
