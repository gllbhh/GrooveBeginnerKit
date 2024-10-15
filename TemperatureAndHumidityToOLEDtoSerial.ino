/*
  Sketch for Grove Beginner Kit for Arduino board
  that reads temperature and humidity from the DHT20 sensor
  and displays the readings on the OLED display 
  and sends them to the Serial Port.
  Based on Lesson 8 from the board documentation.
            By Gleb B. for Fab Lab Suomi Bootcamp
*/

//Temperature and Humidity Sensor
#include <DFRobot_DHT20.h>
//#include <Arduino.h>
#include <U8x8lib.h>
int messageInterval = 1000; // interval between messages to the serial port 1000 = 1s
DFRobot_DHT20 dht;
U8X8_SSD1306_128X64_ALT0_HW_I2C u8x8(/* reset=*/U8X8_PIN_NONE);
void setup(void) {
  Serial.begin(9600);
  Serial.println("DHT20 test!");
  dht.begin();
  //dht.startMeasure();
  Serial.println("DHT20 Sensor Initialized");
  u8x8.begin();
  u8x8.setPowerSave(0);
  u8x8.setFlipMode(1);
}
void loop(void) {
  //dht.startMeasure();
  float temp, humi;
  temp = dht.getTemperature(); //save temperature reading to temp variable
  humi = dht.getHumidity() * 100; // save humidity reading to humi variable multiplied by 100
  // display the readings on OLED display
  u8x8.setFont(u8x8_font_chroma48medium8_r);
  u8x8.setCursor(0, 33);
  u8x8.print("Temp:");
  u8x8.print(temp);
  u8x8.print("C");
  u8x8.setCursor(0, 50);
  u8x8.print("Humidity:");
  u8x8.print(humi);
  u8x8.print("%");
  u8x8.refreshDisplay();
  // send readings to the Serial port
  Serial.print(temp);   // print temperature
  Serial.print(" ");    // print \s
  Serial.println(humi); // print humidity and go to a new line
  // wait before sending the next message
  delay(messageInterval);
}
