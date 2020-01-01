#include <Wire.h>

// Standard adress: 0x28
#define HYT221_ADDR 0x28

// Ultrasonic sensor
#define trig 7
#define echo 6

// Moisture sensor
#define in_moisture_sensor 1

// Pump
#define out_pump 12

// temperature and Humidity variables
double humidity;
double temperature;
byte data [4];

//  Ultrasonic sensor variables
long measure;
float cm;

// Moisture sensor variables
double moisture;
double measurement;

// Pump variables
int pumpstatus;

// Serial variales
char c;


void getData_Temp_Humidity(){
  // initiate measurement
  Wire.beginTransmission(HYT221_ADDR);
  Wire.write(0);
  Wire.available();
  int Ack = Wire.read(); // receive a byte

  Wire.endTransmission(); 
  delay(100);

  // READ DATA from here on
  Wire.beginTransmission(HYT221_ADDR);
  Wire.requestFrom(HYT221_ADDR,4);  //Reade 1 byte
  Wire.available();
  data[0] = Wire.read(); // receive a byte
  data[1] = Wire.read(); // receive a byte
  data[2] = Wire.read(); // receive a byte
  data[3] = Wire.read(); // receive a byte
  Wire.write(0); //NACK

  // combine the bits
  unsigned int RawHumidBin = data[0] << 8 | data[1];
  // compound bitwise to get 14 bit measurement first two bits
  // are status/stall bit (see intro text)
  RawHumidBin =  (RawHumidBin & 0x3FFF); 
  humidity = 100.0/pow(2,14)*RawHumidBin;

  data[3] = (data[3] &= 0x3F); //Mask away 2 least sign. bits see HYT 221 doc
  unsigned int RawTempBin = data[2] << 6 | data[3];
  temperature = 165.0/pow(2,14)*RawTempBin-40;

  Wire.endTransmission();
}


void getData_Ultrasonic() {
  
  // SEND TRIGGER
    digitalWrite(trig,LOW);
    delayMicroseconds(2);
    digitalWrite(trig,HIGH);
    delayMicroseconds(10);
    digitalWrite(trig,LOW);
    
  //MEASURE ECHO-PIN
    measure=pulseIn(echo,HIGH);
    cm=measure/58;
}

void getData_Moisture() {
  moisture = analogRead(in_moisture_sensor);
}

//setup
void setup(){
  // Setup Serial connection
  Serial.begin(9600);
  delay(1000);
  // join I2C bus
  Wire.begin(); 
  delay(1000);
  // Define Inputs and Outputs
  pinMode(trig,OUTPUT);
  pinMode(echo, INPUT);
  pinMode(in_moisture_sensor, INPUT);
  pinMode(out_pump,OUTPUT);          

}

void loop()
{

    /* DEBUGGING
    */

    if (Serial.available()>0)
    { 
      while (Serial.available() > 0)
      {
        // Read comma-seperated voltages from Smart-Meter
        c=Serial.read();
      }

      pumpstatus = 1;

      //only start pump when char = !
      if (c == '!')
      {
        pumpstatus = 2;
        measurement = analogRead(in_moisture_sensor);
        Serial.print("Starting the pump...");
        digitalWrite(out_pump,HIGH); // Start the pump
        delay(1000*10);             // 30 Sec
        digitalWrite(out_pump, LOW); // Stop the pump
      }  

      getData_Temp_Humidity();
      getData_Moisture();
      getData_Ultrasonic();
      
      // if sensor measurement is zero try again
      if (cm == 0)
      {
        delay(1000);
        getData_Ultrasonic();
      }

      Serial.print(humidity);
      Serial.print(";");
      Serial.print(temperature);
      Serial.print(";");
      Serial.print(moisture);
      Serial.print(";");
      Serial.print(cm);
      Serial.print(";");
      Serial.print(pumpstatus);
      
      Serial.print("!"); // Ende-Zeichen

    } 
}

// touch Makefile
// nano Makefile
// ----
//ARDUINO_DIR = /usr/share/arduino
//BOARD_TAG    = uno
//ARDUINO_PORT = /dev/ttyACM*
//ARDUINO_LIBS = include /usr/share/arduino/Arduino.mk
//----
//make
//make upload

