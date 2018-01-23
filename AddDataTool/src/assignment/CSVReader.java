package assignment;


import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.dstu2.composite.*;
import ca.uhn.fhir.model.primitive.InstantDt;
import ca.uhn.fhir.rest.client.IGenericClient;
import ca.uhn.fhir.model.dstu2.resource.Bundle;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.model.dstu2.resource.Observation;
import ca.uhn.fhir.model.dstu2.resource.Bundle.Entry;
import ca.uhn.fhir.rest.gclient.TokenClientParam;
import ca.uhn.fhir.rest.api.MethodOutcome;
import ca.uhn.fhir.model.primitive.IdDt;
import ca.uhn.fhir.model.dstu2.valueset.ObservationStatusEnum;

public class CSVReader {

    public void AddPatients(){
        String csvFile = "C:\\Users\\Joel\\OneDrive\\Documents\\OMSCS\\Health_Informatics\\FHIR Power\\CSV Data\\demographics.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        Connection conn = new Connection("http://35.188.235.179:8080/baseDstu3");
        SimpleRead simpleRead = new SimpleRead(conn);
        AdvancedAdd advancedAdd = new AdvancedAdd(conn);

        try {

            br = new BufferedReader(new FileReader(csvFile));
            boolean firstline = true;
            while ((line = br.readLine()) != null) {

                if (!firstline){
                    // use comma as separator
                    String[] data = line.split(cvsSplitBy);

                    //patient	age	gender	unitname	hospitalname	labdate
                    System.out.println("patient= " + data[0] + "\n" +
                            "firstname=" + data[1] + "\n" +
                            "lastname=" + data[2] + "\n" +
                            "age=" + data[3] + "\n" +
                            "gender=" + data[4] + "\n" +
                            "unitname=" + data[5] + "\n" +
                            "hosptialname=" + data[6] + "\n" +
                            "labdate=" + data[7] + "\n" + "\n");

                    String patID1 = advancedAdd.addPatient(data[1],data[2]);
                    System.out.print("New Patient ID:  ");
                    System.out.println(patID1);

//                String labdate = data[0];
//                String patient = data[1];
//                String heartrate = data[1];
//                String sao2 = data[1];
//                String temperature = data[1];
//                String systemicsystolic = data[1];
//                String systemicmean = data[1];
//                String systemicdiastolic = data[1];
//                String respiration = data[1];
//                String etco2 = data[1];


                }
                firstline = false;


            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

    }

    public void AddObservations() {

        //LOCATION OF CSV FILE
        String csvFile = "C:\\Users\\Joel\\OneDrive\\Documents\\OMSCS\\Health_Informatics\\FHIR Power\\CSV Data\\combined.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        boolean firstline = true;

        //SETUP CONNECTION
        Connection conn = new Connection("http://35.188.235.179:8080/baseDstu3");
        AdvancedAdd advancedAdd = new AdvancedAdd(conn);
        SimpleRead simpleRead2 = new SimpleRead(conn);

        int iterator = 0;

        //PARSE THROUGH EACH LINE
        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {

                if (!firstline) {

                    iterator++;
                    System.out.println("------------------------------------------------");
                    System.out.println("PARSING ENTRY " + String.valueOf(iterator) + " of 2422");
                    System.out.println("------------------------------------------------");


                    // use comma as separator
                    String[] data = line.split(cvsSplitBy);

                    //GRAB EACH DATA POINT
                    String labdate = data[0];
                    String patient = data[1];
                    String name = data[2];
                    String heartrate = data[3];
                    String sao2 = data[4];
                    String temperature = data[5];
                    String systemicsystolic = data[6];
                    String systemicmean = data[7];
                    String systemicdiastolic = data[8];
                    String respiration = data[9];
                    String etco2 = data[10];

                    //PRINT OUT DATA FOR CURRENT PATIENT
                    System.out.println("labdate= " + labdate + "\n" +
                            "patient=" + patient + "\n" +
                            "name=" + name + "\n" +
                            "heartrate=" + heartrate + "\n" +
                            "sao2=" + sao2 + "\n" +
                            "temperature=" + temperature + "\n" +
                            "systemicsystolic=" + systemicsystolic + "\n" +
                            "systemicmean=" + systemicmean + "\n" +
                            "systemicdiastolic=" + systemicdiastolic + "\n" +
                            "respiration=" + respiration + "\n" +
                            "etco2=" + etco2 + "\n");

                    //LIKELY LOINC CODES
                    //heartrate:  8867-4
                    //sao2: 59408-5
                    //temperatuer:  8310-5
                    //systemicsystolic:  35094-2
                    //systemicmean
                    //systemicdiastolic:  8462-4
                    //respiration:  9304-7
                    //etco2: 33437-5

                    //ADD OBSERVATIONS TO THE FHIR SERVER
                    List<String> patID = new ArrayList<String>();
                    patID = simpleRead2.getIDByPatientName(name);
                    System.out.println("adding data for patient " + patID.get(0));
                    if (heartrate.substring(0,1).equals("N")){heartrate="0";}          System.out.println(advancedAdd.addObservation(patID.get(0), "8867-4", "heartrate", Double.parseDouble(heartrate), "bpm", "bpm",labdate));
                    if (sao2.substring(0,1).equals("N")){sao2="0";}               System.out.println(advancedAdd.addObservation(patID.get(0), "59408-5", "sao2", Double.parseDouble(sao2), "percent", "percent",labdate));
                    if (temperature.substring(0,1).equals("N")){temperature="0";}        System.out.println(advancedAdd.addObservation(patID.get(0), "8310-5", "temperature", Double.parseDouble(temperature), "F", "F",labdate));
                    if (systemicsystolic.substring(0,1).equals("N")){systemicsystolic="0";}   System.out.println(advancedAdd.addObservation(patID.get(0), "35094-2", "systemicsystolic", Double.parseDouble(systemicsystolic), "mmHg", "mmHg",labdate));
                    if (systemicmean.substring(0,1).equals("N")){systemicmean="0";}       System.out.println(advancedAdd.addObservation(patID.get(0), "1111-1", "systemicmean", Double.parseDouble(systemicmean), "mmHg", "mmHg",labdate));
                    if (systemicdiastolic.substring(0,1).equals("N")){systemicdiastolic="0";}  System.out.println(advancedAdd.addObservation(patID.get(0), "8462-4", "systemicdiastolic", Double.parseDouble(systemicdiastolic), "mmHg", "mmHg",labdate));
                    if (respiration.substring(0,1).equals("N")){respiration="0";}        System.out.println(advancedAdd.addObservation(patID.get(0), "9304-7", "respiration", Double.parseDouble(respiration), "bpm", "bpm",labdate));
                    if (etco2.substring(0,1).equals("N")){etco2="0";}              System.out.println(advancedAdd.addObservation(patID.get(0), "33437-5", "etco2", Double.parseDouble(etco2), "percent", "percent",labdate));

                    //System.out.println(advancedAdd.addObservation(patID.get(0), "789-8", "testname", 7, "kg", "kg",labdate));

                    System.out.println("------------------------------------------------");

                }
                firstline = false;

            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

    }

}
