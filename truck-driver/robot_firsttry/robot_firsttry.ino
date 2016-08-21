
#include <Servo.h>
  int control = 4;
  Servo servo1;
  Servo servo2;
  int d = 1.5;
  int countcycle = 0;
  void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600); 
   servo1.attach(3);
   servo2.attach(4); 
  
}

void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available() > 0) {
                // read the incoming byte
                char control_read = Serial.read();
                if (control != (int) control_read) 
                    countcycle = 0;
                // say what you got:
                control = (int)control_read;
                // Serial.print("I received:");
                // Serial.print(control);
   }
  if (control =='w'){
      servo1.write(110);
      servo2.write(90);
      countcycle++;
  } 
  else if (control =='a'){
    servo1.write(90);
    servo2.write(110);
    countcycle++;
  }
  else if (control == 'd'){
     servo1.write(90);
     servo2.write(70); 
     countcycle++;
  }
  else if (control == 's'){
     servo1.write(70);
     servo2.write(90); 
    countcycle++;
  }
  else if (control == 'q'){
     servo1.write(100);
     servo2.write(90); 
    countcycle++;
  } 
  else if (control == 'e'){
     servo1.write(115);
     servo2.write(90); 
    countcycle++;
  }   
  else if (control =='i'){
      servo1.write(100);
      servo2.write(90);
      countcycle++;
      if (countcycle >= 20) {
        control = 'h';
      }
  } 
  else if (control =='I'){
      servo1.write(100);
      servo2.write(90);
      countcycle++;
      if (countcycle >= 100) {
        control = 'h';
        Serial.print('.');
      }
  } 
  else if (control =='j'){
      servo1.write(90);
      servo2.write(110);
      countcycle++;
      if (countcycle >= 68) {
        control = 'h';
        Serial.print('.');
      }
  }
  else if(control =='o' ){
      servo1.write(90);
      servo2.write(70);
      countcycle++;
      if (countcycle >= 200) { //264 rotate 360 degree
        control = 'h';
      }
  }
  else if(control =='O' ){
      servo1.write(90);
      servo2.write(70);
      countcycle++;
      if (countcycle >= 264) { //rotate 360 degree
        control = 'h';
        Serial.print('.');
      }
  }
  else if (control == 'l'){
     servo1.write(90);
     servo2.write(70); 
     countcycle++;
      if (countcycle >= 55) {
        control = 'h';
        Serial.print('.');
      }
  }
  else if (control =='k'){
      servo1.write(90);
      servo2.write(110);
      countcycle++;
      if (countcycle >= 218) {
        control = 'h';
        Serial.print('.');
      }
  }
  else{
    servo1.write(90);
    servo2.write(90);
  }
  
  delay(20);
  // Serial.print("control is");
  // Serial.print(control); 
  // Serial.println(" ");
  // Serial.println("need" );
  // Serial.print(countcycle);
}
