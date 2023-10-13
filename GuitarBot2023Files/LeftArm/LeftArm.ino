
#include "src/logger.h"
#include "src/sliderController.h"

SliderController* pController = nullptr;

String inputString = "";
bool stringComplete = false;

// the setup function runs once when you press reset or power the board
void setup() {
  LOG_LOG("Initializing GuitarBot's sliders...");
  inputString.reserve(10);
  pController = SliderController::createInstance();
  int err = pController->init(MotorSpec::EC45);
  if (err != 0) {
      LOG_ERROR("Controller Init failed");
      return;
  }

  LOG_LOG("Successfully Initialized! Controller Starting...");
  pController->start();
  delay(75);
  LOG_LOG("Listening for commands...");   // "in format (ascii characters) < >< >< >"
}

// the loop function runs over and over again forever
void loop() {
  // delay(1000);
  // uint8_t idCode = 1;
  // uint8_t midiVelocity = 80;
  // uint8_t chPressure =1;
  // char cMode = 0;
  // LOG_LOG("mode %c, idCode: %i, velocity: %i, pressure: %i", cMode, idCode, midiVelocity, chPressure);
  // pController->executeCommand(idCode, cMode, midiVelocity, chPressure);
  

  if (stringComplete) {
        // LOG_LOG("%s", inputString);
        uint8_t idCode;
        uint8_t midiVelocity;
        uint8_t chPressure;
        char cMode;
        Error_t err = parseCommand(inputString, cMode, idCode, midiVelocity, chPressure);
        inputString = "";
        stringComplete = false;

        if (err == kNoError) {
            LOG_LOG("mode %c, idCode: %i, velocity: %i, pressure: %i", cMode, idCode, midiVelocity, chPressure);
            pController->executeCommand(idCode, cMode, midiVelocity, chPressure);
        }
    }
}

//reads info from Arduino to parse a command
void serialEvent() {
  while (Serial.available()) {
      char inChar = (char) Serial.read();
      inputString += inChar;
      if (inChar == '\n') {
          stringComplete = true;
      }
  }
}

// Format example to strike using motor 1 with velocity 80: s<SCH>P ... explanation s -> normal slide, <SCH> -> ascii of 0b00000001, P -> ascii of 80
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