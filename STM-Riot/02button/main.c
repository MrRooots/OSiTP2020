#include "xtimer.h"
#include "timex.h"
#include "periph/gpio.h"

#define INTERVAL 100000

// Количество микросекунд, прошедших с последнего вызова обработчика
uint32_t last_time = 0;

// Обработчик прерывания по нажатию кнопки
void btn_handler(void *arg) {
  (void)arg;
  if (gpio_read(GPIO_PIN(PORT_A,0)) > 0) {
    if ((xtimer_usec_from_ticks(xtimer_now()) - last_time) > 100000){ 
      gpio_set(GPIO_PIN(PORT_C, 8));
      last_time = xtimer_usec_from_ticks(xtimer_now());
    }
  }
  else {
    gpio_clear(GPIO_PIN(PORT_C, 8));
  }
}

int main(void) {
  gpio_init_int(GPIO_PIN(PORT_A, 0), GPIO_IN, GPIO_BOTH, btn_handler, NULL);
  gpio_init(GPIO_PIN(PORT_C, 8), GPIO_OUT);

  while(1){}
  return 0;
}