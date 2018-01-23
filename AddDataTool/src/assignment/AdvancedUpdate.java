package assignment;

import assignment.Connection;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.api.IDatatype;
import ca.uhn.fhir.rest.client.IGenericClient;
import ca.uhn.fhir.model.dstu2.resource.Bundle;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.model.dstu2.resource.Observation;
import ca.uhn.fhir.model.dstu2.resource.Bundle.Entry;
import ca.uhn.fhir.rest.gclient.TokenClientParam;
import ca.uhn.fhir.rest.api.MethodOutcome;
import ca.uhn.fhir.model.dstu2.composite.ResourceReferenceDt;
import ca.uhn.fhir.model.primitive.IdDt;
import ca.uhn.fhir.model.dstu2.valueset.ContactPointUseEnum;
import ca.uhn.fhir.model.dstu2.valueset.ObservationStatusEnum;
import ca.uhn.fhir.model.dstu2.composite.ContactPointDt;
import ca.uhn.fhir.model.dstu2.composite.QuantityDt;

/**
 *
 */
public class AdvancedUpdate {

    //This Connection object is the same as the one you implemented in the first FHIR task
    private Connection connection = null;

    public AdvancedUpdate(Connection connection) {
        this.connection = connection;
    }

    public String updatePatientHomePhone(String patientId, String homePhoneNumber) {
        //Place your code here
        //Return the Outcome ID
        //Be sure it is just the logical ID Part
        IGenericClient client = connection.getClient();

        //Get the patient
        Patient pat = client.read(Patient.class,patientId);

        //Create the list of contact points and add the home phone number
        List<ContactPointDt> contactPoints = new ArrayList<ContactPointDt>();
        ContactPointDt phoneNum = new ContactPointDt();
        //ContactPointUseEnum cpsenum = new ContactPointUseEnum();
        phoneNum.setValue(homePhoneNumber);
        phoneNum.setUse(ContactPointUseEnum.HOME);
        contactPoints.add(phoneNum);

        //set the contact points to the patient
        pat.addTelecom(phoneNum);
        //pat.setTelecom(contactPoints);

        //Update the database
        MethodOutcome outcome = client.update()
                .resource(pat)
                .prettyPrint()
                .encodedJson()
                .execute();

        FhirContext ctx = FhirContext.forDstu2();
        String encoded = ctx.newJsonParser().encodeResourceToString(pat);
        //System.out.println(encoded);

        //get the ID
        IdDt id = (IdDt) outcome.getId();

        return id.getIdPart();

    }

    public String updateObservationValue(String observationId, double value) {
        //Place your code here
        //Return the Outcome ID
        //Be sure it is just the logical ID Part
        IGenericClient client = connection.getClient();

        //Get the patient
        Observation ob = client.read(Observation.class,observationId);

        //ob.setId(observationId);
        ob.setValue(new QuantityDt().setValue(value));

        //Update the database
        MethodOutcome outcome = client.update()
                .resource(ob)
                .prettyPrint()
                .encodedJson()
                .execute();

        //get the ID
        IdDt id = (IdDt) outcome.getId();

        return id.getIdPart();
    }

}