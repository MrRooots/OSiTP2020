#include "thread.h"
#include "xtimer.h"
#include "timex.h"
#include "periph/gpio.h"

// Define the pins
#define LED_BLUE  GRPIO_PIN(PORT_C, 8)
#define LED_GREEN GRPIO_PIN(PORT_C, 9)

char first_stack[THREAD_STACKSIZE_DEFAULT];
char second_stack[THREAD_STACKSIZE_DEFAULT];

// First thread
void *thread(void *arg) {
  // Receive main thread arguments
  int period = ((int*) arg)[0];
  int PIN_IDENTIFIER = ((int*) arg)[1];
  
  xtimer_ticks32_t last_wakeup_one = xtimer_now();
  
  while(1) {
    // Toggle `PIN_IDENTIFIER` pin
    gpio_toggle(GPIO_PIN(PORT_C, PIN_IDENTIFIER));
    
    // Force thread to sleep for `period` microseconds
    xtimer_periodic_wakeup(&last_wakeup_one, period);
  }
  
  return NULL;
}


int main(void) {
  // Initialize PC8 and PC9 pin
	gpio_init(GPIO_PIN(PORT_C, 8), GPIO_OUT);
  gpio_init(GPIO_PIN(PORT_C, 9), GPIO_OUT);

  int green_led_args[] = {500000, 8};
  int blue_led_args[]  = {250000, 9};

  // Initialize first thread
  thread_create(
    first_stack,                 // Stack-allocated memory
    sizeof(first_stack),         // Stack size
    THREAD_PRIORITY_MAIN - 1,    // Thread priority
    THREAD_CREATE_STACKTEST,   
    thread,                      // Handler function
    (void*)(green_led_args),     // Arguments that will be sent to thread
    "first_thread"               // Descriptor
  );

  // Initialize the second thread for green led
  // Initialize first thread
  thread_create(
    second_stack,                 // Stack-allocated memory
    sizeof(second_stack),         // Stack size
    THREAD_PRIORITY_MAIN - 1,     // Thread priority
    THREAD_CREATE_STACKTEST,   
    thread,                      // Handler function
    (void*)(blue_led_args),      // Arguments that will be sent to thread
    "second_thread"              // Descriptor
  );

  return 0;
}
