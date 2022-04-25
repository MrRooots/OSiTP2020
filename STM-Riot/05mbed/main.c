#include "mbed.h"

Serial pc(USBTX, USBRX);
PwmOut led(LED1);

char CODE[] = "1234";

int main() {
  pc.printf("Enter four digits code\n\r");
    

  while(1) {
    char code[50];
    pc.gets(code,5);  // Get code from console
    wait(0.001);
    
    if (strlen(code) == 4 && strcmp(code, CODE) == 0) {
      pc.printf("Valid code");
      for (size_t i = 0; i < 10; i++) {
        led = !led;
        wait_ms(1000);
      }
    } else {
      pc.printf("Invalid code!");
    }      
  }
  
  if (led) {led = !led;}
}   