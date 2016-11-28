/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 3;
String incoming = "";

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
  Serial.begin(57600);
  Serial.setTimeout(1);
}

// the loop routine runs over and over again forever:
void loop() {
// Read serial input:
  incoming = Serial.readString();
  if (incoming == "1"){
    digitalWrite(led, HIGH);
  } else if (incoming == "0"){
    digitalWrite(led, LOW);
  }
}
