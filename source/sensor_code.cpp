#include <Wire.h>           
#include <ESP8266WiFi.h>                                              
#include <FirebaseArduino.h>                                       
 
#define FIREBASE_HOST "childobj-default-rtdb.firebaseio.com"              // the project name address from firebase id
#define FIREBASE_AUTH "jo12vqov0RgnteD6HertyuioYOyuURXId8pRyI8HT"        //  secret key generated from firebase
#define WIFI_SSID "homeiot"                                          
#define WIFI_PASSWORD "homeiot01"        

String fireStatus = "";  
String fireStatus1 = "";    
 int buz =D5;
 const int trigPin = D2;
const int echoPin = D1;

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;

 void setup()  
  {  
    Serial.begin(9600);
    pinMode(buz, OUTPUT);
    digitalWrite(buz, LOW);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                               
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) 
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);                  // connect to firebase
  Firebase.setString("CHILD_IOT/LOAD_STATUS", "0");  
  Firebase.setString("CHILD_IOT/LOAD_STATUS1", "0");                     //send initial string of led status
  Firebase.setString("CHILD_IOT/Td", "no");
  }  
 void loop()   
  {  

  fireStatus = Firebase.getString("CHILD_IOT/OBJ_STATUS");  
  fireStatus1 = Firebase.getString("CHILD_IOT/Dist"); 

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_VELOCITY/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance on the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  Serial.println(fireStatus);
  //Firebase.setString("CHILD_IOT/Dist", String(distanceCm));  
  delay(500);
if(fireStatus != "")
{
  Firebase.setString("CHILD_IOT/Dist", String(distanceCm));  

   if(distanceCm <30)
   {
     digitalWrite(buz, HIGH);
     delay(200);
     Firebase.setString("CHILD_IOT/Td", "yes");
   } 
   else
   {
      digitalWrite(buz, LOW);
     delay(200);
     Firebase.setString("CHILD_IOT/Td", "no");

   }
   
  }  
  else
  {
    digitalWrite(buz, LOW);
    Serial.print("no object");
    distanceCm =0;
    Firebase.setString("CHILD_IOT/Dist", String(distanceCm)); 
    Firebase.setString("CHILD_IOT/Td", "no");
    delay(500);
  }
  }