#define max_cmd_length 20
char strReceived[max_cmd_length];
int currentChar = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    strReceived[currentChar] = c;
    currentChar = (currentChar+1)%max_cmd_length;

    if (c=='\n') {
      currentChar = 0;
      Serial.print("recieved: ");
      Serial.println(strReceived);
    }
  }
}
