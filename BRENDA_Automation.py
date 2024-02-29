#!/usr/bin/python
from zeep import Client
import hashlib
password = "Gbnclo*252BKey"

wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
password = hashlib.sha256("myPassword".encode("utf-8")).hexdigest()
client = Client(wsdl)

parameters = ("john.docter@colorado.edu",password)
resultString = client.service.getEcNumbersFromInhibitors(*parameters)
print(resultString)