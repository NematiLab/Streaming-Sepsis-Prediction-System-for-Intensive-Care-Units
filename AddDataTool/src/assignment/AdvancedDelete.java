package assignment;

import assignment.Connection;

import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.rest.client.IGenericClient;
import org.hl7.fhir.instance.model.api.IBaseOperationOutcome;

import ca.uhn.fhir.model.primitive.IdDt;

/**
 *
 */
public class AdvancedDelete {

    //This Connection object is the same as the one you implemented in the first FHIR task
    private Connection connection = null;

    public AdvancedDelete(Connection connection) {
        this.connection = connection;
    }

    public void deletePatient(String patientId) {
        //Place your code here

        IGenericClient client = connection.getClient();

        IBaseOperationOutcome resp = client.delete().resourceById(new IdDt("Patient", patientId)).execute();

    }

    public void deleteObservation(String observationId) {
        //Place your code here
        IGenericClient client = connection.getClient();

        IBaseOperationOutcome resp = client.delete().resourceById(new IdDt("Observation", observationId)).execute();

    }

}