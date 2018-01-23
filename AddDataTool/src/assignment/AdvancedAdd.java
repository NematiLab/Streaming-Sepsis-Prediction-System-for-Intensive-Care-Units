package assignment;

import assignment.Connection;

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

/**
 *
 */
public class AdvancedAdd {

    //This Connection object is the same as the one you implemented in the first FHIR task
    private Connection connection = null;

    public AdvancedAdd(Connection connection) {
        this.connection = connection;
    }

    public String addPatient(String firstName, String lastName) {
        //Place your code here
        //Return the ID of the new patient
        //Be sure it is just the logical ID Part

        IGenericClient client = connection.getClient();

        Patient patient = new Patient();
        // ..populate the patient object..
        //patient.addIdentifier().setSystem("urn:system").setValue("12345");
        HumanNameDt humanName = new HumanNameDt();
        humanName.addFamily(lastName);
        humanName.addGiven(firstName);
//        patient.addName().addFamily(lastName).addGiven(firstName);
        patient.addName(humanName);
        System.out.println(client.create().resource(patient).prettyPrint());

        // Invoke the server create method (and send pretty-printed JSON
        // encoding to the server
        // instead of the default which is non-pretty printed XML)
        MethodOutcome outcome = client.create()
                .resource(patient)
                .prettyPrint()
                .encodedJson()
                .execute();

        // The MethodOutcome object will contain information about the
        // response from the server, including the ID of the created
        // resource, the OperationOutcome response, etc. (assuming that
        // any of these things were provided by the server! They may not
        // always be)
        IdDt id = (IdDt) outcome.getId();
        //System.out.println("Got ID: " + id.getValue());
        //System.out.println(id.getIdPart());
        return id.getIdPart();

    }

    public String addObservation(String patientId, String loincCode, String loincDisplayName,
                                 double value, String valueUnit, String valueCode, String instant) {
        //Place your code here
        //Return the ID of the new Observation
        //Be sure it is just the logical ID Part

        IGenericClient client = connection.getClient();

        // Create an Observation instance
        Observation observation = new Observation();

        // Give the observation a status
        observation.setStatus(ObservationStatusEnum.FINAL);

        // Create an get the patient
//        Patient pat = client.read(Patient.class,patientId);

        //InstantDt myInstant = new InstantDt("2017-10-25T09:19:11.403-05:00");//2017-10-02 09:00:00-04
        //InstantDt myInstant2 = new InstantDt("2017-10-02T09:00:00-04:00");//
        InstantDt myInstant2 = new InstantDt(instant);

        //before:  2017-10-02 09:00:00-04
        //after:  2017-10-02T09:00:00-04:00

        //Loinc:  HR: 8867-4
        //heartrate 	 sao2 	 temperature 	 systemicsystolic 	 systemicmean 	 systemicdiastolic 	 respiration 	 etco2
        //heartrate:  8867-4
        //sao2: 59408-5
        //temperatuer:  8310-5
        //systemicsystolic:  35094-2
        //systemicmean
        //systemicdiastolic:  8462-4
        //respiration:  9304-7
        //etco2: 33437-5


        // Create a quantity datatype
        QuantityDt myValue = new QuantityDt();
        myValue.setValue(value).setSystem("http://unitsofmeasure.org").setCode(valueCode).setUnit(valueUnit);
        observation.setValue(myValue);

        CodingDt coding = observation.getCode().addCoding();
        coding.setCode(loincCode).setSystem("http://loinc.org").setDisplay(loincDisplayName);

        observation.setIssued(new InstantDt(myInstant2));
        observation.setSubject(new ResourceReferenceDt(new IdDt("Patient",patientId)));

        MethodOutcome outcome = client.create()
                .resource(observation)
                .prettyPrint()
                .encodedJson()
                .execute();

        System.out.println(outcome);
        IdDt id = (IdDt) outcome.getId();
        //System.out.println("Got ID: " + id.getValue());
        //System.out.println(id.getIdPart());
        return id.getIdPart();
    }

}