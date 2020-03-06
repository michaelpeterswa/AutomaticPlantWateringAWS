//arduino code

long timeToRun = 0;
int garbage = 0;

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    timeToRun = Serial.parseInt();
    garbage = Serial.parseInt();
    Serial.print(analogRead(A0));
    digitalWrite(10, HIGH);
    digitalWrite(9, HIGH);
    delayMicroseconds(timeToRun);
    digitalWrite(10, LOW);
    digitalWrite(9, LOW);
  }
}
