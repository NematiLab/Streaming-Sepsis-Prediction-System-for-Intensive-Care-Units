package assignment;

import assignment.Connection;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.api.Include;
import ca.uhn.fhir.model.primitive.InstantDt;
import ca.uhn.fhir.rest.client.IGenericClient;
import ca.uhn.fhir.model.dstu2.resource.Bundle;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.model.dstu2.resource.Observation;
import ca.uhn.fhir.model.dstu2.resource.Bundle.Entry;
import ca.uhn.fhir.rest.gclient.TokenClientParam;

/**
 *
 */
public class AdvancedRead {

    //This Connection object is the same as the one you implemented in the first FHIR task
    private Connection connection = null;

    public AdvancedRead(Connection connection) {
        this.connection = connection;
    }

    public int getTotalNumPatientsByObservation(String loincCode) {
        //Place your code here
        int total = 0;
        IGenericClient client = connection.getClient();

        Bundle results = client.search().forResource(Observation.class)
                .where(Observation.CODE.exactly().code(loincCode))
                .returnBundle(ca.uhn.fhir.model.dstu2.resource.Bundle.class)
                .execute();

        int size = results.getEntry().size();

        List<Bundle.Entry> list = results.getEntry();
        List<String> patIDs = new ArrayList<String>();


        for (Bundle.Entry be : list) {
            Observation ob = (Observation) be.getResource();
            String id = ob.getSubject().getReference().getIdPart();
            if (patIDs.contains(id)){}
            else{patIDs.add(id);}

        }

        return patIDs.size();
    }

    public void getObservationValue(String loincCode, String instant) {

        InstantDt myInstant = new InstantDt(instant);
        IGenericClient client = connection.getClient();

//        Bundle results1 = client
//                .search()
//                .forResource(Patient.class)
//                .where(Patient.FAMILY.matches().value("duck"))
//                .returnBundle(ca.uhn.fhir.model.dstu2.resource.Bundle.class)
//                .execute();
//
//        Bundle response = client.search()
//                .forResource(Observation.class)
//                .where(Observation.PATIENT.matches().values("4967"))
//                .and(Observation)
//                .and(Patient.ADDRESS.matches().values("Ontario"))
//                .and(Patient.ADDRESS.matches().values("Canada"))
//                .returnBundle(Bundle.class)
//                .execute();
//
//        Bundle results = client.search().forResource(Observation.class)
//                .where(Observation.CODE.exactly().code(loincCode))
//                .and(Observation.PATIENT.)
//                .returnBundle(ca.uhn.fhir.model.dstu2.resource.Bundle.class)
//                .execute();

//        System.out.println("Found " + results.getEntry().size() + " patients named 'duck'");

    }

}