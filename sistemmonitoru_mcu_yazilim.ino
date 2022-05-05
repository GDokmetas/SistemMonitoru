#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3F, 20, 4);  
int lcd_backlight = 1;
void setup() {
Serial.begin(9600);
Serial.write('}');
Serial.write('}');
Serial.write('}');
Serial.write('}');
lcd.begin();
lcd.backlight();
lcd.clear();
lcd.home();
lcd.print("Sistem Monitoru");
lcd.setCursor(0, 1);
lcd.print("Gokhan DOKMETAS");
lcd.setCursor(0, 2);
lcd.print("Elektronik Teknoloj.");
lcd.setCursor(0, 3);
lcd.print("203702001");
delay(2000);
lcd.home();
lcd.clear();
}

void loop() {
if(Serial.available() > 1)
{
  char ch = Serial.read();
  if(ch == '*')
  {
    lcd.clear();
    lcd.setCursor(0, 0);
  }
  else if(ch == '\\')
  {
    if(lcd_backlight == true)
    {
      lcd.noBacklight();
      lcd_backlight = false;
    }
    else
    {
     lcd.backlight();
     lcd_backlight = true;
    }
  }
  else if(ch == '?')
  lcd.setCursor(0, 0);
  else if(ch == '}')
  Serial.write('}');
  else
  lcd.print(ch);
}
}
