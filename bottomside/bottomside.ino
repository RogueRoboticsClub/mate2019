#include <Servo.h>

#define max_cmd_length 25
unsigned char strReceived[max_cmd_length];
int currentChar = 0;
Servo boxServo;

bool checkCmd(char* cmd) {
  return !memcmp(cmd,strReceived,strlen(cmd));
}
void acknowledge() {
  Serial.print("received: ");
  for (int x = 0; x<max_cmd_length && strReceived[x]!='\n'; x++)
    Serial.write(strReceived[x]);
  Serial.write('\n');
  //sends "received: [text]" back
  //  to acknowledge to .py script that it's been received
}

Servo thrusters[7]; //6 thrusters and one camera servo

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  for (int i=0;i<6;i++) {
    thrusters[i].attach(2+i); //WHAT PINS?
    thrusters[i].writeMicroseconds(1500); //stop
  }
  boxServo.attach(9);
  boxServo.write(0);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    strReceived[currentChar] = c;
    currentChar = (currentChar+1)%max_cmd_length;
    //read Serial into strReceived
    //max length is 25, after which it loops around to loc 0

    if (c=='\n') { //commands end in \n
      currentChar = 0;
      acknowledge();

      if (checkCmd("hi"))
        Serial.write("hi\n");
      else if (checkCmd("on"))
        digitalWrite(LED_BUILTIN,HIGH);
      else if (checkCmd("off"))
        digitalWrite(LED_BUILTIN,LOW);
      else if (checkCmd("speeds")) {
        for (int i=0;i<6;i++)
          thrusters[i].writeMicroseconds((int)(strReceived[6+(i*2)] << 8) + (int)strReceived[7+(i*2)]);
      } else if (checkCmd("open"))
        boxServo.write(85);
      else if (checkCmd("close"))
        boxServo.write(0);
      //COMMANDS ADDED HERE
    }
  }
}
