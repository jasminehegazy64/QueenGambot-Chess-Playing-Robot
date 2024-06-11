#include <Servo.h>

Servo gripperServo;
Servo baseServo;
Servo joint1Servo;
Servo joint2Servo;

const int gripperPin = 3;
const int joint1Pin = 9;
const int joint2Pin = 10;
const int basePin = 11;

const int openPosition = 50;
const int closePosition = 0;

const int defaultBaseAngle = 0;
const int defaultJoint1Angle = 30;
const int defaultJoint2Angle = 30;
const int defaultgripperAngle = 10;


void setup() {
    Serial.begin(9600);
    delay(2000);
    gripperServo.attach(gripperPin);
    joint1Servo.attach(joint1Pin);
    joint2Servo.attach(joint2Pin);
    baseServo.attach(basePin);

    // Move servos to default positions
    moveToDefaultPosition();
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readString();
        char startCol = command.charAt(0);
        char startRow = command.charAt(1);
        char endCol = command.charAt(2);
        char endRow = command.charAt(3);

        moveToPosition(startCol, startRow);
        pickUpPiece();
        moveToPosition(endCol, endRow);
        dropPiece();
        moveToDefaultPosition();
    }
}

void moveToPosition(char col, char row) {
    int baseAngle;
    // Define custom mapping ranges based on position choice
    int joint1_min_angle = 0;
    int joint1_max_angle = 120;
    int joint2_min_angle = 45;
    int joint2_max_angle = 135;

    if (row >= '1' && row <= '4') {
        joint1_min_angle = 0;
        joint1_max_angle = 90;
        joint2_min_angle = 90;
        joint2_max_angle = 120;
    } else if (row >= '5' && row <= '8') {
        joint1_min_angle = 0;
        joint1_max_angle = 130;
        joint2_min_angle = 90;
        joint2_max_angle = 150;
    }

    int joint1Angle = map(row - '1', 0, 7, joint1_min_angle, joint1_max_angle);
    int joint2Angle = map(row - '1', 0, 7, joint2_min_angle, joint2_max_angle);
  
    switch (col) {
        case 'a': baseAngle = 30; break;
        case 'b': baseAngle = 45; break;
        case 'c': baseAngle = 60; break;
        case 'd': baseAngle = 90; break;
        case 'e': baseAngle = 105; break;
        case 'f': baseAngle = 115; break;
        case 'g': baseAngle = 120; break;
        case 'h': baseAngle = 135; break;
        default: baseAngle = 90; break;
    }

    moveToDefaultPosition();

    // Move base
    moveServo(baseServo, baseAngle);
    // Move joint1
    moveServo(joint1Servo, joint1Angle);
    // Move joint2
    moveServo(joint2Servo, joint2Angle);
}

void moveServo(Servo servo, int targetAngle) {
    int currentAngle = servo.read();
    if (currentAngle < targetAngle) {
        for (int angle = currentAngle; angle <= targetAngle; angle++) {
            servo.write(angle);
            delay(20);
        }
    } else {
        for (int angle = currentAngle; angle >= targetAngle; angle--) {
            servo.write(angle);
            delay(20);
        }
    }
}

void moveToDefaultPosition() {
    moveServo(baseServo, defaultBaseAngle);
    moveServo(joint1Servo, defaultJoint1Angle);
    moveServo(joint2Servo, defaultJoint2Angle);
    moveServo(gripperServo, defaultgripperAngle);
}

void pickUpPiece() {
  gripperServo.write(50);
    for (int pos = openPosition; pos >= 10; pos--) {
        gripperServo.write(pos);
        delay(20);
    }
}

void dropPiece() {
    gripperServo.write(openPosition);
    delay(20);
}
