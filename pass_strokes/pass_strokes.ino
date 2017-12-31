#include <hidboot.h>
#include <usbhub.h>
#include <SPI.h>

class Parser: public KeyboardReportParser {
  protected:
    void OnControlKeysChanged(uint8_t before, uint8_t after);
    void OnKeyDown(uint8_t mod, uint8_t key);
    void OnKeyUp(uint8_t mod, uint8_t key);
};

void Parser::OnControlKeysChanged(uint8_t before, uint8_t after) {
  Serial.write(2);
  Serial.write(after);
};

void Parser::OnKeyDown(uint8_t mod, uint8_t key) {
  Serial.write(0);
  Serial.write(key);
};

void Parser::OnKeyUp(uint8_t mod, uint8_t key) {
  Serial.write(1);
  Serial.write(key);
};

USB Usb;
HIDBoot<USB_HID_PROTOCOL_KEYBOARD> HidKeyboard(&Usb);
Parser Prs;

void setup() {
  Serial.begin(9600);
  Usb.Init();
  HidKeyboard.SetReportParser(0, &Prs);
}

void loop() {
  Usb.Task();
}

