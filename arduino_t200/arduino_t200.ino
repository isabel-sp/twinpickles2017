#include <Servo.h>

//THRUSTER VALUES and PINS
#define ZERO_THRUST 1500

byte pin_t0 = 5;
byte pin_t1 = 6;
byte pin_t2 = 9;
byte pin_t3 = 10;

Servo t0;
Servo t1;
Servo t2;
Servo t3;

// String data = "0, 0.5, 1, 0";
int thrustInputs[4] = {1500, 1500, 1500, 1500};
char data_chararray[30];

void parse(char testString[], char delimiters[]){
  char temp[10];
  char *ptr;
  int index = 0;
  ptr = strtok(testString, delimiters);

  while (ptr != NULL) {
    thrustInputs[index] = atoi(ptr);
    // Serial.print("thrustInputs[");
    // Serial.print(index);
    // Serial.print("] = ");
    // Serial.println(thrustInputs[index++]);
    thrustInputs[index++];
    ptr = strtok(NULL, delimiters);
  }

}

void update_thrustInputs() {
  t0.writeMicroseconds(thrustInputs[0]);
  //ADD t1, t2, t3

  // Serial.print("thurst inputs updated to (only t0 for now): ");
  // Serial.print(thrustInputs[0]);   //Serial.print(", ");
  // Serial.print(thrustInputs[1]);   Serial.print(", ");
  // Serial.print(thrustInputs[2]);   Serial.print(", ");
  // Serial.println(thrustInputs[3]);
}

void setup() {
  Serial.begin(9600);
  Serial.println("hi! starting nowwwww - arduino");
  
  //INITIALIZE THRUSTERS:
  t0.attach(pin_t0);
  //ADD t1, t2, t3

  //ARM THRUSTERS:
  t0.writeMicroseconds(ZERO_THRUST); 
  //ADD t1, t2, t3

  

  // delay to allow the ESC to recognize the stopped signal.
  delay(7000); 

  Serial.println("done w setup! - arduino");
}

void loop() {
  // Serial.println("checking for data!");

  if(Serial.available() > 0) {
    //RECIEVED DATA
    String data = Serial.readStringUntil('\n');

    // String data = "1550, 1500, 1600, 1400";
    
    // Serial.println("arduino received data");
    // Serial.println(data);

    data.toCharArray(data_chararray,data.length()+1);
    // Serial.println("data converted to:");
    // Serial.println(data_chararray);

    parse(data_chararray, ",");
    
    Serial.print(thrustInputs[0]);

    delay(200);
  }

  // Serial.println("waiting...");
  delay(100);
  update_thrustInputs();

}
