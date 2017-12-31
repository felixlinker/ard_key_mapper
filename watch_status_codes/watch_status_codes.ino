#include <hidboot.h>
#include <usbhub.h>
#include <SPI.h>

class Parser: public KeyboardReportParser {
  protected:
    void OnKeyDown(uint8_t mod, uint8_t key);
};

void Parser::OnKeyDown(uint8_t mod, uint8_t key) {
  Serial.print("key pressed: ");
  Serial.print(key);
  Serial.print('\n');
};

USB Usb;
HIDBoot<USB_HID_PROTOCOL_KEYBOARD> HidKeyboard(&Usb);
Parser Prs;

void setup() {
  Serial.begin(9600);
  if (Usb.Init() == -1) {
    Serial.println("OSC did not start");
  }
  Serial.println("Start");
  HidKeyboard.SetReportParser(0, &Prs);
}

void loop() {
  Usb.Task();
}

