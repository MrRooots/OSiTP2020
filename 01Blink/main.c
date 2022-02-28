// Подключение библиотек
#include "xtimer.h"
#include "timex.h"
#include "periph/gpio.h"

// Макрос для интервала времени, в течение которого трэд будет спать
#define HALFSECONDINTERVAL 5000000

int main(void) {
  xtimer_ticks32_t last_wakeup = xtimer_now();
  gpio_init(GPIO_PIN(PORT_C, 9), GPIO_OUT);
  gpio_init(GPIO_PIN(PORT_C, 8), GPIO_OUT);

  while(1) {
    gpio_toggle(GPIO_PIN(PORT_C, 8));
    xtimer_periodic_wakeup(&last_wakeup, HALFSECONDINTERVAL);
    gpio_toggle(GPIO_PIN(PORT_C, 9));
  }

  return 0;
}

/* 
Задание 1. Установите интервал переключения светодиода на 0.5 секунды. +
Задание 2. Сделайте так, чтобы вместо одного светодиода моргал другой. +
Задание 3. Сделайте так, чтобы светодиоды моргали попеременно - один выключился, другой включился. +
*/
