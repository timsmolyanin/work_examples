/*
	STM32F051R8T6
	STM32F0DISCOVERY BOARD
		
	Encoding Russion Windows-1251
		
	User LEDS: LED3 - PC9, LED4 - PC8
	UART1 - PA9(TX), PA10(RX)
	EXTI0 - PA0
	One Pulse Mode - PB4 (TIM3_CH1)
*/

/*
	Includes:
*/
#include "stm32f0xx.h"                  										// Device header
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/****************************End of includes************************************/

/*
	Defines:
*/
#define LED_3_ON GPIOC->ODR = 1 << 9											//
#define LED_3_OFF GPIOC->ODR = 0 << 9											//

/* Для буфера приемника USART1*/
#define BUF_SIZE    16 															// размер буфера
#define BUF_MASK    (BUF_SIZE-1) 												// 
/*****************************End of defines************************************/

/*
	User variables:
*/
uint8_t 		DOV_Flag;														//

uint8_t 		idxIN, idxOUT;													//
char 			buffer[BUF_SIZE];												//
uint8_t     	rx_data;														//
const char 		s[1] = " ";														//

char* 			tok;															//
uint32_t 		status, delay_fp, delay_tx, width_pulse;						//

/* Для системного таймера */
uint32_t     	tim_delay;														//
uint8_t      	rx_status;														//

/***************************End of user variables*******************************/
/*
	User functions:
*/
// Функция временной задержки в милисекундах
void Delay_ms(uint32_t delay) {
   tim_delay = delay;
   while (tim_delay != 0) {
      if (rx_status == 1) return;
   }
}
/*******************************************************************************/

/*
	Функция инициализации режима одиночного импульса TIM3_CH1, PB4 
*/
void OPM_Init(void){

	RCC->AHBENR |= RCC_AHBENR_GPIOBEN;											// Тактирование порта B
	RCC->APB1ENR |= RCC_APB1ENR_TIM3EN;											// Тактирование таймера №3
	
	GPIOB->MODER &= ~(0x1UL << 8U);												// Обнуление бита режима альтер-ой функции для PB4
	GPIOB->MODER |= (0x2UL << 8U);												// Выбор режима альтернативной функции
	
//	GPIOA->AFR[0] &= ~(0xFUL << 24U);											//
	GPIOB->AFR[0] |= (0x1UL << 16U);											// Выбор номера альтернативной функции TIM3_CH1 PB4
		
	TIM3->PSC = 8000; 															// prescaler APBCLK/ 
//	TIM3->ARR = 100; 															// Длительность импульса
	TIM3->CCR1 = 10; 															// Задержка перед формированием импульса
	TIM3->CCMR1 |= TIM_CCMR1_OC1M_2 | TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_0;		// PWM mode, 

	TIM3->CCER |= TIM_CCER_CC1E; 												//
	TIM3->BDTR |= TIM_BDTR_MOE; 												//
		
	TIM3->CR1 |= TIM_CR1_OPM; 													//
	TIM3->EGR |= TIM_EGR_UG;													//
		
//	TIM3->CR1 |= TIM_CR1_CEN;													// Включение таймера №3
		
}
/*
	Функция формирования длительности одиночного импульса
*/
void Pulse_BABAH(int duty){
	
	TIM3->ARR = duty;															// Длительность импульса
	TIM3->CR1 |= TIM_CR1_CEN;													// Включение таймера
}
/*******************************************************************************/

/*
	Функция инициализации USART1
*/
void USART_Init(void){
    
   RCC->AHBENR |= RCC_AHBENR_GPIOAEN; 											// Тактирование GPIOA
   RCC->APB2ENR  |= RCC_APB2ENR_USART1EN;                     					// Тактирование блока USART1
   GPIOA->MODER  |= (GPIO_MODER_MODER9_1 | GPIO_MODER_MODER10_1);   			// Выбор режима альтернативной функ-ии
   GPIOA->AFR[1] |= (0x1UL << 4U) | (0x1UL << 8U);;								// Номер альтернативной функ-ии USART1 (PA9 - TX, PA10 - RX)
   USART1->BRR   |= 8000000/9600;                              					// 9600
   USART1->CR1   |= USART_CR1_TE;                            					// Разрешить передатчик
   USART1->CR1   |= USART_CR1_RE;                            					// Разрешить приёмник
   USART1->CR1   |= USART_CR1_UE;                            					// Разрешить USART
   USART1->CR1   |= USART_CR1_RXNEIE;                         					// Разрешить прерывание по приему данных
   NVIC_EnableIRQ (USART1_IRQn);                            			  		// Разрешить прерывания от USART1
    
}
/*******************************************************************************/

/*
	Функция отправляет байт в USART
*/ 
void send_uart(uint_fast8_t data) {
	while (!(USART1->ISR & USART_ISR_TC))                						// Ждем пока бит TC в регистре ISR станет 1
		USART1->TDR=data;                                    					// Отсылаем байт через USART1
}
/*******************************************************************************/

/*
	Функция отправляет строку в USART
*/
void send_str(char * string) {
	uint8_t i = 0;
	while (string[i]) {
		send_uart(string[i]);
		i++;
   }
	send_uart('\r');
	send_uart('\n');
}
/*******************************************************************************/

/*
	Функция инициализации внешнего прерывания EXTI0 PA0
*/
void EXTI_Init(void){
			
	RCC->AHBENR |= RCC_AHBENR_GPIOAEN; 											// Тактирование порта А
	RCC->APB2ENR |= RCC_APB2ENR_SYSCFGCOMPEN;									// Тактирование блока SYSCFG

	GPIOA->MODER |= GPIO_MODER_MODER0_1;										// Режим альтернативной функ-ии PA0
//	GPIOA->MODER &= ~GPIO_MODER_MODER0_1;
			
	GPIOA->PUPDR |= GPIO_PUPDR_PUPDR0; 											// Вход Pull Up/Pull Down
	
	SYSCFG->EXTICR[0] |= SYSCFG_EXTICR1_EXTI0_PA;								// Выбор номера альтернативной функ-ии (EXTI0)
			
	EXTI->IMR |= EXTI_IMR_MR0;													// 
	EXTI->RTSR |= EXTI_RTSR_TR0; 												// По переднему фронту
//	EXTI->FTSR |= EXTI_FTSR_TR0; 												// По заднему фронту
	EXTI->PR |= EXTI_PR_PR0;  
			
	NVIC_EnableIRQ(EXTI0_1_IRQn); 												// Разрешить прерывания от EXTI0
	NVIC_SetPriority(EXTI0_1_IRQn, 2); 											// Приоритет прерывания - 2
	DOV_Flag = 0;																// Обнуление флага
}
/*******************************************************************************/

/********************************End of user functions**************************/

/*
	Main()
*/
int main(){
    
    RCC->AHBENR |= RCC_AHBENR_GPIOCEN;
    
    GPIOC->MODER |= 0x50000;
    
    GPIOC->OTYPER |= 0x0;
    
    GPIOC->OSPEEDR |= 0;
/*
	Инициализация:
*/	
	SystemInit();																//
	SysTick_Config(SystemCoreClock/1000);										//
    
    USART_Init();																//
	EXTI_Init();																//
	OPM_Init();																	//
/*****************************End of initializations****************************/    

/*
	While()
*/
while(1){
			
	switch (status){
	
		case 1:		
			if (DOV_Flag == 1){
        
				DOV_Flag = 0;
//				LED_3_ON;
				Delay_ms(delay_fp);
				Pulse_BABAH(width_pulse);
				Delay_ms(delay_tx);
				send_str("1");
			}
			else{
        
				LED_3_OFF;
				send_str("0");
				Delay_ms(1000);
			}
			break;
			
		case 0:
			send_str("0");
			Delay_ms(1000);
		break;
}
	} // while
    
} // main
/*******************************************************************************/
/* 
	Обработчик прерывания системного таймера, прерывания каждую 1 ms
*/
void SysTick_Handler(void) {
   if (tim_delay != 0) tim_delay--;
}
/*******************************************************************************/
/*
	Обработчик прерывания от USART1
*/
void USART1_IRQHandler(void) {
   if ((USART1->ISR & USART_ISR_RXNE) != 0) { 									//
       
      USART1->ISR &= ~USART_ISR_RXNE; 											//
     
      rx_data = USART1->RDR;                              						//
      buffer[idxIN++] = rx_data;												//
		  if (idxIN >= BUF_SIZE){												//
				idxIN = 0;														//
				tok = strtok(buffer, s); status = atoi(tok);					//
				tok = strtok(NULL, s); delay_fp = atoi(tok);					//
				tok = strtok(NULL, s); delay_tx = atoi(tok);					//
				tok = strtok(NULL, s); width_pulse = atoi(tok);					//
		  }
		  
   }
}
/*******************************************************************************/
/*
	Обработчик внешнего прерывания EXTI0 PA0
*/
void EXTI0_1_IRQHandler(void) {
	if(EXTI->PR & EXTI_PR_PR0) {
		EXTI->PR |= EXTI_PR_PR0; 												// Сбрасываем флаг прерывания
		DOV_Flag = 1;															// Выставляем флаг
	}
}
/*******************************************************************************/