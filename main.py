import json
import re
from Model1 import Model1
from Model2 import Model2

model1 = Model1()
model1.build()

model2 = Model2()
model2.build()

print(model2.search("scuze"))
print(model1.check_word("deinitie", patience = 0))

