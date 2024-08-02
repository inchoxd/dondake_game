#include <M5StickCPlus.h>

float accX = 0.0F;
float accY  = 0.0F;
float accZ = 0.0F;
float magnitude = 0.0F;
bool lastDondake = false;
int dondakeCnt = 0;
int maxDondake = 0;
int dondakeeState = 0;
bool gameStatus = false;

boolean checkGameStatus(boolean serialStatus) {
  if(serialStatus) {
    byte isStart = Serial.read();
    if(isStart == 'T') {
      digitalWrite(10, LOW);
      Serial.println("{\"is_start\":\"true\"}");
      return true;
    } else {
      digitalWrite(10, HIGH);
      Serial.println("{\"is_start\":\"false\"}");
      return false;
    }
  } else {
    return gameStatus;
  }
}

void setup() {
  M5.begin();
  M5.Imu.Init();
  M5.Axp.ScreenBreath(0);

  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
}

void loop() {
  gameStatus = checkGameStatus(Serial.available());
  if(gameStatus) {
    while(dondakeCnt < 3) {
      M5.IMU.getAccelData(&accX, &accY, &accZ);
      magnitude = abs(sqrt(accX + accY + accZ));
      if(magnitude > 0.0) abs(magnitude -= 1.0);
      if(magnitude < 0.0) magnitude = magnitude * -1;
      if(isnan(magnitude)) magnitude = 0.0;
      if(magnitude > 0.5 && 1.0 > magnitude) {
        dondakeeState = 1;
        if(lastDondake == true) {
          dondakeCnt = 0;
          lastDondake = false;
        }
      } else if(magnitude > 1.0 && 1.7 > magnitude) {
        dondakeeState = 2;
        if(lastDondake == false && dondakeCnt < 1) {
          lastDondake = true;
          dondakeCnt += 1;
        } else if(lastDondake == true) {
          dondakeCnt += 1;
          if(maxDondake < dondakeCnt) {
            maxDondake += 1;
          }
        }
        if(maxDondake < dondakeCnt) {
          maxDondake += 1;
        }
      } else {
        dondakeCnt = 0;
        dondakeeState = 0;
        lastDondake = false;
      }
      Serial.println("{\"magnitude\":\"" + String(magnitude) + "\", \"dondakeCnt\":\"" + String(dondakeCnt) + "\", \"dondakeeState\":\"" + String(dondakeeState) +  "\", \"lastDondake\":\"" + String(lastDondake) + "\", \"maxDondake\":\"" + maxDondake + "\"}");
      delay(150);
      if(checkGameStatus(Serial.available()) == false) {
        gameStatus = false;
        dondakeCnt = 0;
        dondakeeState = 0;
        lastDondake = false;
        maxDondake = 0;
        break;
      }
    }
    dondakeeState = 3;
    if(gameStatus) {
      gameStatus = false;
      Serial.println("{\"is_start\":\"false\"}");
      dondakeCnt = 0;
      dondakeeState = 0;
      lastDondake = false;
      maxDondake = 1;
      digitalWrite(10, HIGH);
    delay(150);
    }
  }
  M5.update();
}
