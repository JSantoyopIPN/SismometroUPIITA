#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads; // Versión para ADS1115

void setup(void)
{
  Serial.begin(115200);
  ads.begin();
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3;
  float volts0, volts1, volts2, volts3;

  adc0 = ads.readADC_SingleEnded(0);
  adc2 = ads.readADC_SingleEnded(2);

  String stringADC = "A" + String(adc0) + " " + "B" + String(adc2);
  Serial.println(stringADC);

  delay(15);
}
