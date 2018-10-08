#define max_cmd_length 20
char strReceived[max_cmd_length];
int currentChar = 0;

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

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    strReceived[currentChar] = c;
    currentChar = (currentChar+1)%max_cmd_length;
    //read Serial into strReceived
    //max length is 20, after which it loops around to loc 0

    if (c=='\n') { //commands end in \n
      currentChar = 0;
      acknowledge();

      if (checkCmd("on"))
        digitalWrite(LED_BUILTIN,HIGH);
      else if (checkCmd("off"))
        digitalWrite(LED_BUILTIN,LOW);
      else if (checkCmd("analogwrite"))
        analogWrite(strReceived[10],strReceived[11]);
      else if (checkCmd("num")) { //takes a number and returns that number + 1
        Serial.write(strReceived[3]+1);
        Serial.write('\n');
      }
      //COMMANDS ADDED HERE
    }
  }
}
