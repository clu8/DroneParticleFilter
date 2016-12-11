
// Requires NewPing library
#include <NewPing.h>
#include <SoftwareSerial.h>
#include "RunningAverage.h"

char buf [100];

// RunningMedian library attached in folder
#include "RunningMedian.h"

#define DEBUG
//#define DEBUGXY

#define SONAR_NUM     1 // Number of sensors.
#define MAX_DISTANCE 255 // Maximum distance (in cm) to ping.
#define LR_PING_INTERVAL 0 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo; 10 used since LR are opposite ends).
#define BACK_PING_INTERVAL 0 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

#define FIELD_MAX_DIST 210 // Max distance to subtract from to get x sonar measurement from left sonar

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
float cm[SONAR_NUM];         // Where the ping distances are stored.
byte currentSensor = 0;          // Keeps track of which sensor is active.

NewPing sonar[SONAR_NUM] = {     // Sensor object array.
  NewPing(12, 11, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
};

// Running median for median filter (protection from noise), using 10 samples running median
RunningMedian sonar1samples = RunningMedian(30);
RunningAverage xRA(100);
RunningAverage yRA(100);
long lastMillis = 0;
float velocity = 0;
float pos = 0;
float lastPos = 0;

SoftwareSerial bluetoothLink(8, 9);

int xcenter = 324;
int xmax = 155;

void calibrateAccelerometer()
{
  Serial.println("Press enter to start calibration.");
  while (!Serial.available()) ;
  while (Serial.available()) Serial.read();
  
  Serial.println("Calibrating. Hold the accelerometer flat for 3 seconds.");
  int start = millis();
  
  while (millis() - start < 3000)
  {
      xRA.addValue(analogRead(A3));
  }
  xcenter = xRA.getAverage();
  xRA.clear();


  Serial.print("X acceleration centered at: ");
  Serial.println(xcenter);

  Serial.println("Calibrating. Hold the accelerometer vertically for 3 seconds.");
  Serial.println("Starting...");

  start = millis();
  while (millis() - start < 3000)
  {
      xRA.addValue(analogRead(A3));
  }
  xmax = xRA.getAverage();


  Serial.print("X acceleration max at: ");
  Serial.println(xmax);

  Serial.println("Press enter to end calibration.");
  
  while (!Serial.available()) ;
  while (Serial.available()) Serial.read();
}

void setup() 
{
  Serial.begin(115200);

  bluetoothLink.begin(115200);

  // Initialize ping Timers (with custom LR_PING/BACK_PING intervals
  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.

  // calibrateAccelerometer();
}

byte floatBytes[4];
void float2Bytes(float val,byte* bytes_array){
  // Create union of shared memory space
  union {
    float float_variable;
    byte temp_array[4];
  } u;
  // Overite bytes of union with float variable
  u.float_variable = val;
  // Assign bytes to input array
  memcpy(bytes_array, u.temp_array, 4);
}

float xaccel;

void loop() {

  // Sonar measurement logic
    if (millis() >= pingTimer[0]) {         // Is it this sensor's time to ping?
      pingTimer[0] += LR_PING_INTERVAL + 2 * BACK_PING_INTERVAL;  // Set next time this sensor will be pinged.
      oneSensorCycle(); // Sensor ping cycle complete, do something with the results.
      sonar[0].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
      sonar[0].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
    
      xaccel = (analogRead(A3) - xcenter) * 9.8 / xmax;
    }
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[0].check_timer() && sonar[0].ping_result)
    cm[0] = sonar[0].ping_result / ((float)US_ROUNDTRIP_CM);
    sonar1samples.add(cm[0]);
}

// One sensor cycle, send all information (median)
byte sonarRequest = 0;
void oneSensorCycle() { // Sensor ping cycle complete, do something with the results.
      #ifdef DEBUG
        Serial.print(sonar1samples.getMedian());
        Serial.print(",");
        velocity += (abs(xaccel-0.45) > 0.3? xaccel-0.45:0.0f) * (millis()-lastMillis)/1000.0f;
        pos += 1 * (millis()-lastMillis)/1000.0f;
        Serial.print(pos);
        lastPos = pos;
        lastMillis = millis();
        Serial.print(",");
        Serial.println(millis());
        
        bluetoothLink.print("1: ");
        bluetoothLink.println(round(sonar1samples.getMedian()));
      #endif
}
