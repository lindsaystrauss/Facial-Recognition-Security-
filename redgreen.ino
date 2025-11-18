String input = "";

int greenLED = 12;
int redLED = 13;

void setup() {
  Serial.begin(9600);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();  // removes spaces + \r + \n

    Serial.println("Received: " + input); // DEBUG

    if (input == "APPROVED") {
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
      delay(2000);
      digitalWrite(greenLED, LOW);
    }

    if (input == "DENIED") {
      digitalWrite(redLED, HIGH);
      digitalWrite(greenLED, LOW);
      delay(2000);
      digitalWrite(redLED, LOW);
    }
  }
}
