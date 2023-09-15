
String inputString = "";
bool stringComplete = false;

// the setup function runs once when you press reset or power the board
void setup() {

}

// the loop function runs over and over again forever
void loop() {
  int sliderInput[6];
  int presserInput[6];
}

// usable?
void serialEvent() {
    while (Serial.available()) {
        char inChar = (char) Serial.read();
        inputString += inChar;
        if (inChar == '\n') {
            stringComplete = true;
        }
    }
}

// Format example to strike using motor 1 with velocity 80: s<SCH>P ... explanation s -> normal strike, <SCH> -> ascii of 0b00000001, P -> ascii of 80
// Pressure is another parameter to map when using choreo
// To stop tremolo, send mode t with velocity 0
Error_t parseCommand(const String& cmd, char& mode, uint8_t& idCode, uint8_t& midiVelocity, uint8_t& channelPressure) {
    if (cmd.length() < 4) return kCorruptedDataError;

    mode = cmd[0];
    idCode = cmd[1];
    midiVelocity = cmd[2];
    if (cmd.length() == 5) {
        channelPressure = cmd[3];
    }

    return kNoError;
}
