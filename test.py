import modules.objectLib as ol
from classes.Priority import Priority
from classes.EditType import EditType
from time import sleep

db=ol.dbSelfHost()

print("Rozpoczynanie testu jednostkowego:")
sleep(1)
print("Testowana klasa: EditType(enum)")
print("Tworzenie instancji")
test = EditType.DESC
sleep(1)
print("Oczekiwana wartość = 2")
print("Wynik=", test.value)
sleep(1)
if test.value == 2:
    print("[OK]\n")
else:
    print("[Blad]\n")
sleep(1)
print("Testowana klasa: Priority(enum)")
print("Tworzenie instancji")
test = Priority.HIGH
sleep(1)
print("Oczekiwana wartość = 1")
print("Wynik=", test.value)
sleep(1)
if test.value == 1:
    print("[OK]\n")
else:
    print("[Blad]\n")

sleep(1)
print("Testowana klasa: Task")
print("Tworzenie instancji")
test = ol.createTask("test","test",Priority.HIGH.value,db)
sleep(1)
if isinstance(test,int):
    print("Wynik=", ol.getTask(test,db))
    print("[OK]")
else:
    print("Wynik=", test)
    print("[Blad]")
sleep(1)
print("Zmiana pola complete")
status = ol.editTask(test,EditType.COMPL,True,db)
sleep(1)
if status==0:
    print("Wynik=", ol.getTask(test,db))
    print("[OK]")
else:
    print("Wynik=", ol.getTask(test,db))
    print("[Blad]")
sleep(1)
print("Usuwanie instancji")
status = ol.deleteTask(test,db)
sleep(1)
if status==0:
    print("Wynik= ok")
    print("[OK]")
else:
    print("Wynik=", ol.getTask(test,db))
    print("[Blad]")
sleep(1)
print("Tworzenie instancji z błędnymi danymi")
test = ol.createTask(1,1,Priority.HIGH,db)
sleep(1)
if not isinstance(test,int):
    print("Wynik=", test)
    print("[OK]\n")
else:
    print("Wynik=", ol.getTask(test,db))
    print("[Blad]\n")