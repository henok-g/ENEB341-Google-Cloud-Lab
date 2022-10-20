#include <stdlib.h>
#include <stdio.h>

double *reportData()
{
	static double ret[7];
	double zipcode = 20850;
	double latitude = 29.2;
	double longitude = 35.5;
	double temperature = 84.4;
	double humidity = 0.0;
	double dewpoint = 1.1;
	double pressure = 1004.1;

	ret[0] = zipcode;
	ret[1] = latitude;
	ret[2] = longitude;
	ret[3] = temperature;
	ret[4] = humidity;
	ret[5] = dewpoint;
	ret[6] = pressure;

	return ret;
}

int main()
{
	double* data;
	data = reportData();
	printf("zipcode: %f\nlatitude: %f\nlongitude: %f\ntemperature: %f\nhumidity: %f\ndewpoint: %f\npressure: %f\n", data[0], data[1], data[2], data[3], data[4], data[5], data[6]);	
	return 0;
}
