#define max_cmd_length 20
char strReceived[max_cmd_length];
int currentChar = 0;

bool checkCmd(char* cmd) {
  return !memcmp(cmd,strReceived,strlen(cmd));
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

    if (c=='\n') {
      currentChar = 0;
      Serial.print("received: ");
      Serial.println(strReceived);
      //commands end in \n
      //sends "received: [text]" back
      //  to acknowledge to .py script that it's been received

      if (checkCmd("on"))
        digitalWrite(LED_BUILTIN,HIGH);
      else if (checkCmd("off"))
        digitalWrite(LED_BUILTIN,LOW);
      //COMMANDS ADDED HERE
    }
  }
}
