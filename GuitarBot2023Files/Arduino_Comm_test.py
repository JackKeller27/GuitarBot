import serial
import time


slider_controller = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.1)
time.sleep(1)
print(slider_controller.read_all().decode())
# data = [('s', 1, 80), ('s', 2, 80), ('s', 3, 80), ('s', 4, 80), ('s', 5, 80), ('s', 6, 80), ('s', 7, 80)]
# data = [('s', 2, 32, 0), ('s', 2, 64, 0), ('s', 3, 96, 0), ('s', 6, 127, 0)]

data = [[2, 2, 3, 1, 2, 3], [4, 5, 6, 6, 5, 4]]
# // playcommand, fretnumbers

# for d in data:
#     for i in range(8):
#         id = 1 << (d[1] - 1)
#         msg = f"{d[0]}{chr(id)}{chr(d[2])}{chr(d[3])}\n"
#         # print(d[0], id, d[2], d[3], msg, end="")
#         slider_controller.write(bytes(msg, encoding='utf-8'))
#         time.sleep(0.051)
#         while (slider_controller.in_waiting > 0):
#             print(slider_controller.readline().decode().strip('\n\r'))

arr = [0] * 12
index = 0
for d in data:
    for i in d:
        arr[index] = i
        index += 1

msg = f"{chr(arr[0])}{chr(arr[1])}{chr(arr[2])}{chr(arr[3])}{chr(arr[4])}{chr(arr[5])}{chr(arr[6])}{chr(arr[7])}{chr(arr[8])}{chr(arr[9])}{chr(arr[10])}{chr(arr[11])}\n"
slider_controller.write(bytes(msg, encoding='utf-8'))
time.sleep(2)


while (slider_controller.in_waiting > 0):
    print(slider_controller.readline().decode().strip('\n\r'))

time.sleep(0.1)

while (slider_controller.in_waiting > 0):
    print(slider_controller.readline().decode().strip('\n\r'))
    time.sleep(0.0011)


slider_controller.close()