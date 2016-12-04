/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int LED1 = 3;
int LED2 = 2;
String incoming = "";

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  Serial.begin(57600);
  Serial.setTimeout(0);
}

// the loop routine runs over and over again forever:
void loop() {
// Read serial input:
  incoming = Serial.readString();
  if (incoming == "0"){
    digitalWrite(LED1, LOW);
    //digitalWrite(LED2, LOW);
  } else if (incoming == "1"){
    digitalWrite(LED1, HIGH);
    //digitalWrite(LED2, LOW);
  } else if (incoming == "2"){
    //digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
  } else if (incoming == "3"){
    //digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
  }
}
