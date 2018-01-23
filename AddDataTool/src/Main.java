import assignment.*;
import ca.uhn.fhir.model.dstu2.resource.Patient;
import ca.uhn.fhir.rest.client.IGenericClient;

import java.util.List;

public class Main {

    public static void main(String[] args) {



        CSVReader cr = new CSVReader();
        cr.AddPatients();
        cr.AddObservations();

        //Connection conn1 = new Connection("http://35.188.235.179:8080/baseDstu3");
        //AdvancedDelete advancedDelete = new AdvancedDelete(conn1);

        //advancedDelete.deleteObservation("4955");

        //SimpleRead simpleRead2 = new SimpleRead(conn1);
        //System.out.println(simpleRead2.getIDByPatientName("Neil"));


    }




}
