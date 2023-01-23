# Транслятор из C++ в Python

Выполнили студенты группы Б9119-09.03.04прогин

* Дудко Денис Олегович
* Сазонтова Мария Дмитриевна
* Самойленко Варвара Сергеевна
* Якимова Анна Владимировна

Поднятый инстанс сайта: https://dendudko.pythonanywhere.com/

UNIT-тесты залиты на GitHub, благодаря использованию TDD имеем 0 ошибок при заданных тестах.

## Поддерживаются:
* ### Типы данных:
	```int, bool, float, std::string, double, void```
* ### Циклы:
	```while, for```
* ### Условия:
	```if, else```
* ### Операторы:
	```+, -, *, /, =, <, >, <=, >=, !=, ==```
* ### Возврат значения:
	```return```

## Input Code

```cpp
int func1(int a){
    for (int i = 1; i < 10; i = i + 2){
        a = a + i;
    }
    int b = a;
    
    for (int i = 1; i <= 10; i = i + 1 ){
        b = b + 1;
    }
    int c = b;
    
    for (int i = 12; i > 1; i = i - 2){
        c = c + i;
    }
    int d = c;    
    
    for (int i = 12; i >= 5; i = i - 1){
        d = d + i;
    }
    int e = d;

    return e;
}
    

int func2(int a){
    a = a + 1;
    return a;
}

int main(){
    int a = 3;
    int b = func1(a);
    int c = 15; 
    int d = 0;

    for (int i = 1; i <= 5; i = i + 1){ 
        for (int j = 5; j < 10; j = j + 2){ 
            for (int k = 15; k > 12; k = k - 2){ 
                c = c + k;
                c = c - i;
                if (c < 30){
                    b = b + j;
                } 
            }                
        }
        d = d + 1;
    }
    while (d <= 20){
        int e = 10;
        while (e >= 5){
            d = func2(d);
            e = e - 1;
        }
        d = d + 1;
    }
    bool istina = true;
    bool lozh = false;
    std::string stroka = 'stroka';    
}
```

## Output Code

```python
def func1(a):
	for i in range(1, 10, 2):
		a = a + i
	b = a
	for i in range(1, 10 + 1, 1):
		b = b + 1
	c = b
	for i in range(12, 1, -2):
		c = c + i
	d = c
	for i in range(12, 5 - 1, -1):
		d = d + i
	e = d
	return e

def func2(a):
	a = a + 1
	return a

def main():
	a = 3
	b = func1(a)
	c = 15
	d = 0
	for i in range(1, 5 + 1, 1):
		for j in range(5, 10, 2):
			for k in range(15, 12, -2):
				c = c + k
				c = c - i
				if c < 30:
					b = b + j
		d = d + 1
	while d <= 20:
		e = 10
		while e >= 5:
			d = func2(d)
			e = e - 1
		d = d + 1
	istina = True
	lozh = False
	stroka = 'stroka'


if __name__ == "__main__":
    main()
```
