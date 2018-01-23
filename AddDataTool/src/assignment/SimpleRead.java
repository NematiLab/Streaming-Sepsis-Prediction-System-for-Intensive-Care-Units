package assignment;

import java.util.List;
import java.util.ArrayList;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.dstu2.composite.HumanNameDt;
import ca.uhn.fhir.model.dstu2.composite.IdentifierDt;
import ca.uhn.fhir.model.dstu2.resource.Bundle;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.model.dstu2.resource.Bundle.Entry;
import ca.uhn.fhir.model.dstu2.valueset.NameUseEnum;
import ca.uhn.fhir.parser.IParser;
import ca.uhn.fhir.rest.client.IGenericClient;
import ca.uhn.fhir.rest.client.ServerValidationModeEnum;
import org.hl7.fhir.instance.model.api.IBaseResource;

/**
 *
 */
public class SimpleRead {

    //This Connection object is the same as the one you implemented in the first FHIR task
    private Connection connection = null;

    public SimpleRead(Connection connection) {
        this.connection = connection;
    }

    public String getNameByPatientID(String id) {
        //Place your code here
        //return the patient full name (e.g. Mr. Chuck Jones)
        //if the patient has multiple names (e.g. current and maiden), just return th e first one

        IGenericClient client = connection.getClient();

        Patient pat2 = client.read(Patient.class,id);
        String fullName = pat2.getName().get(0).getNameAsSingleString();

        return fullName;
    }

    public List<String> getIDByPatientName(String name) {
        List<String> answer = new ArrayList<String>();

        IGenericClient client = connection.getClient();

        Bundle results = client.search().forResource(Patient.class)
                .where(Patient.NAME.matches().value(name))//using FAMILY will return 2 values,  GIVEN is same as NAME
                .returnBundle(ca.uhn.fhir.model.dstu2.resource.Bundle.class)
                .execute();

        List<Bundle.Entry> list = results.getEntry();

        for (Bundle.Entry be : list){
            Patient p1 = (Patient) be.getResource();
            answer.add(p1.getId().getIdPart());
        }

        return answer;
    }

}