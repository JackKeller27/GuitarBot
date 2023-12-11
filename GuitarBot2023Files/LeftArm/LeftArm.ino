
#include "src/logger.h"
#include "src/strikerController.h"

StrikerController* pController = nullptr;

String inputString = "";
bool stringComplete = false;

// the setup function runs once when you press reset or power the board
void setup() {
  delay(2000);
  LOG_LOG("Initializing GuitarBot's sliders...");
  inputString.reserve(10);
  pController = StrikerController::createInstance();
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
  
  if (stringComplete) {
      uint8_t playcommand1;
      uint8_t playcommand2;
      uint8_t playcommand3;
      uint8_t playcommand4;
      uint8_t playcommand5;
      uint8_t playcommand6;
      uint8_t fret1;
      uint8_t fret2;
      uint8_t fret3;
      uint8_t fret4;
      uint8_t fret5;
      uint8_t fret6;

      Error_t err = parseCommand(inputString, playcommand1, playcommand2, playcommand3, playcommand4, playcommand5, playcommand6, fret1, fret2, fret3, fret4, fret5, fret6);
      inputString = "";
      stringComplete = false;
  
      if (err == kNoError) {
          LOG_LOG("playcommand 1: %i, playcommand 2: %i, playcommand 3: %i, playcommand 4: %i, playcommand 5: %i, playcommand 6: %i", playcommand1, playcommand2, playcommand3, playcommand4, playcommand5, playcommand6);
          LOG_LOG("fret 1: %i, fret 2: %i, fret 3: %i, fret 4: %i, fret 5: %i, fret 6: %i", fret1, fret2, fret3, fret4, fret5, fret6);
          //
          pController->executeCommand(1, 's', fret4, 0);
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
          //LOG_LOG("%s", inputString);
      }
  }
}

// Format example to strike using motor 1 with velocity 80: s<SCH>P ... explanation s -> normal slide, <SCH> -> ascii of 0b00000001, P -> ascii of 80
// Pressure is another parameter to map when using choreo
// To stop tremolo, send mode t with velocity 0
Error_t parseCommand(const String& cmd, uint8_t& playcommand1, uint8_t& playcommand2, uint8_t& playcommand3, uint8_t& playcommand4, uint8_t& playcommand5, uint8_t& playcommand6, uint8_t& fret1, uint8_t& fret2, uint8_t& fret3, uint8_t& fret4, uint8_t& fret5, uint8_t& fret6) {
    if (cmd.length() < 13) return kCorruptedDataError;

    playcommand1 = cmd[0];
    playcommand2 = cmd[1];
    playcommand3 = cmd[2];
    playcommand4 = cmd[3];
    playcommand5 = cmd[4];
    playcommand6 = cmd[5];
    fret1 = cmd[6];
    fret2 = cmd[7];
    fret3 = cmd[8];
    fret4 = cmd[9];
    fret5 = cmd[10];
    fret6 = cmd[11];
    return kNoError;
}
